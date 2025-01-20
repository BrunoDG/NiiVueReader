<template>
    <div class="relative w-full h-[80%] content-center">
        <!-- Canvas -->
        <canvas id="canvasContainer" ref="canvasContainer" class="w-full h-full"></canvas>

        <!-- Floating Dropdown Menu Button -->
        <div class="absolute -top-10 right-4 z-10 text-white text-xl">
            {{ selectedView }} View
        </div>

        <!-- Opacity Slider -->
        <div class="absolute -bottom-12 right-2 z-10 bg-white p-4 rounded shadow-md">
            <div class="flex items-center gap-4">
                <label for="opacity-slider" class="text-sm font-medium">Opacity</label>
                <Slider
                    class="w-[100px]"
                    v-model="opacity"
                    :default-value="[100]"
                    :min="0"
                    :max="100"
                    :step="1"
                    :onValueChange="setOpacity(opacity)"
                />
                <span class="text-sm font-medium">{{ opacity[0] }}%</span>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue';
import * as niivue from '@niivue/niivue';
import {cmapper} from '@niivue/niivue';
import axios from 'axios';
// UI Components
import { Slider } from '@/components/ui/slider';
// Stores
import { usePointsStore } from '@/stores/PointsStore';
import { useVisualizationStore } from '@/stores/VisualizationStore';

// Props
const props = defineProps({
    volumeUrl: String,
});

const pointsStore = usePointsStore();
const visualizationStore = useVisualizationStore();

// Refs and variables
const canvasContainer = ref(null);
const canvasHeight = ref(600); // Initial canvas height
const selectedView = ref('Mixed');
let nv = null;
const opacity = ref([100]);

/**
 * Define a opacidade do modelo 3D.
 * @param {number} value Valor da opacidade (0 a 100).
 */
function setOpacity(value) {
  if (nv && nv.volumes.length > 0) {
    console.log('Opacity value changed to ', value);
    nv.volumes[0].opacity = value / 100; // Converte para intervalo de 0 a 1
    nv.updateGLVolume();
  }
}

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

/**
 * Updates all mesh nodes labels
 */
function updateLabels() {
    const nodes = nv.meshes[0].nodes;
    if (!nodes || nodes.length === 0) return;

    // Encontra o maior node
    const largest = nodes.reduce((a, b) => (a.sizeValue > b.sizeValue ? a : b)).sizeValue;

    let min = nodes[0].colorValue;
    let max = nodes[0].colorValue;

    // Define min e max para os valores de cor
    for (let i = 1; i < nodes.length; i++) {
        if (nodes[i].colorValue < min) min = nodes[i].colorValue;
        if (nodes[i].colorValue > max) max = nodes[i].colorValue;
    }

    const lut = cmapper.colormap('viridis', false); // Exemplo de colormap
    const lutNeg = cmapper.colormap('magma', false); // Colormap negativo, se necessário

    for (let i = 0; i < nodes.length; i++) {
        let color = nodes[i].colorValue;
        let isNeg = color < 0;
        if (isNeg) color = -color;

        color = Math.round(((color - min) / (max - min)) * 255) * 4;
        let rgba = [lut[color], lut[color + 1], lut[color + 2], 255];

        if (isNeg) {
            rgba = [lutNeg[color], lutNeg[color + 1], lutNeg[color + 2], 255];
        }

        nodes[i].label = {
            name: nodes[i].name,
            color: rgba,
            scale: nodes[i].sizeValue / largest,
        };
    }

    console.log('Labels updated successfully.');
}

/**
 * Adds node to mesh and updates canvas
 * @param {Object} node - Node to be added
 */
function addConnectomeNode(node) {
    let nodes = nv.meshes[0].nodes;
    if (!nodes)
    {
        nv.meshes[0].nodes = [];
        nv.meshes[0].nodes.push(node);
    } else {
        nv.meshes[0].nodes.push(node);
    }

    updateLabels();
    nv.meshes[0].updateMesh(nv.gl);
    nv.updateGLVolume();

    console.log('Node added:', node);
}


/**
 * Removes node from mesh based on proximity
 * @param {Object} point - Node to be removed.
 */
function deleteConnectomeNode(point) {
    const nodes = nv.meshes[0].nodes || [];
    if (nodes.length === 0) return;

    let minDx = Infinity;
    let minIdx = -1;

    for (let i = 0; i < nodes.length; i++) {
        const dx = Math.sqrt(
            Math.pow(point.mm[0] - nodes[i].x, 2) +
            Math.pow(point.mm[1] - nodes[i].y, 2) +
            Math.pow(point.mm[2] - nodes[i].z, 2)
        );

        if (dx < minDx) {
            minDx = dx;
            minIdx = i;
        }
    }

    if (minDx > 15) { // 15mm tolerance
        console.log('No nodes within tolerance.');
        return;
    }

    nodes.splice(minIdx, 1); // Remove o node
    updateLabels();
    nv.meshes[0].updateMesh(nv.gl);
    nv.updateGLVolume();

    console.log('Node deleted:', point);
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
                deleteConnectomeNode(payload);
            } else {
                // Adding new node, since it doesn't exist on the stored list
                addConnectomeNode({
                    name: 'node',
                    x: payload.mm[0],
                    y: payload.mm[1],
                    z: payload.mm[2],
                    colorValue: payload.idx[0],
                    sizeValue: 1
                });
                pointsStore.addPoint(payload);
            }
        }
    };

    adjustCanvasHeight(); // Adjust size on reload
});

window.addEventListener('resize', adjustCanvasHeight);

watch(
    () => visualizationStore.selectedView,
    (newView) => {
        setView(newView);
    }
);
</script>
