<template>
  <div id="app" :class="{ 'dark': isDarkMode }">
    <router-view />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useThemeStore } from '@/stores/theme'

const themeStore = useThemeStore()
const isDarkMode = computed(() => themeStore.isDarkMode)
</script>

<style scoped>
#app {
  font-family: Inter, system-ui, Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>