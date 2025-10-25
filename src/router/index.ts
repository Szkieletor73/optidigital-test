import CampaignsView from '@/components/CampaignsView.vue'
import LoginView from '@/components/LoginView.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: CampaignsView,
      meta: { requiresAuth: true },
    },
    {
      path: '/login',
      component: LoginView,
      meta: { requiresAuth: false },
    },
  ],
})

router.beforeEach((to, from, next) => {
  // Import auth service here to avoid circular dependency
  const token = localStorage.getItem('access_token')
  const requiresAuth = to.meta.requiresAuth

  if (requiresAuth && !token) {
    // Route requires auth but user is not authenticated
    next('/login')
  } else if (to.path === '/login' && token) {
    // User is authenticated but trying to access login page
    next('/')
  } else {
    // Allow navigation
    next()
  }
})

export default router
