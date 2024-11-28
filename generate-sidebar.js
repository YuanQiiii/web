const fs = require('fs');
const path = require('path');

const docsDir = path.join(__dirname, 'docs');
const sidebarItemsFile = path.join(docsDir, '.vitepress', 'sidebarItems.js');

// 获取所有 Markdown 文件，组织为导航菜单项
// 最多两层目录 笔记>书签>具体文件
function getSidebarItems(dir, basePath = '') {
  const items = [];
  const entries = fs.readdirSync(dir);

  entries.forEach((entry) => {
    const fullPath = path.join(dir, entry);
    const stats = fs.statSync(fullPath);

    if (stats.isDirectory()) {
      // 遇到目录，递归处理
      const subItems = getSidebarItems(fullPath, path.posix.join(basePath, entry));
      if (subItems.length > 0) {
        items.push({
          text: entry,
          items: subItems
        });
      }
    } else if (stats.isFile() && entry.endsWith('.md')) {
      // 遇到 Markdown 文件
      const name = entry.replace('.md', '');
      // 忽略 index.md
      if (name.toLowerCase() !== 'index') {
        items.push({
          text: name,
          link: path.posix.join('/', basePath, name)
        });
      }
    }
  });

  return items;
}
// 获取所有 Markdown 文件，组织为导航菜单项
const sidebarItems = getSidebarItems(docsDir);

// 定义生成的代码内容
const sidebarCode = `// 此文件由 generate-sidebar 自动生成，请勿手动修改
export default ${JSON.stringify(sidebarItems, null, 2)};
`;

// 确保 .vitepress 目录存在
const vitepressDir = path.join(docsDir, '.vitepress');
if (!fs.existsSync(vitepressDir)) {
  fs.mkdirSync(vitepressDir);
}

// 将生成的代码写入 navItems.js 文件
fs.writeFileSync(sidebarItemsFile, sidebarCode, 'utf-8');
console.log('sidebarItems.js 生成成功');