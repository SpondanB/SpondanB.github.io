---
# hide-toc: true
# hide-navigation: true
myst:
  html_meta:
    "description": "Projects by Spondan Bandyopadhyay — ML, AI, Computer Vision, and more."
    "keywords": "projects, data science, machine learning, AI, Spondan Bandyopadhyay"
---
# 📁 Projects

```{toctree}
:hidden:
:maxdepth: 1
:caption: Project List

face-avatar-project
genetic-algorithm
gesture-flappy-bird
pca-study
pathfinding
```

> A collection of things I've built, explored, and learned from.
> Some are polished. Some are experiments. All of them taught me something.

---

```{raw} html
<!-- Filter Buttons -->
<div class="proj-filters">
  <button class="proj-filter-btn active" data-filter="all">All</button>
  <button class="proj-filter-btn" data-filter="ml">Machine Learning</button>
  <button class="proj-filter-btn" data-filter="cv">Computer Vision</button>
  <button class="proj-filter-btn" data-filter="generative">Generative</button>
  <button class="proj-filter-btn" data-filter="study">Study / Research</button>
  <button class="proj-filter-btn" data-filter="webdev">Web Dev</button>
  <button class="proj-filter-btn" data-filter="graphics">Computer Graphics</button>
</div>

<!-- Project Cards Grid -->
<div class="proj-grid">

  <!-- Head Pose–Driven Facial Avatar (3D Skull) -->
  <div class="proj-card" data-tags="ml cv graphics">
    <div class="proj-card-header">
      <span class="proj-emoji">💀</span>
      <div class="proj-tag-list">
        <span class="proj-tag">Machine Learning</span>
        <span class="proj-tag">Computer Vision</span>
        <span class="proj-tag">Computer Graphics</span>
      </div>
    </div>
    <h3 class="proj-title">Head Pose–Driven Facial Avatar (3D Skull)</h3>
    <p class="proj-question"><em>How do Virtual Youtubers have their Avatars move with their own movement</em></p>
    <p class="proj-desc">Explored implementation of a Vtuber Model setup from scratch - built using the python language and opencv and Mediapipe libraries.This project demonstrates a real-time, camera-driven 3D animation system where a virtual skull mirrors a user's head orientation, eye blinks, and mouth movements using a standard webcam.</p>
    <div class="proj-meta">
      <span>🛠 Python · OpenCV · Mediapipe</span>
      <span>✅ Complete</span>
    </div>
    <div class="proj-links">
      <a href="https://github.com/SpondanB/Virtual-Skull-Avatar" target="_blank" class="proj-btn">GitHub →</a>
      <a href="../projects/face-avatar-project.html" class="proj-btn proj-btn-secondary">Read More →</a>
    </div>
  </div>
  
  <!-- Image Generation via Genetic Algorithm -->
  <div class="proj-card" data-tags="ml generative">
    <div class="proj-card-header">
      <span class="proj-emoji">🧬</span>
      <div class="proj-tag-list">
        <span class="proj-tag">Machine Learning</span>
        <span class="proj-tag">Generative</span>
      </div>
    </div>
    <h3 class="proj-title">Image Generation via Genetic Algorithm</h3>
    <p class="proj-question"><em>What if evolution could paint a picture?</em></p>
    <p class="proj-desc">Explored genetic algorithms by evolving pixel populations
    toward a target image — a hands-on way to understand selection, mutation, and
    fitness functions outside the usual ML stack.</p>
    <div class="proj-meta">
      <span>🛠 JavaScript · p5.js</span>
      <span>✅ Complete</span>
    </div>
    <div class="proj-links">
      <a href="https://github.com/SpondanB/2105907_AI" target="_blank" class="proj-btn">GitHub →</a>
      <a href="../projects/genetic-algorithm.html" class="proj-btn proj-btn-secondary">Read More →</a>
    </div>
  </div>

  <!-- Gesture-Controlled Flappy Bird -->
  <div class="proj-card" data-tags="cv ml graphics">
    <div class="proj-card-header">
      <span class="proj-emoji">🎮</span>
      <div class="proj-tag-list">
        <span class="proj-tag">Computer Vision</span>
        <span class="proj-tag">Machine Learning</span>
        <span class="proj-tag">Game Dev</span>
      </div>
    </div>
    <h3 class="proj-title">Gesture-Controlled Flappy Bird</h3>
    <p class="proj-question"><em>Your hands are the controller.</em></p>
    <p class="proj-desc">Built a real-time hand-tracking pipeline to replace keyboard
    input in a game. Turned out hand tracking is trickier — and more fun — than it looks.</p>
    <div class="proj-meta">
      <span>🛠 Python · OpenCV · MediaPipe</span>
      <span>✅ Complete</span>
    </div>
    <div class="proj-links">
      <a href="https://github.com/SpondanB/FlappyBirdWithGestures" target="_blank" class="proj-btn">GitHub →</a>
      <a href="../projects/gesture-flappy-bird.html" class="proj-btn proj-btn-secondary">Read More →</a>
    </div>
  </div>

  <!-- PCA Study -->
  <div class="proj-card" data-tags="ml study">
    <div class="proj-card-header">
      <span class="proj-emoji">📐</span>
      <div class="proj-tag-list">
        <span class="proj-tag">Machine Learning</span>
        <span class="proj-tag">Study / Research</span>
      </div>
    </div>
    <h3 class="proj-title">PCA — From Scratch vs sklearn</h3>
    <p class="proj-question"><em>Does the library do what you think it does?</em></p>
    <p class="proj-desc">Implemented PCA from scratch, then compared it against
    sklearn's version on real data. Benchmarked both with KNN to measure the
    accuracy cost (or gain) of reducing dimensions.</p>
    <div class="proj-meta">
      <span>🛠 Python · NumPy · scikit-learn</span>
      <span>✅ Complete</span>
    </div>
    <div class="proj-links">
      <a href="https://github.com/SpondanB/PrincipleComponentAnalysisStudy" target="_blank" class="proj-btn">GitHub →</a>
      <a href="../projects/pca-study.html" class="proj-btn proj-btn-secondary">Read More →</a>
    </div>
  </div>

  <div class="proj-card" data-tags="graphics study">
    <div class="proj-card-header">
      <span class="proj-emoji">🗺️</span>
      <div class="proj-tag-list">
        <span class="proj-tag">Computer Graphics</span>
        <span class="proj-tag">Study / Research</span>
      </div>
    </div>
    <h3 class="proj-title">A* Pathfinding — Heuristic Search</h3>
    <p class="proj-question"><em>How do machines find the most efficient path?</em></p>
    <p class="proj-desc">An interactive implementation of the A* algorithm using Pygame. 
    Features a real-time grid where users can place obstacles and watch the 
    weighted graph search balance cost (g) and heuristic (h) to find the optimal route.</p>
    <div class="proj-meta">
      <span>🛠 Python · Pygame · Data Structures</span>
      <span>✅ Complete</span>
    </div>
    <div class="proj-links">
      <a href="https://github.com/SpondanB/A-Star_Path_finding_python" target="_blank" class="proj-btn">GitHub →</a>
      <a href="../projects/pathfinding.html" class="proj-btn proj-btn-secondary">Read More →</a>
    </div>
  </div>

  <!-- Placeholder for future projects -->
  <!-- <div class="proj-card" data-tags="webdev">
    <div class="proj-card-header">
      <span class="proj-emoji">🌐</span>
      <div class="proj-tag-list">
        <span class="proj-tag">Web Dev</span>
      </div>
    </div>
    <h3 class="proj-title">Shopping Cart App</h3>
    <p class="proj-question"><em>Full-stack from the ground up.</em></p>
    <p class="proj-desc">Built during my Hexaware internship — a full-stack shopping
    cart with a customer storefront and admin dashboard, backed by MongoDB. Covered
    auth, database integration, and UI design end to end.</p>
    <div class="proj-meta">
      <span>🛠 React · Node.js · MongoDB</span>
      <span>✅ Complete</span>
    </div>
    <div class="proj-links">
      <a href="#" class="proj-btn proj-btn-muted">Private Repo</a>
    </div>
  </div> -->

</div>

<!-- No results message -->
<p class="proj-empty" style="display:none;">
  No projects found for this filter. More coming soon!
</p>

<script>
  const filterBtns = document.querySelectorAll('.proj-filter-btn');
  const cards = document.querySelectorAll('.proj-card');
  const empty = document.querySelector('.proj-empty');

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const filter = btn.dataset.filter;
      let visible = 0;

      cards.forEach(card => {
        const tags = card.dataset.tags.split(' ');
        const show = filter === 'all' || tags.includes(filter);
        card.style.display = show ? 'flex' : 'none';
        if (show) visible++;
      });

      empty.style.display = visible === 0 ? 'block' : 'none';
    });
  });
</script>
```