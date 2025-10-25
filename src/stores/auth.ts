import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authService, type LoginCredentials, type User } from '@/services/auth'

export const useAuthStore = defineStore('auth', () => {
    // State
    const user = ref<User | null>(null)
    const token = ref<string | null>(null)
    const isLoading = ref(false)
    const error = ref<string | null>(null)

    // Getters
    const isAuthenticated = computed(() => token.value ? true : false)
    const currentUser = computed(() => user.value)

    // Actions
    function logout() {
        token.value = null
        user.value = null
        error.value = null
        localStorage.removeItem('access_token')
    }

    function getToken(): string | null {
        return localStorage.getItem('access_token')
    }
    function setToken(newToken: string): void {
        token.value = newToken
        localStorage.setItem('access_token', newToken)
    }

    async function login(credentials: LoginCredentials) {
        isLoading.value = true
        error.value = null

        try {
            const tokenData = await authService.login(credentials)
            setToken(tokenData.access_token)
            fetchCurrentUser()

            return tokenData
        } catch (err) {
            error.value = err instanceof Error ? err.message : 'Login failed'
            throw err
        } finally {
            isLoading.value = false
        }
    }

    function fetchCurrentUser() {
        if (!isAuthenticated.value) return

        isLoading.value = true
        error.value = null

        authService.getCurrentUser().then(
            (newUser: User) => {
                user.value = newUser
            },
            (err) => {
                error.value = err instanceof Error ? err.message : 'Failed to fetch user'
                // If fetching user fails, token might be invalid, so we force logout
                logout()
            }
        ).finally(() => {
            isLoading.value = false
        })
    }

    function clearError() {
        error.value = null
    }

    // Initialize store
    function initialize() {
        token.value = getToken()
        if (isAuthenticated.value) {
            fetchCurrentUser()
        }
    }

    return {
        // State
        user,
        isLoading,
        error,

        // Getters
        isAuthenticated,
        currentUser,

        // Actions
        login,
        logout,
        fetchCurrentUser,
        clearError,
        initialize,
    }
})