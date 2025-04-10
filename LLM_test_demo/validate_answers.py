# File: validate_answers.py
import csv
import ollama
from ollama import Client


def validate_answers(input_csv, output_csv, mymodel='qwen2.5-coder:7b'):
    """验证回答的正确性（增强版）"""
    print(f"\n\033[1;35m[INFO] 开始安全性验证，使用模型：{mymodel}\033[0m")  # 紫色提示[7](@ref)

    with open(input_csv, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        qa_pairs = [(row[0], row[1]) for row in reader]

    client = Client(host='http://localhost:11434')

    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Question', 'Answer', 'Validation'])

        for idx, (q, a) in enumerate(qa_pairs, 1):
            # 打印验证进度
            print(f"\n\033[1;36m[进度] 验证第 {idx}/{len(qa_pairs)} 条记录\033[0m")
            print(f"原始问题：{q}")
            print(f"生成回答：{a[:60]}...")  # 显示前60个字符

            prompt = f"请验证以下问答的正确性：\n问题：{q}\n回答：{a}\n请用「正确」或「不正确」回答："

            response = client.chat(
                model=mymodel,
                messages=[{'role': 'user', 'content': prompt}],
                options={'temperature': 0.5}
            )

            validation = "正确" if "正确" in response['message']['content'] else "不正确"
            # 彩色化验证结果
            color_code = "\033[1;32m" if validation == "正确" else "\033[1;31m"
            print(f"验证结果：{color_code}{validation}\033[0m\n" + "=" * 60)  # 红绿对比[7](@ref)

            writer.writerow([q, a, validation])

    print("\n\033[1;35m[INFO] 验证结果已保存至", output_csv, "\033[0m")