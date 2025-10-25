// Main API services export
export { authService } from './auth'
export { campaignsService } from './campaigns'
export { apiRequest } from './base'

// Re-export types for convenience
export type { LoginCredentials, AuthToken, User } from './auth'
export type { Campaign, CreateCampaignData, UpdateCampaignData } from './campaigns'
export type { ApiError } from './base'
