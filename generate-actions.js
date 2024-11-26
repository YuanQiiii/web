const fs = require('fs');
const path = require('path');

// 指定要修改的文件路径
const indexPath = path.join(__dirname, 'docs/index.md');
// 指定要递归遍历的目录路径
const targetDirectory = path.join(__dirname, 'docs');
// 要忽略的文件列表
const ignoreFiles = ['index.md', 'friends.md', 'functions.md'];

// 主题数组 - 只使用 VitePress 支持的主题
const themes = ['brand', 'alt'];

// 递归遍历目录，生成 actions
function generateActions(dir) {
  let actions = '';
  const files = fs.readdirSync(dir);

  files.forEach((file, index) => {
    const fullPath = path.join(dir, file);
    const stat = fs.statSync(fullPath);

    if (stat.isDirectory()) {
      actions += generateActions(fullPath);
    } else if (stat.isFile() && path.extname(fullPath) === '.md' && !ignoreFiles.includes(file)) {
      let relativePath = path.relative(__dirname, fullPath).replace(/\\/g, '/');
      relativePath = relativePath.replace(/^docs\//, '');
      const fileName = path.basename(fullPath, '.md');
      const theme = themes[index % themes.length];
      actions += `
    - theme: ${theme}
      text: ${fileName}
      link: ${relativePath}
`;
    }
  });

  return actions;
}

// 读取和处理文件
fs.readFile(indexPath, 'utf8', (err, data) => {
  if (err) {
    console.error('Error reading file:', err);
    return;
  }

  // 查找 actions: 的位置
  const actionsIndex = data.indexOf('actions:');
  if (actionsIndex === -1) {
    console.error('Cannot find actions: marker in the file');
    return;
  }

  // 保留 actions: 之前的内容
  const header = data.substring(0, actionsIndex + 'actions:'.length);
  
  // 生成新的 actions 内容
  const newActions = generateActions(targetDirectory);
  
  // 组合新的文件内容
  const updatedContent = `${header}\n${newActions}\n---`;

  // 写回文件
  fs.writeFile(indexPath, updatedContent, 'utf8', (err) => {
    if (err) {
      console.error('Error writing file:', err);
    } else {
      console.log('Actions updated successfully');
    }
  });
});