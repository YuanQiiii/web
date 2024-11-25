import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  lastUpdated: true, // 最后更新时间
  markdown: {
    math: true,
    image: {
      // 默认禁用图片懒加载
      lazyLoading: true
    }
  },
  base: '/web/',
  title: "HomePage",
  description: "Eric's HomePage",
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Home', link: '/' },
    ],
    socialLinks: [
      { icon: 'github', link: 'https://github.com/vuejs/vitepress' }
    ]
  }
})
