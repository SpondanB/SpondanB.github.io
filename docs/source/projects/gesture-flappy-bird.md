---
myst:
  html_meta:
    "description": "Gesture-Controlled Flappy Bird — Spondan Bandyopadhyay"
---

# Gesture-Controlled Flappy Bird

**A Computer Vision-driven game interface using MediaPipe and OpenCV to bridge physical movement and digital play.**

:::{button-link} https://github.com/SpondanB/FlappyBirdWithGestures
:color: primary
:outline:
View Source on GitHub
:::

---

## 🖐️ The Innovation
While Flappy Bird is traditionally a "tap-to-play" game, this project replaces tactile input with **Real-time Hand Tracking**. By leveraging a webcam, the system identifies specific landmarks on the user's hand to control the bird's flight, transforming a simple game into an interactive HCI experiment.



---

## 🛠️ How it Works

The project is built on a modular Python architecture that separates the vision processing from the game engine.

### 1. Computer Vision Pipeline
The core of the interaction relies on **MediaPipe’s Hands API**. 
* **Landmark Tracking:** The system tracks 21 3D hand landmarks at 30+ FPS.
* **Gesture Logic:** I implemented a distance-threshold algorithm. When the distance between the **Index Finger Tip (ID 8)** and **Thumb Tip (ID 4)** falls below a specific threshold, a "pinch" is registered.
* **Input Mapping:** This pinch gesture triggers the "jump" function in the game's physics engine.

### 2. Game Engine (Pygame)
The game environment is built using **Pygame**, handling:
* **Frame-Independent Physics:** Ensuring the bird's gravity feels consistent regardless of the camera's processing speed.
* **Collision Detection:** Pixel-perfect detection between the bird sprite and the moving pipe obstacles.
* **Dynamic Scoring:** Real-time UI updates to show the player's progress.

---

## 🚀 Technical Challenges

### Latency vs. Accuracy
The primary challenge was minimizing the "input lag" between a physical pinch and the bird's reaction. 
* **Solution:** I optimized the OpenCV frame processing by resizing the input buffer and limiting the MediaPipe detection to a single hand, significantly reducing the CPU overhead and ensuring a "snappy" feel.

### Lighting and Calibration
Variations in background lighting can often break hand-tracking models.
* **Solution:** I implemented a robust thresholding logic that focuses on the relative distance between landmarks rather than absolute pixel positions, making the gesture recognition invariant to the user's distance from the camera.

---

## 📋 Features
* **Real-time Visualization:** Overlay of the hand skeleton directly on the webcam feed for user feedback.
* **Automated Scaling:** The game adjusts its difficulty based on the stability of the gesture detection.
* **High-Performance Loop:** Seamless integration of a CV loop and a Game loop using Python’s multi-threading principles.

---

## 🧰 Tech Stack
* **Language:** Python
* **Vision:** OpenCV, MediaPipe
* **Game Dev:** Pygame
* **Math:** NumPy (for coordinate transformations and distance calculations)

---

### Project Impact
This project serves as a proof-of-concept for **touchless interfaces**. The same logic used here to make a bird fly can be applied to surgical interfaces, sterile industrial environments, or accessible technology for users with limited motor skills.