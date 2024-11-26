<script setup>
import { onMounted, onBeforeUnmount, h, ref } from 'vue'

// 声明全局变量
let canvas = null
let ctx = null
let dpr = window.devicePixelRatio || 1
let particles = []
let connections = []
let particleCount = 100
let maxDistance = 150
const connectionProbability = 0.05
let bounds = {
  width: 0,
  height: 0
}


// 定义粒子类
class Particle {
  constructor() {
    this.x = (Math.random() * 2 - 1) * canvas.width * 0.5 + canvas.width * 0.5
    this.y = (Math.random() * 2 - 1) * canvas.height * 0.5 + canvas.height * 0.5
    this.vx = (Math.random() - 0.5) * 3
    this.vy = (Math.random() - 0.5) * 3
    this.radius = 3
  }

  update() {
    this.x += this.vx
    this.y += this.vy

    // 使用最新的边界值进行反弹检测
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
// 粒子数组初始化函数
function initializeParticles() {
  particles = Array.from({ length: particleCount }, () => new Particle())
  connections.length = 0
}

// 定义设备设置函数
function determineDeviceSettings() {
  const width = window.innerWidth
  if (width < 768) {
    particleCount = 50
    maxDistance = 100
  } else {
    particleCount = 100
    maxDistance = 150
  }
}

//定义画布调整函数
function resizeCanvas() {
  const dimensions = setupHiDPICanvas()
  if (!dimensions) return

  const { width } = dimensions
  // 根据宽度调整设置
  if (width < 768) {
    particleCount = 50
    maxDistance = 100
  } else {
    particleCount = 100
    maxDistance = 200
  }

  // 重新初始化粒子
  initializeParticles()
}


// Canvas 初始化和设置
function setupHiDPICanvas() {
  if (!canvas) return null

  const rect = canvas.getBoundingClientRect()
  canvas.width = rect.width * dpr
  canvas.height = rect.height * dpr
  canvas.style.width = `${rect.width}px`
  canvas.style.height = `${rect.height}px`
  ctx = canvas.getContext('2d')
  ctx.scale(dpr, dpr)

  // 返回尺寸对象
  return {
    width: rect.width,
    height: rect.height
  }
}
// 更新边界
function updateBounds() {
  if (!canvas) return
  const rect = canvas.getBoundingClientRect()
  bounds.width = rect.width
  bounds.height = rect.height
}
// 添加防抖以优化性能
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

// 生成随机颜色的函数
function getRandomColor() {
  const r = Math.floor(Math.random() * 256)
  const g = Math.floor(Math.random() * 256)
  const b = Math.floor(Math.random() * 256)
  const a = (Math.random() * 0.2 + 0.8).toFixed(2) // 透明度在0.5到1之间 
  return `rgba(${r}, ${g}, ${b}, ${a})`
}

// 在 resizeCanvas 函数前定义 debouncedResize
const debouncedResize = debounce(() => {
  const dimensions = setupHiDPICanvas()
  if (!dimensions) return

  const { width } = dimensions
  // 根据宽度调整设置
  if (width < 768) {
    particleCount = 50
    maxDistance = 100
  } else {
    particleCount = 100
    maxDistance = 150
  }

  // 重新初始化粒子
  initializeParticles()
}, 250)
// 绘制连接线
function drawConnections() {
  // 清除不再连接的线
  for (let i = connections.length - 1; i >= 0; i--) {
    const connection = connections[i]
    const p1 = particles[connection.index1]
    const p2 = particles[connection.index2]
    const dx = p1.x - p2.x
    const dy = p1.y - p2.y
    const distance = Math.sqrt(dx * dx + dy * dy)
    if (distance > maxDistance) {
      connections.splice(i, 1) // 移除连接
    }
  }

  // 添加新的连接
  for (let i = 0; i < particles.length; i++) {
    const p1 = particles[i]
    for (let j = i + 1; j < particles.length; j++) {
      const p2 = particles[j]
      const dx = p1.x - p2.x
      const dy = p1.y - p2.y
      const distance = Math.sqrt(dx * dx + dy * dy)
      if (distance < maxDistance && Math.random() < connectionProbability) {
        // 检查是否已经存在连接
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

  // 绘制所有连接
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

// 动画函数
function animate() {
  ctx.clearRect(0, 0, canvas.width, canvas.height)
  particles.forEach(p => {
    p.update()
    p.draw()
  })
  drawConnections()
  requestAnimationFrame(animate)
}





// 生命周期钩子
onMounted(() => {
  // 创建 canvas
  canvas = document.createElement('canvas')
  canvas.style.position = 'fixed'
  canvas.style.top = '0'
  canvas.style.left = '0'
  canvas.style.width = '100%'
  canvas.style.height = '100%'
  canvas.style.pointerEvents = 'none'
  canvas.style.zIndex = '999999'
  // 添加到 body
  document.body.appendChild(canvas)
  // 初始化设置
  setupHiDPICanvas()
  // 更新边界
  updateBounds()
  // 添加事件监听器
  window.addEventListener('resize', debouncedResize)
  // 重新设置canvas
  resizeCanvas()
  // 动画开始
  animate()
})

onBeforeUnmount(() => {
  // 移除事件监听器
  window.removeEventListener('resize', debouncedResize)

  // 清理 canvas
  if (canvas && canvas.parentNode) {
    canvas.parentNode.removeChild(canvas)
  }
})
</script>




<template>
  <div class="effect-container"></div>
</template>

<style scoped>
.effect-container {
  width: 100%;
  height: 100%;
  position: relative;
}
</style>