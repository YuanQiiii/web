<script setup>
import { onMounted, onBeforeUnmount, ref, watch } from 'vue'
// 渲染相关变量
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
// 控制栏相关变量
const controls = ref(null)
const isExpanded = ref(false)
let collapseTimeout = null
// 性能监控变量,初始化标志
let lastFrameTime = 0
let frameTimeHistory = []
let isFirstFrame = true
const FRAME_HISTORY_LENGTH = 60
const FRAME_TIME_THRESHOLD = 1000 / 50
let isPausedByPerformance = false


function calculateDistance(p1, p2) {
  const dx = p1.x - p2.x
  const dy = p1.y - p2.y
  return dx * dx + dy * dy // 返回距离平方
}
// 显示控制栏
const showControls = () => {
  isExpanded.value = true
  clearCollapseTimer()
}
// 开始收起计时器
const startCollapseTimer = () => {
  clearCollapseTimer()
  collapseTimeout = setTimeout(() => {
    isExpanded.value = false
  }, 500) // 调整后0.5秒后自动收起
}
// 清除收起计时器
const clearCollapseTimer = () => {
  if (collapseTimeout) {
    clearTimeout(collapseTimeout)
    collapseTimeout = null
  }
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
  ctx.setTransform(1, 0, 0, 1, 0, 0) // 重置变换矩阵
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

const debouncedResize = debounce(() => {
  updateBounds()
  initializeParticles()
}, 250)
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

// 使用 requestAnimationFrame 的回调函数优化
let animationId
let isAnimating = false


const render = () => {
  // 渲染逻辑
  // 清空画布
  ctx.clearRect(0, 0, canvas.width, canvas.height)
  // 绘制粒子
  particles.forEach(p => {
    p.update()
    p.draw()
  })
  // 绘制连接
  drawConnections()
}





// 2. 修改性能检测函数
const checkPerformance = () => {
  const currentTime = performance.now()

  if (isFirstFrame) {
    lastFrameTime = currentTime
    isFirstFrame = false
    return
  }

  const frameTime = currentTime - lastFrameTime
  lastFrameTime = currentTime

  frameTimeHistory.push(frameTime)
  if (frameTimeHistory.length > FRAME_HISTORY_LENGTH) {
    frameTimeHistory.shift()
  }

  // 增加缓冲期，收集足够的新数据再进行判断
  if (frameTimeHistory.length >= Math.min(10, FRAME_HISTORY_LENGTH)) {
    // 只使用最近的帧数据计算平均值
    const recentFrames = frameTimeHistory.slice(-10)
    const averageFrameTime = recentFrames.reduce((a, b) => a + b, 0) / recentFrames.length

    if (averageFrameTime > FRAME_TIME_THRESHOLD && !isPausedByPerformance) {
      isPausedByPerformance = true
      showPerformanceAlert.value = true // 显示提示
      pauseAnimation()
    }
  }
}

// 3. 在动画循环中添加性能检测

// 动画循环主函数
const animate = () => {
  if (!isAnimating || !ctx) return
  // 添加性能检测
  checkPerformance()
  render()
  animationId = requestAnimationFrame(animate)
}


function resetCollapseTimer() {
  clearTimeout(collapseTimeout)
  collapseTimeout = setTimeout(() => {
    isExpanded.value = false
  }, 500)
}

const resumeAnimation = () => {
  if (!isAnimating) {
    // 重置所有性能检测相关状态
    showPerformanceAlert.value = false // 隐藏提示
    isFirstFrame = true
    frameTimeHistory = []
    lastFrameTime = 0
    isPausedByPerformance = false
    // 启动动画
    isAnimating = true
    animate()
  }
}

// 监听用户操作，重置自动收缩定时器
watch(
  [particleCount, distance, connectionProbability],
  () => {
    if (isExpanded.value) {
      resetCollapseTimer()
      // 如果是因性能问题暂停的，则尝试恢复动画
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


// 页面不可见时暂停,可见时恢复
const handleVisibilityChange = () => {
  if (document.hidden) {
    pauseAnimation()
  } else {
    resumeAnimation()
  }
}

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
  window.addEventListener('resize', debouncedResize, resumeAnimation)
  isAnimating = true
  animate()
  document.addEventListener('visibilitychange', handleVisibilityChange)
  checkPerformance()
})


onBeforeUnmount(() => {
  // 清理时要记得取消
  isAnimating = false
  if (animationId) {
    cancelAnimationFrame(animationId)
    animationId = null
  }
  clearCollapseTimer()
  window.removeEventListener('resize', debouncedResize)
  document.removeEventListener('visibilitychange', handleVisibilityChange)
  if (canvas && canvas.parentNode) {
    canvas.parentNode.removeChild(canvas)
  }
})

</script>

<template>
  <div class="effect-container">
    <!-- 添加提示组件 -->
    <div v-if="showPerformanceAlert" class="performance-alert">
      因性能不足而暂停动画，请调整参数
    </div>
    <!-- 悬浮窗 -->
    <div class="floating-btn" :class="{ 'hidden': isExpanded }" @click="showControls">
      <span class="icon">⚙️</span>
    </div>

    <!-- 控制栏 -->
    <div ref="controls" class="controls-panel" :class="{ 'expanded': isExpanded }" @mouseleave="startCollapseTimer"
      @mouseenter="clearCollapseTimer">
      <div class="controls-content">
        <!-- 控制栏内容保持不变 -->
        <label>
          粒子数量: {{ particleCount }}
          <input type="range" v-model.number="particleCount" @input="updateParticles" min="10" max="200" />
        </label>
        <label>
          最大连接距离:{{ distance }}
          <input type="range" v-model.number="distance" @input="updateConnections" min="10" max="200" />
        </label>
        <label>
          连接概率:{{ connectionProbability }}
          <input type="range" v-model.number="connectionProbability" @input="updateConnections" step="0.01" min="0"
            max="1" />
        </label>
      </div>
    </div>
  </div>
</template>

<style scoped>
.effect-container {
  position: relative;
}

.floating-btn {
  position: fixed;
  right: 20px;
  top: 90%;
  transform: translateY(-50%);
  z-index: 1000;
  cursor: pointer;
  background: rgba(255, 255, 255, 0.2);
  padding: 10px;
  border-radius: 50%;
  transition: opacity 0.3s ease;
}

.floating-btn.hidden {
  opacity: 0;
  pointer-events: none;
}

.performance-alert {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  /* 更强的背景色和不透明度 */
  background: linear-gradient(to right,
      rgba(255, 50, 50, 0.25),
      rgba(255, 80, 80, 0.3));
  /* 加深文字颜色并添加文字阴影 */
  color: #ff1111;
  text-shadow: 0 0 2px rgba(255, 0, 0, 0.3);
  padding: 10px 20px;
  /* 增强投影效果 */
  box-shadow:
    0 2px 8px rgba(255, 0, 0, 0.25),
    inset 0 0 15px rgba(255, 0, 0, 0.1);
  border-radius: 4px;
  /* 更醒目的边框 */
  border: 2px solid rgba(255, 51, 51, 0.8);
  z-index: 1000;
  font-size: 14px;
  font-weight: bold;
  pointer-events: none;
  transition: all 0.3s ease;
  /* 增强微光动画效果 */
  animation: glow 2s infinite;
  /* 添加磨砂玻璃效果 */
  backdrop-filter: blur(2px);
}

@keyframes glow {
  0% {
    box-shadow: 0 0 5px rgba(255, 0, 0, 0.3), inset 0 0 15px rgba(255, 0, 0, 0.1);
  }

  50% {
    box-shadow: 0 0 20px rgba(255, 0, 0, 0.5), inset 0 0 25px rgba(255, 0, 0, 0.2);
  }

  100% {
    box-shadow: 0 0 5px rgba(255, 0, 0, 0.3), inset 0 0 15px rgba(255, 0, 0, 0.1);
  }
}

.controls-panel {
  position: fixed;
  right: -280px;
  /* 控制栏初始位置在屏幕外 */
  top: 50%;
  transform: translateY(-50%);
  width: 250px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  padding: 20px;
  border-radius: 10px;
  transition: right 0.3s ease;
  z-index: 100000;
}

.controls-panel.expanded {
  right: 20px;
}

.controls-content {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.controls-content label {
  display: flex;
  flex-direction: column;
  gap: 5px;
  color: rgba(0, 127, 28, 0.863);
}

input[type="range"] {
  width: 100%;
}
</style>