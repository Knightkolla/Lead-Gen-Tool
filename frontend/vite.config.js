import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  optimizeDeps: {
    include: ['use-sync-external-store/with-selector'],
  },
  resolve: {
    alias: {
      'use-sync-external-store/with-selector': 'use-sync-external-store/with-selector',
    },
  },
});