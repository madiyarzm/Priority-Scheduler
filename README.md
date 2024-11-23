# Priority Scheduler

A **Priority Scheduler** designed by Madiyar Zhunussov to optimize daily task management. This scheduler dynamically prioritizes tasks based on **dependencies**, **importance**, **duration**, and **fixed time constraints**. It employs **Max-Heap** and **Priority Queues** to efficiently allocate tasks while minimizing idle time and ensuring logical task execution.

---

## Features

### 1. **Task Prioritization**
- **Dynamic Utility Calculation**:
  - **Fixed Tasks**: Always scheduled at their designated times.
  - **Flexible Tasks**: Scheduled dynamically based on utility.
    - **Utility Formula**:  
      - `Utility = 100 − (Dependencies * 10) − Duration Penalty + Importance Bonus`
    - **Importance Levels**:
      - High: +30 points
      - Medium: +15 points
      - Low: +0 points
- Tasks with higher **importance** and **longer durations** are prioritized.

### 2. **Dependency Management**
- Tasks with dependencies are only scheduled after their prerequisites are completed.

### 3. **Efficiency Optimization**
- Minimizes idle time by fitting flexible tasks between fixed tasks.
- Dynamically recalculates task priorities after each completion.

### 4. **Flexibility**
- Supports fixed and flexible tasks, making it adaptable to real-life schedules.

---

## Code Implementation

### **MaxHeap**
Custom implementation of a max-heap for managing task priorities:
- **Time Complexity**:
  - `heappush`: O(log n)
  - `heappop`: O(log n)
- **Space Complexity**: O(n)

### **Task Class**
Defines tasks with attributes such as `id`, `description`, `duration`, `dependencies`, `importance`, and `is_fixed`.  
- **Key Method**: `calculate_priority()` computes task utility dynamically.

### **TaskScheduler**
Manages task execution using a priority queue:
- Handles fixed and flexible tasks.
- Resolves dependencies dynamically.
- Ensures efficient task ordering.


## Advantages

### Advantages
- Efficient handling of fixed and flexible tasks.
- Dynamic prioritization balances task importance and dependencies.
- Optimized scheduling minimizes idle time.

## Visualization

The scheduler's performance metrics were plotted using **Matplotlib** to analyze runtime efficiency and task order consistency.

---

## Getting Started

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/priority-scheduler.git
   ```
2. Install necessary libraries (if required):
   ```bash
   pip install matplotlib pandas
   ```
3. Run the `priority_scheduler.py` script:
   ```bash
   python priority_scheduler.py
   ```

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
