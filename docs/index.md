---
layout: home
hero:
  name: "Start Page"
  text: "Hello World!"
---

<script setup>
import { defineClientComponent } from 'vitepress'
import { onMounted, onBeforeUnmount, h } from 'vue'
let dpr = window.devicePixelRatio || 1

const Effect = defineClientComponent(() => {
  return new Promise((resolve) => {
    resolve({
      render() {
        return h('div') // 使用渲染函数替代 template
      },
      mounted() {
        // 创建并设置 Canvas
        const canvas = document.createElement('canvas')
        canvas.style.position = 'fixed'
        canvas.style.top = '0'
        canvas.style.left = '0'
        canvas.style.width = '100%'
        canvas.style.height = '100%'
        canvas.style.pointerEvents = 'none'
        canvas.style.zIndex = '999999'

        document.body.appendChild(canvas)
        const ctx = canvas.getContext('2d')
    
        // 设置高分辨率 canvas
        function setupHiDPICanvas(canvas) {
          const dpr = window.devicePixelRatio || 1
          const rect = canvas.getBoundingClientRect()
          
          // 设置 canvas 的实际像素尺寸
          canvas.width = rect.width * dpr
          canvas.height = rect.height * dpr
          
          // 设置 canvas 的 CSS 尺寸
          canvas.style.width = `${rect.width}px`
          canvas.style.height = `${rect.height}px`
          
          // 缩放绘图上下文以匹配像素比
          const ctx = canvas.getContext('2d')
          ctx.scale(dpr, dpr)
          
          return { width: rect.width, height: rect.height, dpr }
        }
    
        // 1. 首先定义 Particle 类
        class Particle {
          constructor() {
            this.x = Math.random() * canvas.width
            this.y = Math.random() * canvas.height
            this.vx = (Math.random() - 0.5) * 1.5
            this.vy = (Math.random() - 0.5) * 1.5
            this.radius = 3
          }
    
          update() {
            this.x += this.vx
            this.y += this.vy
    
            // 边界反弹
            if (this.x <= 0 || this.x >= canvas.width) this.vx *= -1
            if (this.y <= 0 || this.y >= canvas.height) this.vy *= -1
          }
    
          draw() {
            ctx.beginPath()
            ctx.arc(this.x, this.y, this.radius * dpr, 0, Math.PI * 2)
            ctx.strokeStyle = 'rgba(125, 125, 125, 0.8)'
            ctx.lineWidth = 2
            ctx.stroke()
          }
        }
    
        // 2. 然后声明变量
        let particleCount = 100
        let maxDistance = 150
        let particles = []
        const connections = []
    
        // 3. 定义设备设置函数
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
    
        // 4. 定义初始化函数
        function initializeParticles() {
          particles = Array.from({ length: particleCount }, () => new Particle())
          connections.length = 0
        }
    
        // 5. 定义画布调整函数
        function resizeCanvas() {
          const { width, height, dpr } = setupHiDPICanvas(canvas)
          determineDeviceSettings()
          initializeParticles()
        }
    
        // 6. 初始化
        resizeCanvas()
    
        // 定义连接概率
        const connectionProbability = 0.05
    
        // 生成随机颜色的函数
        function getRandomColor() {
          const r = Math.floor(Math.random() * 256)
          const g = Math.floor(Math.random() * 256)
          const b = Math.floor(Math.random() * 256)
          const a = (Math.random() * 0.2 + 0.8).toFixed(2) // 透明度在0.5到1之间 
          return `rgba(${r}, ${g}, ${b}, ${a})`
        }
    
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
    
        animate()
    
        // 处理窗口大小变化
        function handleResize() {
          resizeCanvas()
        }
    
        window.addEventListener('resize', handleResize)
    
        // 使用 onBeforeUnmount 替代 this.$once
        onBeforeUnmount(() => {
          window.removeEventListener('resize', handleResize)
          document.body.removeChild(canvas)
        })
      }
    })
  })
})
</script>

<ClientOnly>
  <Effect/>
</ClientOnly>