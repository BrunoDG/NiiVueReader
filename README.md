# Niivue 3D File Reader - Test task

The task was to create a simple 3D `.nii.gz` file viewer with Vue 3, Typescript, Niivue and Plotly.
It was decided that this was to be created with the stack defined below.

## Tech Stack

- Frontend:
  - Vue 3
  - Typescript
  - Plotly.js
  - Niivue

- Backend:
  - Python 3.12
  - FastAPI

## Project Structure

This project uses the following structure:

- backend
  - main.py
    - _Main file where all endpoints are located_
  - poetry.lock
    - _.lock file, similar to package-json.lock on frontend_
  - pyproject.toml
    - _contains all backend dependencies, similar to package.json on frontend_

- neuro-frontend
  - public
  - src
    - assets
    - components
      - NiivueViewer.vue
        - _Package responsible to visualize `.nii.gz` files on the browser_
      - TimeSeriesChart.vue
        - _Package responsible to create the time series chart, using Plotly.js_
    - stores
      - PointsStore.ts
        - _Pinia store file to separate points from one view to another_
    - App.vue
      - _Main file that renders the project on browser_
