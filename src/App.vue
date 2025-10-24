<script setup lang="ts">
import { computed } from 'vue'
import router from './router'

const isAuthenticated = computed(() => {
    return !!localStorage.getItem('access_token')
})

const logout = () => {
    localStorage.removeItem('access_token')
    router.push('/login')
}
</script>

<template>
    <nav v-if="isAuthenticated">
        <button @click="logout">Logout</button>
    </nav>
    <main class="container">
        <RouterView></RouterView>
    </main>
</template>

<style scoped></style>
