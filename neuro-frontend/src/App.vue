<template>
  <NiivueViewer :volumeUrl="volumeUrl" @point-added="onPointAdded" />

  <!-- Lista de pontos selecionados -->
  <div v-for="(p, idx) in pointsStore.points" :key="idx">
    {{ p.mm }} (mm) - {{ p.idx }} (voxel)
    <button @click="removePoint(idx)">Remover</button>
  </div>

  <TimeSeriesChart :points="pointsStore.points" />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import NiivueViewer from './components/NiivueViewer.vue'
import TimeSeriesChart from './components/TimeSeriesChart.vue'
import { usePointsStore } from './stores/PointsStore.ts'

export default defineComponent({
  name: 'App',
  components: {
    NiivueViewer,
    TimeSeriesChart,
  },
  setup() {
    const pointsStore = usePointsStore()

    const volumeUrl = 'http://localhost:8000/api/data' // Exemplo

    function onPointAdded(payload: { mm: [number, number, number], idx: [number, number, number] }) {
      pointsStore.addPoint(payload)
    }

    function removePoint(index: number) {
      pointsStore.removePoint(index)
    }

    return {
      volumeUrl,
      pointsStore,
      onPointAdded,
      removePoint,
    }
  },
})
</script>