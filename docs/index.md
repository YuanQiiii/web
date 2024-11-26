---
layout: home
hero:
  name: "Start Page"
  text: "Hello World!"
---

<script setup>
import { defineClientComponent } from 'vitepress'

const MouseEffect = defineClientComponent(() => {
  return new Promise((resolve) => {
    resolve({
      mounted() {
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
              const force = (1 - distance / 200) * 0.2
              this.x += dx * force
              this.y += dy * force
              this.orbitAngle += this.orbitSpeed * 2
            } else {
              const dx = this.originX - this.x
              const dy = this.originY - this.y
              this.x += dx * 0.05
              this.y += dy * 0.05
              this.orbitAngle += this.orbitSpeed
            }
            
            // 公转运动
            this.x += Math.cos(this.orbitAngle) * this.orbitRadius * 0.1
            this.y += Math.sin(this.orbitAngle) * this.orbitRadius * 0.1
            
            // 随机运动
            this.x += (Math.random() - 0.5) * 4
            this.y += (Math.random() - 0.5) * 4
          }
          
          draw(ctx) {
            const { startX, startY, endX, endY } = this.getEndPoints()
            
            // 绘制线条
            ctx.beginPath()
            ctx.moveTo(startX, startY)
            ctx.lineTo(endX, endY)
            ctx.strokeStyle = 'rgba(125, 125, 125, 0.5)'
            ctx.lineWidth = 1
            ctx.stroke()
            
            // 绘制端点空心圆
            ctx.beginPath()
            ctx.arc(startX, startY, 3, 0, Math.PI * 2)
            ctx.strokeStyle = 'rgba(125, 125, 125, 0.8)'
            ctx.lineWidth = 1
            ctx.stroke()
            
            ctx.beginPath()
            ctx.arc(endX, endY, 3, 0, Math.PI * 2)
            ctx.stroke()
          }
        }
        
        const lines = Array.from({ length: 200 }, () => new Line())
        let mouseX = 0, mouseY = 0
        
        function resize() {
          canvas.width = window.innerWidth
          canvas.height = window.innerHeight
          lines.forEach(line => line.reset())
        }
        
        window.addEventListener('resize', resize)
        resize()
        
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
                if (distance < 50) {
                  const alpha = (1 - distance/50) * 0.3
                  ctx.beginPath()
                  ctx.moveTo(x1, y1)
                  ctx.lineTo(x2, y2)
                  ctx.strokeStyle = `rgba(125, 125, 125, ${alpha})`
                  ctx.lineWidth = 1
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
      }
    })
  })
})
</script>

<MouseEffect />