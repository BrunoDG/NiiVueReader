<template>
    <div v-if="isVisible" class="fixed inset-0 flex justify-center items-center bg-gray-500 bg-opacity-50 z-50">
        <div class="bg-white w-[90%] max-w-lg p-4 rounded shadow-lg relative">
            <h2 class="text-lg font-bold mb-4">Upload or Select a File</h2>

            <!-- File Picker -->
            <FilePicker @file-uploaded="handleFileUpload" />

            <!-- File Selection Section -->
            <div class="mt-6">
                <h3 class="font-semibold mb-2">Select an Existing File</h3>
                <ul>
                    <li v-for="file in files" :key="file" class="mb-2">
                        <Button @click="selectFile(file)">
                            {{ file }}
                        </Button>
                    </li>
                </ul>
            </div>

            <!-- Close Button -->
            <button class="absolute top-2 right-2 text-gray-500 hover:text-gray-800" @click="close">
                <CircleX :size="24" color="red" />
            </button>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import FilePicker from '@/components/FilePicker.vue';
import axios from 'axios';
import { Button } from '@/components/ui/button';
import { CircleX } from 'lucide-vue-next';

const emit = defineEmits(['close', 'file-selected']);
const files = ref([]);

const props = defineProps({
    isVisible: Boolean,
});

// Busca os arquivos disponíveis no backend
async function fetchFiles() {
    try {
        const response = await axios.get('http://localhost:8000/api/files');
        files.value = response.data.files;
    } catch (error) {
        console.error('Error fetching files:', error);
    }
}

// Processa o arquivo enviado pelo FilePicker
function handleFileUpload(file) {
    const formData = new FormData();
    formData.append('file', file);

    axios
        .post('http://localhost:8000/api/upload', formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
        })
        .then(() => {
            alert('File uploaded successfully!');
            emit('file-selected', `http://localhost:8000/api/volume?filename=${file.name}`);
            fetchFiles(); // Atualiza a lista de arquivos
        })
        .catch((error) => {
            alert('Failed to upload file.');
            console.error('Upload error:', error);
        });
}

// Seleciona um arquivo existente
function selectFile(file) {
    const fileUrl = `http://localhost:8000/api/volume/?filename=${file}`;
    emit('file-selected', fileUrl);
}

// Fecha o modal
function close() {
    emit('close');
}

onMounted(() => {
    fetchFiles();
});
</script>
