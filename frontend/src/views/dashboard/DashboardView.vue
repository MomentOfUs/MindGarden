<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- 导航栏 -->
    <nav class="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <h1 class="text-xl font-bold text-gray-900 dark:text-white">MindGarden</h1>
          </div>
          
          <div class="flex items-center space-x-4">
            <router-link 
              to="/cards" 
              class="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white px-3 py-2 rounded-md text-sm font-medium"
            >
              知识卡片
            </router-link>
            <router-link 
              to="/media" 
              class="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white px-3 py-2 rounded-md text-sm font-medium"
            >
              媒体收藏
            </router-link>
            <button 
              @click="themeStore.toggleTheme"
              class="p-2 text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white rounded-md"
            >
              <Sun v-if="themeStore.isDarkMode" class="w-5 h-5" />
              <Moon v-else class="w-5 h-5" />
            </button>
            <div class="relative">
              <button 
                @click="showUserMenu = !showUserMenu"
                class="flex items-center text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white"
              >
                <User class="w-6 h-6" />
              </button>
              
              <div v-if="showUserMenu" class="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 rounded-md shadow-lg py-1 z-50">
                <router-link 
                  to="/profile" 
                  class="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
                >
                  个人资料
                </router-link>
                <button 
                  @click="handleLogout"
                  class="block w-full text-left px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
                >
                  退出登录
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <!-- 主内容区 -->
    <main class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
      <!-- 欢迎信息 -->
      <div class="mb-8">
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white">
          欢迎回来，{{ authStore.user?.full_name || '用户' }}！
        </h2>
        <p class="mt-1 text-sm text-gray-600 dark:text-gray-400">
          开始整理您的知识卡片和媒体收藏
        </p>
      </div>

      <!-- 统计卡片 -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div class="card p-6">
          <div class="flex items-center">
            <div class="p-2 bg-blue-100 dark:bg-blue-900 rounded-lg">
              <BookOpen class="w-6 h-6 text-blue-600 dark:text-blue-400" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">知识卡片</p>
              <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ stats.cards }}</p>
            </div>
          </div>
        </div>

        <div class="card p-6">
          <div class="flex items-center">
            <div class="p-2 bg-green-100 dark:bg-green-900 rounded-lg">
              <FolderOpen class="w-6 h-6 text-green-600 dark:text-green-400" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">笔记本</p>
              <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ stats.notebooks }}</p>
            </div>
          </div>
        </div>

        <div class="card p-6">
          <div class="flex items-center">
            <div class="p-2 bg-purple-100 dark:bg-purple-900 rounded-lg">
              <Image class="w-6 h-6 text-purple-600 dark:text-purple-400" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">媒体项目</p>
              <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ stats.media }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 快捷操作 -->
      <div class="mb-8">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">快捷操作</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <router-link 
            to="/cards/new" 
            class="card p-6 hover:shadow-md transition-shadow cursor-pointer"
          >
            <div class="flex items-center">
              <div class="p-3 bg-blue-100 dark:bg-blue-900 rounded-lg">
                <Plus class="w-6 h-6 text-blue-600 dark:text-blue-400" />
              </div>
              <div class="ml-4">
                <h4 class="font-semibold text-gray-900 dark:text-white">创建新卡片</h4>
                <p class="text-sm text-gray-600 dark:text-gray-400">开始记录您的知识</p>
              </div>
            </div>
          </router-link>

          <router-link 
            to="/cards" 
            class="card p-6 hover:shadow-md transition-shadow cursor-pointer"
          >
            <div class="flex items-center">
              <div class="p-3 bg-green-100 dark:bg-green-900 rounded-lg">
                <BookOpen class="w-6 h-6 text-green-600 dark:text-green-400" />
              </div>
              <div class="ml-4">
                <h4 class="font-semibold text-gray-900 dark:text-white">浏览卡片</h4>
                <p class="text-sm text-gray-600 dark:text-gray-400">查看您的知识库</p>
              </div>
            </div>
          </router-link>
        </div>
      </div>

      <!-- 最近的活动 -->
      <div>
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">最近的活动</h3>
        <div class="card p-6">
          <p class="text-gray-600 dark:text-gray-400 text-center py-8">
            开始使用 MindGarden，记录您的第一个知识卡片吧！
          </p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'
import { 
  BookOpen, 
  FolderOpen, 
  Image, 
  Plus, 
  User, 
  Sun, 
  Moon 
} from 'lucide-vue-next'

const router = useRouter()
const authStore = useAuthStore()
const themeStore = useThemeStore()

const showUserMenu = ref(false)
const stats = ref({
  cards: 0,
  notebooks: 0,
  media: 0
})

const handleLogout = async () => {
  await authStore.logout()
  router.push('/auth')
}

onMounted(() => {
  themeStore.initializeTheme()
})
</script>