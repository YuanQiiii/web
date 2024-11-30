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

### <Badge type="info" text="写作业" />
### <Badge type="info" text="READING Neuron Science-Exploring the Brain " />
### <Badge type="info" text="READING Neuron AI的25种可能 " />
### <Badge type="tip" text="废寝忘食" />
### <Badge type="warning" text="合理使用时间" />
### <Badge type="danger" text="加油" />


            
<script setup>
import EffectSelector from './components/EffectSelector.vue'
import CommitCount from './components/CommitCount.vue'
</script>

<ClientOnly>
  <EffectSelector/>
  <CommitCount/>
</ClientOnly>