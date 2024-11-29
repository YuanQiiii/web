
//import navItems from './navItems' // 导入生成的导航菜单项
import sidebarItems from './sidebarItems' // 导入生成的侧边栏

export default {
  lastUpdated: true, // 使用 git 提交获取时间戳，使默认主题能够显示页面的上次更新时间
  ignoreDeadLinks: true, // 不会因死链接而使构建失败
  markdown: {
    lineNumbers: true, // 显示代码行数
    math: true, // 支持数学公式
    image: {
      // 默认禁用图片懒加载
      lazyLoading: true
    }
  },
  base: '/web/', // 部署站点的基础路径
  head: [['link', { rel: 'icon', href: '/web/favicon.ico' }]], // 网站图标
  title: "Home",
  description: "a long story",
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    search: {
      provider: 'local'
    },
    //nav: [
    //  ...navItems // 合并生成的导航菜单项
    //],
    sidebar: [
      ...sidebarItems // 合并生成的侧边栏
    ]
  }
}
