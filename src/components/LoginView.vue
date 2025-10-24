<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import type { LoginCredentials } from '@/services/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')

const handleLogin = async () => {
    if (!username.value || !password.value) {
        return
    }

    try {
        const credentials: LoginCredentials = {
            username: username.value,
            password: password.value
        }

        await authStore.login(credentials)

        // Redirect to home/campaigns
        router.push('/')
    } catch (error) {
        // Error is handled by the store
        console.error('Login failed:', error)
    }
}
</script>

<template>
    <div class="login-container">
        <h2 class="title">Login</h2>

        <form @submit.prevent="handleLogin" class="login-form">
            <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" id="username" v-model="username" :disabled="authStore.isLoading" required>
            </div>

            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" v-model="password" :disabled="authStore.isLoading" required>
            </div>

            <div v-if="authStore.error" class="error-message">
                {{ authStore.error }}
            </div>

            <button type="submit" :disabled="authStore.isLoading" class="login-button">
                {{ authStore.isLoading ? 'Logging in...' : 'Login' }}
            </button>
        </form>
    </div>
</template>

<style scoped>
.login-container {
    position: absolute;
    left: 0;
    top: 0;
    right: 0;
    bottom: 0;

    width: 400px;
    height: fit-content;
    max-height: 400px;

    margin: auto;
    padding: 32px;

    border: 1px solid var(--color-gray-700);
    border-radius: 4px;

    box-shadow: 0px 4px 8px 2px rgba(0, 0, 0, 0.5);

    background: var(--color-gray-800);
}

.title {
    color: var(--color-gray-50);
    text-align: center;
    margin-top: 0;
    margin-bottom: 16px;
    padding: 0;
}

.login-form {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.form-group input {
    background-color: var(--color-gray-900);
    color: var(--color-gray-50);

    padding: 8px;

    border: 1px solid var(--color-gray-700);
    border-radius: 4px;

    font-size: 1rem;
}

.form-group input:focus {
    outline: none;
    border-color: var(--color-primary);
    box-shadow: 0 0 4px 0 var(--color-primary);
}

.form-group input:disabled {
    background-color: var(--color-gray-700);
    cursor: not-allowed;
}

.error-message {
    background-color: var(--color-error);
    color: var(--color-error-50);

    padding: 0.5rem;
    font-size: 0.875rem;

    border: 1px solid var(--color-error);
    border-radius: 4px;
}

.login-button {
    background-color: var(--color-primary);
    color: var(--color-primary-0);

    padding: 0.75rem;

    border: none;
    border-radius: 4px;

    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.2s;
}

.login-button:hover:not(:disabled) {
    background-color: var(--color-primary-800);
}

.login-button:disabled {
    background-color: var(--color-gray-700);
    cursor: not-allowed;
}
</style>