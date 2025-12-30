import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      redirect: '/dashboard'
    },
    {
      path: '/auth',
      name: 'auth',
      component: () => import('@/views/auth/AuthView.vue'),
      meta: { requiresGuest: true }
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('@/views/dashboard/DashboardView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/cards',
      name: 'cards',
      component: () => import('@/views/library/CardsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/cards/new',
      name: 'new-card',
      component: () => import('@/views/library/NewCardView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/cards/:id',
      name: 'card-detail',
      component: () => import('@/views/library/CardDetailView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/media',
      name: 'media',
      component: () => import('@/views/media/MediaView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('@/views/profile/ProfileView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: () => import('@/views/NotFoundView.vue')
    }
  ]
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/auth')
  } else if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router