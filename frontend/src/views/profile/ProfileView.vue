<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <div class="max-w-4xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
      <div class="card p-6">
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-6">个人资料</h2>
        
        <div class="space-y-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              邮箱
            </label>
            <p class="text-gray-900 dark:text-white">{{ authStore.user?.email }}</p>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              姓名
            </label>
            <p class="text-gray-900 dark:text-white">{{ authStore.user?.full_name }}</p>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              注册时间
            </label>
            <p class="text-gray-900 dark:text-white">{{ formatDate(authStore.user?.created_at || '') }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { formatDate } from '@/utils/utils'

const authStore = useAuthStore()
</script>