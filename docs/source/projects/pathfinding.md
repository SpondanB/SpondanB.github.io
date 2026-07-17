---
myst:
  html_meta:
    "description": "A* Pathfinding: Heuristic Grid Search — Spondan Bandyopadhyay"
---

# A* Pathfinding: Heuristic Grid Search

**An interactive visualization of the A* algorithm, demonstrating optimal pathfinding in a weighted graph environment.**

:::{button-link} https://github.com/SpondanB/A-Star_Path_finding_python
:color: primary
:outline:
View Source on GitHub
:::

---

## 🗺️ The Objective
The goal of this project was to demystify how autonomous agents—from GPS units to video game NPCs—find the shortest path between two points while navigating obstacles. By building a real-time visualizer, I can observe how the algorithm evaluates the search space and makes decisions based on cost and distance.



---

## 🛠️ The Mathematics of the Search
The A* algorithm is unique because it combines the strengths of **Dijkstra’s Algorithm** (shortest path) and **Greedy Best-First Search** (speed). It uses the following formula to rank nodes:

$$f(n) = g(n) + h(n)$$

* **$g(n)$**: The actual cost from the start node to the current node $n$.
* **$h(n)$**: The **Heuristic**—an estimated cost from node $n$ to the goal. In this project, I utilized the **Manhattan Distance** (L1 Norm) for the heuristic calculation.
* **$f(n)$**: The total estimated cost of the cheapest solution through node $n$.

---

## 🚀 Features & Functionality
The application is built using **Pygame**, allowing for a highly tactile experience:
* **Dynamic Grid:** Users can "draw" barriers and walls in real-time.
* **Interactive Placement:** Left-click to place start/end points and obstacles; right-click to erase.
* **Visual Debugging:** The grid changes color to represent the algorithm's state:
    * **Turquoise:** The "Closed Set" (nodes already evaluated).
    * **Red:** The "Open Set" (nodes discovered but not yet evaluated).
    * **Green:** The final calculated path.



---

## 🔧 Technical Challenges

### Priority Queue Management
Efficiently picking the node with the lowest $f(n)$ score is critical for performance. 
* **Solution:** I implemented a **Min-Priority Queue** using Python’s `heapq` module. This ensures that the algorithm always evaluates the most promising node next, keeping the time complexity to approximately $O(E \log V)$.

### Grid Scalability
Handling large grids requires efficient state management to avoid frame drops during the search.
* **Solution:** By decoupling the "State Logic" (the algorithm) from the "Rendering Logic" (Pygame), the visualizer remains responsive even as the search space expands.

---

## 🧰 Tech Stack
* **Language:** Python
* **Library:** Pygame
* **Data Structures:** Priority Queues, Sets, 2D Arrays

---

### Why this matters
Pathfinding is more than just games; it’s **optimization**. In a business context, these same principles apply to **logistics**, **supply chain routing**, and **resource allocation**. Understanding how to weigh current costs against future estimates is a core competency in operational strategy.