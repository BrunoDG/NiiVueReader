import { Niivue, NVMesh, type NVConnectomeNode } from "@niivue/niivue";

declare module "@niivue/niivue" {
  export class NVConnectome extends NVMesh {
    addConnectomeNode(node: NVConnectomeNode): void;
    deleteConnectomeNode(node: NVConnectomeNode): void;
    updateMesh(gl: WebGL2RenderingContext): void;
    updateLabels(): void;
    updateConnectomeNodeByPoint(
      point: [number, number, number],
      updatedNode: NVConnectomeNode
    ): void;
    updateConnectomeNodeByIndex(
      index: number,
      updatedNode: NVConnectomeNode
    ): void;
    findClosestConnectomeNode(
      point: number[],
      distance: number
    ): NVConnectomeNode | null;
    updateConnectome(gl: WebGL2RenderingContext): void;
  }
}
