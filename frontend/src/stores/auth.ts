import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export interface User {
  id: string
  email: string
  full_name: string
  is_active: boolean
  created_at: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface RegisterRequest {
  email: string
  password: string
  full_name: string
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token'))
  const isLoading = ref(false)

  const isAuthenticated = computed(() => !!token.value && !!user.value)

  const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL,
  })

  api.interceptors.request.use((config) => {
    if (token.value) {
      config.headers.Authorization = `Bearer ${token.value}`
    }
    return config
  })

  api.interceptors.response.use(
    (response) => response,
    async (error) => {
      if (error.response?.status === 401) {
        await logout()
      }
      return Promise.reject(error)
    }
  )

  const login = async (credentials: LoginRequest) => {
    try {
      isLoading.value = true
      const response = await api.post('/auth/login', credentials)
      const { access_token, user: userData } = response.data
      
      token.value = access_token
      user.value = userData
      localStorage.setItem('token', access_token)
      
      return { success: true }
    } catch (error: any) {
      return { 
        success: false, 
        error: error.response?.data?.detail || '登录失败' 
      }
    } finally {
      isLoading.value = false
    }
  }

  const register = async (userData: RegisterRequest) => {
    try {
      isLoading.value = true
      const response = await api.post('/auth/register', userData)
      const { access_token, user: newUser } = response.data
      
      token.value = access_token
      user.value = newUser
      localStorage.setItem('token', access_token)
      
      return { success: true }
    } catch (error: any) {
      return { 
        success: false, 
        error: error.response?.data?.detail || '注册失败' 
      }
    } finally {
      isLoading.value = false
    }
  }

  const logout = async () => {
    try {
      await api.post('/auth/logout')
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      token.value = null
      user.value = null
      localStorage.removeItem('token')
    }
  }

  const fetchCurrentUser = async () => {
    try {
      if (!token.value) return
      
      const response = await api.get('/auth/me')
      user.value = response.data
    } catch (error) {
      console.error('Failed to fetch current user:', error)
      await logout()
    }
  }

  const initializeAuth = async () => {
    if (token.value) {
      await fetchCurrentUser()
    }
  }

  return {
    user,
    token,
    isLoading,
    isAuthenticated,
    login,
    register,
    logout,
    fetchCurrentUser,
    initializeAuth,
    api
  }
})