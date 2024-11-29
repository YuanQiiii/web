<!-- EffectExtreme.vue -->
<script setup>
import { onMounted, onBeforeUnmount, reactive } from 'vue'

let canvas = null
let ctx = null
let offscreenCanvas = null
let offscreenCtx = null
const dpr = window.devicePixelRatio || 1

const state = reactive({
    isAnimating: false,
    particleCount: 300,       // 粒子数量
    particles: [],
    rotationX: 0,             // X 轴旋转角度
    rotationY: 0,             // Y 轴旋转角度
    rotationSpeedX: 0.005,    // X 轴旋转速度
    rotationSpeedY: 0.005,    // Y 轴旋转速度
    perspective: 800,         // 透视距离
    sphereRadius: 200,        // 球体半径
    centerX: 0,
    centerY: 0,
    showPanel: false,
})

const bounds = { width: 0, height: 0 }
function getRandomColor() {
    const r = Math.floor(Math.random() * 256)
    const g = Math.floor(Math.random() * 256)
    const b = Math.floor(Math.random() * 256)
    const a = (Math.random() * 0.5 + 0.5).toFixed(2) // 透明度在 0.5 到 1 之间
    return `rgba(${r}, ${g}, ${b}, ${a})`
}

class Particle {
    constructor() {
        // 球面坐标随机生成位置
        const theta = Math.random() * Math.PI * 2
        const phi = Math.acos(2 * Math.random() - 1)
        const r = state.sphereRadius * Math.pow(Math.random(), 1 / 3) // 使用立方根使分布更均匀

        // 3D 坐标
        this.x3d = r * Math.sin(phi) * Math.cos(theta)
        this.y3d = r * Math.sin(phi) * Math.sin(theta)
        this.z3d = r * Math.cos(phi)

        // 2D 投影坐标
        this.x = 0
        this.y = 0
        this.scale = 1
        this.alpha = 1
        this.radius = 2

        // 随机颜色
        this.color = getRandomColor()
    }

    project() {
        // 3D 旋转
        const cosX = Math.cos(state.rotationX)
        const sinX = Math.sin(state.rotationX)
        const cosY = Math.cos(state.rotationY)
        const sinY = Math.sin(state.rotationY)

        // 绕 X 轴旋转
        let y = this.y3d * cosX - this.z3d * sinX
        let z = this.y3d * sinX + this.z3d * cosX
        let x = this.x3d

        // 绕 Y 轴旋转
        let x2 = x * cosY - z * sinY
        let z2 = x * sinY + z * cosY

        // 投影到 2D 平面
        const scale = state.perspective / (state.perspective + z2)
        this.x = state.centerX + x2 * scale
        this.y = state.centerY + y * scale
        this.scale = scale
        this.alpha = scale
    }

    update() {
        this.project()
    }

    draw(ctx) {
        ctx.beginPath()
        ctx.arc(this.x, this.y, this.radius * this.scale, 0, Math.PI * 2)
        ctx.fillStyle = this.color
        ctx.fill()
    }
}

function initializeParticles() {
    state.particles = []
    for (let i = 0; i < state.particleCount; i++) {
        state.particles.push(new Particle())
    }
}

function setupCanvas() {
    ctx = canvas.getContext('2d')
    offscreenCanvas = document.createElement('canvas')
    offscreenCtx = offscreenCanvas.getContext('2d')
}

function updateBounds() {
    bounds.width = window.innerWidth
    bounds.height = window.innerHeight

    state.centerX = bounds.width / 2
    state.centerY = bounds.height / 2

    canvas.width = bounds.width * dpr
    canvas.height = bounds.height * dpr
    canvas.style.width = `${bounds.width}px`
    canvas.style.height = `${bounds.height}px`

    offscreenCanvas.width = canvas.width
    offscreenCanvas.height = canvas.height

    ctx.scale(dpr, dpr)
}

function render() {
    state.rotationX += state.rotationSpeedX
    state.rotationY += state.rotationSpeedY

    offscreenCtx.clearRect(0, 0, offscreenCanvas.width, offscreenCanvas.height)

    // 绘制粒子
    state.particles.forEach(particle => {
        particle.update()
    })

    // 根据 z 坐标排序，模拟深度效果
    state.particles.sort((a, b) => b.scale - a.scale)

    // 批量绘制
    state.particles.forEach(particle => {
        particle.draw(offscreenCtx)
    })

    ctx.clearRect(0, 0, canvas.width, canvas.height)
    ctx.drawImage(offscreenCanvas, 0, 0)
}

function animate() {
    if (!state.isAnimating) return
    render()
    requestAnimationFrame(animate)
}

onMounted(() => {
    canvas = document.createElement('canvas')
    Object.assign(canvas.style, {
        position: 'fixed',
        top: '0',
        left: '0',
        width: '100%',
        height: '100%',
        pointerEvents: 'none',
        zIndex: '0',
    })
    document.body.appendChild(canvas)

    setupCanvas()
    updateBounds()
    initializeParticles()
    state.isAnimating = true
    animate()

    window.addEventListener('resize', () => {
        updateBounds()
        initializeParticles()
    })
})

onBeforeUnmount(() => {
    state.isAnimating = false
    window.removeEventListener('resize', updateBounds)
    if (canvas && canvas.parentNode) canvas.parentNode.removeChild(canvas)
})
</script>

<template>
    <div class="effect-container">
        <!-- 控制面板 -->
        <div class="control-panel" :class="{ 'expanded': state.showPanel }">
            <div class="control-header" @click="state.showPanel = !state.showPanel">
                <span class="control-title">⚙️</span>
                <span class="control-toggle">{{ state.showPanel ? '−' : '+' }}</span>
            </div>

            <div class="control-content" v-if="state.showPanel">
                <div class="control-item">
                    <label>Particle Count</label>
                    <input type="range" v-model.number="state.particleCount" min="100" max="500"
                        @input="initializeParticles" />
                    <span class="value">{{ state.particleCount }}</span>
                </div>

                <div class="control-item">
                    <label>Rotation Speed X</label>
                    <input type="range" v-model.number="state.rotationSpeedX" min="-0.01" max="0.01" step="0.0005" />
                    <span class="value">{{ state.rotationSpeedX.toFixed(4) }}</span>
                </div>

                <div class="control-item">
                    <label>Rotation Speed Y</label>
                    <input type="range" v-model.number="state.rotationSpeedY" min="-0.01" max="0.01" step="0.0005" />
                    <span class="value">{{ state.rotationSpeedY.toFixed(4) }}</span>
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