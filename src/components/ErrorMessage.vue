<script setup lang="ts">
interface Props {
    message: string
}

interface Emits {
    (e: 'close'): void
}

defineProps<Props>()
defineEmits<Emits>()
</script>

<template>
    <div class="error-message">
        {{ message }}
        <button @click="$emit('close')" class="close-error">×</button>
    </div>
</template>

<style scoped>
.error-message {
    z-index: 300;
    position: absolute;
    top: 64px;
    left: 50%;
    transform: translate(-50%);

    display: flex;
    justify-content: space-between;
    align-items: center;

    background-color: var(--color-error);
    color: var(--color-error-50);

    padding: 16px;
    margin-top: 64px;
    width: fit-content;
    height: fit-content;

    border: 1px solid var(--color-error-400);
    border-radius: 4px;
}

.close-error {
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    color: var(--color-error-50);
}
</style>