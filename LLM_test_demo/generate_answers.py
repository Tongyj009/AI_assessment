# File: generate_answers.py
import csv
import ollama
from ollama import Client


# 在原有代码基础上添加打印功能
def generate_answers(input_csv, output_csv, mymodel='qwen2.5-coder:7b'):
    """读取CSV第二列问题并生成回答（增强版）"""
    print(f"\n\033[1;34m[INFO] 开始生成回答，使用模型：{mymodel}\033[0m")  # 蓝色提示[7](@ref)

    with open(input_csv, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        questions = [row[1] for row in reader if len(row) >= 2]

    client = Client(host='http://localhost:11434')

    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Question', 'Answer'])

        for idx, q in enumerate(questions, 1):
            # 生成回答前打印进度
            print(f"\n\033[1;36m[进度] 正在处理第 {idx}/{len(questions)} 个问题\033[0m")  # 青色进度条[7](@ref)
            print(f"问题：{q}")

            response = client.chat(
                model=mymodel,
                messages=[{'role': 'user', 'content': q}],
                options={'temperature': 0.5}
            )

            # 打印带格式的响应结果
            print(f"\033[1;32m生成回答：\033[0m\n{response['message']['content']}\n" + "-" * 50)  # 绿色标题[7](@ref)

            writer.writerow([q, response['message']['content']])

    print("\n\033[1;34m[INFO] 所有回答已保存至", output_csv, "\033[0m")