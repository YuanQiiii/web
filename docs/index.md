---
layout: home

hero:
  name: "Start Page"
  text: "Hello World!"
  actions:
    - theme: brand
      text: 作者
      link: 关于/作者.md
    - theme: alt
      text: 内容
      link: 内容.md
    - theme: brand
      text: 朋友
      link: 朋友.md
---

<script setup>
import { defineClientComponent } from 'vitepress'

const Effect = defineClientComponent(() => {
  return import('./components/Effect.vue')
})
const CommitCount = defineClientComponent(() => {
  return import('./components/CommitCount.vue')
})
</script>

<ClientOnly>
  <Effect/>
</ClientOnly>
