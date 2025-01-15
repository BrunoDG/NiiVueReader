<template>
  <div class="flex flex-col lg:flex-row">
    <!-- Viewer Section (Left) -->
    <div class="flex-1 lg:w-[60%] h-full p-1">
      <div class="h-full border rounded bg-gray-50 shadow">
        <NiivueViewer :volumeUrl="volumeUrl" />
      </div>
    </div>

    <!-- Right Section (Chart and Table) -->
    <div class="flex flex-col lg:w-[40%] h-full p-1 gap-2">
      <!-- Time Series Chart -->
      <div class="flex-1">
        <TimeSeriesChart :points="pointsStore.points" />
      </div>

      <!-- Nodes Table -->
      <div class="flex-1">
        <Card class="h-full">
          <CardHeader>
            <CardTitle class="items-center">Selected Points</CardTitle>
            <CardDescription>
              Manage selected points from the viewer.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <NodesTable />
          </CardContent>
        </Card>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import NiivueViewer from '@/components/NiivueViewer.vue'
import TimeSeriesChart from '@/components/TimeSeriesChart.vue'
import NodesTable from '@/components/NodesTable.vue'
import { usePointsStore } from '@/stores/PointsStore'
import { Card, CardHeader, CardContent, CardTitle, CardDescription } from '@/components/ui/card'

// Store and variables
const pointsStore = usePointsStore()
const volumeUrl = 'http://localhost:8000/api/volume'
</script>

<style scoped>
/* Personalize estilos aqui, se necessário */
</style>
