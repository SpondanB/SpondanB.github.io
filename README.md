# SpondanB.github.io

This repository contains the source for my personal website and portfolio, built with Sphinx and published to GitHub Pages. The site hosts documentation and project write-ups covering machine learning, computer vision, and other experiments.

## Repository structure

- [docs/source](docs/source): Sphinx source files written in Markdown/MyST, including the landing page, project pages, and about page.
- [docs/build](docs/build): generated HTML output from local Sphinx builds.
- [.github/workflows/deploy-docs.yml](.github/workflows/deploy-docs.yml): GitHub Actions workflow that builds the documentation on pushes to the main branch and deploys it to GitHub Pages.
- [requirements.txt](requirements.txt): Python dependencies required to build the documentation locally.

## Local development

1. Create and activate a Python virtual environment.
2. Install the dependencies:
   `pip install -r requirements.txt`
3. Build the documentation:
   `cd docs`
   `make html`
4. Open the generated site at [docs/build/html/index.html](docs/build/html/index.html).

## Deployment

Pushing to the main branch triggers the deployment workflow, which installs the required packages, builds the Sphinx site, and publishes the generated HTML to GitHub Pages.

## Notes

The documentation content currently includes project pages for topics such as genetic algorithms, gesture-controlled Flappy Bird, PCA, and pathfinding.
