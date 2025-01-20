<template>
    <form @submit.prevent="submitFile">
        <div class="flex flex-col gap-4">
            <!-- Input para selecionar o arquivo -->
            <div>
                <Label for="fileInput">Choose a .nii or .nii.gz file</Label>
                <Input id="fileInput" type="file" accept=".nii,.nii.gz" @change="handleFileChange" required />
            </div>

            <!-- Botão de envio -->
            <Button type="submit" variant="default" :disabled="!selectedFile">
                Upload File
            </Button>
        </div>
    </form>
</template>

<script setup>
import { ref } from 'vue';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Button } from '@/components/ui/button';

const emit = defineEmits(['file-uploaded']);
const selectedFile = ref(null);

// Atualiza o arquivo selecionado
function handleFileChange(event) {
    const file = event.target.files[0];
    if (file) {
        selectedFile.value = file;
    }
}

// Emite o arquivo selecionado para o componente pai
function submitFile() {
    if (selectedFile.value) {
        emit('file-uploaded', selectedFile.value);
        selectedFile.value = null; // Limpa a seleção após o envio
    }
}
</script>
