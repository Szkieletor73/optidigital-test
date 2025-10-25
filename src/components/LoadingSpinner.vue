<script setup lang="ts">
interface Props {
    message?: string
}

withDefaults(defineProps<Props>(), {
    message: 'Loading...'
})
</script>

<template>
    <div class="loading">
        {{ message }}
    </div>
</template>

<style scoped>
.loading {
    text-align: center;
    padding: 16px;
    color: var(--color-gray-50);
}
</style>