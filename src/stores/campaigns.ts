import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import {
    campaignsService,
    type Campaign,
    type CreateCampaignData,
    type UpdateCampaignData
} from '@/services/campaigns'

export const useCampaignsStore = defineStore('campaigns', () => {
    // State
    const campaigns = ref<Campaign[]>([])
    const currentCampaign = ref<Campaign | null>(null)
    const isLoading = ref(false)
    const error = ref<string | null>(null)

    // Getters
    const campaignsList = computed(() => campaigns.value)
    const activeCampaigns = computed(() =>
        campaigns.value.filter(campaign => campaign.status)
    )
    const inactiveCampaigns = computed(() =>
        campaigns.value.filter(campaign => !campaign.status)
    )
    const totalBudget = computed(() =>
        campaigns.value.reduce((sum, campaign) => sum + campaign.budget, 0)
    )

    // Actions
    async function fetchCampaigns() {
        isLoading.value = true
        error.value = null

        try {
            campaigns.value = await campaignsService.getCampaigns()
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to fetch campaigns')
            throw err
        } finally {
            isLoading.value = false
        }
    }

    async function fetchCampaign(id: number) {
        isLoading.value = true
        error.value = null

        try {
            currentCampaign.value = await campaignsService.getCampaign(id)
            return currentCampaign.value
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to fetch campaign')
            throw err
        } finally {
            isLoading.value = false
        }
    }

    async function createCampaign(campaignData: CreateCampaignData) {
        isLoading.value = true
        error.value = null

        try {
            const newCampaign = await campaignsService.createCampaign(campaignData)
            campaigns.value.push(newCampaign)
            return newCampaign
        } catch (err) {
            setError(error.value = err instanceof Error ? err.message : 'Failed to create campaign')
            throw err
        } finally {
            isLoading.value = false
        }
    }

    async function updateCampaign(id: number, campaignData: UpdateCampaignData) {
        isLoading.value = true
        error.value = null

        try {
            const updatedCampaign = await campaignsService.updateCampaign(id, campaignData)

            // Update in campaigns list
            const index = campaigns.value.findIndex(c => c.id === id)
            if (index !== -1) {
                campaigns.value[index] = updatedCampaign
            }

            // Update current campaign if it's the same
            if (currentCampaign.value?.id === id) {
                currentCampaign.value = updatedCampaign
            }

            return updatedCampaign
        } catch (err) {
            setError(error.value = err instanceof Error ? err.message : 'Failed to update campaign')
            throw err
        } finally {
            isLoading.value = false
        }
    }

    async function deleteCampaign(id: number) {
        isLoading.value = true
        error.value = null

        try {
            await campaignsService.deleteCampaign(id)

            // Remove from campaigns list
            campaigns.value = campaigns.value.filter(c => c.id !== id)

            // Clear current campaign if it's the deleted one
            if (currentCampaign.value?.id === id) {
                currentCampaign.value = null
            }

            return { success: true }
        } catch (err) {
            setError(error.value = err instanceof Error ? err.message : 'Failed to delete campaign')
            throw err
        } finally {
            isLoading.value = false
        }
    }

    function setError(newError: string) {
        error.value = newError
    }

    function clearError() {
        error.value = null
    }

    function clearCurrentCampaign() {
        currentCampaign.value = null
    }

    // Helper function to get campaign by ID from store
    function getCampaignById(id: number): Campaign | undefined {
        return campaigns.value.find(c => c.id === id)
    }

    return {
        // State
        campaigns,
        currentCampaign,
        isLoading,
        error,

        // Getters
        campaignsList,
        activeCampaigns,
        inactiveCampaigns,
        totalBudget,

        // Actions
        fetchCampaigns,
        fetchCampaign,
        createCampaign,
        updateCampaign,
        deleteCampaign,
        setError,
        clearError,
        clearCurrentCampaign,
        getCampaignById,
    }
})