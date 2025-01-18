<template>
    <div class="relative w-full h-[80%] content-center">
        <!-- Canvas -->
        <canvas id="canvasContainer" ref="canvasContainer" class="w-full h-full"></canvas>

        <!-- Floating Dropdown Menu Button -->
        <div class="absolute -top-10 right-2 z-10">
        <DropdownMenu>
            <DropdownMenuTrigger asChild>
            <Button variant="outline" size="sm">
                {{ selectedView }} View
            </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent class="relative right-2">
            <DropdownMenuItem @click="setView('Axial')">Axial</DropdownMenuItem>
            <DropdownMenuItem @click="setView('Sagittal')">Sagittal</DropdownMenuItem>
            <DropdownMenuItem @click="setView('Coronal')">Coronal</DropdownMenuItem>
            <DropdownMenuItem @click="setView('3D')">3D</DropdownMenuItem>
            <DropdownMenuItem @click="setView('Mixed')">Mixed</DropdownMenuItem>
            </DropdownMenuContent>
        </DropdownMenu>
        </div>
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import * as niivue from '@niivue/niivue';
import axios from 'axios';
// UI Components
import { DropdownMenu, DropdownMenuItem, DropdownMenuTrigger, DropdownMenuContent } from '@/components/ui/dropdown-menu';
import { Button } from '@/components/ui/button';
// Points store
import { usePointsStore } from '@/stores/PointsStore';

// Props
const props = defineProps({
    volumeUrl: String,
});

const pointsStore = usePointsStore();

// Refs and variables
const canvasContainer = ref(null);
const canvasHeight = ref(600); // Initial canvas height
const selectedView = ref('Mixed');
let nv = null;

/**
 * Set NIfTI file rendering view on canvas
 * @param {string} view - View mode rendered on canvas
 */
function setView(view) {
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

    nv.updateGLVolume();
}

/**
 * Adjust canvas height to default size
 */
function adjustCanvasHeight() {
    const width = canvasContainer.value?.offsetWidth || 800; // Default width
    canvasHeight.value = (width / 16) * 9; // 16:9 aspect ratio
}

function addConnectomeNode(node) {
    log.debug('adding node', node)
    if (!this.nodes) {
      throw new Error('nodes not defined')
    }

    ;(this.nodes).push(node)
    this.updateLabels()
    this.nodesChanged.dispatchEvent(new CustomEvent('nodeAdded', { detail: { node } }))
  }

function deleteConnectomeNode(node){
    // delete any connected edges
    const index = (this.nodes).indexOf(node)
    const edges = this.edges
    if (edges) {
      this.edges = edges.filter((e) => e.first !== index && e.second !== index)
    }
    this.nodes = (this.nodes).filter((n) => n !== node)

    this.updateLabels()
    this.updateConnectome(this.gl)
    this.nodesChanged.dispatchEvent(new CustomEvent('nodeDeleted', { detail: { node } }))
  }

/**
 * Add node to the mesh and update the canvas
 * @param {{ mm: number[], idx: number[], string: string }} point - Node to add
 */
function addNode(point) {
    try {
        let nodes = nv.meshes[0].nodes;
        /*nv.meshes[0].addConnectomeNode({
            name: 'node',
            x: point.mm[0],
            y: point.mm[1],
            z: point.mm[2],
            colorValue: 1,
            sizeValue: 1
        });*/

        if (!nodes) {
            throw new Error('nodes not defined')
        }

        ;(nodes).push({
            name: 'node',
            x: point.mm[0],
            y: point.mm[1],
            z: point.mm[2],
            colorValue: 1,
            sizeValue: 1
        });
        nv.meshes[0].updateLabels();

        nv.meshes[0].updateMesh(nv.gl);
        nv.updateGLVolume();

        console.log('Node added successfully');

        pointsStore.addPoint(point);
        nv.drawScene();
    } catch (error) {
        console.error('Error adding node: ', error.message);
    }
}

/**
 * Remove node from the mesh and update the canvas
 * @param {{ mm: number[], idx: number[]. string: string }} point - Node to remove
 */
function deleteNode(point) {
    try {
        let nodes = nv.meshes[0].nodes;
        if (nodes.length < 1) return;
        let pts = convertPointToNode(point);
        let minDx = Number.POSITIVE_INFINITY;
        let minIdx = 0;
        for (let i = 0; i < nodes.length; i++) {
            let dx = Math.sqrt(
                Math.pow(XYZmm[0] - nodes[i].x, 2) +
                Math.pow(XYZmm[1] - nodes[i].y, 2) +
                Math.pow(XYZmm[2] - nodes[i].z, 2)
            );
            if (dx < minDx) {
                minDx = dx;
                minIdx = i;
            }
        }
        console.log("Node " + minIdx + " is " + minDx + "mm from the click");
        const tolerance = 15.0; //e.g. only 15mm from clicked location
        if (minDx > tolerance) return;
        
        nv.meshes[0].deleteConnectionNode(nv.meshes[0].nodes(minIdx));
        nv.meshes[0].updateMesh(nv.gl);
        nv.updateGLVolume();
    } catch (error) {
        console.log('Error deleting node: ', error.message);
    }
}

/**
 * Verifies if there's a point at the list
 * @param {number[]} mm Points coordinates in mm [x, y, z]
 * @returns {number} Returns found point index or -1 if it doesn't exist
 */
function findPointIndex(mm) {
    return pointsStore.points.findIndex(
        (point) =>
        point.mm[0] === mm[0] &&
        point.mm[1] === mm[1] &&
        point.mm[2] === mm[2]
    );
}

// Initialize Niivue
onMounted(async () => {
    let coordChange = false;
    let payload = {
        mm: [0, 0, 0],
        idx: [0, 0, 0],
        string: '',
    };

    nv = new niivue.Niivue();
    nv.attachTo("canvasContainer");

    const nodeMesh = new niivue.NVMesh(
        new Float32Array(payload.mm),
        new Uint32Array([]),
        'nodeMesh',
        new Uint8Array([255, 0, 0, 255]),
        1.0,
        true,
        nv.gl
    );
    nv.addMesh(nodeMesh);

    try {
        const response = await axios.get(props.volumeUrl);
        const volumeUrl = response.data.url;
        await nv.loadVolumes([{ url: volumeUrl }]);
    } catch (error) {
        console.log('Error handling volume: ', error);
    }
    
    nv.onLocationChange = (data) => {
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

            // verifying if node already exists
            const existingPointIndex = findPointIndex(payload.mm);

            if (existingPointIndex !== -1) {
                // Deleting existing node
                deleteNode(existingPointIndex);
            } else {
                // Adding new node, since it doesn't exist on the stored list
                addNode(payload);
            }
        }
    };

    adjustCanvasHeight(); // Adjust size on reload
});

window.addEventListener('resize', adjustCanvasHeight);
</script>
