---
# https://vitepress.dev/reference/default-theme-home-page
layout: home

hero:
  name: "Page"
  text: "a living man"
  actions:
    - theme: brand
      text: 普心
      link: \笔记\当前的学习重心\普通心理学B.md
    - theme: brand
      text: 社心
      link: \笔记\当前的学习重心\社会心理学.md

features:
  - icon: A
    title: Markdown
    details: 支持Markdown文档
  - icon: B
    title: Latex
    details: 支持Latex公式
  - icon: C
    title: 图片
    details: 支持Markdown中的图片

  
---

::: info
下面是一些功能测试!
:::

***

## 数学公式

$\sum_{n=1}^{\infty} \frac{x^n}{n!} = e^x$

## 代码块

```python
print("Hello World!")
```

```cpp
#include<iostream>
using namespace std;
int main(){
  cout<<"Hello World!"<<endl; "hello="" %="" 0;="" <-="" ```="" ```r="" return="" str="" world!"="" }="">% print()
```

## 自定义容器

::: info
This is an info box.
:::

::: tip
This is a tip.
:::

::: warning
This is a warning.
:::

::: danger
This is a dangerous warning.
:::

::: details
This is a details block.
:::

::: danger STOP
危险区域,请勿继续
:::

::: details 点我查看代码

```js
console.log('Hello, VitePress!')
```

:::

## GitHub 风格的警报

> [!NOTE]
> 强调用户在快速浏览文档时也不应忽略的重要信息.

> [!TIP]
> 有助于用户更顺利达成目标的建议性信息.

> [!IMPORTANT]
> 对用户达成目标至关重要的信息.

> [!WARNING]
> 因为可能存在风险,所以需要用户立即关注的关键内容.

> [!CAUTION]
> 行为可能带来的负面影响.

## 代码块中聚焦

在某一行上添加 `// [!code focus]` 注释将聚焦它并模糊代码的其他部分.

此外,可以使用 `// [!code focus:<lines>]` 定义要聚焦的行数.

```js
export default {
  data () {
    return {
      msg: 'Focused!' // [!code focus]
    }
  }
}
```

## 代码块中的颜色差异

在某一行添加 `// [!code --]` 或 `// [!code ++]` 注释将会为该行创建 diff,同时保留代码块的颜色.

```js
export default {
  data () {
    return {
      msg: 'Removed' // [!code --]
      msg: 'Added' // [!code ++]
    }
  }
}
```

## 高亮"错误"和"警告"

在某一行添加 // [!code warning] 或 // [!code error] 注释将会为该行相应的着色.

```js
export default {
  data () {
    return {
      msg: 'Error', // [!code error]
      msg: 'Warning' // [!code warning]
    }
  }
}
```

## 代码组

可以像这样对多个代码块进行分组:

::: code-group

```js [config.js]
/**
 * @type {import('vitepress').UserConfig}
 */
const config = {
  // ...
}

export default config
```

```ts [config.ts]
import type { UserConfig } from 'vitepress'

const config: UserConfig = {
  // ...
}

export default config
```

:::
