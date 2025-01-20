<template>
    <div v-if="isVisible" class="fixed inset-0 flex justify-center items-center bg-gray-500 bg-opacity-50 z-50">
        <h2 class="text-lg font-bold mb-4">Upload or Select a File</h2>

        <!-- Upload Section -->
        <div class="mb-8">
            <FilePicker @file-selected="handleFileUpload" />
        </div>

        <!-- File Selection Section -->
        <div>
            <ul>
                <li v-for="file in files" :key="file" class="mb-2">
                    <button class="text-blue-500 hover:underline" @click="selectFile(file)">
                        {{ file }}
                    </button>
                </li>
            </ul>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import FilePicker from '@/components/FilePicker.vue';
import axios from 'axios';

const files = ref([]);

const props = defineProps({
    isVisible: Boolean, // Exibição do modal
});

async function fetchFiles() {
    try {
        const response = await axios.get('http://localhost:8000/api/files');
        files.value = response.data.files;
    } catch (error) {
        console.error('Error fetching files:', error);
    }
}

function handleFileUpload(file) {
    const formData = new FormData();
    formData.append('file', file);

    axios
        .post('http://localhost:8000/api/upload', formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
        })
        .then(() => {
            alert('File uploaded successfully!');
            fetchFiles();
        })
        .catch((error) => {
            alert('Failed to upload file.');
            console.error('Upload error:', error);
        });
}

function selectFile(file) {
    alert(`File selected: ${file}`);
}

onMounted(() => {
    fetchFiles();
});
</script>
