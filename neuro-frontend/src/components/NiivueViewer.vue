<template>
    <div ref="canvasContainer" class="niivue-container"></div>
</template>

<script lang="ts" setup>
// 1) Imports
import { onMounted, ref } from 'vue'
import { Niivue } from '@niivue/niivue'

// 2) Definir props e emits com as novas APIs
interface PointAddedPayload {
    mm: [number, number, number]
    idx: [number, number, number]
}

const props = defineProps<{
    volumeUrl: string
}>()

const emit = defineEmits<{
    (e: 'point-added', payload: PointAddedPayload): void
}>()

// 3) Lógica do setup
const canvasContainer = ref<HTMLDivElement | null>(null)
let nv: Niivue | null = null

onMounted(async () => {
    nv = new Niivue()
    if (canvasContainer.value) {
        // TODO: Check what did he want to do with this canvas
        nv.attachToCanvas(canvasContainer.value)
    }
    await nv.loadVolumes([{ url: props.volumeUrl, name: 'mainVolume' }])

    // TODO: Verify how function onLocationChange works proper
    nv.onLocationChange = (mm: any, vx: any) => {
        emit('point-added', { mm, idx: vx })
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
