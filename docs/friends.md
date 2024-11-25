---
layout: page
---
<script setup>
import {
  VPTeamPage,
  VPTeamPageTitle,
  VPTeamMembers
} from 'vitepress/theme'

const members = [
  {
    avatar: 'https://pku-cs-cjw.top/image/头像.jpg',
    name: 'c+v',
    title: 'Friend',
    links: [
      { icon: 'github'
      , link: 'https://pku-cs-cjw.top/' }
    ]
  }
]

</script>

<VPTeamPage>
  <VPTeamPageTitle>
    Friends
  </VPTeamPageTitle>
  <VPTeamMembers :members="members" />
</VPTeamPage>
