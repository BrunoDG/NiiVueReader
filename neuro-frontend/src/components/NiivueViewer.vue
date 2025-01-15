<template>
    <canvas ref="canvasContainer" class="niivue-container"></canvas>
</template>

<script lang="ts" setup>
// 1) Imports
import { onMounted, ref, watch } from 'vue'
import { Niivue, type NVConnectomeNode} from '@niivue/niivue'
import { usePointsStore, type Point } from '../stores/PointsStore'
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
    let payload: Point = {
        mm: [0, 0, 0],
        idx: [0,0,0],
    }

    if (canvasContainer.value) {
        // TODO: Check what did he want to do with this canvas
        // Fixed. Now canvasContainer is a HTMLCanvasElement 
        nv.attachToCanvas(canvasContainer.value)
    }

    try {
        const response = await axios.get(props.volumeUrl)
        await nv.loadVolumes([{ url: response.data.url }])
    } catch (error) {
        console.error('Error loading volume: ', error);
    }

    nv.onLocationChange = (point: Point) => {
        payload = {
            mm: point.mm,
            idx: point.idx,
        };
    }
    
    // TODO: Verify how function onLocationChange works properly
    nv.onMouseUp = () => {
        if (payload.mm && payload.idx) {
            emit('point-added', payload);
        } else {
            console.warn('Ignored interaction, since it\'s not on a 2D view')
        }
    }
})
</script>