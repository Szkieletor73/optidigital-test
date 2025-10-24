<script setup lang="ts">
interface Props {
    title: string
    message: string
}

defineProps<Props>()
</script>

<template>
    <div class="empty-state">
        <h3>{{ title }}</h3>
        <p>{{ message }}</p>
    </div>
</template>

<style scoped>
.empty-state {
    text-align: center;
    color: var(--color-gray-500);
}

.empty-state h3 {
    margin-bottom: 1rem;
    color: var(--color-gray-300);
}
</style>