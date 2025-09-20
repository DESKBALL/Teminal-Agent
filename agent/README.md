# 轻量级电脑助手 Agent

一个基于 OpenAI API 的终端助手，支持通过 XML 格式与模型交互，提供文件读写和终端命令执行功能。

## 功能特性

- 🤖 通过 OpenAI SDK 与 AI 模型交互
- 📁 支持文件读取和写入操作
- �� 支持执行终端命令
- 📝 XML 格式的指令和响应
- 🔄 对话上下文保持
- 🚀 轻量级，易于使用

## 安装要求

- Python 3.8+
- OpenAI API 密钥

## 安装步骤

1. 克隆或下载项目文件
2. 安装依赖：
   \\\ash
   pip install -r requirements.txt
   \\\

3. 设置环境变量：
   \\\ash
   # Linux/Mac
   export OPENAI_API_KEY=\
你的-api-key\
   
   # Windows (PowerShell)
   \=\你的-api-key\
   \\\

## 使用方法

1. 运行助手：
   \\\ash
   python assistant.py
   \\\

2. 输入你的请求，例如：
   - \查看当前目录的文件列表\
   - \创建一个名为
test.txt
的文件，内容为
hello
world\
   - \读取
README.md
文件的内容\

3. 输入 'quit' 或 'exit' 退出程序

## XML 交互格式

助手使用 XML 格式与模型交互：

\\\xml
<response>
<action type=\read_file\ path=\文件路径\/>
<action type=\write_file\ path=\文件路径\>文件内容</action>
<action type=\execute_command\ command=\终端命令\/>
这里是助手的文本响应...
</response>
\\\

## 示例

\\\
💬 请输入你的请求: 查看当前目录的文件列表
🔄 处理中...

🔧 执行操作: execute_command
💻 执行命令: dir
📋 输出:
 Volume in drive C is Windows
 Volume Serial Number is XXXX-XXXX

 Directory of C:\\Users\\10165\\Desktop\\python\\teminAgent\\agent

2025/09/16  22:03    <DIR>          .
2025/09/16  22:03    <DIR>          ..
2025/09/16  22:05               517 assistant.py
2025/09/16  22:06                13 requirements.txt
               2 File(s)            530 bytes
               2 Dir(s)  100,000,000,000 bytes free

🤖 助手回复:
已执行命令查看当前目录的文件列表。
\\\

## 注意事项

- 确保已设置 OPENAI_API_KEY 环境变量
- 文件操作和命令执行有相应的权限限制
- 建议在安全环境下使用
