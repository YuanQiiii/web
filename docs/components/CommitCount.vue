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
            `https://api.github.com/repos/${owner}/${repo}/commits?per_page=1`
        )

        if (!response.ok) {
            throw new Error('Failed to fetch commits')
        }

        // 获取总提交数
        const linkHeader = response.headers.get('Link')
        const lastPageMatch = linkHeader?.match(/page=(\d+)>; rel="last"/)
        commitCount.value = lastPageMatch ? parseInt(lastPageMatch[1]) : 0

        // 获取最新提交信息
        const [latestCommit] = await response.json()
        if (latestCommit) {
            latestMessage.value = latestCommit.commit.message || 'No commit message'
        } else {
            latestMessage.value = 'No commits'
        }

    } catch (e) {
        error.value = e.message
        commitCount.value = 0
        latestMessage.value = ''
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
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
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
    transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.expanded .commit-icon {
    transform: rotate(180deg);
}

.control-content {
    padding: 16px;
    transform-origin: top;
    transform: scaleY(0);
    opacity: 0;
    transition:
        transform 0.4s cubic-bezier(0.4, 0, 0.2, 1),
        opacity 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.content-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    transform-origin: top;
    transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.expanded .control-content {
    transform: scaleY(1);
    opacity: 1;
}

/* 其他样式保持不变 */
.commit-item {
    width: 100%;
    margin-bottom: 16px;
    display: flex;
    flex-direction: column;
    align-items: center;
    color: #000;
    opacity: 0;
    transform: translateY(10px);
    transition:
        opacity 0.3s cubic-bezier(0.4, 0, 0.2, 1),
        transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.expanded .commit-item {
    opacity: 1;
    transform: translateY(0);
}

/* 为每个 commit-item 添加延迟动画 */
.expanded .commit-item:nth-child(1) {
    transition-delay: 0.1s;
}

.expanded .commit-item:nth-child(2) {
    transition-delay: 0.15s;
}

.expanded .commit-item:nth-child(3) {
    transition-delay: 0.2s;
}

/* 其他样式保持原样 */
</style>