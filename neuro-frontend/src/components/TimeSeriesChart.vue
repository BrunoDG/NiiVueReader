<template>
    <div ref="chartDiv" style="width: 100%; height: 400px;"></div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, watch } from 'vue'
import Plotly from 'plotly.js/dist/plotly'
import type { Point } from '../stores/PointsStore'

export default defineComponent({
    name: 'TimeSeriesChart',
    props: {
        points: {
            type: Array as () => Point[],
            default: () => [],
        },
    },
    setup(props) {
        const chartDiv = ref<HTMLDivElement | null>(null)

        // Gera dados (exemplo) para cada ponto
        function fetchTimeSeriesData(points: Point[]): Plotly.Data[] {
            return points.map((p, idx) => {
                const xValues = Array.from({ length: 10 }, (_, i) => i)
                const yValues = xValues.map(() => Math.random() * 100)

                return {
                    x: xValues,
                    y: yValues,
                    type: 'scatter',
                    mode: 'lines+markers',
                    name: `Point ${idx}`,
                } as Plotly.ScatterData
            })
        }

        function plotChart() {
            if (!chartDiv.value) return

            const data = fetchTimeSeriesData(props.points)
            const layout: Partial<Plotly.Layout> = {
                title: 'Time Series for Selected Points',
                xaxis: { title: 'Time' },
                yaxis: { title: 'Signal Intensity' },
            }
            const config: Partial<Plotly.Config> = { responsive: true }

            Plotly.newPlot(chartDiv.value, data, layout, config)
        }

        // Render inicial
        onMounted(() => {
            plotChart()
        })

        // Re-render quando 'points' mudar
        watch(
            () => props.points,
            () => {
                plotChart()
            },
            { deep: true }
        )

        return {
            chartDiv,
        }
    },
})
</script>
