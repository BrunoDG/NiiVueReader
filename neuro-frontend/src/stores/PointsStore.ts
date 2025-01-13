import { defineStore } from "pinia";

export interface Point {
  mm: [number, number, number];
  idx: [number, number, number];
}

export const usePointsStore = defineStore("points", {
  state: () => ({
    points: [] as Point[],
  }),
  actions: {
    addPoint(point: Point) {
      this.points.push(point);
    },
    removePoint(index: number) {
      this.points.splice(index, 1);
    },
  },
});
