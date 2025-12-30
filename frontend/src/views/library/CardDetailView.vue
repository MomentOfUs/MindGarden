<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- 顶部导航栏 -->
    <div class="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <router-link to="/cards" class="flex items-center">
              <ArrowLeft class="w-6 h-6 text-gray-600 dark:text-gray-300 mr-2" />
              <h1 class="text-xl font-bold text-gray-900 dark:text-white">{{ card?.title || '卡片详情' }}</h1>
            </router-link>
          </div>
          
          <div class="flex items-center space-x-2">
            <button 
              @click="router.push(`/cards/${card?.id}/edit`)"
              class="btn btn-secondary"
            >
              <Edit class="w-4 h-4 mr-2" />
              编辑
            </button>
            <button 
              @click="handleDeleteCard"
              class="btn btn-outline text-red-600 border-red-300 hover:bg-red-50 dark:text-red-400 dark:border-red-600 dark:hover:bg-red-900/20"
            >
              <Trash2 class="w-4 h-4 mr-2" />
              删除
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 主内容区 -->
    <div class="max-w-4xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
      <div v-if="isLoading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        <p class="mt-2 text-gray-600 dark:text-gray-400">加载中...</p>
      </div>

      <div v-else-if="card" class="space-y-6">
        <!-- 卡片头部 -->
        <div class="card p-6">
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">{{ card.title }}</h2>
          
          <div class="flex flex-wrap gap-2 mb-4">
            <span
              v-for="tag in card.tags"
              :key="tag"
              class="px-3 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 text-sm rounded-full"
            >
              {{ tag }}
            </span>
          </div>

          <div class="flex items-center text-sm text-gray-600 dark:text-gray-400 space-x-4">
            <span>创建于 {{ formatDate(card.created_at) }}</span>
            <span>更新于 {{ formatDate(card.updated_at) }}</span>
            <span v-if="card.notebook_id">笔记本: {{ getNotebookName(card.notebook_id) }}</span>
          </div>
        </div>

        <!-- 卡片内容 -->
        <div class="card p-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">内容</h3>
          <div class="prose dark:prose-invert max-w-none">
            <pre class="whitespace-pre-wrap text-gray-700 dark:text-gray-300">{{ card.content }}</pre>
          </div>
        </div>
      </div>

      <div v-else class="text-center py-12">
        <p class="text-gray-600 dark:text-gray-400">卡片不存在或已被删除</p>
        <router-link to="/cards" class="btn btn-primary mt-4">
          返回卡片列表
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { cardsApi, type KnowledgeCard, type Notebook } from '@/services/cards'
import { formatDate } from '@/utils/utils'
import { 
  ArrowLeft, 
  Edit, 
  Trash2 
} from 'lucide-vue-next'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const card = ref<KnowledgeCard | null>(null)
const notebooks = ref<Notebook[]>([])
const isLoading = ref(false)

const loadCard = async () => {
  try {
    isLoading.value = true
    const cardId = route.params.id as string
    card.value = await cardsApi.getCard(cardId)
  } catch (error) {
    console.error('Failed to load card:', error)
  } finally {
    isLoading.value = false
  }
}

const loadNotebooks = async () => {
  try {
    notebooks.value = await cardsApi.getNotebooks()
  } catch (error) {
    console.error('Failed to load notebooks:', error)
  }
}

const getNotebookName = (notebookId: string) => {
  const notebook = notebooks.value.find(n => n.id === notebookId)
  return notebook?.name || '未知笔记本'
}

const handleDeleteCard = async () => {
  if (!card.value) return
  
  if (confirm('确定要删除这个卡片吗？')) {
    try {
      await cardsApi.deleteCard(card.value.id)
      router.push('/cards')
    } catch (error) {
      console.error('Failed to delete card:', error)
      alert('删除失败，请重试')
    }
  }
}

onMounted(() => {
  loadCard()
  loadNotebooks()
})
</script>