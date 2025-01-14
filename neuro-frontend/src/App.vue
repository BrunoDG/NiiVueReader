<template>
  <div>
    <NiivueViewer :volumeUrl="volumeUrl" @point-added="onPointAdded" />

    <!-- Lista de pontos selecionados -->
    <div v-for="(p, idx) in pointsStore.points" :key="idx">
      {{ p.mm }} (mm) - {{ p.idx }} (voxel)
      <button @click="removePoint(idx)">Remover</button>
    </div>
  </div>
  <div>
    <TimeSeriesChart :points="pointsStore.points" />
  </div>
</template>

<script lang="ts" setup>
import NiivueViewer from './components/NiivueViewer.vue'
import TimeSeriesChart from './components/TimeSeriesChart.vue'
import { usePointsStore } from './stores/PointsStore.ts'

// Store and variables
const pointsStore = usePointsStore()
const volumeUrl = 'http://localhost:8000/api/volume'

// event functions
function onPointAdded(payload: { mm: [number, number, number]; idx: [number, number, number] }) {
  pointsStore.addPoint(payload)
}

function removePoint(index: number) {
  pointsStore.removePoint(index)
}
</script>