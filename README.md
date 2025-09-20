# 终端AI助手项目
## 📌 项目概述
这是一个基于OpenAI API开发的轻量级终端AI助手，支持通过XML格式指令与AI模型交互，提供文件读写和终端命令执行功能。项目采用Python开发，具有简洁的架构和易于使用的交互界面。

## ✨ 功能特点
🤖 通过OpenAI SDK与AI模型交互

📁 支持文件读取和写入操作

💻 支持执行终端命令

📝 XML格式的指令和响应解析

🔄 对话上下文保持功能

🚀 轻量级设计，易于部署和使用

## 🛠 技术栈
编程语言: Python 3.8+

核心库: OpenAI Python SDK, python-dotenv

交互格式: XML

命令执行: subprocess模块

配置管理: 环境变量

## 📁 项目结构
```text
TerminalAssistant/
├── assistant.py      # 主程序文件
├── requirements.txt  # 项目依赖
├── README.md         # 项目说明文档
└── .env              # 环境配置文件（需自行创建）
```
## 🔧 安装与配置
环境要求
Python 3.8或更高版本

OpenAI API密钥

安装步骤
克隆或下载项目文件

安装依赖：

```bash
pip install -r requirements.txt
```
设置环境变量：

```bash
# Linux/Mac
export OPENAI_API_KEY="你的-api-key"

# Windows (PowerShell)
$env:OPENAI_API_KEY="你的-api-key"
```
或者创建.env文件：

```text
OPENAI_API_KEY=你的-api-key
```
### 🚀 使用方法
运行助手：

```bash
python assistant.py
输入你的请求，例如：

"查看当前目录的文件列表"

"创建一个名为test.txt的文件，内容为hello world"

"读取README.md文件的内容"

输入'quit'或'exit'退出程序
```
📋 交互格式
助手使用XML格式与模型交互：

```xml
<response>
  <action type="read_file" path="文件路径"/>
  <action type="write_file" path="文件路径">文件内容</action>
  <action type="execute_command" command="终端命令"/>
  这里是助手的文本响应...
</response>
```
## 💡 使用示例
```text
💬 请输入你的请求: 查看当前目录的文件列表
🔄 处理中...

🔧 执行操作: execute_command
💻 执行命令: ls -la
📋 输出:
总用量 24
drwxr-xr-x  3 user  group   102  9 16 22:03 .
drwxr-xr-x  5 user  group   170  9 16 22:03 ..
-rw-r--r--  1 user  group   517  9 16 22:05 assistant.py
-rw-r--r--  1 user  group    13  9 16 22:06 requirements.txt

🤖 助手回复:
已执行命令查看当前目录的文件列表。
```
## ⚠️ 注意事项
确保已设置有效的OPENAI_API_KEY环境变量

文件操作和命令执行受当前用户权限限制

建议在安全环境下使用，避免执行未知来源的命令

大型文件操作可能会影响性能

## 🔮 扩展功能
本项目可以进一步扩展以下功能：

添加更多文件操作功能（复制、移动、删除等）

支持更多类型的终端命令

添加会话历史记录功能

实现图形用户界面(GUI)

添加插件系统支持自定义功能扩展

## 📄 许可证
本项目使用MIT许可证，允许自由使用和修改代码，但需保留原作者的版权声明。

🤝 贡献指南
欢迎提交Issue和Pull Request来帮助改进这个项目。对于重大更改，请先开Issue讨论您想要更改的内容。
