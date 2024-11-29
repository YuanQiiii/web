<!-- components/EffectSelector.vue -->
<template>
    <div>
        <!-- 切换开关 -->
        <div class="effect-selector">
            <div class="toggle-switch" @click="toggleEffect">
                <div class="switch-handle" :class="{ 'active': selectedEffect === 'EffectExtreme' }"></div>
            </div>
        </div>

        <!-- 组件渲染区域 -->
        <component :is="selectedComponent" />
    </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import Effect from './Effect.vue'
import EffectExtreme from './Effect_extreme.vue'

const selectedEffect = ref('Effect')

const toggleEffect = () => {
    selectedEffect.value = selectedEffect.value === 'Effect' ? 'EffectExtreme' : 'Effect'
}

const componentsMap = {
    Effect,
    EffectExtreme
}

const selectedComponent = computed(() => componentsMap[selectedEffect.value])
</script>

<style scoped>
.effect-selector {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 1000;
    padding: 4px;
}

.toggle-switch {
    width: 40px;
    height: 20px;
    background: rgba(200, 200, 200, 0.3);
    border-radius: 10px;
    position: relative;
    cursor: pointer;
    transition: all 0.2s ease;
}

.toggle-switch:hover {
    background: rgba(200, 200, 200, 0.5);
}

.switch-handle {
    width: 16px;
    height: 16px;
    background: white;
    border-radius: 50%;
    position: absolute;
    top: 2px;
    left: 2px;
    transition: all 0.2s ease;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.switch-handle.active {
    transform: translateX(20px);
    background: #4CAF50;
}
</style>