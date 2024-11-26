---
layout: home
hero:
  name: "Start Page"
  text: "Hello World!"
---

<script setup>
import { defineClientComponent } from 'vitepress'

const Effect = defineClientComponent(() => {
  return new Promise((resolve) => {
    resolve({
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
        resizeCanvas()

        window.addEventListener('resize', resizeCanvas)

        // 定义粒子类
        class Particle {
          constructor() {
            this.x = Math.random() * canvas.width
            this.y = Math.random() * canvas.height
            this.vx = (Math.random() - 0.5) * 1.5
            this.vy = (Math.random() - 0.5) * 1.5
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
            ctx.arc(this.x, this.y, 3, 0, Math.PI * 2)
            ctx.strokeStyle = 'rgba(125, 125, 125, 0.8)'
            ctx.lineWidth = 1
            ctx.stroke()
          }
        }

        // 创建粒子数组
        const particleCount = 100
        const particles = Array.from({ length: particleCount }, () => new Particle())

        // 定义连接概率和最大距离
        const connectionProbability = 0.05
        const maxDistance = 150 // 最大连接距离，根据需要调整

        // 存储当前连接的数组
        const connections = []

        // 生成随机颜色的函数
        function getRandomColor() {
          const r = Math.floor(Math.random() * 256)
          const g = Math.floor(Math.random() * 256)
          const b = Math.floor(Math.random() * 256)
          const a = (Math.random() * 0.5 + 0.5).toFixed(2) // 透明度在0.5到1之间
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
            ctx.lineWidth = 0.3
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

        // 调整 Canvas 尺寸
        function resizeCanvas() {
          canvas.width = window.innerWidth
          canvas.height = window.innerHeight
        }

        // 清理函数
        this.$once('hook:beforeDestroy', () => {
          window.removeEventListener('resize', resizeCanvas)
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