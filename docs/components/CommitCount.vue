<!-- components/CommitCount.vue -->
<script setup>
import { ref, onMounted } from 'vue'

const commitCount = ref(0)
const loading = ref(true)
const error = ref(null)
const errorMessage = ref('')

onMounted(async () => {
    try {
        const response = await fetch('https://api.github.com/repos/YuanQiiii/web/commits?per_page=1')
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`)
        }
        const link = response.headers.get('link')
        if (!link) {
            throw new Error('No pagination info found')
        }

        const match = link.match(/&page=(\d+)>; rel="last"/)
        if (!match) {
            throw new Error('Could not parse commit count')
        }

        commitCount.value = parseInt(match[1])
    } catch (e) {
        error.value = true
        errorMessage.value = e.message || 'Failed to fetch commit count'
        console.error('Error fetching commits:', e)
    } finally {
        loading.value = false
    }
})
</script>

<template>
    <div class="commit-count" :class="{ 'has-error': error }">
        <span v-if="loading">Loading commits...</span>
        <span v-else-if="error" class="error-message">
            <span class="error-icon">⚠️</span>
            {{ errorMessage }}
        </span>
        <span v-else>Commits: {{ commitCount }}</span>
    </div>
</template>

<style scoped>
.commit-count {
    position: fixed;
    left: 0.75rem;
    bottom: 0.75rem;
    padding: 0.35rem 0.75rem;
    border-radius: 3px;
    background: linear-gradient(to right,
            rgba(255, 255, 255, 0.25),
            rgba(255, 255, 255, 0.35));
    backdrop-filter: blur(8px);
    font-size: 0.85rem;
    color: rgba(0, 0, 0, 0.85);
    box-shadow:
        0 2px 8px rgba(0, 0, 0, 0.12),
        inset 0 0 16px rgba(255, 255, 255, 0.2);
    z-index: 100;
    transition: all 0.3s ease;
    min-height: 2rem;
    display: flex;
    align-items: center;
    text-shadow: 0 1px 1px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.3);
}

.commit-count.has-error {
    background: linear-gradient(to right,
            rgba(255, 50, 50, 0.25),
            rgba(255, 80, 80, 0.35));
    border: 1px solid rgba(255, 0, 0, 0.4);
    text-shadow: 0 1px 1px rgba(255, 0, 0, 0.1);
}

.error-message {
    color: #ff2222;
    font-weight: bold;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}

.error-icon {
    font-size: 1rem;
    text-shadow: 0 0 3px rgba(255, 0, 0, 0.3);
}

.commit-count:hover {
    opacity: 0.95;
    transform: translateY(-1px);
    box-shadow:
        0 4px 12px rgba(0, 0, 0, 0.15),
        inset 0 0 20px rgba(255, 255, 255, 0.25);
}
</style>