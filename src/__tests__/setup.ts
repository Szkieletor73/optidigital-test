import { vi } from 'vitest'

// Mock localStorage for tests
const localStorageMock = {
    getItem: vi.fn(),
    setItem: vi.fn(),
    removeItem: vi.fn(),
    clear: vi.fn(),
    length: 0,
    key: vi.fn(),
}

Object.defineProperty(window, 'localStorage', {
    value: localStorageMock,
    writable: true,
})

// Mock sessionStorage as well
Object.defineProperty(window, 'sessionStorage', {
    value: localStorageMock,
    writable: true,
})

// Disable Vue DevTools in tests
Object.defineProperty(window, '__VUE_DEVTOOLS_GLOBAL_HOOK__', {
    value: {
        Vue: {},
        enabled: false,
        emit: vi.fn(),
        on: vi.fn(),
        once: vi.fn(),
        off: vi.fn(),
    },
    writable: true,
})

// Set NODE_ENV to test
process.env.NODE_ENV = 'test'