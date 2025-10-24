<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { apiService, type LoginCredentials } from '@/services/api'

const router = useRouter()

const username = ref('')
const password = ref('')
const isLoading = ref(false)
const errorMessage = ref('')

const handleLogin = async () => {
  if (!username.value || !password.value) {
    errorMessage.value = 'Please enter both username and password'
    return
  }

  isLoading.value = true
  errorMessage.value = ''

  try {
    const credentials: LoginCredentials = {
      username: username.value,
      password: password.value
    }

    const tokenData = await apiService.login(credentials)
    
    // Store the token
    localStorage.setItem('access_token', tokenData.access_token)
    
    // Redirect to home/campaigns
    router.push('/')
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'Login failed'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
    <div class="login-container">
        <h2>Login</h2>
        
        <form @submit.prevent="handleLogin" class="login-form">
            <div class="form-group">
                <label for="username">Username:</label>
                <input 
                    type="text" 
                    id="username" 
                    v-model="username"
                    :disabled="isLoading"
                    required
                >
            </div>
            
            <div class="form-group">
                <label for="password">Password:</label>
                <input 
                    type="password" 
                    id="password" 
                    v-model="password"
                    :disabled="isLoading"
                    required
                >
            </div>
            
            <div v-if="errorMessage" class="error-message">
                {{ errorMessage }}
            </div>
            
            <button type="submit" :disabled="isLoading" class="login-button">
                {{ isLoading ? 'Logging in...' : 'Login' }}
            </button>
        </form>
    </div>
</template>

<style scoped>
.login-container {
    max-width: 400px;
    margin: 2rem auto;
    padding: 2rem;
    border: 1px solid #ddd;
    border-radius: 8px;
    background: white;
}

.login-form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.form-group label {
    font-weight: 500;
}

.form-group input {
    padding: 0.75rem;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 1rem;
}

.form-group input:focus {
    outline: none;
    border-color: #007bff;
    box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.form-group input:disabled {
    background-color: #f5f5f5;
    cursor: not-allowed;
}

.error-message {
    color: #dc3545;
    font-size: 0.875rem;
    padding: 0.5rem;
    background-color: #f8d7da;
    border: 1px solid #f5c6cb;
    border-radius: 4px;
}

.login-button {
    padding: 0.75rem;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.2s;
}

.login-button:hover:not(:disabled) {
    background-color: #0056b3;
}

.login-button:disabled {
    background-color: #6c757d;
    cursor: not-allowed;
}

h2 {
    text-align: center;
    margin-bottom: 1.5rem;
    color: #333;
}
</style>