# File: main.py
import argparse

from dynamic_change import dynamic_change
from generate_answers import generate_answers
from validate_answers import validate_answers
from safety_answers import safety_answers

if __name__ == "__main__":

    # 第一步，选择一个种子题库进行动态变形
    dynamic_change('input_jzg.csv', 'input_jzg_changed.csv')

    # 第二步：生成回答
    model_answer = 'qwen2.5-coder:7b'
    answer_file = "qwen2.5_answers.csv"
    generate_answers("input_jzg_changed.csv", answer_file, model_answer)


    # 第三步：验证回答
    validate_answers(answer_file, 'output_zq.csv')
    safety_answers(answer_file, 'output_aq.csv')