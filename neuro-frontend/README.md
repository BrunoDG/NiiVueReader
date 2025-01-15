# Frontend Structure

- public
- src
  - assets
  - components
    - NiivueViewer.vue
      - _Component responsible for rendering `.nii.gz` files on browser_
    - TimeSeriesChart.vue
      - _Component responsible for the time series chart, using Plotly.js_
    - NodesTble.vue
      - _Component responsible for drawing table with all saved nodes positions_
    - ui
      - _Folder with all Shadcn/Vue components that were imported within the project_
  - stores
    - PointsStore.ts
      - _Pinia store file to separate points from one view to another_
  - App.vue
    - _Main file that renders the project on browser_
