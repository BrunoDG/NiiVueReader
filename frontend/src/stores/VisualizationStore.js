import { defineStore } from "pinia";

export const useVisualizationStore = defineStore("visualizationStore", {
  state: () => ({
    selectedView: "Mixed",
  }),
  actions: {
    setView(view) {
      this.selectedView = view;
    },
  },
});
