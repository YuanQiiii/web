<script setup>
import { onMounted, onBeforeUnmount, ref, watch } from 'vue'

let canvas = null
let ctx = null
let dpr = window.devicePixelRatio || 1
let particles = []
let connections = []
const particleCount = ref(50)
const maxDistance = ref(100)
const connectionProbability = ref(0.02)
let bounds = {
  width: 0,
  height: 0
}
const controls = ref(null)
const isExpanded = ref(false)
let collapseTimeout = null


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
  }, 2000) // 3秒后自动收起
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
function setupHiDPICanvas() {
  if (!canvas) return null
  const rect = canvas.getBoundingClientRect()
  canvas.width = rect.width * dpr
  canvas.height = rect.height * dpr
  canvas.style.width = `${rect.width}px`
  canvas.style.height = `${rect.height}px`
  ctx = canvas.getContext('2d')
  ctx.scale(dpr, dpr)
  return {
    width: rect.width,
    height: rect.height
  }
}
function updateBounds() {
  bounds.width = window.innerWidth
  bounds.height = window.innerHeight
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
    const dx = p1.x - p2.x
    const dy = p1.y - p2.y
    const distance = Math.hypot(dx, dy)
    if (distance > maxDistance.value) {
      connections.splice(i, 1)
    }
  }
  for (let i = 0; i < particles.length; i++) {
    const p1 = particles[i]
    for (let j = i + 1; j < particles.length; j++) {
      const p2 = particles[j]
      const dx = p1.x - p2.x
      const dy = p1.y - p2.y
      const distance = Math.hypot(dx, dy)
      if (distance < maxDistance.value && Math.random() < connectionProbability.value) {
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

function animate() {
  ctx.clearRect(0, 0, canvas.width, canvas.height)
  particles.forEach(p => {
    p.update()
    p.draw()
  })
  drawConnections()
  requestAnimationFrame(animate)
}
function resetCollapseTimer() {
  clearTimeout(collapseTimeout)
  collapseTimeout = setTimeout(() => {
    isExpanded.value = false
  }, 2000)
}

// 监听用户操作，重置自动收缩定时器
watch(
  [particleCount, maxDistance, connectionProbability],
  () => {
    if (isExpanded.value) {
      resetCollapseTimer()
    }
  }
)

onMounted(() => {
  canvas = document.createElement('canvas')
  canvas.style.position = 'fixed'
  canvas.style.top = '0'
  canvas.style.left = '0'
  canvas.style.width = '100%'
  canvas.style.height = '100%'
  canvas.style.pointerEvents = 'none'
  canvas.style.zIndex = '999'
  document.body.appendChild(canvas)
  setupHiDPICanvas()
  updateBounds()
  initializeParticles()
  window.addEventListener('resize', debouncedResize)
  debouncedResize()
  animate()
})

onBeforeUnmount(() => {
  clearCollapseTimer()
  window.removeEventListener('resize', debouncedResize)
  if (canvas && canvas.parentNode) {
    canvas.parentNode.removeChild(canvas)
  }
})

</script>

<template>
  <div class="effect-container">
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
          最大连接距离:{{ maxDistance }}
          <input type="range" v-model.number="maxDistance" @input="updateConnections" min="10" max="300" />
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
  top: 50%;
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