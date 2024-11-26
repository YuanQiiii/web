---
layout: home
hero:
  name: "Start Page"
  text: "Hello World!"
---

<script setup>
import { defineClientComponent } from 'vitepress'

const Effect = defineClientComponent(() => {
  return import('./components/Effect.vue')
})
</script>

<ClientOnly>
  <Effect/>
</ClientOnly>