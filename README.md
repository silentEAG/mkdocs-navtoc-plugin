# mkdocs-navtoc-plugin

mkdocs 页面自动内嵌 nav 插件

## 使用

```shell
pip install git+https://github.com/silentEAG/mkdocs-navtoc-plugin.git
```

在 `mkdocs.yml` 开启插件
```yml
plugins:
  - navtoc
```

然后在需要 toc 的地方设置 markdown 文件的 metadata:
```md
---
navtoc: true

---

your content
```

效果:
![](./screen.png)