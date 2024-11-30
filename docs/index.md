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

### <Badge type="info" text="加油写作业" />
### <Badge type="tip" text="废寝忘食" />
### <Badge type="warning" text="是不是花太多时间了？" />
### <Badge type="danger" text="该放一放了" />


            
<script setup>
import EffectSelector from './components/EffectSelector.vue'
import CommitCount from './components/CommitCount.vue'
</script>

<ClientOnly>
          <script async src="//busuanzi.ibruce.info/busuanzi/2.3/busuanzi.pure.mini.js"></script>
            <span id="busuanzi_container_site_pv">本站总访问量<span id="busuanzi_value_site_pv"></span>次</span>
  <EffectSelector/>
  <CommitCount/>
</ClientOnly>