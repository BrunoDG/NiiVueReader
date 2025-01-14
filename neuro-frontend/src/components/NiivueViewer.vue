<template>
    <canvas ref="canvasContainer" class="niivue-container"></canvas>
</template>

<script lang="ts" setup>
// 1) Imports
import { onMounted, ref } from 'vue'
import { Niivue } from '@niivue/niivue'
import type { Point } from '../stores/PointsStore'
import axios from 'axios'

const props = defineProps<{
    volumeUrl: string
}>()

const emit = defineEmits<{
    (e: 'point-added', payload: Point): void
}>()

// 3) Lógica do setup
const canvasContainer = ref<HTMLCanvasElement | null>(null)
let nv: Niivue | null = null

onMounted(async () => {
    nv = new Niivue()
    if (canvasContainer.value) {
        // TODO: Check what did he want to do with this canvas
        // Fixed. Now canvasContainer is a HTMLCanvasElement 
        nv.attachToCanvas(canvasContainer.value)
    }

    try {
        console.log('Fetching volume...')
        const response = await axios.get(props.volumeUrl)

        console.log('Volume fetched, loading on Niivue...')

        await nv.loadVolumes([{ url: response.data.url }])

        console.log('Volume loaded succesfully')
    } catch (error) {
        console.error('Error loading volume: ', error);
    }
    
    // TODO: Verify how function onLocationChange works properly
    nv.onLocationChange = (point: Point) => {
        const payload: Point = {
            mm: point.mm,
            idx: point.idx,
        };
        emit('point-added', payload);
    }
})
</script>

<style scoped>
.niivue-container {
    width: 100%;
    height: 600px;
    position: relative;
}
</style>
