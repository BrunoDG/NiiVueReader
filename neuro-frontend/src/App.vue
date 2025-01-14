<template>
  <div>
      <NiivueViewer :volumeUrl="volumeUrl" @point-added="onPointAdded" />
  </div>

  <!-- Selected points list -->
  <div class="mt-4 flex flex-col lg:flex-row">
    <!-- Data Chart -->
    <div class="flex-1 p-4 border rounded bg-gray-100 shadow">
      <TimeSeriesChart :points="pointsStore.points" />
    </div>
    <div class="flex-1 p-4 border rounded bg-gray-100 shadow">
      <h2 class="text-lg font-bold justify-between">Selected Points</h2>
      <div v-for="(p, idx) in pointsStore.points" :key="idx" class="flex items-center gap-2 mt-2 border rounded shadow">
        <div>
          {{ p.mm }} (mm) - {{ p.idx }} (voxel)
        </div>
        <button @click="removePoint(idx)" class="px-2 py-1 bg-red-500 text-white rounded hover:bg-red-700">
          Remove
        </button>
      </div>
    </div>
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