// Authentication service
import { apiRequest } from './base'

export interface LoginCredentials {
    username: string
    password: string
}

export interface AuthToken {
    access_token: string
    token_type: string
}

export interface User {
    id: number
    username: string
}

export class AuthService {
    /**
     * Performs the login action on the backend.
     * @param credentials username and password
     * @returns Authentication token if the user was logged in
     */
    async login(credentials: LoginCredentials): Promise<AuthToken> {
        // FastAPI OAuth2PasswordRequestForm expects form data
        const formData = new FormData()
        formData.append('username', credentials.username)
        formData.append('password', credentials.password)

        const response = await fetch(`${import.meta.env.VITE_API_BASE_URL || '/api'}/auth/login`, {
            method: 'POST',
            body: formData,
        })

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({
                detail: `HTTP ${response.status}: ${response.statusText}`
            }))
            throw new Error(errorData.detail)
        }

        return await response.json()
    }

    async getCurrentUser(): Promise<User> {
        return apiRequest<User>('/auth/me')
    }
}

export const authService = new AuthService()