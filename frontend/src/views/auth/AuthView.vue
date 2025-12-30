<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div class="text-center">
        <h1 class="text-4xl font-bold text-gray-900 dark:text-white mb-2">MindGarden</h1>
        <p class="text-gray-600 dark:text-gray-400">个人知识库和媒体收藏系统</p>
      </div>
      
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8">
        <div class="flex space-x-1 mb-6">
          <button
            @click="activeTab = 'login'"
            :class="[
              'flex-1 py-2 px-4 text-sm font-medium rounded-md transition-colors',
              activeTab === 'login'
                ? 'bg-primary-500 text-white'
                : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300'
            ]"
          >
            登录
          </button>
          <button
            @click="activeTab = 'register'"
            :class="[
              'flex-1 py-2 px-4 text-sm font-medium rounded-md transition-colors',
              activeTab === 'register'
                ? 'bg-primary-500 text-white'
                : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300'
            ]"
          >
            注册
          </button>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-6">
          <div v-if="activeTab === 'register'" class="space-y-4">
            <div>
              <label for="full_name" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                姓名
              </label>
              <input
                id="full_name"
                v-model="registerForm.full_name"
                type="text"
                required
                class="input w-full"
                placeholder="请输入您的姓名"
              />
            </div>
          </div>

          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              邮箱
            </label>
            <input
              id="email"
              v-model="loginForm.email"
              type="email"
              required
              class="input w-full"
              placeholder="请输入您的邮箱"
            />
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              密码
            </label>
            <input
              id="password"
              v-model="loginForm.password"
              type="password"
              required
              class="input w-full"
              placeholder="请输入密码"
            />
          </div>

          <div v-if="error" class="text-red-600 text-sm bg-red-50 dark:bg-red-900/20 dark:text-red-400 p-3 rounded-md">
            {{ error }}
          </div>

          <button
            type="submit"
            :disabled="authStore.isLoading"
            class="btn btn-primary w-full py-2 px-4"
          >
            <span v-if="authStore.isLoading" class="inline-block animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></span>
            {{ activeTab === 'login' ? '登录' : '注册' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const activeTab = ref<'login' | 'register'>('login')
const error = ref('')

const loginForm = reactive({
  email: '',
  password: ''
})

const registerForm = reactive({
  full_name: '',
  email: '',
  password: ''
})

const handleSubmit = async () => {
  error.value = ''
  
  if (activeTab.value === 'login') {
    const result = await authStore.login(loginForm)
    if (result.success) {
      router.push('/dashboard')
    } else {
      error.value = result.error || '登录失败'
    }
  } else {
    const result = await authStore.register({
      ...registerForm,
      email: loginForm.email
    })
    if (result.success) {
      router.push('/dashboard')
    } else {
      error.value = result.error || '注册失败'
    }
  }
}

onMounted(() => {
  authStore.initializeAuth()
})
</script>