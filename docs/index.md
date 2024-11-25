---
# https://vitepress.dev/reference/default-theme-home-page
layout: home

hero:
  name: "HomePage"
  text: "Eric's HomePage"
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


$\sum_{n=1}^{\infty} \frac{x^n}{n!} = e^x$

```python
print("Hello World!")
```

```cpp
#include<iostream>
using namespace std;
int main(){
  cout<<"Hello World!"<<endl;
  return 0;
}
```

```r
str <- "Hello World!" %>% print()
```
