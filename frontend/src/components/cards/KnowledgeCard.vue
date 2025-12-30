<template>
  <div 
    class="card p-6 cursor-pointer hover:shadow-lg transition-all duration-200 hover:-translate-y-1"
    @click="$emit('click')"
  >
    <!-- 卡片头部 -->
    <div class="flex justify-between items-start mb-3">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white line-clamp-2">
        {{ card.title }}
      </h3>
      <button 
        @click.stop="$emit('delete', card.id)"
        class="opacity-0 group-hover:opacity-100 p-1 text-gray-400 hover:text-red-500 transition-opacity"
      >
        <Trash2 class="w-4 h-4" />
      </button>
    </div>

    <!-- 卡片内容 -->
    <p class="text-gray-600 dark:text-gray-400 text-sm mb-4 line-clamp-3">
      {{ card.content }}
    </p>

    <!-- 标签 -->
    <div class="flex flex-wrap gap-1 mb-3">
      <span
        v-for="tag in card.tags.slice(0, 3)"
        :key="tag"
        class="px-2 py-1 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 text-xs rounded-full"
      >
        {{ tag }}
      </span>
      <span
        v-if="card.tags.length > 3"
        class="px-2 py-1 bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400 text-xs rounded-full"
      >
        +{{ card.tags.length - 3 }}
      </span>
    </div>

    <!-- 卡片底部 -->
    <div class="flex justify-between items-center text-xs text-gray-500 dark:text-gray-400">
      <span>{{ formatRelativeTime(card.updated_at) }}</span>
      <span v-if="card.notebook_id" class="flex items-center">
        <FolderOpen class="w-3 h-3 mr-1" />
        笔记本
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'
import { formatRelativeTime } from '@/utils/utils'
import { 
  FolderOpen, 
  Trash2 
} from 'lucide-vue-next'

interface Props {
  card: {
    id: string
    title: string
    content: string
    tags: string[]
    notebook_id?: string
    updated_at: string
  }
}

defineProps<Props>()
defineEmits<{
  click: []
  delete: [id: string]
}>()
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>