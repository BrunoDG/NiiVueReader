import { defineStore } from "pinia";

export const usePointsStore = defineStore("pointsStore", {
  state: () => ({
    points: [],
  }),
  actions: {
    addPoint(point) {
      this.points.push(point);
    },
    removePoint(index) {
      this.points.splice(index, 1);
    },
  },
});
