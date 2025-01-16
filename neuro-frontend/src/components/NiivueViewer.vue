<template>
    <div class="relative w-full h-[80%] align-middle">
        <!-- Canvas -->
        <canvas ref="canvasContainer" class="w-full h-full"></canvas>

        <!-- Floating Dropdown Menu Button -->
        <div class="absolute top-4 left-4 z-10">
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
    </div>
    <Toast />
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue';
import { Niivue, NVMesh, type NVConnectomeNode } from '@niivue/niivue';
import axios from 'axios';
// Ui Components
import { DropdownMenu, DropdownMenuItem, DropdownMenuTrigger, DropdownMenuContent } from '@/components/ui/dropdown-menu';
import { Button } from '@/components/ui/button';
import { useToast } from '@/components/ui/toast';
// Points store properties
import { Point, usePointsStore } from '@/stores/PointsStore';
import { isConstructorDeclaration } from 'typescript';

const props = defineProps<{
    volumeUrl: string
}>()

const pointsStore = usePointsStore();
const { toast } = useToast();

// Refs and variáveis
const canvasContainer = ref<HTMLCanvasElement | null>(null);
const canvasHeight = ref(600); // Initial canvas height
const selectedView = ref('Mixed');
let nv: Niivue | null = null;

/**
 * Set NIfTI file rendering view on canvas
 * @param view View mode rendered on canvas
 */
function setView(view: 'Axial' | 'Sagittal' | 'Coronal' | '3D' | 'Mixed') {
    if (!nv) return;

    selectedView.value = view;

    switch (view) {
        case 'Axial':
            nv.setSliceType(nv.sliceTypeAxial);
            break;
        case 'Sagittal':
            nv.setSliceType(nv.sliceTypeSagittal);
            break;
        case 'Coronal':
            nv.setSliceType(nv.sliceTypeCoronal);
            break;
        case '3D':
            nv.setSliceType(nv.sliceTypeRender);
            break;
        case 'Mixed':
            nv.setSliceType(nv.sliceTypeMultiplanar);
            break;
        default:
            console.warn('Unknown view type:', view);
    }

    // Update canvas size
    nv.updateGLVolume();
}

// Converter Point para NVConnectomeNode
function convertPointToNode(point: { mm: [number, number, number] }): NVConnectomeNode {
    return {
        name: 'node',
        x: point.mm[0],
        y: point.mm[1],
        z: point.mm[2],
        sizeValue: 5,
        colorValue: 1,
    }
}

/**
 * Adjust canvas height to default size
 */
function adjustCanvasHeight() {
    const width = canvasContainer.value?.offsetWidth || 800; // Default width
    canvasHeight.value = (width / 16) * 9; // 16:9 Screen size
}

/**
 * Includes node to the mesh and updates the canvas to draw them
 * @param point node to be added
 */
function addNode(point: Point) {

    try {
        if (!nv) {
            throw new Error("No visualization to alter");
        }

        /*if (nv.meshes.length === 0) {
            console.warn('No meshes found. Creating new Mesh...');

            const newConnectome = new NVMesh(
                new Float32Array(point.mm),
                new Uint32Array([]),
                'connectomeMesh',
                new Uint8Array([255, 0, 0, 255]),
                1.0,
                true,
                nv.gl
            )

            nv.addMesh(newConnectome);
            //nv.updateGLVolume();
            nv.drawScene();
        }

        const pts = convertPointToNode(point)

        const connectome = nv.meshes[0];
        if (!connectome.nodes) {
            connectome.nodes = [];
            connectome.nodes.push(pts);
        } else {
            connectome.nodes?.push(pts);
        }

        //nv.handleNodeAdded(pts);
        nv.meshes[0].updateMesh(nv.gl);*/
        toast({
            title: "Success",
            description: "Node added succesfully"
        });
        pointsStore.addPoint(point);
    } catch (error) {
        console.error(error);
        toast({
            title: "Error",
            description: `${error}`,
            variant: 'destructive'
        });
    }
}

// Initialize Niivue
onMounted(async () => {
    nv = new Niivue();
    let coordChange = false;
    let payload: Point = {
        mm: [0, 0, 0],
        idx: [0, 0, 0],
        string: ''
    };

    if (canvasContainer.value) {
        nv.attachToCanvas(canvasContainer.value);
    }

    try {
        const response = await axios.get(props.volumeUrl);
        const volumeUrl = response.data.url;
        await nv.loadVolumes([{ url: volumeUrl }]);
    } catch (error) {
        toast({
            title: 'Error',
            description: `Error loading volume: ${error}`,
            variant: 'destructive'
        });
    }

    nv.onLocationChange = (data: any) => {
        if (!data.mm || !data.vox) return;

        coordChange = true;
        payload = {
            mm: data.mm,
            idx: data.vox,
            string: data.string,
        };
    };

    nv.onMouseUp = () => {
        if (coordChange) {
            coordChange = false;
            addNode(payload);
        }
    };

    adjustCanvasHeight(); // Adjust size on reload
});

window.addEventListener('resize', adjustCanvasHeight);

</script>
