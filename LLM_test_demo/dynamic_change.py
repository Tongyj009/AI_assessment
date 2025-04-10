# File: validate_answers.py
import csv
import ollama
from ollama import Client


def dynamic_change(input_csv, output_csv, mymodel='qwen2.5-coder:7b'):
    """题目随机变形"""
    print(f"\n\033[1;35m[INFO] 开始题目动态变形\033[0m")  # 紫色提示[7](@ref)

    with open(input_csv, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        qa_pairs = [(row[0], row[1]) for row in reader]

    client = Client(host='http://localhost:11434')

    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        for idx, (q, a) in enumerate(qa_pairs, 1):
            # 打印验证进度
            print(f"\n\033[1;36m[进度] 验证第 {idx}/{len(qa_pairs)} 条记录\033[0m")
            print(f"原始问题：{a}")

            prompt = f"请将下面的问题进行同义词替换，主动句与被动句转换，改变语序，改变句式结构中的其中一种变形，只需要一种，仅输出转换后的一个语句，不添加任何额外内容。\n问题：{a}"

            response = client.chat(
                model=mymodel,
                messages=[{'role': 'user', 'content': prompt}],
                options={'temperature': 0.5}
            )

            # 彩色化验证结果
            color_code = "\033[1;32m"
            print(f"变形后语句：{color_code}\033[0m\n" + "=" * 60)  # 红绿对比[7](@ref)
            transformed = response['message']['content']
            print(f"{response['message']['content']}...")
            writer.writerow([q, transformed])

    print("\n\033[1;35m[INFO] 变形结果已保存至", output_csv, "\033[0m")