<template>
    <canvas ref="canvasContainer" class="niivue-container"></canvas>
</template>

<script lang="ts" setup>

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

const canvasContainer = ref<HTMLCanvasElement | null>(null)
let nv: Niivue | null = null

onMounted(async () => {
    nv = new Niivue()
    let payload: Point = {
        mm: [0, 0, 0],
        idx: [0,0,0],
    }

    if (canvasContainer.value) {
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

    // TODO: read from uiData, how is it calling and how do I read this property
    nv.onMouseUp = () => {
        if (payload.mm && payload.idx) {
            emit('point-added', payload);
        } else {
            console.warn('Ignored interaction, since it\'s not on a 2D view')
        }
    }
})
</script>