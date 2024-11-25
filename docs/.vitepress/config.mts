import { defineConfig } from 'vitepress'
import markdownItMathjax from 'markdown-it-mathjax3'
import navItems from './navItems' // 导入生成的导航菜单项

export default defineConfig({
  lastUpdated: true, // 最后更新时间
  markdown: {
    lineNumbers: true,
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
    search: {
      provider: 'local'
    },
    nav: [
      { text: 'Home', link: '/' },
      ...navItems // 合并生成的导航菜单项
    ],
    socialLinks: [
      { icon: 'github', link: 'https://github.com/YuanQiiii' }
    ]
  }
})
