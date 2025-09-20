#!/usr/bin/env python3
"""
轻量级电脑助手Agent
通过OpenAI SDK与模型交互，支持XML格式的指令和响应
提供文件读写和终端命令执行工具
"""

import os
import sys
import subprocess
import xml.etree.ElementTree as ET
from openai import OpenAI
from typing import Dict, List, Optional
from dotenv import load_dotenv
import json


class ComputerAssistant:
    def __init__(self, api_key: Optional[str] = None):
        """初始化助手"""
        load_dotenv()
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key is required. Set OPENAI_API_KEY environment variable."
            )

        self.client = OpenAI(api_key=self.api_key, base_url="https://api.deepseek.com")
        self.model = "deepseek-chat"  # 可以根据需要修改模型

    def read_file(self, file_path: str) -> str:
        """读取文件内容"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"Error reading file {file_path}: {str(e)}"

    def write_file(self, file_path: str, content: str) -> str:
        """写入文件内容"""
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return f"Successfully wrote to {file_path}"
        except Exception as e:
            return f"Error writing to file {file_path}: {str(e)}"

    def execute_command(self, command: str) -> str:
        """执行终端命令"""
        try:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, cwd=os.getcwd()
            )
            if result.returncode == 0:
                return result.stdout
            else:
                return f"Command failed with return code {result.returncode}:\n{result.stderr}"
        except Exception as e:
            return f"Error executing command: {str(e)}"

    def parse_xml_response(self, response: str) -> Dict:
        """解析模型的XML响应"""
        try:
            root = ET.fromstring(response)
            actions = []

            for action in root.findall("action"):
                action_type = action.get("type")
                if action_type == "read_file":
                    file_path = action.get("path")
                    result = self.read_file(file_path)
                    actions.append(
                        {"type": "read_file", "path": file_path, "result": result}
                    )

                elif action_type == "write_file":
                    file_path = action.get("path")
                    content = action.text or ""
                    result = self.write_file(file_path, content)
                    actions.append(
                        {"type": "write_file", "path": file_path, "result": result}
                    )

                elif action_type == "execute_command":
                    command = action.get("command")
                    result = self.execute_command(command)
                    actions.append(
                        {
                            "type": "execute_command",
                            "command": command,
                            "result": result,
                        }
                    )

            return {
                "actions": actions,
                "response": (
                    root.find("response").text
                    if root.find("response") is not None
                    else ""
                ),
            }

        except ET.ParseError:
            # 如果不是有效的XML，直接返回响应
            return {"actions": [], "response": response}

    def generate_prompt(self, user_input: str, context: List[Dict] = None) -> str:
        """生成包含工具说明的提示词"""
        tools_prompt = """
你是一个电脑助手，可以通过XML格式与我交互。你可以使用以下工具：

1. 读取文件：<action type="read_file" path="文件路径"/>
2. 写入文件：<action type="write_file" path="文件路径">文件内容</action>
3. 执行命令：<action type="execute_command" command="终端命令"/>

请将你的响应包装在<response>标签中，并在其中包含任何需要执行的操作。

示例：
<response>
<action type="read_file" path="example.txt"/>
<action type="execute_command" command="ls -la"/>
这里是你的文本响应...
</response>

当前工作目录：{cwd}
        """.format(
            cwd=os.getcwd()
        )

        if context:
            context_str = "\n之前的对话：\n" + "\n".join(
                [f"用户: {c['user']}\n助手: {c['assistant']}" for c in context[-5:]]
            )
        else:
            context_str = ""

        return f"{tools_prompt}{context_str}\n\n用户输入：{user_input}"

    def process_request(self, user_input: str, context: List[Dict] = None) -> Dict:
        """处理用户请求"""
        prompt = self.generate_prompt(user_input, context)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个有帮助的电脑助手，可以使用XML格式的工具与用户交互。",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=2000,
            )

            model_response = response.choices[0].message.content
            parsed_response = self.parse_xml_response(model_response)

            return {
                "model_response": model_response,
                "parsed_response": parsed_response,
                "actions": parsed_response["actions"],
            }

        except Exception as e:
            return {
                "error": f"Error communicating with OpenAI: {str(e)}",
                "actions": [],
            }


def main():
    """主函数"""
    print("🤖 轻量级电脑助手启动中...")
    print("输入 'quit' 或 'exit' 退出程序")
    print("-" * 50)

    try:
        assistant = ComputerAssistant()
    except ValueError as e:
        print(f"错误: {e}")
        print("请设置 OPENAI_API_KEY 环境变量")
        sys.exit(1)

    context = []

    while True:
        try:
            user_input = input("\n💬 请输入你的请求: ").strip()

            if user_input.lower() in ["quit", "exit", "q"]:
                print("👋 再见！")
                break

            if not user_input:
                continue

            print("🔄 处理中...")

            result = assistant.process_request(user_input, context)

            if "error" in result:
                print(f"❌ 错误: {result['error']}")
                continue

            # 执行操作并显示结果
            for action in result["actions"]:
                print(f"\n🔧 执行操作: {action['type']}")
                if action["type"] == "read_file":
                    print(f"📖 读取文件: {action['path']}")
                    print(f"📄 内容:\n{action['result']}")
                elif action["type"] == "write_file":
                    print(f"📝 写入文件: {action['path']}")
                    print(f"✅ 结果: {action['result']}")
                elif action["type"] == "execute_command":
                    print(f"💻 执行命令: {action['command']}")
                    print(f"📋 输出:\n{action['result']}")

            # 显示模型响应
            if result["parsed_response"]["response"]:
                print(f"\n🤖 助手回复:\n{result['parsed_response']['response']}")

            # 更新上下文
            context.append({"user": user_input, "assistant": result["model_response"]})

        except KeyboardInterrupt:
            print("\n👋 再见！")
            break
        except Exception as e:
            print(f"❌ 发生错误: {str(e)}")


if __name__ == "__main__":
    main()
