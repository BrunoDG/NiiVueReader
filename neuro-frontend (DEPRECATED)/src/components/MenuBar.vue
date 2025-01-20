<template>
  <Menubar>
    <MenubarMenu>
      <MenubarTrigger>File</MenubarTrigger>
      <MenubarContent>
        <MenubarItem @click="uploadFile">Upload</MenubarItem>
        <MenubarItem>Settings</MenubarItem>
        <MenubarSeparator />
        <MenubarItem>Logout</MenubarItem>
      </MenubarContent>
    </MenubarMenu>
    <MenubarMenu>
      <MenubarTrigger>View</MenubarTrigger>
      <MenubarContent>
        <MenubarItem @click="setView('Axial')">Axial</MenubarItem>
        <MenubarItem @click="setView('Sagittal')">Sagittal</MenubarItem>
        <MenubarItem @click="setView('Coronal')">Coronal</MenubarItem>
        <MenubarItem @click="setView('3D')">3D</MenubarItem>
        <MenubarItem @click="setView('Mista')">Mixed</MenubarItem>
      </MenubarContent>
    </MenubarMenu>
  </Menubar>
</template>

<script lang="ts" setup>
import { Menubar, MenubarMenu, MenubarTrigger, MenubarContent, MenubarItem, MenubarSeparator } from '@/components/ui/menubar'

// Função para upload (placeholder)
function uploadFile() {
    console.log('Upload clicked')
}

// Função para alternar visualização (placeholder)
function setView(view: string) {
    console.log(`Switching to ${view} view`)
}
</script>
