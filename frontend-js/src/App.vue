<template>
    <div class="flex flex-col h-screen bg-black">
        <!-- MenuBar -->
        <MenuBar class="bg-gray-800 text-white shadow-md" />

        <!-- Viewer Section -->
        <div class="flex-1 bg-black content-center">
            <NiivueViewer :volume-url="volumeUrl" />
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
    </div>
</template>

<script setup>
import MenuBar from '@/components/MenuBar.vue';
import NiivueViewer from '@/components/NiivueViewer.vue';
import TimeSeriesChart from '@/components/TimeSeriesChart.vue';
import NodesTable from '@/components/NodesTable.vue';
import { usePointsStore } from '@/stores/PointsStore';

const pointsStore = usePointsStore();
const volumeUrl = 'http://localhost:8000/api/volume';

</script>
