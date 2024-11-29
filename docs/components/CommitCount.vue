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
        <span v-else>Total Commits: {{ commitCount }}</span>
    </div>
</template>

<style scoped>
.commit-count {
    position: fixed;
    left: 1rem;
    bottom: 1rem;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    background: rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(4px);
    font-size: 0.9rem;
    color: rgba(0, 0, 0, 0.7);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    z-index: 100;
    transition: all 0.3s ease;
    min-height: 2.5rem;
    display: flex;
    align-items: center;
}

.commit-count.has-error {
    background: rgba(255, 0, 0, 0.1);
    border: 1px solid rgba(255, 0, 0, 0.3);
}

.error-message {
    color: #ff4444;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.error-icon {
    font-size: 1rem;
}

.commit-count:hover {
    opacity: 0.8;
}
</style>