<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- 顶部导航栏 -->
    <div class="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <router-link to="/cards" class="flex items-center">
              <ArrowLeft class="w-6 h-6 text-gray-600 dark:text-gray-300 mr-2" />
              <h1 class="text-xl font-bold text-gray-900 dark:text-white">新建卡片</h1>
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- 主内容区 -->
    <div class="max-w-4xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
      <div class="card p-6">
        <form @submit.prevent="handleSubmit" class="space-y-6">
          <!-- 标题 -->
          <div>
            <label for="title" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              标题 *
            </label>
            <input
              id="title"
              v-model="form.title"
              type="text"
              required
              class="input w-full"
              placeholder="请输入卡片标题"
            />
          </div>

          <!-- 内容 -->
          <div>
            <label for="content" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              内容 *
            </label>
            <textarea
              id="content"
              v-model="form.content"
              required
              rows="10"
              class="input w-full"
              placeholder="请输入卡片内容..."
            ></textarea>
          </div>

          <!-- 标签 -->
          <div>
            <label for="tags" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              标签
            </label>
            <div class="flex flex-wrap gap-2 mb-3">
              <span
                v-for="(tag, index) in form.tags"
                :key="index"
                class="inline-flex items-center px-3 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 text-sm rounded-full"
              >
                {{ tag }}
                <button
                  @click="removeTag(index)"
                  type="button"
                  class="ml-2 text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-200"
                >
                  <X class="w-3 h-3" />
                </button>
              </span>
            </div>
            <div class="flex gap-2">
              <input
                v-model="newTag"
                @keydown.enter.prevent="addTag"
                type="text"
                class="input flex-1"
                placeholder="输入标签后按回车添加"
              />
              <button
                @click="addTag"
                type="button"
                class="btn btn-secondary"
              >
                <Plus class="w-4 h-4" />
              </button>
            </div>
          </div>

          <!-- 笔记本 -->
          <div>
            <label for="notebook" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              笔记本
            </label>
            <select
              id="notebook"
              v-model="form.notebook_id"
              class="input w-full"
            >
              <option value="">选择笔记本（可选）</option>
              <option
                v-for="notebook in notebooks"
                :key="notebook.id"
                :value="notebook.id"
              >
                {{ notebook.name }}
              </option>
            </select>
          </div>

          <!-- 错误信息 -->
          <div v-if="error" class="text-red-600 text-sm bg-red-50 dark:bg-red-900/20 dark:text-red-400 p-3 rounded-md">
            {{ error }}
          </div>

          <!-- 按钮 -->
          <div class="flex justify-end space-x-4">
            <router-link to="/cards" class="btn btn-secondary">
              取消
            </router-link>
            <button
              type="submit"
              :disabled="isSubmitting"
              class="btn btn-primary"
            >
              <span v-if="isSubmitting" class="inline-block animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></span>
              {{ isSubmitting ? '保存中...' : '保存卡片' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { cardsApi, type Notebook } from '@/services/cards'
import { 
  ArrowLeft, 
  Plus, 
  X 
} from 'lucide-vue-next'

const router = useRouter()

const form = reactive({
  title: '',
  content: '',
  tags: [] as string[],
  notebook_id: ''
})

const newTag = ref('')
const notebooks = ref<Notebook[]>([])
const error = ref('')
const isSubmitting = ref(false)

const addTag = () => {
  const tag = newTag.value.trim()
  if (tag && !form.tags.includes(tag)) {
    form.tags.push(tag)
    newTag.value = ''
  }
}

const removeTag = (index: number) => {
  form.tags.splice(index, 1)
}

const loadNotebooks = async () => {
  try {
    notebooks.value = await cardsApi.getNotebooks()
  } catch (error) {
    console.error('Failed to load notebooks:', error)
  }
}

const handleSubmit = async () => {
  error.value = ''
  isSubmitting.value = true

  try {
    const cardData = {
      ...form,
      notebook_id: form.notebook_id || undefined
    }
    
    await cardsApi.createCard(cardData)
    router.push('/cards')
  } catch (err: any) {
    error.value = err.response?.data?.detail || '保存失败，请重试'
  } finally {
    isSubmitting.value = false
  }
}

onMounted(() => {
  loadNotebooks()
})
</script>