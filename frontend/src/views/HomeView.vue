<template>
    <div class="flex flex-col h-screen bg-black">
        <!-- MenuBar -->
        <MenuBar class="bg-gray-800 text-white shadow-md" @upload-file="openFilePickerModal" />

        <!-- Viewer Section -->
        <div class="flex-1 bg-black content-center">
            <NiivueViewer :volume-url="currentFileUrl" />
        </div>

        <!-- Bottom Section -->
        <div class="flex flex-col lg:flex-row h-[40%] p-2 gap-2 bg-black">
            <!-- Time series chart -->
            <div class="flex-1">
                <TimeSeriesChart :points="pointsStore.points" />
            </div>
            <!-- Node points table -->
            <div class="flex-1">
                <NodesTable />
            </div>
        </div>

        <!-- File Picker Modal -->
        <FilePickerView :isVisible="showModal" @close="closeFilePickerModal" @file-selected="loadFile" />
    </div>
</template>

<script setup>
import MenuBar from '@/components/MenuBar.vue';
import NiivueViewer from '@/components/NiivueViewer.vue';
import TimeSeriesChart from '@/components/TimeSeriesChart.vue';
import NodesTable from '@/components/NodesTable.vue';
import FilePickerView from '@/views/FilePickerView.vue';
import { usePointsStore } from '@/stores/PointsStore';
import { ref } from 'vue';

const pointsStore = usePointsStore();
const currentFileUrl = ref('http://localhost:8000/api/volume');

const showModal = ref(false);

function openFilePickerModal() {
    showModal.value = true;
};

function closeFilePickerModal() {
    showModal.value = false;
}

function loadFile(fileUrl) {
    currentFileUrl.value = fileUrl;
    closeFilePickerModal();
}

</script>
