import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

export interface KnowledgeCard {
  id: string
  title: string
  content: string
  tags: string[]
  notebook_id?: string
  created_at: string
  updated_at: string
  owner_id: string
}

export interface CreateCardRequest {
  title: string
  content: string
  tags: string[]
  notebook_id?: string
}

export interface UpdateCardRequest {
  title?: string
  content?: string
  tags?: string[]
  notebook_id?: string
}

export interface Notebook {
  id: string
  name: string
  description?: string
  created_at: string
  updated_at: string
  owner_id: string
}

export const cardsApi = {
  async getCards(params?: { 
    page?: number
    limit?: number
    search?: string
    tags?: string[]
  }) {
    const response = await authStore.api.get('/cards', { params })
    return response.data
  },

  async getCard(id: string) {
    const response = await authStore.api.get(`/cards/${id}`)
    return response.data
  },

  async createCard(card: CreateCardRequest) {
    const response = await authStore.api.post('/cards', card)
    return response.data
  },

  async updateCard(id: string, card: UpdateCardRequest) {
    const response = await authStore.api.put(`/cards/${id}`, card)
    return response.data
  },

  async deleteCard(id: string) {
    await authStore.api.delete(`/cards/${id}`)
  },

  async getNotebooks() {
    const response = await authStore.api.get('/notebooks')
    return response.data
  },

  async createNotebook(notebook: { name: string; description?: string }) {
    const response = await authStore.api.post('/notebooks', notebook)
    return response.data
  }
}