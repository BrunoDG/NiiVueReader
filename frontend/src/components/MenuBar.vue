<template>
  <Menubar>
    <MenubarMenu>
      <MenubarTrigger>File</MenubarTrigger>
      <MenubarContent>
        <MenubarItem @click="uploadFile">Upload</MenubarItem>
      </MenubarContent>
    </MenubarMenu>
    <MenubarMenu>
      <MenubarTrigger>View</MenubarTrigger>
      <MenubarContent>
        <MenubarItem @click="setView('Axial')">Axial</MenubarItem>
        <MenubarItem @click="setView('Sagittal')">Sagittal</MenubarItem>
        <MenubarItem @click="setView('Coronal')">Coronal</MenubarItem>
        <MenubarItem @click="setView('3D')">3D</MenubarItem>
        <MenubarItem @click="setView('Mixed')">Mixed</MenubarItem>
      </MenubarContent>
    </MenubarMenu>
  </Menubar>
</template>

<script setup>
import { Menubar, MenubarMenu, MenubarTrigger, MenubarContent, MenubarItem } from '@/components/ui/menubar';
import { useVisualizationStore } from '@/stores/VisualizationStore';

const visualizationStore = useVisualizationStore();
const emit = defineEmits(['upload-file']);

// Função para upload (placeholder)
function uploadFile() {
    console.log('Upload clicked');
    emit('upload-file');
}

// Função para alternar visualização (placeholder)
function setView(view) {
    visualizationStore.setView(view);
    console.log(`Switching to ${view} view`);
}
</script>
