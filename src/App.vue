<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const logout = () => {
    authStore.logout()
    router.push('/login')
}

onMounted(() => {
    authStore.initialize()
})
</script>

<template>
    <nav class="user-controls" v-if="authStore.isAuthenticated">
        <div class="user-greet">Welcome, {{ authStore?.user?.username }}</div>
        <button class="logout-button" @click="logout">Logout</button>
    </nav>
    <main class="container">
        <RouterView></RouterView>
    </main>
</template>

<style scoped>
.user-controls {
    display: flex;
    flex-direction: row;
    justify-content: flex-end;
    align-items: center;
    gap: 16px;

    width: 100%;
    padding: 4px 32px;

    background: var(--color-gray-800);
    border-bottom: 1px solid var(--color-gray-700);
}

.user-greet {
    padding-right: 16px;
    border-right: 1px solid var(--color-gray-700);
}

.logout-button {
    background-color: var(--color-gray-800);
    color: var(--color-gray-50);

    padding: 8px;

    border: none;
    border-radius: 2px;

    font-size: 0.875rem;
    text-transform: uppercase;
    cursor: pointer;
    transition: background-color 0.2s;
}

.logout-button:hover {
    background-color: var(--color-gray-700);
}
</style>
