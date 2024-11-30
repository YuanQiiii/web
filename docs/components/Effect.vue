<!-- Effect.vue -->
<script setup>
import { onMounted, onBeforeUnmount, reactive } from 'vue'

/* 集中状态管理 */
const state = reactive({
  canvas: null,
  ctx: null,
  offscreenCanvas: null,
  offscreenCtx: null,
  dpr: window.devicePixelRatio || 1,
  particles: [],
  grid: {},
  gridSize: 100, // 网格大小，可根据需要调整
  particleCount: 50,
  maxDistance: 100,
  connectionProbability: 0.02,
  bounds: {
    width: 0,
    height: 0
  },
  isAnimating: false,
  animationId: null,
  showPanel: false,
  connectionColors: new Map(), // 存储连接的颜色
})


/* 粒子类 */
class Particle {
  constructor() {
    this.x = Math.random() * state.bounds.width
    this.y = Math.random() * state.bounds.height
    this.vx = (Math.random() * 2 - 1) * 2
    this.vy = (Math.random() * 2 - 1) * 2
    this.radius = 3 * state.dpr
  }

  update() {
    this.x += this.vx
    this.y += this.vy

    if (this.x <= 0 || this.x >= state.bounds.width) {
      this.vx *= -1
      this.x = Math.max(0, Math.min(this.x, state.bounds.width))
    }
    if (this.y <= 0 || this.y >= state.bounds.height) {
      this.vy *= -1
      this.y = Math.max(0, Math.min(this.y, state.bounds.height))
    }
  }

  draw(ctx) {
    // 修复：使用传入的 ctx 而不是 state.ctx
    ctx.beginPath()
    ctx.arc(this.x, this.y, this.radius * state.dpr, 0, Math.PI * 2)
    ctx.strokeStyle = 'rgba(128, 128, 192, 0.7)'  // 边框颜色
    ctx.lineWidth = 1 * state.dpr  // 调整边框宽度
    ctx.stroke()  // 绘制边框
    // 不使用 fill() 方法，保持空心效果
  }
}

/* 初始化粒子 */
function initializeParticles() {
  state.particles = []
  for (let i = 0; i < state.particleCount; i++) {
    state.particles.push(new Particle())
  }
}

/* 初始化网格 */
function initializeGrid() {
  state.grid = {}
  const cols = Math.ceil(state.bounds.width / state.gridSize)
  const rows = Math.ceil(state.bounds.height / state.gridSize)
  for (let i = 0; i <= cols; i++) {
    state.grid[i] = {}
    for (let j = 0; j <= rows; j++) {
      state.grid[i][j] = []
    }
  }
}

/* 更新粒子数量 */
function updateParticles() {
  resetState()
}

/* 更新网格 */
function updateGrid() {
  initializeGrid()
  state.particles.forEach(particle => {
    const col = Math.floor(particle.x / state.gridSize)
    const row = Math.floor(particle.y / state.gridSize)
    state.grid[col][row].push(particle)
  })
}

/* 获取相邻网格中的粒子 */
function getNeighbors(col, row) {
  const neighbors = []
  for (let i = col - 1; i <= col + 1; i++) {
    for (let j = row - 1; j <= row + 1; j++) {
      if (state.grid[i] && state.grid[i][j]) {
        neighbors.push(...state.grid[i][j])
      }
    }
  }
  return neighbors
}

function getConnectionId(p1, p2) {
  // 确保相同的两个粒子生成相同的ID
  const id1 = state.particles.indexOf(p1)
  const id2 = state.particles.indexOf(p2)
  return id1 < id2 ? `${id1}-${id2}` : `${id2}-${id1}`
}


/* 绘制粒子和连接 */
// 修改 render 函数中的连接线绘制部分
function render() {
  // 清空离屏画布
  state.offscreenCtx.clearRect(0, 0, state.bounds.width, state.bounds.height)

  // 更新所有粒子
  state.particles.forEach(particle => {
    particle.update()
  })

  // 更新网格
  updateGrid()

  // 批量绘制连接线

  const newConnections = []
  const maxDistanceSquared = state.maxDistance ** 2
  state.offscreenCtx.lineWidth = 0.2 * state.dpr

  // 遍历网格检查连接
  for (let col in state.grid) {
    for (let row in state.grid[col]) {
      const cellParticles = state.grid[col][row]
      if (cellParticles.length > 0) {
        const neighbors = getNeighbors(parseInt(col), parseInt(row))
        cellParticles.forEach(particle => {
          neighbors.forEach(other => {
            if (particle !== other) {
              const dx = particle.x - other.x
              const dy = particle.y - other.y
              const distanceSquared = dx * dx + dy * dy

              if (distanceSquared < maxDistanceSquared) {
                const connectionId = getConnectionId(particle, other)

                // 使用缓存的颜色或生成新颜色
                if (!state.connectionColors.has(connectionId) && Math.random() < state.connectionProbability) {
                  state.connectionColors.set(connectionId, getRandomColor())
                }

                if (state.connectionColors.has(connectionId)) {
                  newConnections.push({
                    id: connectionId,
                    x1: particle.x,
                    y1: particle.y,
                    x2: other.x,
                    y2: other.y,
                    distance: Math.sqrt(distanceSquared)
                  })
                }
              }
            }
          })
        })
      }
    }
  }

  // 清理断开的连接
  for (const [id, _] of state.connectionColors) {
    if (!newConnections.some(conn => conn.id === id)) {
      state.connectionColors.delete(id)
    }
  }

  // 绘制连接线
  newConnections.forEach(conn => {
    const alpha = Math.max(0, 1 - conn.distance / state.maxDistance)
    state.offscreenCtx.beginPath()
    state.offscreenCtx.strokeStyle = state.connectionColors.get(conn.id)
    state.offscreenCtx.moveTo(conn.x1, conn.y1)
    state.offscreenCtx.lineTo(conn.x2, conn.y2)
    state.offscreenCtx.stroke()
  })

  // 批量绘制粒子
  state.particles.forEach(particle => {
    particle.draw(state.offscreenCtx)
  })

  // 一次性将离屏画布内容复制到主画布
  state.ctx.clearRect(0, 0, state.bounds.width, state.bounds.height)
  state.ctx.drawImage(state.offscreenCanvas, 0, 0)
}

/* 获取随机颜色 */
function getRandomColor() {
  const r = Math.floor(Math.random() * 256)
  const g = Math.floor(Math.random() * 256)
  const b = Math.floor(Math.random() * 256)
  const o = Math.floor(Math.random() * 256)
  return `rgba(${r}, ${g}, ${b}, ${o})`
}

/* 动画循环 */
function animate() {
  if (!state.isAnimating) return
  render()
  state.animationId = requestAnimationFrame(animate)
}

/* 设置画布 */
function setupCanvas() {
  if (!state.canvas) return
  state.ctx = state.canvas.getContext('2d')
  state.bounds.width = window.innerWidth
  state.bounds.height = window.innerHeight
  state.canvas.width = state.bounds.width * state.dpr
  state.canvas.height = state.bounds.height * state.dpr
  state.canvas.style.width = `${state.bounds.width}px`
  state.canvas.style.height = `${state.bounds.height}px`
  state.ctx.scale(state.dpr, state.dpr)

  // 设置离屏画布
  state.offscreenCanvas = document.createElement('canvas')
  state.offscreenCtx = state.offscreenCanvas.getContext('2d')
  state.offscreenCanvas.width = state.bounds.width
  state.offscreenCanvas.height = state.bounds.height
}


/* 事件处理 */
function handleResize() {
  setupCanvas()
  resetState()
}

function handleVisibilityChange() {
  if (document.hidden) {
    pauseAnimation()
  } else {
    startAnimation()
  }
}

/* 启动动画 */
function startAnimation() {
  if (!state.isAnimating) {
    state.isAnimating = true
    animate()
  }
}

/* 暂停动画 */
function pauseAnimation() {
  state.isAnimating = false
  if (state.animationId) {
    cancelAnimationFrame(state.animationId)
    state.animationId = null
  }
}

/* 重置状态 */
function resetState() {
  initializeParticles()
  initializeGrid()
  // 重置状态时清理连接缓存
  state.connectionColors.clear()
}

/* 初始加载 */
onMounted(() => {
  // 创建 canvas
  state.canvas = document.createElement('canvas')
  state.canvas.style.position = 'fixed'
  state.canvas.style.top = '0'
  state.canvas.style.left = '0'
  state.canvas.style.width = '100%'
  state.canvas.style.height = '100%'
  state.canvas.style.pointerEvents = 'none'
  state.canvas.style.zIndex = '0'
  document.body.appendChild(state.canvas)

  // 设置画布和粒子
  setupCanvas()
  resetState()

  // 启动动画
  startAnimation()

  // 事件绑定
  window.addEventListener('resize', handleResize)
  document.addEventListener('visibilitychange', handleVisibilityChange)
})

/* 组件销毁 */
onBeforeUnmount(() => {
  // 事件解绑
  window.removeEventListener('resize', handleResize)
  document.removeEventListener('visibilitychange', handleVisibilityChange)

  // 停止动画
  pauseAnimation()

  // 移除 canvas
  if (state.canvas && state.canvas.parentNode) {
    state.canvas.parentNode.removeChild(state.canvas)
  }
})
</script>

<template>
  <div class="effect-container">
    <div class="control-panel" :class="{ 'expanded': state.showPanel }">
      <div class="control-header" @click="state.showPanel = !state.showPanel">
        <span class="control-title">⚙️</span>

      </div>

      <div class="control-content" v-if="state.showPanel">
        <div class="control-item">
          <label>Particle Count</label>
          <input type="range" v-model.number="state.particleCount" min="10" max="200" @input="updateParticles" />
          <span class="value">{{ state.particleCount }}</span>

        </div>

        <div class="control-item">
          <label>Max Distance</label>
          <input type="range" v-model.number="state.maxDistance" min="50" max="300" @input="updateConnections" />
          <span class="value">{{ state.maxDistance }}</span>

        </div>

        <div class="control-item">
          <label>Connection Probability</label>
          <input type="range" v-model.number="state.connectionProbability" step="0.01" min="0" max="1"
            @input="updateConnections" />
          <span class="value">{{ state.connectionProbability.toFixed(2) }}</span>
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
  /* 加深图标颜色 */
  transition: all 0.3s ease;
}

.control-toggle:hover {
  color: #000;
  /* 悬停时更深 */
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
  /* 加深文字颜色 */
}

.control-item:last-child {
  margin-bottom: 0;
}

.control-item label {
  display: flex;
  flex-direction: column;
  gap: 5px;
  font-weight: 500;
  font-size: 12px;
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
  /* 悬停时更深 */
}
</style>
