---
myst:
  html_meta:
    "description": "Dimensionality Reduction: A PCA Dive — Spondan Bandyopadhyay"
---

# Dimensionality Reduction: A PCA Dive

**An analytical study on Principal Component Analysis (PCA) for high-dimensional data visualization and feature compression.**

:::{button-link} https://github.com/SpondanB/PrincipleComponentAnalysisStudy
:color: primary
:outline:
View Source on GitHub
:::

---

## 📉 The Objective
In modern data analytics, "The Curse of Dimensionality" often obscures meaningful patterns. This project is a comprehensive technical study of **Principal Component Analysis (PCA)**—a linear dimensionality reduction technique that transforms a large set of variables into a smaller one that still contains most of the information.



---

## 🛠️ Methodology & Implementation

The study follows a rigorous mathematical workflow to decompose complex datasets into their most significant components.

### 1. Data Preprocessing & Standardization
Since PCA is sensitive to the variances of the initial variables, I implemented a robust standardization pipeline.
* **Feature Scaling:** Centering the data around the mean with a standard deviation of 1 to ensure that all features contribute equally to the analysis.

### 2. Covariance Matrix & Eigen-Decomposition
The core of the study involves computing the **Covariance Matrix** to identify correlations.
* **Eigenvectors:** Determining the directions of the new feature space (Principal Components).
* **Eigenvalues:** Determining the magnitude (variance) explained by each component.

### 3. Dimensionality Selection
I utilized **Scree Plots** and **Cumulative Variance** analysis to determine the optimal number of components.
* **The Goal:** Retain ~95% of the dataset's variance while reducing the feature count by 50-70%.

---

## 📊 Key Visualizations

The study focuses on making abstract high-dimensional data interpretable through visualization.

::::{grid} 1 2 2 2
:gutter: 3

:::{grid-item-card} Feature Variance

^^^
Visualizing how much information each Principal Component captures from the original dataset.
:::

:::{grid-item-card} 2D/3D Projection

^^^
Transforming multi-dimensional clusters into 2D space to identify hidden patterns and outliers.
:::

::::

---

## 🚀 Practical Applications
This study demonstrates the utility of PCA in several real-world scenarios:
* **Data Compression:** Reducing storage and computational requirements for machine learning models.
* **Noise Filtering:** Removing minor variations (noise) by discarding components with low eigenvalues.
* **Feature Engineering:** Creating uncorrelated features to improve the performance of linear regression and clustering models.

---

## 🧰 Tech Stack
* **Language:** Python
* **Libraries:** NumPy (Matrix Math), Pandas (Data Manipulation), Matplotlib/Seaborn (Visualization)
* **Frameworks:** Scikit-Learn (PCA Implementation & Pipeline)
