<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useCampaignsStore } from '@/stores/campaigns'
import type { CreateCampaignData, Campaign } from '@/services/campaigns'
import CampaignForm from './CampaignForm.vue'
import CampaignStats from './CampaignStats.vue'
import CampaignsList from './CampaignsList.vue'
import ErrorMessage from './ErrorMessage.vue'
import LoadingSpinner from './LoadingSpinner.vue'
import EmptyState from './EmptyState.vue'

const campaignsStore = useCampaignsStore()
const showCreateForm = ref(false)
const editingCampaign = ref<Campaign | null>(null)

onMounted(async () => {
    try {
        await campaignsStore.fetchCampaigns()
    } catch (error) {
        console.error('Failed to load campaigns:', error)
    }
})

const handleCreateCampaign = async (campaignData: CreateCampaignData) => {
    try {
        if (editingCampaign.value) {
            await campaignsStore.updateCampaign(editingCampaign.value.id, {
                id: editingCampaign.value.id,
                ...campaignData
            })
        } else {
            await campaignsStore.createCampaign(campaignData)
        }
        showCreateForm.value = false
        editingCampaign.value = null
    } catch (error) {
        console.error('Failed to save campaign:', error)
    }
}

const handleValidationError = (err: string) => {
    campaignsStore.setError(err)
}

const handleDeleteCampaign = async (id: number) => {
    if (confirm('Are you sure you want to delete this campaign?')) {
        try {
            await campaignsStore.deleteCampaign(id)
        } catch (error) {
            console.error('Failed to delete campaign:', error)
        }
    }
}

const handleEditCampaign = (campaign: Campaign) => {
    editingCampaign.value = campaign
    showCreateForm.value = true
}

const handleToggleCampaign = (campaign: Campaign) => {
    console.log(campaign.status)
    campaign.status = !campaign.status
    console.log(campaign.status)
    campaignsStore.updateCampaign(campaign.id, campaign)
}

const handleCancelForm = () => {
    showCreateForm.value = false
    editingCampaign.value = null
}
</script>

<template>
    <div class="campaigns-container">
        <div class="campaigns-header">
            <h1>Campaigns</h1>
            <button v-if="!showCreateForm" @click="showCreateForm = !showCreateForm" class="create-button">
                Create Campaign
            </button>
        </div>

        <!-- Error message -->
        <ErrorMessage v-if="campaignsStore.error" :message="campaignsStore.error"
            @close="campaignsStore.clearError()" />

        <!-- Create/Edit campaign form -->
        <CampaignForm v-if="showCreateForm" :is-loading="campaignsStore.isLoading" :edit-campaign="editingCampaign"
            @submit="handleCreateCampaign" @error="handleValidationError" @cancel="handleCancelForm" />

        <!-- Loading state -->
        <LoadingSpinner v-if="campaignsStore.isLoading && !showCreateForm" message="Loading campaigns..." />

        <!-- Campaigns list -->
        <div v-else-if="campaignsStore.campaignsList.length > 0" class="campaigns-list">
            <CampaignStats :total-campaigns="campaignsStore.campaignsList.length"
                :active-campaigns="campaignsStore.activeCampaigns.length" :total-budget="campaignsStore.totalBudget" />

            <CampaignsList :campaigns="campaignsStore.campaignsList" @delete="handleDeleteCampaign"
                @edit="handleEditCampaign" @toggle="handleToggleCampaign" />
        </div>

        <!-- Empty state -->
        <EmptyState v-else title="No campaigns found" message="Create your first campaign to get started." />
    </div>
</template>

<style scoped>
.campaigns-container {
    padding: 2rem;
    max-width: 1200px;
    margin: 0 auto;
}

.campaigns-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.campaigns-header h1 {
    margin: 0;
    height: 48px;
    color: var(--color-gray-10);
}

.create-button {
    background-color: var(--color-primary-600);
    color: var(--color-primary-50);

    padding: 12px 24px;

    border: none;
    border-radius: 4px;

    cursor: pointer;
    font-size: 1rem;
    transition: background-color 0.2s;
}

.create-button:hover {
    background-color: var(--color-primary-500);
}

@media (max-width: 768px) {
    .campaigns-container {
        padding: 16px;
    }

    .campaigns-header {
        flex-direction: column;
        gap: 16px;
        align-items: stretch;
    }
}
</style>