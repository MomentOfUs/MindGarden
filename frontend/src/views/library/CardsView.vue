<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- 顶部导航栏 -->
    <div class="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <router-link to="/dashboard" class="flex items-center">
              <BookOpen class="w-6 h-6 text-gray-600 dark:text-gray-300 mr-2" />
              <h1 class="text-xl font-bold text-gray-900 dark:text-white">知识卡片</h1>
            </router-link>
          </div>
          
          <div class="flex items-center space-x-4">
            <div class="relative">
              <input
                v-model="searchQuery"
                type="text"
                placeholder="搜索卡片..."
                class="input pl-10 pr-4 w-64"
              />
              <Search class="w-5 h-5 text-gray-400 absolute left-3 top-2.5" />
            </div>
            
            <button 
              @click="router.push('/cards/new')"
              class="btn btn-primary"
            >
              <Plus class="w-4 h-4 mr-2" />
              新建卡片
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 主内容区 -->
    <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
      <!-- 筛选标签 -->
      <div class="mb-6">
        <div class="flex flex-wrap gap-2">
          <button
            @click="selectedTag = ''"
            :class="[
              'px-3 py-1 text-sm rounded-full border transition-colors',
              selectedTag === '' 
                ? 'bg-primary-100 border-primary-300 text-primary-700 dark:bg-primary-900 dark:border-primary-700 dark:text-primary-300'
                : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50 dark:bg-gray-800 dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-700'
            ]"
          >
            全部
          </button>
          <button
            v-for="tag in allTags"
            :key="tag"
            @click="selectedTag = tag"
            :class="[
              'px-3 py-1 text-sm rounded-full border transition-colors',
              selectedTag === tag 
                ? 'bg-primary-100 border-primary-300 text-primary-700 dark:bg-primary-900 dark:border-primary-700 dark:text-primary-300'
                : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50 dark:bg-gray-800 dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-700'
            ]"
          >
            {{ tag }}
          </button>
        </div>
      </div>

      <!-- 卡片网格 -->
      <div v-if="isLoading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        <p class="mt-2 text-gray-600 dark:text-gray-400">加载中...</p>
      </div>

      <div v-else-if="filteredCards.length === 0" class="text-center py-12">
        <BookOpen class="w-16 h-16 text-gray-400 mx-auto mb-4" />
        <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">
          {{ searchQuery || selectedTag ? '没有找到匹配的卡片' : '还没有任何卡片' }}
        </h3>
        <p class="text-gray-600 dark:text-gray-400 mb-4">
          {{ searchQuery || selectedTag ? '试试调整搜索条件' : '开始创建您的第一个知识卡片吧！' }}
        </p>
        <button 
          v-if="!searchQuery && !selectedTag"
          @click="router.push('/cards/new')"
          class="btn btn-primary"
        >
          <Plus class="w-4 h-4 mr-2" />
          创建卡片
        </button>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <KnowledgeCard
          v-for="card in filteredCards"
          :key="card.id"
          :card="card"
          @click="viewCard(card.id)"
          @delete="handleDeleteCard"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { cardsApi, type KnowledgeCard } from '@/services/cards'
import KnowledgeCard from '@/components/cards/KnowledgeCard.vue'
import { 
  BookOpen, 
  Plus, 
  Search 
} from 'lucide-vue-next'

const router = useRouter()
const authStore = useAuthStore()

const cards = ref<KnowledgeCard[]>([])
const isLoading = ref(false)
const searchQuery = ref('')
const selectedTag = ref('')

const allTags = computed(() => {
  const tags = new Set<string>()
  cards.value.forEach(card => {
    card.tags.forEach(tag => tags.add(tag))
  })
  return Array.from(tags)
})

const filteredCards = computed(() => {
  let filtered = cards.value

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(card => 
      card.title.toLowerCase().includes(query) ||
      card.content.toLowerCase().includes(query)
    )
  }

  if (selectedTag.value) {
    filtered = filtered.filter(card => 
      card.tags.includes(selectedTag.value)
    )
  }

  return filtered
})

const loadCards = async () => {
  try {
    isLoading.value = true
    const data = await cardsApi.getCards()
    cards.value = data.items || []
  } catch (error) {
    console.error('Failed to load cards:', error)
  } finally {
    isLoading.value = false
  }
}

const viewCard = (id: string) => {
  router.push(`/cards/${id}`)
}

const handleDeleteCard = async (id: string) => {
  if (confirm('确定要删除这个卡片吗？')) {
    try {
      await cardsApi.deleteCard(id)
      cards.value = cards.value.filter(card => card.id !== id)
    } catch (error) {
      console.error('Failed to delete card:', error)
      alert('删除失败，请重试')
    }
  }
}

onMounted(() => {
  loadCards()
})
</script>