import { StateCreator, create } from "zustand";

import { Experiment } from "../types/types";

interface ExperimentSlice {
  experiments: Experiment[];
  experiment?: Experiment;
  setExperiments: (experiments: Experiment[]) => void;
  setExperiment: (experiment: Experiment) => void;
  patchExperiment: (experiment: Partial<Experiment>) => void;
}

const createExperimentSlice: StateCreator<ExperimentSlice> = (set) => ({
  experiments: [],
  experiment: undefined,
  setExperiments: (experiments) => set(() => ({ experiments })),
  setExperiment: (experiment) => set(() => ({ experiment })),
  patchExperiment: (experiment) => set((state) => {
    return { experiment: { ...state.experiment, ...experiment } };
  })
});

export interface Toast {
  message: string;
  duration: number;
  level: "info" | "warning" | "error";
}

interface ToastsSlice {
  toasts: Toast[];
  addToast: (toast: Toast) => void;
}

const createToastsSlice: StateCreator<ToastsSlice> = (set) => ({
  toasts: [],
  addToast: (toast) => {
    // Add toast to the list of toasts, then, based on the toast's duration, remove it after a certain amount of time
    set((state) => ({ toasts: [...state.toasts, toast] }));
    setTimeout(() => {
      set((state) => ({ toasts: state.toasts.filter((t) => t !== toast) }));
    }, toast.duration);
  },
});

export const useBoundStore = create<
  ExperimentSlice & ToastsSlice
>((...args) => ({
  ...createExperimentSlice(...args),
  ...createToastsSlice(...args),
}));

export default useBoundStore;
