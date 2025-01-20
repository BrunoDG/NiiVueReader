<template>
  <div class="flex flex-col h-screen bg-black">
    <!-- MenuBar -->
    <MenuBar class="bg-gray-800 text-white shadow-md" />

    <!-- Viewer Section (Canvas) -->
    <div class="flex-1 bg-black content-center">
      <NiivueViewer :volumeUrl="volumeUrl" />
    </div>

    <!-- Bottom Section (Chart and Table) -->
    <div class="flex flex-col lg:flex-row h-[40%] p-2 gap-2 bg-black">
      <!-- Time Series Chart -->
      <div class="flex-1">
        <TimeSeriesChart :points="pointsStore.points" />
      </div>

      <!-- Nodes Table -->
      <div class="flex-1">
        <NodesTable />
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import MenuBar from '@/components/MenuBar.vue';
import NiivueViewer from '@/components/NiivueViewer.vue';
import TimeSeriesChart from '@/components/TimeSeriesChart.vue';
import NodesTable from '@/components/NodesTable.vue';
import { usePointsStore } from '@/stores/PointsStore';

const pointsStore = usePointsStore();
const volumeUrl = 'http://localhost:8000/api/volume';
</script>
