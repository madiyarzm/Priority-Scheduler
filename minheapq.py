class MinHeap:
    def __init__(self):
        self.heap = []

    def left(self, i):
        return 2 * i + 1

    def right(self, i):
        return 2 * i + 2

    def parent(self, i):
        return (i - 1) // 2

    def heappush(self, task):
        self.heap.append(task)
        self._bubble_up(len(self.heap) - 1)

    def _bubble_up(self, index):
        while index > 0:
            parent_index = self.parent(index)
            if self.heap[index] < self.heap[parent_index]:  # Min-heap property
                self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
                index = parent_index
            else:
                break

    def heappop(self):
        if not self.heap:
            raise IndexError("Heap is empty")
        
        # If there's only one element, pop and return it directly
        if len(self.heap) == 1:
            return self.heap.pop()
        
        # Swap the first and last elements, pop the last element, and heapify
        min_task = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify(0)
        return min_task

    def _heapify(self, i):
        smallest = i
        left = self.left(i)
        right = self.right(i)
        
        if left < len(self.heap) and self.heap[left] < self.heap[smallest]:
            smallest = left
        if right < len(self.heap) and self.heap[right] < self.heap[smallest]:
            smallest = right
        if smallest != i:
            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
            self._heapify(smallest)

    def __len__(self):
        return len(self.heap)

class Task:
    def __init__(self, id, description, duration, dependencies, start_time=None, priority=0, status="N"):
        self.id = id
        self.description = description
        self.duration = duration
        self.dependencies = dependencies
        self.start_time = start_time  # Optional scheduled start time
        self.priority = priority  # Initial priority; calculated dynamically in the scheduler
        self.status = status

    def calculate_priority(self, current_time, k1=1, k2=10, k3=1, k4=5):
        # Calculate time difference; if no start time, set it to a large value
        time_difference = abs(self.start_time - current_time) if self.start_time else float('inf')
        dependency_count = len(self.dependencies)

        # Calculate priority based on the utility formula
        self.priority = (k1 / self.duration) + (k2 / max(time_difference, 1)) - (k3 * dependency_count) + k4

    def __lt__(self, other):
        # Primary sort by priority (higher priority first)
        if self.priority != other.priority:
            return self.priority > other.priority  # Max priority for highest value
        # Secondary sort by start_time if priorities are the same (earlier start times first)
        if self.start_time != other.start_time:
            return (self.start_time or float('inf')) < (other.start_time or float('inf'))
        # Tertiary sort by ID if both priority and start_time are the same
        return self.id < other.id


class TaskScheduler:
    NOT_STARTED = 'N'
    IN_PRIORITY_QUEUE = 'I'
    COMPLETED = 'C'
    
    def __init__(self, tasks):
        self.tasks = tasks
        self.priority_queue = MinHeap()
        
    def print_self(self):
        print("Tasks added to the simple scheduler:")
        print("--------------------------------------")
        for t in self.tasks:
            print(f"➡️'{t.description}', duration = {t.duration} mins, priority = {t.priority}.")   
            if len(t.dependencies) > 0:
                print(f"\t ⚠️ This task depends on others!")     

    def remove_dependency(self, id):
        for t in self.tasks:
            if t.id != id and id in t.dependencies:
                t.dependencies.remove(id)           
    
    def get_tasks_ready(self, current_time):
        for task in self.tasks:
            if task.status == self.NOT_STARTED and not task.dependencies:
                task.calculate_priority(current_time)  # Calculate task priority
                task.status = self.IN_PRIORITY_QUEUE 
                self.priority_queue.heappush(task)
    
    def check_unscheduled_tasks(self):
        for task in self.tasks:
            if task.status == self.NOT_STARTED:
                return True
        return False   
    
    def format_time(self, time):
        return f"{time//60}h{time%60:02d}"
    
    def run_task_scheduler(self, starting_time):
        current_time = starting_time
        print("Running a priority-based scheduler:\n")
        while self.check_unscheduled_tasks() or len(self.priority_queue) > 0:
            self.get_tasks_ready(current_time)
            if len(self.priority_queue) > 0:
                task = self.priority_queue.heappop()
                print(f"🕰t={self.format_time(current_time)}")
                print(f"\tstarted '{task.description}' for {task.duration} mins, priority = {task.priority}.")
                current_time += task.duration            
                print(f"\t✅ t={self.format_time(current_time)}, task completed!") 
                self.remove_dependency(task.id)
                task.status = self.COMPLETED
        total_time = current_time - starting_time             
        print(f"\n🏁 Completed all planned tasks in {total_time//60}h{total_time%60:02d}min!")

# Create tasks with optional start times and initialize scheduler
tasks = [
    Task(id=1, description='get up at 9:00 AM', duration=5, dependencies=[], start_time=9 * 60), 
    Task(id=2, description='morning care routine', duration=10, dependencies=[1], start_time=9 * 60 + 10), 
    Task(id=3, description='branch from a local Taiwanese family', duration=30, dependencies=[1, 2], start_time=10 * 60), 
    Task(id=4, description='take morning medicines', duration=5, dependencies=[3]), 
    Task(id=5, description='work on a personal project', duration=240, dependencies=[1, 3]), 
    Task(id=6, description='get boba (+walk)', duration=60, dependencies=[3, 5]), 
    Task(id=7, description='2 classes (+PCWs)', duration=360, dependencies=[1], start_time=13 * 60), 
    Task(id=8, description='dinner from a local Taiwanese family', duration=30, dependencies=[7], start_time=19 * 60),
    Task(id=9, description='take bedtime medicines', duration=30, dependencies=[8]),
    Task(id=10, description='go to sleep', duration=5, dependencies=[1, 2, 3, 4, 5, 6, 7, 8, 9], start_time=22 * 60)
]

tasks2 = [
    Task(id=10, description='go to sleep', duration=5, dependencies=[1, 2, 3, 4, 5, 6, 7, 8, 9], start_time=22 * 60),
    Task(id=3, description='branch from a local Taiwanese family', duration=30, dependencies=[1, 2], start_time=10 * 60), 
    Task(id=4, description='take morning medicines', duration=5, dependencies=[3]), 
    Task(id=6, description='get boba (+walk)', duration=60, dependencies=[3, 5]), 
    Task(id=2, description='morning care routine', duration=10, dependencies=[1], start_time=9 * 60 + 10), 
    Task(id=1, description='get up at 9:00 AM', duration=5, dependencies=[], start_time=9 * 60), 
    Task(id=5, description='work on a personal project', duration=240, dependencies=[1, 3]), 
    
    Task(id=7, description='2 classes (+PCWs)', duration=360, dependencies=[1], start_time=13 * 60), 
    Task(id=8, description='dinner from a local Taiwanese family', duration=30, dependencies=[7], start_time=19 * 60),
    Task(id=9, description='take bedtime medicines', duration=30, dependencies=[8])
]

task_scheduler = TaskScheduler(tasks)
task_scheduler.print_self()

# Start the scheduler at 9:00 AM (9 * 60 minutes)
start_scheduler_at = 9 * 60
task_scheduler.run_task_scheduler(start_scheduler_at)

task_scheduler = TaskScheduler(tasks2)
task_scheduler.print_self()

# Start the scheduler at 9:00 AM (9 * 60 minutes)
start_scheduler_at = 9 * 60
task_scheduler.run_task_scheduler(start_scheduler_at)