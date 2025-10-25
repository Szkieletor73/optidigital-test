import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'
import { createRouter, createWebHistory } from 'vue-router'
import App from '../App.vue'
import { useAuthStore } from '@/stores/auth'

// Create a mock router for testing
const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/', component: { template: '<div>Home</div>' } },
        { path: '/login', component: { template: '<div>Login</div>' } }
    ]
})

describe('App', () => {
    it('mounts and renders properly', async () => {
        const pinia = createTestingPinia({
            createSpy: vi.fn,
            stubActions: false
        })

        const wrapper = mount(App, {
            global: {
                plugins: [pinia, router],
                stubs: {
                    RouterView: true
                }
            }
        })

        // Wait for component to be fully mounted
        await wrapper.vm.$nextTick()

        // Test that the component mounts without errors
        expect(wrapper.exists()).toBe(true)

        // Test that RouterView is present
        expect(wrapper.findComponent({ name: 'RouterView' }).exists()).toBe(true)
    })

    it('shows user controls when authenticated', async () => {
        const pinia = createTestingPinia({
            createSpy: vi.fn,
            stubActions: false
        })

        const wrapper = mount(App, {
            global: {
                plugins: [pinia, router],
                stubs: {
                    RouterView: true
                }
            }
        })

        // Get the auth store and set authenticated state
        const authStore = useAuthStore(pinia)
        authStore.user = { id: 1, username: 'testuser' }

        // Mock localStorage to simulate having a token
        vi.mocked(window.localStorage.getItem).mockReturnValue('fake-token')

        // Initialize the store to pick up the token from localStorage
        authStore.initialize()

        await wrapper.vm.$nextTick()

        // Should show user controls when authenticated
        expect(wrapper.find('.user-controls').exists()).toBe(true)
        expect(wrapper.text()).toContain('Welcome, testuser')
        expect(wrapper.find('.logout-button').exists()).toBe(true)
    })

    it('hides user controls when not authenticated', async () => {
        const pinia = createTestingPinia({
            createSpy: vi.fn,
            stubActions: false
        })

        const wrapper = mount(App, {
            global: {
                plugins: [pinia, router],
                stubs: {
                    RouterView: true
                }
            }
        })

        // Get the auth store and ensure it's not authenticated (default state)
        const authStore = useAuthStore(pinia)
        authStore.user = null

        // Mock localStorage to return null (no token)
        vi.mocked(window.localStorage.getItem).mockReturnValue(null)

        // Initialize the store to pick up the lack of token
        authStore.initialize()

        await wrapper.vm.$nextTick()

        // Should not show user controls when not authenticated
        expect(wrapper.find('.user-controls').exists()).toBe(false)
    })
})
