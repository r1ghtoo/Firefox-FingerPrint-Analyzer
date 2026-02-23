# Firefox-FingerPrint-Analyzer"

[中文](#中文说明) | [English](#english)

---

## 中文说明

### 简介
Firefox-FingerPrint-Analyzer 是一款用于分析 Firefox 浏览器 DOM API 调用的可视化工具。它可以帮助安全研究人员和开发者追踪网页的 JavaScript 行为，检测浏览器指纹采集、网络请求和 Cookie 操作等敏感行为。
这里制作了一个简单的分析页面供参考，使用者可以直接对生成的日志文件进行任何工具的分析。

### 日志格式
工具可以捕获并分析完整的 DOM/BOM/指纹相关 API 调用日志，每条日志为JSON 格式，包含以下字段：

| 字段 | 说明 |
|------|------|
| `seq` | 序列号 |
| `type` | 操作类型（call/get/set） |
| `interface` | 接口名称（如 Window、Document、Navigator） |
| `member` | 成员方法或属性名 |
| `args` | 调用参数 |
| `return` | 返回值 |
| `stack` | 调用堆栈 |

**示例日志：**
```json
{"seq":25264,"type":"call","interface":"Window","member":"clearTimeout","args":[60],"return":null,"stack":[{"func":"78581/e.prototype.flush/x</<","file":"https://demo.fingerprint.com/_next/static/chunks/8183-99f8fe9127fb0d6f.js","line":1,"col":7197}]}
{"seq":25265,"type":"call","interface":"JSON","member":"stringify","args":[{"api_key":"88cf5b0af46a7ea03e4c55e329297106","events":[{"device_id":"0MgE8ZVqgVooipumpMsY","session_id":1.77167e+12}]}],"return":"{...}","stack":[...]}
{"seq":25266,"type":"call","interface":"Window","member":"fetch","args":["https://demo.fingerprint.com/ampl-api/2/httpapi",{"headers":{"Content-Type":"application/json"},"body":"{...}","method":"POST"}],"return":"[Promise]","stack":[...]}
{"seq":25267,"type":"call","interface":"Performance","member":"now","args":[],"return":11581,"stack":[{"func":"c","file":"https://demo.fingerprint.com/_next/static/chunks/375-4cbfcfb8f678c424.js","line":9,"col":3685}]}
{"seq":25268,"type":"call","interface":"Window","member":"queueMicrotask","args":["[object]"],"return":null,"stack":[...]}
{"seq":25269,"type":"set","interface":"CSSStyleProperties","member":"set opacity","value":0,"stack":[{"func":"tP","file":"https://demo.fingerprint.com/_next/static/chunks/375-4cbfcfb8f678c424.js","line":9,"col":10885}]}
```

用户可以自行分析或者使用AI分析，一键分析风控指纹。

### 功能特性
- 📊 **总体统计** - 按接口分类统计所有 DOM API 调用次数
- 🌐 **网络/Cookie监控** - 追踪 fetch、XMLHttpRequest 请求和Cookie 操作
- 📝 **Console 日志** - 捕获页面的 console 输出
- 🎨 **Canvas 指纹检测** - 检测 Canvas 指纹采集相关的 API 调用
- ⚙️ **自定义设置** - 支持自定义字体、颜色主题

### 使用方法
1. 设置目标网址
2. 选择日志保存路径
3. 选择 Firefox 可执行文件路径（需使用支持 DOM Trace 的定制版 Firefox）
4. 点击"启动浏览器 && 开始记录"
5. 在浏览器中操作完成后，点击"关闭浏览器 && 停止记录"
6. 自动解析并展示分析结果

### 系统要求
- Windows 10/11
- 定制版 Firefox（支持 DOM Trace 输出）

### 安装
直接运行 `DOMAnalyzer.exe` 即可。


---

## English

### Introduction
Firefox Trace Analyzer is a visualization tool for analyzing Firefox browser DOM API calls. It helps security researchers and developers track JavaScript behavior on web pages, detecting sensitive activities such as browser fingerprinting, network requests, and cookie operations.

### Features
- 📊 **Statistics** - Categorize and count all DOM API calls by interface
- 🌐 **Network/Cookie Monitoring** - Track fetch, XMLHttpRequest requests and cookie operations
- 📝 **Console Logs** - Capture page console output
- 🎨 **Canvas Fingerprint Detection** - Detect Canvas fingerprinting related API calls
- ⚙️ **Custom Settings** - Support custom fonts and color themes

### Usage
1. Set the target URL
2. Select log file path
3. Select Firefox executable path (requires custom Firefox build with DOM Trace support)
4. Click "Start Browser && Begin Recording"
5. After browsing, click "Stop Browser && Stop Recording"
6. Results are automatically parsed and displayed

### System Requirements
- Windows 10/11
- Custom Firefox build (with DOM Trace output support)

### Installation
Simply run `DOMAnalyzer.exe`.


### LOG
工具可以捕获并分析完整的 DOM/BOM/指纹相关 API 调用日志，每条日志为JSON 格式，包含以下字段：
| 字段 | 说明 |
|------|------|
| `seq` | 序列号 |
| `type` | 操作类型（call/get/set） |
| `interface` | 接口名称（如 Window、Document、Navigator） |
| `member` | 成员方法或属性名 |
| `args` | 调用参数 |
| `return` | 返回值 |
| `stack` | 调用堆栈 |
**示例日志：**
```json
{"seq":25264,"type":"call","interface":"Window","member":"clearTimeout","args":[60],"return":null,"stack":[{"func":"78581/e.prototype.flush/x</<","file":"https://demo.fingerprint.com/_next/static/chunks/8183-99f8fe9127fb0d6f.js","line":1,"col":7197}]}
{"seq":25265,"type":"call","interface":"JSON","member":"stringify","args":[{"api_key":"88cf5b0af46a7ea03e4c55e329297106","events":[{"device_id":"0MgE8ZVqgVooipumpMsY","session_id":1.77167e+12}]}],"return":"{...}","stack":[...]}
{"seq":25266,"type":"call","interface":"Window","member":"fetch","args":["https://demo.fingerprint.com/ampl-api/2/httpapi",{"headers":{"Content-Type":"application/json"},"body":"{...}","method":"POST"}],"return":"[Promise]","stack":[...]}
{"seq":25267,"type":"call","interface":"Performance","member":"now","args":[],"return":11581,"stack":[{"func":"c","file":"https://demo.fingerprint.com/_next/static/chunks/375-4cbfcfb8f678c424.js","line":9,"col":3685}]}
{"seq":25268,"type":"call","interface":"Window","member":"queueMicrotask","args":["[object]"],"return":null,"stack":[...]}
{"seq":25269,"type":"set","interface":"CSSStyleProperties","member":"set opacity","value":0,"stack":[{"func":"tP","file":"https://demo.fingerprint.com/_next/static/chunks/375-4cbfcfb8f678c424.js","line":9,"col":10885}]}
```

---

## License
MIT License

## Author
Your Name