<template>
    <div>
        <!--<Button variant="outline" @click="triggerFilePicker">Choose File</Button>-->
        <Label for="filePick">Choose .nii file</Label>
        <Input id="filePick" type="file" />
    </div>
</template>

<script setup>
import { ref } from 'vue';
//import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';

//const fileInput = ref(null);

//function triggerFilePicker() {
//    fileInput.value.click();
//}

function onFileChange(event) {
    const file = event.target.files[0];
    if (file) {
        emit('file-selected', file);
    }
}
</script>
