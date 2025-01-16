<template>
    <Card>
        <!-- Header -->
        <CardHeader>
            <CardTitle>Brain Scan Visualization</CardTitle>
            <CardDescription>
                Interact with the medical data visualization below.
            </CardDescription>
        </CardHeader>

        <!-- Canvas -->
        <CardContent>
            <div class="relative">
                <!-- loading spinner -->
                <div v-if="isLoading"
                    class="absolute inset-0 flex items-center justify-center bg-white bg-opacity-50 z-10">
                    <!-- Spinner -->
                    <div class="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
                </div>
                <!-- Canvas -->
                <canvas ref="canvasContainer" class="w-[600px] h-[200px] border rounded"></canvas>
            </div>
        </CardContent>

        <!-- Footer -->
        <CardFooter class="flex justify-between items-center space-x-4">
            <!-- DropdownMenu para Visualizações -->
            <div>
                <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                        <Button variant="outline" size="sm">
                            {{ selectedView }} View
                        </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent>
                        <DropdownMenuItem @click="setView('Axial')">Axial</DropdownMenuItem>
                        <DropdownMenuItem @click="setView('Sagittal')">Sagittal</DropdownMenuItem>
                        <DropdownMenuItem @click="setView('Coronal')">Coronal</DropdownMenuItem>
                        <DropdownMenuItem @click="setView('3D')">3D</DropdownMenuItem>
                        <DropdownMenuItem @click="setView('Mixed')">Mixed</DropdownMenuItem>
                    </DropdownMenuContent>
                </DropdownMenu>
            </div>
            <!-- Botão Reload Volume -->
            <Button variant="default" size="sm" @click="reloadVolume">Reload Volume</Button>
        </CardFooter>
    </Card>
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue';
import { Niivue, NVMesh, type NVConnectomeNode } from '@niivue/niivue';
import { usePointsStore, type Point } from '@/stores/PointsStore';
import axios from 'axios';

import { Card, CardHeader, CardContent, CardFooter, CardTitle, CardDescription } from '@/components/ui/card';
import { DropdownMenu, DropdownMenuItem, DropdownMenuTrigger, DropdownMenuContent } from '@/components/ui/dropdown-menu';
import { Button } from '@/components/ui/button';

// Props
const props = defineProps<{
    volumeUrl: string
}>()

// Store e Canvas
const pointsStore = usePointsStore()
const canvasContainer = ref<HTMLCanvasElement | null>(null)
let nv: Niivue | null = null
const isLoading = ref(false)
const selectedView = ref('Mixed')

// Converter Point para NVConnectomeNode
function convertPointToNode(point: { mm: [number, number, number] }): NVConnectomeNode {
    return {
        name: 'node',
        x: point.mm[0],
        y: point.mm[1],
        z: point.mm[2],
        sizeValue: 5,
        colorValue: 123,
    }
}

// Atualizar Mesh
function updateNodeMesh() {
    if (!nv) return

    const nodes = pointsStore.points.map((point) => convertPointToNode(point))

    const mesh = new NVMesh(
        new Float32Array(nodes.flatMap((node) => [node.x, node.y, node.z])),
        new Uint32Array([]),
        'connectomeMesh',
        new Uint8Array([255, 0, 0, 255]),
        1.0,
        true,
        nv.gl,
        "node"
    )

    nv.addMesh(mesh)
    nv.updateGLVolume()
}

// Change Visualization
function setView(view: 'Axial' | 'Sagittal' | 'Coronal' | '3D' | 'Mixed') {
    if (!nv) return

    selectedView.value = view

    switch (view) {
        case 'Axial':
            nv.setSliceType(nv.sliceTypeAxial)
            break
        case 'Sagittal':
            nv.setSliceType(nv.sliceTypeSagittal)
            break
        case 'Coronal':
            nv.setSliceType(nv.sliceTypeCoronal)
            break
        case '3D':
            nv.setSliceType(nv.sliceTypeRender)
            break
        case 'Mixed':
            nv.setSliceType(nv.sliceTypeMultiplanar)
            break
        default:
            console.warn('Unknown view type:', view)
    }
}

// Reset visualization
function resetView() {
    if (!nv) return;
    nv.setRenderAzimuthElevation(0, 0);
}
// Recarregar o Volume
async function reloadVolume() {
    if (!nv) return

    isLoading.value = true
    try {
        const response = await axios.get(props.volumeUrl)
        await nv.loadVolumes([{ url: response.data.url }])
        console.log('Volume reloaded successfully')
    } catch (error) {
        console.error('Error reloading volume:', error)
    } finally {
        isLoading.value = false
    }
}

onMounted(async () => {
    nv = new Niivue()
    let payload: Point = {
        mm: [0, 0, 0],
        idx: [0, 0, 0],
    }
    let coordChange = false

    if (canvasContainer.value) {
        nv.attachToCanvas(canvasContainer.value)
    }

    isLoading.value = true
    try {
        const response = await axios.get(props.volumeUrl)
        await nv.loadVolumes([{ url: response.data.url }])
    } catch (error) {
        console.error('Error loading volume:', error)
    } finally {
        isLoading.value = false
    }

    nv.onLocationChange = (point: Point) => {
        coordChange = true
        payload = {
            mm: point.mm,
            idx: point.idx,
        }
    }

    nv.onMouseUp = () => {
        if (coordChange) {
            coordChange = false
            pointsStore.addPoint(payload)
            updateNodeMesh()
        }
    }
})
</script>
