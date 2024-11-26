---
layout: home
hero:
  name: "Start Page"
  text: "Hello World!"
---

<script setup>
import { defineClientComponent } from 'vitepress'
import { onMounted, onUnmounted } from 'vue'

const MouseEffect = defineClientComponent(() => {
  return new Promise((resolve) => {
    resolve({
      mounted() {
        // 声明全局变量
        let mouseX = 0
        let mouseY = 0
        
        const canvas = document.createElement('canvas')
        canvas.style.position = 'fixed'
        canvas.style.top = '0'
        canvas.style.left = '0'
        canvas.style.pointerEvents = 'none'
        canvas.style.zIndex = '999999'
        
        document.body.appendChild(canvas)
        const ctx = canvas.getContext('2d')
        
        class Line {
          constructor() {
            this.reset()
          }
          
          reset() {
            this.x = Math.random() * canvas.width
            this.y = Math.random() * canvas.height
            this.length = 30 + Math.random() * 20
            this.angle = Math.random() * Math.PI * 2
            this.originX = this.x
            this.originY = this.y
            this.orbitRadius = Math.random() * 50
            this.orbitSpeed = (Math.random() - 0.5) * 0.02
            this.orbitAngle = Math.random() * Math.PI * 2
          }
          
          getEndPoints() {
            const startX = this.x + Math.cos(this.angle) * this.length / 2
            const startY = this.y + Math.sin(this.angle) * this.length / 2
            const endX = this.x - Math.cos(this.angle) * this.length / 2
            const endY = this.y - Math.sin(this.angle) * this.length / 2
            return { startX, startY, endX, endY }
          }
          
          update(mouseX, mouseY) {
            const dx = mouseX - this.x
            const dy = mouseY - this.y
            const distance = Math.sqrt(dx * dx + dy * dy)
            
            if (distance < 200) {
              // 修改引力计算,使其与距离成反比
              const force = Math.min(1, (1 - distance / 200) * 0.1)
              this.x += dx * force
              this.y += dy * force
              this.orbitAngle += this.orbitSpeed * force * 1
            } else {
              // 缓慢回到原始位置
              const dx = this.originX - this.x
              const dy = this.originY - this.y
              this.x += dx * 0.02
              this.y += dy * 0.02
              this.orbitAngle += this.orbitSpeed
            }
            
            // 公转运动
            this.x += Math.cos(this.orbitAngle) * this.orbitRadius * 0.2
            this.y += Math.sin(this.orbitAngle) * this.orbitRadius * 0.2
            
            // 随机运动
            // 使用正弦函数使运动更加平滑
            const time = Date.now() * 0.001
            this.x += Math.sin(time + this.orbitAngle) * 0.5
            this.y += Math.cos(time + this.orbitAngle) * 0.5
          }
          
          draw(ctx) {
            const { startX, startY, endX, endY } = this.getEndPoints()
            
            // 根据与鼠标的距离计算线条粗细
            const dx = mouseX - this.x
            const dy = mouseY - this.y
            const distance = Math.sqrt(dx * dx + dy * dy)
            const lineWidth = distance < 200 ? 
              1 + (1 - distance / 200) * 0.5 : 
              1
            
            // 绘制线条
            ctx.beginPath()
            ctx.moveTo(startX, startY)
            ctx.lineTo(endX, endY)
            ctx.strokeStyle = 'rgba(125, 125, 125, 0.5)'
            ctx.lineWidth = lineWidth
            ctx.stroke()
            
            // 绘制端点空心圆,大小也随距离变化
            const radius = distance < 200 ? 
              2 + (1 - distance / 200) * 3 : 
              2
              
            ctx.beginPath()
            ctx.arc(startX, startY, radius, 0, Math.PI * 2)
            ctx.strokeStyle = 'rgba(125, 125, 125, 0.8)'
            ctx.lineWidth = 1
            ctx.stroke()
            
            ctx.beginPath()
            ctx.arc(endX, endY, radius, 0, Math.PI * 2)
            ctx.stroke()
          }
        }
        
        // 初始化画布尺寸和鼠标位置
        function initCanvas() {
          canvas.width = window.innerWidth
          canvas.height = window.innerHeight
          mouseX = canvas.width / 2  // 默认鼠标X坐标在画布中心
          mouseY = canvas.height / 2 // 默认鼠标Y坐标在画布中心
        }

        // 检测设备类型和性能
        function getLineCount() {
          const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent)
          const isLowPerformance = window.innerWidth < 768 || isMobile
          return isLowPerformance ? 50 : 100
        }

        // 创建适量的线条
        const lineCount = getLineCount()
        const lines = Array.from({ length: lineCount }, () => new Line())
        
        // 更新 resize 函数
        function resize() {
          initCanvas()
          lines.forEach(line => line.reset())
        }
        
        window.addEventListener('resize', resize)
        resize()
        
        // 更新鼠标事件监听
        window.addEventListener('mousemove', e => {
          mouseX = e.clientX
          mouseY = e.clientY
        })
        
        function drawConnections() {
          for (let i = 0; i < lines.length; i++) {
            const line1 = lines[i]
            const ends1 = line1.getEndPoints()
            
            for (let j = i + 1; j < lines.length; j++) {
              const line2 = lines[j]
              const ends2 = line2.getEndPoints()
              
              const connections = [
                { x1: ends1.startX, y1: ends1.startY, x2: ends2.startX, y2: ends2.startY },
                { x1: ends1.startX, y1: ends1.startY, x2: ends2.endX, y2: ends2.endY },
                { x1: ends1.endX, y1: ends1.endY, x2: ends2.startX, y2: ends2.startY },
                { x1: ends1.endX, y1: ends1.endY, x2: ends2.endX, y2: ends2.endY }
              ]
              
              connections.forEach(({x1, y1, x2, y2}) => {
                const distance = Math.sqrt((x2-x1)**2 + (y2-y1)**2)
                if (distance < 100) {
                  // 调整连接线透明度计算
                  const alpha = Math.pow(1 - distance/50, 2) * 0.7
                  ctx.beginPath()
                  ctx.moveTo(x1, y1)
                  ctx.lineTo(x2, y2)
                  ctx.strokeStyle = `rgba(125, 125, 125, ${alpha})`
                  ctx.lineWidth = 0.5 + (1 - distance/50) * 0.3
                  ctx.stroke()
                }
              })
            }
          }
        }
        
        function animate() {
          ctx.clearRect(0, 0, canvas.width, canvas.height)
          
          lines.forEach(line => {
            line.update(mouseX, mouseY)
            line.draw(ctx)
          })
          
          drawConnections()
          
          requestAnimationFrame(animate)
        }
        
        animate()

        // 清理函数，组件卸载时移除画布
        onUnmounted(() => {
          document.body.removeChild(canvas)
        })
      }
    })
  })
})
</script>

<ClientOnly>
  <MouseEffect />
</ClientOnly>