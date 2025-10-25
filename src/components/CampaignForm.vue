<script setup lang="ts">
import { ref } from 'vue'
import type { CreateCampaignData } from '@/services/campaigns'

interface Props {
    isLoading?: boolean
}

interface Emits {
    (e: 'submit', campaign: CreateCampaignData): void
    (e: 'error', error: string): void
    (e: 'cancel'): void
}

const emit = defineEmits<Emits>()
defineProps<Props>()

const formData = ref<CreateCampaignData>({
    name: '',
    description: '',
    start_date: '',
    end_date: '',
    budget: 0,
    status: true
})

function validate() {
    if (formData.value.start_date >= formData.value.end_date) {
        emit('error', "End date can't be earlier or the same as start date.")
        return false
    }
    if (formData.value.budget <= 0) {
        emit('error', "Budget has to be higher than 0$.")
        return false
    }
    return true
}

const handleSubmit = () => {
    if (validate()) {
        emit('submit', { ...formData.value })
        resetForm()
    }
}

const resetForm = () => {
    formData.value = {
        name: '',
        description: '',
        start_date: '',
        end_date: '',
        budget: 0,
        status: true
    }
}
</script>

<template>
    <div class="overlay">
        <div class="create-form">
            <h3>Creating a new campaign</h3>
            <form @submit.prevent="handleSubmit">
                <div class="form-row">
                    <div class="form-group">
                        <label for="name">Name:</label>
                        <input type="text" id="name" v-model="formData.name" required>
                    </div>
                    <div class="form-group">
                        <label for="budget">Budget:</label>
                        <input type="number" id="budget" v-model="formData.budget" min="0" step="0.01" required>
                    </div>
                </div>

                <div class="form-group">
                    <label for="description">Description:</label>
                    <textarea id="description" v-model="formData.description" rows="3" required></textarea>
                </div>

                <div class="form-row">
                    <div class="form-group">
                        <label for="start_date">Start Date:</label>
                        <input type="datetime-local" id="start_date" v-model="formData.start_date" required>
                    </div>
                    <div class="form-group">
                        <label for="end_date">End Date:</label>
                        <input type="datetime-local" id="end_date" v-model="formData.end_date" required>
                    </div>
                </div>

                <div class="form-group">
                    <label class="checkbox-label">
                        <input type="checkbox" v-model="formData.status">
                        Active
                    </label>
                </div>

                <div class="form-actions">
                    <button type="submit" :disabled="isLoading">
                        {{ isLoading ? 'Submitting...' : 'Submit' }}
                    </button>
                    <button type="button" @click="$emit('cancel')" class="cancel-button">
                        Cancel
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>

<style scoped>
.overlay {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;

    display: flex;
    justify-content: center;
    align-items: center;

    background: rgba(0, 0, 0, 0.3)
}

.create-form {
    height: fit-content;

    min-width: 800px;
    width: fit-content;

    background: var(--color-gray-700);
    padding: 24px;
    margin-bottom: 16px;

    border: 1px solid var(--color-gray-500);
    border-radius: 8px;

    box-shadow: 1px 0 4px 2px var(--color-gray-900);
}

.create-form h3 {
    margin-top: 0;
    margin-bottom: 1.5rem;
    color: var(--color-gray-50);
}

.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
}

.form-group {
    margin-bottom: 1rem;
}

.form-group label {
    display: block;
    margin-bottom: 2px;
    color: var(--color-gray-50);
}

.form-group input,
.form-group textarea {
    color-scheme: dark;
    background-color: var(--color-gray-800);
    color: var(--color-gray-50);

    padding: 8px;

    border: 1px solid var(--color-gray-600);
    border-radius: 4px;

    font-size: 1rem;

    width: 100%;
    padding: 8px 16px;
}

.form-group input:focus,
.form-group textarea:focus {
    outline: none;
    border-color: var(--color-primary);
    box-shadow: 0 0 4px 0 var(--color-primary);
}

.checkbox-label {
    display: flex !important;
    align-items: center;
    gap: 0.5rem;
    cursor: pointer;
}

.checkbox-label input {
    width: auto !important;
}

.form-actions {
    margin-top: 24px;
    display: flex;
    gap: 24px;
}

.form-actions button {
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
    transition: background-color 0.2s;
}

.form-actions button[type="submit"] {
    background-color: var(--color-success);
    color: var(--color-success-50);
}

.form-actions button[type="submit"]:hover:not(:disabled) {
    background-color: var(--color-success-500);
}

.form-actions button[type="submit"]:disabled {
    background-color: var(--color-gray-800);
    cursor: not-allowed;
}

.cancel-button {
    background-color: var(--color-gray-500);
    color: var(--color-gray-50);
}

.cancel-button:hover {
    background-color: var(--color-gray-400);
}

@media (max-width: 768px) {
    .form-row {
        grid-template-columns: 1fr;
    }

    .form-actions {
        flex-direction: column;
    }
}
</style>