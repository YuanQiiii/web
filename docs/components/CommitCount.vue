<!-- CommitCount.vue -->
<script setup>
import { ref, onMounted } from 'vue'

const showDetail = ref(false)
const commits = ref([])
const loading = ref(false)
const error = ref(null)
const commitCount = ref(0)
const latestMessage = ref('')

async function fetchCommits() {
    loading.value = true
    error.value = null

    try {
        const owner = 'YuanQiiii'
        const repo = 'web'
        const response = await fetch(
            `https://api.github.com/repos/${owner}/${repo}/commits`
        )

        if (!response.ok) {
            throw new Error('Failed to fetch commits')
        }

        const data = await response.json()
        commits.value = data.map(commit => ({
            message: commit.commit.message,
            date: new Date(commit.commit.author.date)
        }))

        commitCount.value = commits.value.length
        latestMessage.value = commits.value[0]?.message || 'No commits'
    } catch (e) {
        error.value = e.message
    } finally {
        loading.value = false
    }
}

onMounted(() => {
    fetchCommits()
})
</script>


<template>
    <div class="commit-panel" :class="{ 'expanded': showDetail, 'has-error': error }" @click="showDetail = !showDetail">
        <div class="commit-header">
            <span class="commit-icon">📝</span>
        </div>

        <div class="control-content" v-if="showDetail">
            <div class="content-wrapper">
                <div class="commit-item">
                    <label>Commits Count</label>
                    <span class="value">{{ commitCount }}</span>
                </div>

                <div class="commit-item">
                    <label>Latest Commit</label>
                    <span class="value message">{{ latestMessage }}</span>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.commit-panel {
    position: fixed;
    bottom: 20px;
    left: 20px;
    width: 36px;
    background: rgba(255, 255, 255, 0.3);
    border-radius: 8px;
    overflow: hidden;
    z-index: 1000;
    color: #000;
    transition: all 0.3s ease;
    cursor: pointer;
}

.commit-panel:hover {
    background: rgba(255, 255, 255, 0.5);
}

.commit-panel.expanded {
    width: 260px;
    background: rgba(255, 255, 255, 0.9);
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
}

.commit-header {
    height: 36px;
    width: 36px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.commit-icon {
    font-size: 18px;
    color: #333;
    transition: all 0.3s ease;
}

.control-content {
    padding: 16px;
    opacity: 0;
    max-height: 0;
    transition: all 0.3s ease;
    overflow: hidden;
}

.content-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
}

.expanded .control-content {
    opacity: 1;
    max-height: 500px;
}

.commit-item {
    width: 100%;
    margin-bottom: 16px;
    display: flex;
    flex-direction: column;
    align-items: center;
    color: #000;
}

.commit-item:last-child {
    margin-bottom: 0;
}

.commit-item label {
    font-weight: 600;
    /* 加粗标签 */
    font-size: 12px;
    color: #1a1a1a;
    text-shadow: 0 1px 0 rgba(255, 255, 255, 0.5);
    margin-bottom: 5px;
}

.value {
    text-align: center;
    font-size: 12px;
    color: #1a1a1a;
    font-weight: 400;
    transition: color 0.3s ease;
    width: 100%;
}

.message {
    max-width: 100%;
    word-break: break-word;
}

.commit-panel.has-error {
    background: linear-gradient(to right,
            rgba(255, 50, 50, 0.25),
            rgba(255, 80, 80, 0.35));
    border: 1px solid rgba(255, 0, 0, 0.4);
}

.error-message {
    color: #e60000;
    font-weight: 600;
    text-shadow: 0 1px 0 rgba(255, 255, 255, 0.3);
}

.error-icon {
    font-size: 1rem;
}
</style>