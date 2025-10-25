<script setup lang="ts">
import type { Campaign } from '@/services/campaigns'

interface Props {
    campaign: Campaign
}

interface Emits {
    (e: 'delete', id: number): void
    (e: 'edit', campaign: Campaign): void
    (e: 'toggle', campaign: Campaign): void
}

defineProps<Props>()
defineEmits<Emits>()

const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString()
}

const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount)
}
</script>

<template>
    <div class="campaign-card" :class="{ inactive: !campaign.status }">
        <div class="campaign-header">
            <h3>{{ campaign.name }}</h3>
            <span class="campaign-status" :class="{ active: campaign.status }">
                {{ campaign.status ? 'Active' : 'Inactive' }}
            </span>
        </div>

        <p class="campaign-description">{{ campaign.description }}</p>

        <div class="campaign-details">
            <div class="detail">
                <strong>Budget:</strong> {{ formatCurrency(campaign.budget) }}
            </div>
            <div class="detail">
                <strong>Start:</strong> {{ formatDate(campaign.start_date) }}
            </div>
            <div class="detail">
                <strong>End:</strong> {{ formatDate(campaign.end_date) }}
            </div>
        </div>

        <div class="campaign-actions">
            <button class="edit-button" @click="$emit('edit', campaign)">Edit</button>
            <button class="edit-button" @click="$emit('toggle', campaign)">Toggle</button>
            <div class="action-spacer"></div>
            <button class="delete-button" @click="$emit('delete', campaign.id)">Delete</button>
        </div>
    </div>
</template>

<style scoped>
.campaign-card {
    background: var(--color-gray-700);
    border: 1px solid var(--color-gray-600);
    border-radius: 8px;
    padding: 24px;
    transition: box-shadow 0.2s;
}

.campaign-card:hover {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.6);
}

.campaign-card.inactive {
    background-color: var(--color-gray-800);
}

.campaign-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
}

.campaign-header h3 {
    margin: 0;
    color: var(--color-gray-50);
}

.campaign-status {
    padding: 4px 16px;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    background-color: var(--color-error-700);
    color: var(--color-error-50);
}

.campaign-status.active {
    background-color: var(--color-success-700);
    color: var(--color-success-50);
}

.campaign-description {
    color: var(--color-gray-200);
    margin-bottom: 16px;
    line-height: 1.5;
}

.campaign-details {
    margin-bottom: 24px;
}

.detail {
    margin-bottom: 8px;
    font-size: 0.875rem;
}

.detail strong {
    color: var(--color-gray-50);
}

.campaign-actions {
    display: flex;
    gap: 8px;
}

.edit-button,
.delete-button {
    padding: 8px 16px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.875rem;
    transition: background-color 0.2s;
}

.action-spacer {
    flex: 1;
}

.edit-button {
    background-color: var(--color-primary);
    color: var(--color-primary-50);
}

.edit-button:hover {
    background-color: var(--color-primary-400);
}

.delete-button {
    background-color: var(--color-error);
    color: var(--color-error-50);
}

.delete-button:hover {
    background-color: var(--color-error-400);
}
</style>