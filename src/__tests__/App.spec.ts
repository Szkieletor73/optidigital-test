import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'
import { createRouter, createWebHistory } from 'vue-router'
import App from '../App.vue'

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
        const wrapper = mount(App, {
            global: {
                plugins: [
                    createTestingPinia({
                        createSpy: vi.fn,
                        initialState: {
                            auth: {
                                user: null,
                                token: null,
                                isLoading: false,
                                error: null
                            }
                        }
                    }),
                    router
                ],
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
        const wrapper = mount(App, {
            global: {
                plugins: [
                    createTestingPinia({
                        createSpy: vi.fn,
                        initialState: {
                            auth: {
                                user: { username: 'testuser' },
                                token: 'fake-token',
                                isLoading: false,
                                error: null
                            }
                        }
                    }),
                    router
                ],
                stubs: {
                    RouterView: true
                }
            }
        })

        await wrapper.vm.$nextTick()

        // Should show user controls when authenticated
        expect(wrapper.find('.user-controls').exists()).toBe(true)
        expect(wrapper.text()).toContain('Welcome, testuser')
        expect(wrapper.find('.logout-button').exists()).toBe(true)
    })

    it('hides user controls when not authenticated', async () => {
        const wrapper = mount(App, {
            global: {
                plugins: [
                    createTestingPinia({
                        createSpy: vi.fn,
                        initialState: {
                            auth: {
                                user: null,
                                token: null,
                                isLoading: false,
                                error: null
                            }
                        }
                    }),
                    router
                ],
                stubs: {
                    RouterView: true
                }
            }
        })

        await wrapper.vm.$nextTick()

        // Should not show user controls when not authenticated
        expect(wrapper.find('.user-controls').exists()).toBe(false)
    })
})
