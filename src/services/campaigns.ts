// Campaigns API service
import { apiRequest } from './base'

export interface Campaign {
    id: number
    name: string
    description: string
    start_date: string
    end_date: string
    budget: number
    status: boolean
}

export interface CreateCampaignData {
    name: string
    description: string
    start_date: string
    end_date: string
    budget: number
    status: boolean
}

export interface UpdateCampaignData extends CreateCampaignData {
    id: number
}

/**
 * Sends requests with proper data to the backend, and returns Promises that eventually resolve to the response.
 * All the actual work is done within stores that handle the data.
 */
export class CampaignsService {
    async getCampaigns(): Promise<Campaign[]> {
        return apiRequest<Campaign[]>('/campaigns/')
    }

    async getCampaign(id: number): Promise<Campaign> {
        return apiRequest<Campaign>(`/campaigns/${id}`)
    }

    async createCampaign(campaignData: CreateCampaignData): Promise<Campaign> {
        return apiRequest<Campaign>('/campaigns/', {
            method: 'POST',
            body: JSON.stringify({ id: 0, ...campaignData }),
        })
    }

    async updateCampaign(id: number, campaignData: UpdateCampaignData): Promise<Campaign> {
        return apiRequest<Campaign>(`/campaigns/${id}`, {
            method: 'PUT',
            body: JSON.stringify(campaignData),
        })
    }

    async deleteCampaign(id: number): Promise<{ message: string }> {
        return apiRequest<{ message: string }>(`/campaigns/${id}`, {
            method: 'DELETE',
        })
    }
}

export const campaignsService = new CampaignsService()