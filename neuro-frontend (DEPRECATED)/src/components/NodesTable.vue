<template>
  <Card class="max-w-full lg:max-w-600px h-[360px]">
    <CardHeader>
      <CardTitle class="items-center">Selected Points</CardTitle>
      <CardDescription>
        Manage selected points from the viewer.
      </CardDescription>
    </CardHeader>
    <CardContent>
      <!-- Table Wrapper -->
      <div class="overflow-auto max-h-[240px] h-full">
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
              <TableCell>{{ node.string || '0' }}</TableCell>
              <TableCell>
                <Button variant="destructive" size="sm" @click="deletePoint(index)">
                  <Trash color="white" />
                </Button>
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </div>
    </CardContent>
  </Card>
</template>

<script setup>
import { usePointsStore } from '@/stores/PointsStore';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '@/components/ui/table';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Trash } from 'lucide-vue-next';

const pointsStore = usePointsStore();

function deletePoint(index) {
  pointsStore.points.splice(index, 1);
}
</script>
