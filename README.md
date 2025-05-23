# 智能WPS HTML代码解析器

![示例界面](https://via.placeholder.com/800x500.png/555555/ffffff?text=WPS+Code+Parser) <!-- 建议替换实际截图 -->

## 🚀 功能特性

- **一键粘贴**：直接读取系统剪贴板内容
- **智能解析**：自动识别WPS导出的特殊代码块结构
- **语法保留**：精确保留代码缩进和特殊符号（{}; //等）
- **实时反馈**：状态栏显示解析进度和错误信息
- **响应式设计**：适配不同屏幕尺寸（桌面/移动端）

## 🛠️ 技术实现

### 核心解析逻辑
```javascript
// 使用DOM API解析代码块结构
const codeBlock = temp.querySelector(
  "code.code-block-content.code-block-theme-style"
);

// 多节点遍历算法
children.forEach((el) => {
  if (el.nodeName === "BR") {
    // 处理换行逻辑...
  } else if (el.classList.contains("code-span")) {
    // 处理代码片段...
  }
});

// 正则表达式优化
.replace(/\s+\)/g, ")")       // 消除多余空格
.replace(/([{}])\n */g, "$1\n") // 格式化花括号
```

### 关键技术点
- **剪贴板API**：`navigator.clipboard.readText()`
- **DOM解析**：动态创建虚拟节点避免污染页面
- **异步处理**：使用`async/await`处理剪贴板操作
- **错误边界**：try-catch捕获解析异常

## 📖 使用指南

### 基本操作
1. 从WPS复制代码到剪贴板
2. 点击【📋 一键粘贴】按钮
3. 点击【⚙️ 解析内容】查看结果
4. 从右侧文本框复制解析后的代码

### 输入要求
```html
<!-- WPS导出的典型代码结构 -->
<code class="code-block-content code-block-theme-style">
  <span class="code-span">if</span>
  <span class="code-span">(condition)</span><br>
  ...
</code>
```

## ⚠️ 注意事项

1. **浏览器兼容**：
   - 需要现代浏览器（Chrome 76+/Firefox 66+）
   - 剪贴板功能需HTTPS环境或localhost

2. **安全限制**：
   - 首次使用需授权剪贴板访问权限
   - 建议在可信环境中使用

3. **性能优化**：
   - 推荐处理小于10,000行的代码文件
   - 大文件解析可能有短暂延迟

## 📄 许可协议
[MIT License](LICENSE)
