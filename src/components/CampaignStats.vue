<script setup lang="ts">
interface Props {
    totalCampaigns: number
    activeCampaigns: number
    totalBudget: number
}

defineProps<Props>()

const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount)
}
</script>

<template>
    <div class="campaigns-stats">
        <div class="stat">
            <span class="stat-label">Total Campaigns:</span>
            <span class="stat-value">{{ totalCampaigns }}</span>
        </div>
        <div class="stat">
            <span class="stat-label">Active:</span>
            <span class="stat-value">{{ activeCampaigns }}</span>
        </div>
        <div class="stat">
            <span class="stat-label">Total Budget:</span>
            <span class="stat-value">{{ formatCurrency(totalBudget) }}</span>
        </div>
    </div>
</template>

<style scoped>
.campaigns-stats {
    background-color: var(--color-gray-700);

    display: flex;
    gap: 32px;
    margin-bottom: 32px;
    padding: 16px;
    border-radius: 12px;
}

.stat {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.stat-label {
    font-size: 0.875rem;
    color: var(--color-gray-200);
}

.stat-value {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--color-gray-50);
}

@media (max-width: 768px) {
    .campaigns-stats {
        flex-direction: column;
        gap: 8px;
    }
}
</style>