---
myst:
  html_meta:
    "description": "Head Pose–Driven Facial Avatar (3D Skull) — Spondan Bandyopadhyay"
---

# Head Pose–Driven Facial Avatar (3D Skull)

**An exploration of real-time computer vision and software rendering, where a virtual 3D skull mirrors human facial movements without relying on traditional game engines or graphics APIs.**

:::{button-link} https://github.com/SpondanB/Virtual-Skull-Avatar
:color: primary
:outline:
View Source on GitHub
:::

---

## 📸 The Concept

I've always been fascinated by how digital characters come to life. Whether in games, films, or augmented reality, believable character animation sits at the intersection of **computer vision**, **computer graphics**, and **human-computer interaction**. This project was my attempt to understand that process from the ground up.

Rather than importing a 3D model into Unity or Unreal Engine, I wanted to build the entire pipeline myself—starting from a webcam image and ending with a fully animated 3D object. The result is a system where a virtual skull mirrors my head movements, blinks when I blink, and opens its jaw as I speak, all rendered in real time using nothing more than **Python**, **OpenCV**, **MediaPipe**, **NumPy**, and **Pygame**.

This project is an evolution of an earlier face-tracking experiment that I developed while learning computer vision. Revisiting it gave me the opportunity to redesign the rendering pipeline, improve pose estimation, implement smoother animation, and experiment with procedural visual effects.

The primary goal wasn't simply to create an animated skull—it was to better understand the mathematics and engineering behind modern interactive graphics systems.

---

## 🛠️ Technical Architecture

The project combines several independent systems into a single real-time rendering pipeline.

### 1. Face Tracking

Everything begins with a webcam feed.

Each captured frame is processed using **MediaPipe Face Mesh**, which predicts **468 facial landmarks** in real time. Although the model outputs hundreds of landmarks, only a carefully selected subset is required for pose estimation:

* Nose tip
* Chin
* Left eye corner
* Right eye corner
* Left mouth corner
* Right mouth corner

These landmarks provide a stable geometric representation of the face while remaining computationally lightweight.

---

### 2. Head Pose Estimation

Once the facial landmarks are detected, the next challenge is determining the orientation of the user's head in three-dimensional space.

A predefined 3D facial model is paired with the detected 2D image coordinates and passed into **OpenCV's Perspective-n-Point (PnP)** solver.

The pipeline looks like this:

```text
3D Face Model
        +
2D Facial Landmarks
        │
        ▼
cv2.solvePnP()
        │
        ▼
Rotation Vector
        │
        ▼
Rodrigues Transformation
        │
        ▼
Rotation Matrix
        │
        ▼
Pitch • Yaw • Roll
```

One challenge I encountered was the occasional **180° pose flip**, where solvePnP would suddenly return an alternate but mathematically valid solution. Instead of introducing a complex filtering algorithm, I implemented a lightweight temporal consistency check that compares consecutive rotation matrices and rejects unrealistic jumps. This significantly improved stability while keeping the system responsive.

---

### 3. Facial Animation

Once the head orientation is known, the renderer adds expression through two procedural animations.

#### 👁 Blink Detection

Eye blinking is estimated using the **Eye Aspect Ratio (EAR)**.

Rather than simply toggling between open and closed states, blink intensity is smoothly interpolated over time. The eye sockets gradually transition from dark cavities to lighter "closed" surfaces, producing a surprisingly convincing blink despite the skull's minimalist design.

#### 👄 Jaw Animation

The distance between the upper and lower lip landmarks is used to estimate mouth openness.

Instead of introducing skeletal rigging, the lower jaw vertices are translated downward and slightly forward. Although mathematically simple, this approach captures the essence of jaw movement while keeping the geometry easy to manipulate.

Temporal smoothing ensures that speaking produces fluid motion instead of abrupt jumps.

---

### 4. Building a Software Renderer

Perhaps the most rewarding part of this project was implementing the rendering pipeline manually.

Instead of relying on OpenGL or a game engine, every frame follows the traditional graphics pipeline:

* Construct rotation matrices
* Transform vertices into world space
* Project 3D coordinates into screen space
* Compute polygon normals
* Apply directional lighting
* Sort polygons by depth
* Rasterize triangles using Pygame

Even the skull itself is hand-built from lists of vertices and triangular faces rather than imported from external modelling software.

Implementing these stages from scratch gave me a much deeper appreciation for the mathematics behind modern graphics engines.

---

### 5. Lighting & Depth

To provide depth perception, every face of the skull computes its own surface normal using the cross product.

A directional light source is then applied through a Lambertian diffuse lighting model combined with ambient illumination.

Since Pygame does not include a depth buffer, polygons are sorted using the **Painter's Algorithm**, rendering distant surfaces before closer ones.

Although simple compared to GPU rendering, this approach produces convincing three-dimensional shading while remaining lightweight enough for real-time execution.

---

### 6. Procedural Particle System

To make the final visualization feel less static, I added a procedural particle system beneath the jaw.

Each particle maintains:

* Position
* Velocity
* Lifetime
* Size

Particles spawn beneath the jaw, slowly drift upward under simulated acceleration, gradually fade away using alpha blending, and are continuously recycled.

This feature has little impact on performance but adds personality to the visualization while providing an opportunity to experiment with lightweight physics simulation.

---

## 🔄 Rendering Pipeline

```text
               Webcam
                  │
                  ▼
      MediaPipe Face Mesh
                  │
                  ▼
      Facial Landmark Detection
                  │
                  ▼
        OpenCV solvePnP()
                  │
                  ▼
         Rotation Matrix
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
   Blink Detection     Mouth Detection
        │                   │
        └─────────┬─────────┘
                  ▼
       Skull Transformation
                  │
                  ▼
      Lighting & Projection
                  │
                  ▼
        Depth Sorting
                  │
                  ▼
      Procedural Particles
                  │
                  ▼
        Pygame Renderer
```

---

## 🚀 Challenges & Lessons Learned

One of the biggest challenges wasn't implementing the mathematics—it was making everything behave naturally.

* **Pose Instability:** Small errors in landmark detection occasionally caused dramatic orientation flips. Investigating why this happened taught me more about Perspective-n-Point estimation than simply following tutorials ever could.

* **Software Rendering:** Drawing hundreds of triangles manually every frame made me appreciate how much work modern GPUs perform automatically. Building the renderer myself strengthened my understanding of coordinate systems, transformations, and projection.

* **Animation:** Small details such as smoothing blink intensity or gradually translating the jaw dramatically improved the realism of the final result. It reinforced how animation often depends more on interpolation than complexity.

* **Geometry Design:** Constructing the skull from raw vertices and faces required thinking about topology rather than modelling tools, giving me a better intuition for how 3D meshes are actually represented.

Perhaps the biggest takeaway from this project was that many graphics techniques we take for granted are ultimately elegant applications of linear algebra and geometry.

---

## 🔮 Future Improvements

If I continue developing this project, I'd like to explore:

* Importing detailed meshes from Blender
* Texture mapping and UV coordinates
* Quaternion-based rotation interpolation
* Skeletal animation instead of vertex translation
* GPU rendering with OpenGL or ModernGL
* Multiple face tracking
* Emotion recognition
* Audio-driven lip synchronization
* AR overlays using camera calibration

---

## Conclusion

This project represents much more than an animated skull—it represents my journey into understanding how computer vision and computer graphics intersect.

By building the rendering pipeline from scratch, implementing head pose estimation manually, and designing procedural facial animation without external engines, I gained practical experience in areas that are fundamental to modern graphics, robotics, augmented reality, and intelligent interactive systems.

Looking back, what started as a simple face-tracking experiment evolved into one of the projects that most strengthened my intuition for linear algebra, geometry, rendering, and real-time computer vision. It remains one of my favourite projects because it reflects how I enjoy learning: by building systems from first principles and understanding how every piece fits together.

---

## 🧰 Tech Stack

* **Language:** Python
* **Computer Vision:** OpenCV, MediaPipe Face Mesh
* **Graphics:** Pygame
* **Numerical Computing:** NumPy
* **Concepts:** Head Pose Estimation, Perspective Projection, Linear Algebra, Software Rendering, Computer Vision, Human-Computer Interaction, Procedural Animation, Real-Time Graphics