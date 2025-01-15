<template>
    <section>
        <!-- Table Wrapper -->
        <div class="rounded-md border bg-white shadow">
            <Table>
                <!-- Table Header -->
                <TableHeader>
                    <TableRow>
                        <TableHead>X</TableHead>
                        <TableHead>Y</TableHead>
                        <TableHead>Z</TableHead>
                        <TableHead>Index</TableHead>
                        <TableHead>Actions</TableHead>
                    </TableRow>
                </TableHeader>

                <!-- Table Body -->
                <TableBody>
                    <TableRow v-for="(node, index) in pointsStore.points" :key="index">
                        <TableCell>{{ node.mm[0].toFixed(2) }}</TableCell>
                        <TableCell>{{ node.mm[1].toFixed(2) }}</TableCell>
                        <TableCell>{{ node.mm[2].toFixed(2) }}</TableCell>
                        <TableCell>{{ node.idx || (node.mm[0] * node.mm[1] * node.mm[2]).toFixed(2) }}</TableCell>
                        <TableCell>
                            <Button variant="destructive" size="sm" @click="deletePoint(index)">
                                <Trash color="white"/>
                            </Button>
                        </TableCell>
                    </TableRow>
                </TableBody>
            </Table>
        </div>
    </section>
</template>

<script lang="ts" setup>
import { usePointsStore } from '@/stores/PointsStore'
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { Trash } from 'lucide-vue-next';

const pointsStore = usePointsStore()

// Função para deletar pontos
function deletePoint(index: number) {
    pointsStore.points.splice(index, 1)
}
</script>
