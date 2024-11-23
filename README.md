# 🌟 Priority Scheduler 📅  

A dynamic **Priority Scheduler** designed to manage daily tasks efficiently by leveraging **Max-Heaps** and **Priority Queues**. It ensures optimal scheduling by balancing **importance**, **duration**, and **dependencies**, while seamlessly integrating fixed and flexible tasks.  

---

## ✨ Features  

### 🧠 **Smart Task Prioritization**  
Tasks are assigned utility scores based on:  
- **Fixed Time Constraints** ⏰: Tasks with strict start times are prioritized.  
- **Dynamic Utility Formula** 🤖:  
  - **Utility** = `100 − (Dependencies * 10) − Duration Penalty + Importance Bonus`  
  - **Importance Levels**:  
    - 🟥 High: +30 points  
    - 🟨 Medium: +15 points  
    - 🟩 Low: +0 points  
  - **Duration Bonus**: Long tasks are rewarded to reflect higher energy requirements.  

### 🔗 **Dependency Management**  
- Ensures tasks with dependencies are scheduled only after their prerequisites.  
- Example: **Take Medicine II** 💊 requires **Take Medicine I**.  

### ⚡ **Efficiency Optimization**  
- Minimizes idle time by strategically fitting flexible tasks between fixed ones.  
- Recalculates priorities dynamically after each task completion.  

### 🔄 **Flexibility**  
- Supports a mix of **fixed** and **flexible** tasks.  
- Automatically adapts the schedule to available time slots.  

---

## 🛠️ Code Implementation  

### 📈 **MaxHeap**  
A custom implementation to manage task priorities efficiently:  
- **Operations**:  
  - `heappush` 📥: Add tasks to the heap.  
  - `heappop` 📤: Retrieve the highest-priority task.  
- **Complexity**:  
  - Time: O(log n)  
  - Space: O(n)  

### 🗂️ **Task Class**  
Defines individual tasks with attributes:  
- **ID** 🔢  
- **Description** 📝  
- **Duration** ⏳  
- **Dependencies** 🔗  
- **Importance** 🔴🟡🟢  

### 🏗️ **TaskScheduler**  
Manages task execution and ensures logical ordering:  
- Dynamically recalculates task priorities.  
- Handles **fixed** ⏰ and **flexible** 🕒 tasks seamlessly.  

---

## 🧪 Tests and Results  

### ✅ Test Cases  
1. **No Dependencies**: Executes tasks based on importance and duration.  
2. **Idle Time Optimization**: Fills idle slots with flexible tasks.  
3. **Complex Dependency Chains**: Maintains logical execution order.  

### 📊 Empirical Analysis  
- **Runtime Efficiency**: Logarithmic growth for heap operations.  
- **Consistency**: Execution order remains the same across input variations.  

## 📈 Visualization  

Performance metrics were plotted to analyze runtime efficiency and scheduling consistency.  

---

## 🏁 Getting Started  

1. Clone the repository:  
   ```bash  
   git clone https://github.com/yourusername/priority-scheduler.git  
   ```  
2. Install dependencies:  
   ```bash  
   pip install matplotlib pandas  
   ```  
3. Run the scheduler:  
   ```bash  
   python priority_scheduler.py  
   ```  

## 📜 License  

This project is licensed under the **MIT License**. See the `LICENSE` file for details.  

---  
