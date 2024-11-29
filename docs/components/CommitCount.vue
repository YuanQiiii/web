<!-- components/CommitCount.vue -->
<script setup>
import { ref, onMounted } from 'vue'

const commitCount = ref(0)
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
    try {
        const response = await fetch('https://api.github.com/repos/YuanQiiii/web/commits?per_page=1')
        const link = response.headers.get('link')
        if (link) {
            const match = link.match(/&page=(\d+)>; rel="last"/)
            if (match) {
                commitCount.value = parseInt(match[1])
            }
        }
    } catch (e) {
        error.value = e
    } finally {
        loading.value = false
    }
})
</script>

<template>
    <div class="commit-count">
        <span v-if="loading">Loading commits...</span>
        <span v-else-if="error">Failed to load commits</span>
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
    transition: opacity 0.3s ease;
}

.commit-count:hover {
    opacity: 0.8;
    background: rgba(0, 0, 0, 0.15);
}
</style>