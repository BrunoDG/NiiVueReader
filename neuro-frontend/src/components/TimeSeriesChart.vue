<template>
    <div ref="chartDiv" style="width: 100%; height: 400px;"></div>
</template>

<script lang="ts" setup>
import { onMounted, ref, watch } from 'vue'
import * as Plotly from 'plotly.js-dist-min'
import type { Point } from '../stores/PointsStore'

// Definindo props e seus tipos
const props = defineProps<{
    points: Point[]
}>()

const chartDiv = ref<HTMLDivElement | null>(null)

function plotChart() {
    if (!chartDiv.value) return

    const data: Plotly.Data[] = props.points.map((p, idx) => {
        const xValues = Array.from({ length: 10 }, (_, i) => i)
        const yValues = xValues.map(() => Math.random() * 100)

        return {
            x: xValues,
            y: yValues,
            type: 'scatter',
            mode: 'lines+markers',
            name: `Point ${idx}`,
        }
    })

    const layout = {
        title: 'Time Series for Selected Points',
        xaxis: { title: 'Time' },
        yaxis: { title: 'Signal Intensity' },
    }
    const config = { responsive: true }

    Plotly.newPlot(chartDiv.value, data, layout, config)
}

onMounted(() => {
    plotChart()
})

watch(
    () => props.points,
    () => {
        plotChart()
    },
    { deep: true }
)
</script>
