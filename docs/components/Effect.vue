<script setup>
import { onMounted, onBeforeUnmount, ref, watch, reactive } from 'vue'

/*
初始化阶段：
- onMounted 中创建 canvas 元素并初始化
- 设置画布尺寸和缩放比例
- 初始化粒子系统
- 启动动画循环
动画循环：
- 清空画布
- 更新所有粒子位置
- 绘制粒子
- 计算和绘制连接线
- 性能检测
交互控制：
- 控制面板的显示/隐藏
- 参数调整(粒子数量、连接距离、连接概率)
- 性能监控和自动暂停
*/

/*
- 每帧都重新计算所有可能的连接
- 多重循环导致复杂度为 O(n²)
*/




const state = reactive({ showPanel: false })
let canvas = null
let ctx = null
let dpr = window.devicePixelRatio || 1
let particles = []
let connections = []
const particleCount = ref(50)
const distance = ref(100)
const maxDistanceSquared = ref(distance.value * distance.value)
const connectionProbability = ref(0.02)
const showPerformanceAlert = ref(false)
let bounds = {
  width: 0,
  height: 0
}

let lastFrameTime = 0
let frameTimeHistory = []
let isFirstFrame = true
const FRAME_HISTORY_LENGTH = 60
const FRAME_TIME_THRESHOLD = 1000 / 40
let isPausedByPerformance = false
let isResizing = false
let poorPerformanceCount = 0


function calculateDistance(p1, p2) {
  const dx = p1.x - p2.x
  const dy = p1.y - p2.y
  return dx * dx + dy * dy
}




class Particle {
  constructor() {
    this.x = Math.random() * bounds.width
    this.y = Math.random() * bounds.height
    this.vx = (Math.random() * 2 - 1) * 2
    this.vy = (Math.random() * 2 - 1) * 2
    this.radius = 2 * dpr
  }
  update() {
    this.x += this.vx
    this.y += this.vy
    if (this.x <= 0 || this.x >= bounds.width) {
      this.vx *= -1
      this.x = Math.max(0, Math.min(this.x, bounds.width))
    }
    if (this.y <= 0 || this.y >= bounds.height) {
      this.vy *= -1
      this.y = Math.max(0, Math.min(this.y, bounds.height))
    }
  }
  draw() {
    ctx.beginPath()
    ctx.arc(this.x, this.y, this.radius * dpr, 0, Math.PI * 2)
    ctx.strokeStyle = 'rgba(125, 125, 125, 0.8)'
    ctx.lineWidth = 2
    ctx.stroke()
  }
}
function initializeParticles() {
  particles = Array.from({ length: particleCount.value }, () => new Particle())
  connections = []
}
function updateParticles() {
  initializeParticles()
}
function updateConnections() {
  connections = []
}
function setupCanvas() {
  if (!canvas) return null;
  ctx = canvas.getContext('2d');
}
function updateBounds() {

  bounds.width = window.innerWidth
  bounds.height = window.innerHeight
  canvas.width = bounds.width * dpr
  canvas.height = bounds.height * dpr
  canvas.style.width = `${bounds.width}px`
  canvas.style.height = `${bounds.height}px`
  ctx.setTransform(1, 0, 0, 1, 0, 0)
  ctx.scale(dpr, dpr)
}
function debounce(func, wait) {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}
function getRandomColor() {
  const r = Math.floor(Math.random() * 256)
  const g = Math.floor(Math.random() * 256)
  const b = Math.floor(Math.random() * 256)
  const a = (Math.random() * 0.2 + 0.8).toFixed(2)
  return `rgba(${r}, ${g}, ${b}, ${a})`
}


function drawConnections() {
  for (let i = connections.length - 1; i >= 0; i--) {
    const connection = connections[i]
    const p1 = particles[connection.index1]
    const p2 = particles[connection.index2]
    const distanceSquared = calculateDistance(p1, p2)
    if (distanceSquared > maxDistanceSquared.value) {
      connections.splice(i, 1)
    }
  }
  for (let i = 0; i < particles.length; i++) {
    const p1 = particles[i]
    for (let j = i + 1; j < particles.length; j++) {
      const p2 = particles[j]
      const distanceSquared = calculateDistance(p1, p2)
      if (distanceSquared < maxDistanceSquared.value && Math.random() < connectionProbability.value) {
        const exists = connections.some(
          (conn) =>
            (conn.index1 === i && conn.index2 === j) ||
            (conn.index1 === j && conn.index2 === i)
        )
        if (!exists) {
          connections.push({ index1: i, index2: j, color: getRandomColor() })
        }
      }
    }
  }
  connections.forEach((connection) => {
    const p1 = particles[connection.index1]
    const p2 = particles[connection.index2]
    ctx.beginPath()
    ctx.moveTo(p1.x, p1.y)
    ctx.lineTo(p2.x, p2.y)
    ctx.strokeStyle = connection.color
    ctx.lineWidth = 0.4 * dpr
    ctx.stroke()
  })
}


let animationId
let isAnimating = false

const render = () => {
  ctx.clearRect(0, 0, canvas.width, canvas.height)
  particles.forEach(p => {
    p.update()
    p.draw()
  })
  drawConnections()
}

const checkPerformance = () => {
  const currentTime = performance.now()
  if (isFirstFrame) {
    lastFrameTime = currentTime
    isFirstFrame = false
    return
  }
  const frameTime = currentTime - lastFrameTime
  lastFrameTime = currentTime
  if (isResizing) {
    return
  }

  frameTimeHistory.push(frameTime)
  if (frameTimeHistory.length > FRAME_HISTORY_LENGTH) {
    frameTimeHistory.shift()
  }
  if (frameTimeHistory.length >= Math.min(30, FRAME_HISTORY_LENGTH)) {
    const recentFrames = frameTimeHistory.slice(-10)
    const averageFrameTime = recentFrames.reduce((a, b) => a + b, 0) / recentFrames.length


    if (averageFrameTime > FRAME_TIME_THRESHOLD) {
      poorPerformanceCount++
      if (poorPerformanceCount >= 3 && !isPausedByPerformance) {
        isPausedByPerformance = true
        showPerformanceAlert.value = true
        pauseAnimation()
      }
    } else {
      poorPerformanceCount = 0
    }
  }
}


const animate = () => {
  if (!isAnimating || !ctx) return

  checkPerformance()
  render()
  animationId = requestAnimationFrame(animate)
}




const resumeAnimation = () => {
  if (!isAnimating) {

    showPerformanceAlert.value = false
    isFirstFrame = true
    frameTimeHistory = []
    lastFrameTime = 0
    isPausedByPerformance = false

    isAnimating = true
    animate()
  }
}


watch(
  [particleCount, distance, connectionProbability],
  () => {
    if (isExpanded.value) {

      if (isPausedByPerformance) {
        isPausedByPerformance = false
        resumeAnimation()
      }
    }
  }
)
watch(distance, (newValue) => {
  maxDistanceSquared.value = newValue * newValue
})

const pauseAnimation = () => {
  isAnimating = false
  if (animationId) {
    cancelAnimationFrame(animationId)
    animationId = null
  }
}



const handleVisibilityChange = () => {
  if (document.hidden) {
    pauseAnimation()
  } else {
    resumeAnimation()
  }
}
const debouncedResize = debounce(() => {
  isResizing = true


  updateBounds()
  initializeParticles()


  setTimeout(() => {
    isResizing = false

    frameTimeHistory = []
    isFirstFrame = true
    poorPerformanceCount = 0


    if (isPausedByPerformance) {
      isPausedByPerformance = false
      resumeAnimation()
    }
  }, 500)
}, 100)
onMounted(() => {
  canvas = document.createElement('canvas')
  canvas.style.position = 'fixed'
  canvas.style.top = '0'
  canvas.style.left = '0'
  canvas.style.width = '100%'
  canvas.style.height = '100%'
  canvas.style.pointerEvents = 'none'
  canvas.style.zIndex = '0'
  document.body.appendChild(canvas)
  setupCanvas()
  updateBounds()
  initializeParticles()
  isAnimating = true
  animate()
  window.addEventListener('resize', () => {
    debouncedResize();
    resumeAnimation();
  });
  document.addEventListener('visibilitychange', () => {
    handleVisibilityChange();
    resumeAnimation();
  }
  )
}
)


onBeforeUnmount(() => {

  isAnimating = false
  if (animationId) {
    cancelAnimationFrame(animationId)
    animationId = null
  }
  window.removeEventListener('resize', () => {
    debouncedResize();
  })
  document.removeEventListener('visibilitychange', () => {
    handleVisibilityChange();
    resumeAnimation();
  })
  if (canvas && canvas.parentNode) {
    canvas.parentNode.removeChild(canvas)
  }
})

</script>
<template>
  <div class="effect-container">
    <div v-if="showPerformanceAlert" class="performance-alert">
      因性能不足而暂停动画，请调整参数
    </div>

    <div class="control-panel" :class="{ 'expanded': state.showPanel }">
      <div class="control-header" @click="state.showPanel = !state.showPanel">
        <span class="control-title">⚙️</span>
        <span class="control-toggle">{{ state.showPanel ? '−' : '+' }}</span>
      </div>
      <div class="control-content" v-if="state.showPanel">
        <div class="control-item">
          <label>
            粒子数量
            <input type="range" v-model.number="particleCount" @input="updateParticles" min="10" max="200" />
            <span class="value">{{ particleCount }}</span>
          </label>
        </div>
        <div class="control-item">
          <label>
            最大连接距离
            <input type="range" v-model.number="distance" @input="updateConnections" min="10" max="200" />
            <span class="value">{{ distance }}</span>
          </label>
        </div>
        <div class="control-item">
          <label>
            连接概率
            <input type="range" v-model.number="connectionProbability" @input="updateConnections" step="0.01" min="0"
              max="1" />
            <span class="value">{{ connectionProbability }}</span>
          </label>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.effect-container {
  position: relative;
  width: 100%;
  height: 100%;
}

.control-panel {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 36px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  overflow: hidden;
  z-index: 1000;
  transition: all 0.3s ease;
  cursor: pointer;
}

.control-panel:hover {
  background: rgba(255, 255, 255, 0.5);
}

.control-panel.expanded {
  width: 260px;
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
}

.control-header {
  height: 36px;
  width: 36px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.control-toggle {
  font-size: 18px;
  color: #333;
  transition: all 0.3s ease;
}

.control-toggle:hover {
  color: #000;
}

.expanded .control-toggle {
  transform: rotate(180deg);
}

.control-content {
  padding: 16px;
  opacity: 0;
  max-height: 0;
  transition: all 0.3s ease;
  overflow: hidden;
}

.expanded .control-content {
  opacity: 1;
  max-height: 500px;
}

.control-item {
  margin-bottom: 16px;
  color: #333;
}

.control-item:last-child {
  margin-bottom: 0;
}

.control-item label {
  display: flex;
  flex-direction: column;
  gap: 5px;
  font-weight: 500;
}

.control-item input[type="range"] {
  width: 100%;
  margin-bottom: 4px;
  accent-color: #007f1c;
}

.control-item .value {
  font-size: 12px;
  color: #333;
  font-weight: 500;
  transition: color 0.3s ease;
}

.control-item:hover .value {
  color: #000;
}
</style>