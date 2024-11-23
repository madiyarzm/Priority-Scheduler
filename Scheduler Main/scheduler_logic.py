import heapq

class Task:
    def __init__(self, id, description, duration, dependencies, status="N"):
        self.id = id
        self.description = description
        self.duration = duration
        self.dependencies = dependencies
        self.status = status

    def __lt__(self, other):
        return self.id < other.id    

class TaskScheduler:
    NOT_STARTED = 'N'
    IN_PRIORITY_QUEUE = 'I'
    COMPLETED = 'C'
    
    def __init__(self, tasks):
        self.tasks = tasks
        self.priority_queue = []     
        
    def print_self(self):
        print("Tasks added to the simple scheduler:")
        print("--------------------------------------")
        for t in self.tasks:
            print(f"➡️'{t.description}', duration = {t.duration} mins.")   
            if len(t.dependencies) > 0:
                print(f"\t ⚠️ This task depends on others!")     
            
    def remove_dependency(self, id):
        for t in self.tasks:
            if t.id != id and id in t.dependencies:
                t.dependencies.remove(id)           
    
    def get_tasks_ready(self):
        for task in self.tasks:
            if task.status == self.NOT_STARTED and not task.dependencies: 
                task.status = self.IN_PRIORITY_QUEUE 
                heapq.heappush(self.priority_queue, task)
    
    def check_unscheduled_tasks(self):
        for task in self.tasks:
            if task.status == self.NOT_STARTED:
                return True
        return False   
    
    def format_time(self, time):
        return f"{time//60}h{time%60:02d}"
    
    def run_task_scheduler(self, starting_time):
        current_time = starting_time
        print("Running a simple scheduler:\n")
        while self.check_unscheduled_tasks() or self.priority_queue:
            self.get_tasks_ready()
            if len(self.priority_queue) > 0 :      
                task = heapq.heappop(self.priority_queue)
                print(f"🕰t={self.format_time(current_time)}")
                print(f"\tstarted '{task.description}' for {task.duration} mins...")
                current_time += task.duration            
                print(f"\t✅ t={self.format_time(current_time)}, task completed!") 
                self.remove_dependency(task.id)
                task.status = self.COMPLETED
        total_time = current_time - starting_time             
        print(f"\n🏁 Completed all planned tasks in {total_time//60}h{total_time%60:02d}min!")

# Create tasks and initialize scheduler
tasks = [
    Task(id=1, description='get up at 9:00 AM', duration=5, dependencies=[]), 
    Task(id=2, description='morning care routine', duration=10, dependencies=[1]), 
    Task(id=3, description='branch from a local Taiwanese family', duration=30, dependencies=[1,2]), 
    Task(id=4, description='take morning medicines', duration=5, dependencies=[3]), 
    Task(id=5, description='work on a personal project', duration=240, dependencies=[1, 3]), 
    Task(id=6, description='get boba (+walk)', duration=60, dependencies=[3,5]), 
    Task(id=7, description='2 classes (+PCWs)', duration=360, dependencies=[1]), 
    Task(id=8, description='dinner from a local Taiwanese family', duration=30, dependencies=[7]),
    Task(id=9, description='take bedtime medicines', duration=30, dependencies=[8]),
    Task(id=10, description='go to sleep', duration=5, dependencies=[1,2,3,4,5,6,7,8,9])
]

task_scheduler = TaskScheduler(tasks)
task_scheduler.print_self()

start_scheduler_at = 9 * 60
task_scheduler.run_task_scheduler(start_scheduler_at)
