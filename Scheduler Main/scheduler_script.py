#I am using code from CS110 Session 13 [7.2] Heaps and Priority Queues

class MaxHeap:
    """
    max heap data structure to manage tasks based on their priority. 
    The task with the highest priority will always be at the root of the heap.
    """

    def __init__(self):
        self.heap = [] #empty heap to store tasks

    def heappush(self, task):
        """
        Adds a task to the heap and maintains the heap property by bubbling the task up.
        Parameters:
        task (Task): The task that needs to be added to the heap.
        """
        self.heap.append(task) #add the task to the end of the heap
        self._bubble_up(len(self.heap) - 1) #reorder the heap to ensure the task is placed correctly

    def heappop(self):
        """
        Removes and returns the task with the highest priority (root of the heap).
        
        Returns:
            Task: The task with the highest priority.
        
        Raises:
            IndexError: If the heap is empty and there's no task to pop.
        """
        if not self.heap:
            raise IndexError("Heap is empty") #error if the heap is empty
        
        if len(self.heap) == 1:
            return self.heap.pop() 
        
        max_task = self.heap[0] 
        self.heap[0] = self.heap.pop() #replace the root with the last task in the heap
        self._heapify(0)
        return max_task

    def _bubble_up(self, index):
        while index > 0:
            parent_index = (index - 1) // 2
            if self.heap[index] > self.heap[parent_index]:  #making sure max-heap property
                self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
                index = parent_index
            else:
                break

    def _heapify(self, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        
        if left < len(self.heap) and self.heap[left] > self.heap[largest]:
            largest = left
        if right < len(self.heap) and self.heap[right] > self.heap[largest]:
            largest = right
        if largest != i:
            self.heap[i], self.heap[largest] = self.heap[largest], self.heap[i]
            self._heapify(largest)

    def __len__(self):
        return len(self.heap)

    def reset_heap(self, tasks):
        #refill the heap with tasks to refresh its structure
        self.heap = []
        for task in tasks:
            self.heappush(task)

class Task:
    def __init__(self, id, description, duration, dependencies, is_fixed=False, start_time=None, status="N", importance="medium"):
        self.id = id
        self.description = description 
        self.duration = duration #duration of task
        self.dependencies = dependencies
        self.is_fixed = is_fixed #if task has fixed time
        self.start_time = start_time #it will have fixed starting time
        self.priority = 0 
        self.status = status 
        self.importance = importance  #importance level "high", "medium", or "low" 

    def calculate_priority(self, current_time=None):
        """
        Calculate priority for tasks with the following logic:
        Fixed tasks always have 100 utility points.
        Flexible tasks have a base of 100 and decline based on penalties:
        - Dependency count
        - Duration (longer tasks are penalized less, since they are more important)
        - Importance level (higher importance reduces penalties)
        """
        if current_time is None:
            current_time = 9 * 60  #default to 9:00 AM

        if self.is_fixed:
            #fixed tasks always have a consistent utility score of 100, because they are fixed
            self.priority = 100
        else:
            #base priority for flexible tasks starts from 100 as well
            base = 100

            #dependency penalty
            dependency_penalty = len(self.dependencies) * 10  # 10 points per dependency penalized

            #duration penalty (shorter tasks penalized more to incentivize longer ones)
            duration_penalty = max(0, 40 - (self.duration // 30) * 10)

            #importance bonus (higher importance decreases penalty, and adds for utility)
            importance_bonus = {"high": 30, "medium": 15, "low": 0}[self.importance]

            #final priority calculation for flexible tasks
            self.priority = base - dependency_penalty - duration_penalty + importance_bonus

            #ensure priority doesn't exceed base or drop below 0
            self.priority = round(max(0, min(base, self.priority)))


    def __lt__(self, other):
        return self.priority > other.priority  #reverse for max-heap


class TaskScheduler:
    NOT_STARTED = 'N'
    IN_PRIORITY_QUEUE = 'I'
    COMPLETED = 'C'
    
    def __init__(self, tasks):
        self.tasks = tasks
        self.priority_queue = MaxHeap()
        
    def remove_dependency(self, id):
        for t in self.tasks:
            if t.id != id and id in t.dependencies:
                t.dependencies.remove(id)
    
    def get_tasks_ready(self, current_time):
        #first, add fixed tasks that are due now
        for task in self.tasks:
            if (task.status == self.NOT_STARTED and 
                task.is_fixed and 
                task.start_time == current_time and 
                not task.dependencies):
                task.calculate_priority()
                task.status = self.IN_PRIORITY_QUEUE
                self.priority_queue.heappush(task)
        
        #then add flexible tasks building around fixed tasks
        if len(self.priority_queue) == 0:
            for task in self.tasks:
                if (task.status == self.NOT_STARTED and 
                    not task.dependencies and 
                    (not task.is_fixed or current_time >= task.start_time)):
                    task.calculate_priority()
                    task.status = self.IN_PRIORITY_QUEUE
                    self.priority_queue.heappush(task)
    
    def get_next_fixed_task_time(self, current_time):
        next_time = None
        for task in self.tasks:
            if (task.status == self.NOT_STARTED and 
                task.is_fixed and 
                task.start_time > current_time):
                if next_time is None or task.start_time < next_time:
                    next_time = task.start_time
        return next_time
    
    def update_priorities(self):
        for task in self.tasks:
            if task.status == self.NOT_STARTED:
                task.calculate_priority()
        #rebuild the heap only for tasks in the queue
        self.priority_queue.reset_heap([t for t in self.tasks if t.status == self.IN_PRIORITY_QUEUE])
    
    def check_unscheduled_tasks(self):
        return any(task.status == self.NOT_STARTED for task in self.tasks)
    
    def format_time(self, time):
        return f"{time // 60}h{time % 60:02d}"

    def run_task_scheduler(self, starting_time, completed_task_order=None, suppress_output=False):
        current_time = starting_time
        total_utils = 0

        if not suppress_output:
            print("Running a priority-based scheduler:\n")

        while self.check_unscheduled_tasks():
            #recalculate priorities dynamically for all tasks
            self.update_priorities()  #dynamic recalculation
            self.get_tasks_ready(current_time)
            
            if len(self.priority_queue) > 0:
                task = self.priority_queue.heappop()
                if not suppress_output:
                    print(f"🕰t={self.format_time(current_time)}")
                    task_type = " (Fixed Task)" if task.is_fixed else ""
                    print(f"\tstarted '{task.description}' for {task.duration} mins{task_type}, utils = {task.priority}.")
                current_time += task.duration
                total_utils += task.priority
                self.remove_dependency(task.id)
                task.status = self.COMPLETED
                #recalculate priorities after task completion
                self.update_priorities()
                if completed_task_order is not None:
                    completed_task_order.append(task.id)
                if not suppress_output:
                    print(f"\t✅ t={self.format_time(current_time)}, task completed!")
            else:
                #jump to next fixed task time if available
                next_time = self.get_next_fixed_task_time(current_time)
                if next_time is not None:
                    current_time = next_time
                else:
                    #no more fixed tasks, increment time by 1 minute
                    current_time += 1

        total_time = current_time - starting_time
        if not suppress_output:
            print(f"\n🏁 Completed all planned tasks in {total_time // 60}h{total_time % 60:02d}min!")
            print(f"Total utility points (utils) accumulated: {total_utils}")

#tasks with unordered input
tasks = [
    Task(id=10, description='Go to sleep', duration=10, dependencies=[1, 2, 3, 4, 5, 6, 7, 8, 9], is_fixed=True, start_time=22 * 60, importance="high"),
    Task(id=1, description='Wake-up and Preparation', duration=5, dependencies=[], is_fixed=True, start_time=9 * 60, importance="high"),
    Task(id=6, description='Getting boba drink', duration=30, dependencies=[3, 4, 5], importance="low"),
    Task(id=3, description='Branch from a local Taiwanese family', duration=20, dependencies=[1, 2], importance="low"),
    Task(id=4, description='Medicines I', duration=15, dependencies=[3], importance="medium"),
    Task(id=5, description='Work on a personal project', duration=120, dependencies=[1, 3, 4], is_fixed=True, start_time=10 * 60, importance="medium"),
    Task(id=7, description='2 classes (+PCWs)', duration=360, dependencies=[1, 6, 3, 4], is_fixed=True, start_time=13 * 60, importance="high"),
    Task(id=8, description='Dinner from a local Taiwanese family', duration=40, dependencies=[7, 3], importance="medium"),
    Task(id=2, description='Morning care routine', duration=10, dependencies=[1], importance="high"),
    Task(id=9, description='Medicines II', duration=20, dependencies=[4, 7, 8], importance="medium")
]


#ordered tasks by IDs
task2 = [
    Task(id=1, description='Wake-up and Preparation', duration=5, dependencies=[], is_fixed=True, start_time=9 * 60, importance="high"),
    Task(id=2, description='Morning care routine', duration=10, dependencies=[1], importance="high"),
    Task(id=3, description='Branch from a local Taiwanese family', duration=20, dependencies=[1, 2], importance="low"),
    Task(id=4, description='Medicines I', duration=15, dependencies=[3], importance="medium"),
    Task(id=5, description='Work on a personal project', duration=120, dependencies=[1, 3, 4], is_fixed=True, start_time=10 * 60, importance="medium"),
    Task(id=6, description='Getting boba drink', duration=30, dependencies=[3, 4, 5], importance="low"),
    Task(id=7, description='2 classes (+PCWs)', duration=360, dependencies=[1, 6, 3, 4], is_fixed=True, start_time=13 * 60, importance="high"),
    Task(id=8, description='Dinner from a local Taiwanese family', duration=40, dependencies=[7, 3], importance="medium"),
    Task(id=9, description='Medicines II', duration=20, dependencies=[4, 7, 8], importance="medium"),
    Task(id=10, description='Go to sleep', duration=10, dependencies=[1, 2, 3, 4, 5, 6, 7, 8, 9], is_fixed=True, start_time=22 * 60, importance="high"),
]

#second unordered tasks by IDs
task3 = [
    Task(id=9, description='Medicines II', duration=20, dependencies=[4, 7, 8], importance="medium"),
    Task(id=3, description='Branch from a local Taiwanese family', duration=20, dependencies=[1, 2], importance="low"),
    Task(id=4, description='Medicines I', duration=15, dependencies=[3], importance="medium"),
    Task(id=5, description='Work on a personal project', duration=120, dependencies=[1, 3, 4], is_fixed=True, start_time=10 * 60, importance="medium"),
    Task(id=6, description='Getting boba drink', duration=30, dependencies=[3, 4, 5], importance="low"),
    Task(id=1, description='Wake-up and Preparation', duration=5, dependencies=[], is_fixed=True, start_time=9 * 60, importance="high"),
    Task(id=7, description='2 classes (+PCWs)', duration=360, dependencies=[1, 6, 3, 4], is_fixed=True, start_time=13 * 60, importance="high"),
    Task(id=8, description='Dinner from a local Taiwanese family', duration=40, dependencies=[7, 3], importance="medium"),
    Task(id=10, description='Go to sleep', duration=10, dependencies=[1, 2, 3, 4, 5, 6, 7, 8, 9], is_fixed=True, start_time=22 * 60, importance="high"),
    Task(id=2, description='Morning care routine', duration=10, dependencies=[1], importance="high")
]

task4 = [
    Task(id=3, description='Branch from a local Taiwanese family', duration=20, dependencies=[1, 2], importance="low"),
    Task(id=7, description='2 classes (+PCWs)', duration=360, dependencies=[1, 6, 3, 4], is_fixed=True, start_time=13 * 60, importance="high"),
    Task(id=9, description='Medicines II', duration=20, dependencies=[4, 7, 8], importance="medium"),
    Task(id=5, description='Work on a personal project', duration=120, dependencies=[1, 3, 4], is_fixed=True, start_time=10 * 60, importance="medium"),
    Task(id=6, description='Getting boba drink', duration=30, dependencies=[3, 4, 5], importance="low"),
    Task(id=4, description='Medicines I', duration=15, dependencies=[3], importance="medium"),
    Task(id=1, description='Wake-up and Preparation', duration=5, dependencies=[], is_fixed=True, start_time=9 * 60, importance="high"),
    Task(id=8, description='Dinner from a local Taiwanese family', duration=40, dependencies=[7, 3], importance="medium"),
    Task(id=10, description='Go to sleep', duration=10, dependencies=[1, 2, 3, 4, 5, 6, 7, 8, 9], is_fixed=True, start_time=22 * 60, importance="high"),
    Task(id=2, description='Morning care routine', duration=10, dependencies=[1], importance="high")
]


# Create and run the scheduler with tasks and print the output once
print("Running scheduler with original task order:")
completed_order_tasks = []
task_scheduler1 = TaskScheduler(tasks)
for task in tasks:
    task.status = TaskScheduler.NOT_STARTED  
task_scheduler1.run_task_scheduler(starting_time=9 * 60, completed_task_order=completed_order_tasks)
print("Completed task order:", completed_order_tasks)

# Run with task2
completed_order_task2 = []
for task in task2:
    task.status = TaskScheduler.NOT_STARTED  
task_scheduler2 = TaskScheduler(task2)
task_scheduler2.run_task_scheduler(starting_time=9 * 60, completed_task_order=completed_order_task2, suppress_output=True)

# Run with task3
completed_order_task3 = []
for task in task3:
    task.status = TaskScheduler.NOT_STARTED  
task_scheduler3 = TaskScheduler(task3)
task_scheduler3.run_task_scheduler(starting_time=9 * 60, completed_task_order=completed_order_task3, suppress_output=True)

# Run with task4
completed_order_task4 = []
for task in task4:
    task.status = TaskScheduler.NOT_STARTED  
task_scheduler3 = TaskScheduler(task4)
task_scheduler3.run_task_scheduler(starting_time=9 * 60, completed_task_order=completed_order_task4, suppress_output=True)

# Assert that all execution orders are the same
assert completed_order_tasks == completed_order_task2, "Test failed: Execution order is inconsistent between tasks and task2."
assert completed_order_tasks == completed_order_task3, "Test failed: Execution order is inconsistent between tasks and task3."
assert completed_order_tasks == completed_order_task4, "Test failed: Execution order is inconsistent between tasks and task3."

print("\nAll tests passed! Execution order is consistent across different task input orders.")

task_no_dependencies = [
    Task(id=3, description='Branch from a local Taiwanese family', duration=20, dependencies=[], importance="low"),
    Task(id=7, description='2 classes (+PCWs)', duration=360, dependencies=[], is_fixed=True, start_time=13 * 60, importance="high"),
    Task(id=9, description='Medicines II', duration=20, dependencies=[], importance="medium"),
    Task(id=5, description='Work on a personal project', duration=120, dependencies=[], is_fixed=True, start_time=10 * 60, importance="medium"),
    Task(id=6, description='Getting boba drink', duration=30, dependencies=[], importance="low"),
    Task(id=4, description='Medicines I', duration=15, dependencies=[3], importance="medium"),
    Task(id=1, description='Wake-up and Preparation', duration=5, dependencies=[], is_fixed=True, start_time=9 * 60, importance="high"),
    Task(id=8, description='Dinner from a local Taiwanese family', duration=40, dependencies=[], importance="medium"),
    Task(id=10, description='Go to sleep', duration=10, dependencies=[], is_fixed=True, start_time=22 * 60, importance="high"),
    Task(id=2, description='Morning care routine', duration=10, dependencies=[], importance="high")
]


print("Running scheduler with original task order:")
completed_order_tasks = []
task_scheduler1 = TaskScheduler(task_no_dependencies)