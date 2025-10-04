#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据分析脚本 - Python学习示例
功能：读取Excel文件，分析数据，导出JSON结果

学习要点：
1. pandas库的使用（数据读取和分析）
2. 数据清洗和类型转换
3. 分组统计和聚合计算
4. JSON文件导出
"""

import pandas as pd
import json

# ============================================================
# 第一步：读取Excel文件
# ============================================================
print("正在读取Excel文件...")

# 读取Excel文件
# pd.read_excel() 是pandas读取Excel的函数
df = pd.read_excel('first-80-rows-agentic_ai_performance_dataset_20250622.xlsx')

# Excel第一行是表头，我们需要将它设置为列名
# iloc[0] 表示取第一行数据
new_header = df.iloc[0]

# 从第二行开始才是真正的数据，所以切片[1:]
df = df[1:]

# 将第一行设置为列名
df.columns = new_header

# 重置索引，让行号从0开始
df = df.reset_index(drop=True)

print(f"成功读取 {len(df)} 条数据记录")

# ============================================================
# 第二步：数据类型转换（数据清洗）
# ============================================================
print("正在进行数据类型转换...")

# 将multimodal_capability转换为布尔类型（True/False）
# astype(bool) 是类型转换函数
df['multimodal_capability'] = df['multimodal_capability'].astype(bool)

# 将bias_detection_score转换为数值类型
# to_numeric() 可以将字符串转换为数字，errors='coerce'表示转换失败时设为NaN
df['bias_detection_score'] = pd.to_numeric(df['bias_detection_score'], errors='coerce')

print("数据类型转换完成")

# ============================================================
# 第三步：回答问题1 - Top 3 agent_type（multimodal比例最高）
# ============================================================
print("\n分析问题1：哪些agent_type的multimodal_capability比例最高？")

# groupby() 按agent_type分组
# agg() 聚合函数，对每组进行统计
agent_type_stats = df.groupby('agent_type').agg({
    'multimodal_capability': ['sum', 'count']  # sum计算True的数量，count计算总数
}).reset_index()

# 重命名列名，让它更易读
agent_type_stats.columns = ['agent_type', 'multimodal_count', 'total_count']

# 计算比例：multimodal数量 / 总数量
agent_type_stats['ratio'] = agent_type_stats['multimodal_count'] / agent_type_stats['total_count']

# sort_values() 排序，ascending=False表示降序（从大到小）
agent_type_stats = agent_type_stats.sort_values('ratio', ascending=False)

# head(3) 取前3名
top3_agent = agent_type_stats.head(3)

print("Top 3 agent_type:")
for idx, row in top3_agent.iterrows():
    print(f"  {row['agent_type']}: {row['ratio']:.2%}")

# ============================================================
# 第四步：回答问题2 - Top 3 model_architecture（multimodal比例最高）
# ============================================================
print("\n分析问题2：哪些model_architecture的multimodal_capability比例最高？")

# 同样的逻辑，按model_architecture分组
model_stats = df.groupby('model_architecture').agg({
    'multimodal_capability': ['sum', 'count']
}).reset_index()

model_stats.columns = ['model_architecture', 'multimodal_count', 'total_count']
model_stats['ratio'] = model_stats['multimodal_count'] / model_stats['total_count']
model_stats = model_stats.sort_values('ratio', ascending=False)

top3_model = model_stats.head(3)

print("Top 3 model_architecture:")
for idx, row in top3_model.iterrows():
    print(f"  {row['model_architecture']}: {row['ratio']:.2%}")

# ============================================================
# 第五步：回答问题3 - Top 3 task_category（bias中位数最高）
# ============================================================
print("\n分析问题3：哪些task_category的bias_detection_score中位数最高？")

# 按task_category分组，计算bias_detection_score的中位数
# agg(['median', 'count']) 同时计算中位数和计数
task_bias_stats = df.groupby('task_category')['bias_detection_score'].agg([
    'median', 'count'
]).reset_index()

task_bias_stats.columns = ['task_category', 'median_bias_score', 'count']
task_bias_stats = task_bias_stats.sort_values('median_bias_score', ascending=False)

top3_task = task_bias_stats.head(3)

print("Top 3 task_category:")
for idx, row in top3_task.iterrows():
    print(f"  {row['task_category']}: {row['median_bias_score']:.4f}")

# ============================================================
# 第六步：导出结果为JSON文件
# ============================================================
print("\n正在导出结果到JSON文件...")

# 准备要导出的数据结构
# 这是一个Python字典（dict），包含所有分析结果
results = {
    "total_records": len(df),  # 总记录数
    "question1": {
        "title": "Top 3 Agent Types by Multimodal Capability Ratio",
        "data": [
            {
                "name": row['agent_type'],
                "ratio": float(row['ratio']),  # 转换为float确保JSON兼容
                "multimodal_count": int(row['multimodal_count']),
                "total_count": int(row['total_count'])
            }
            for idx, row in top3_agent.iterrows()  # 列表推导式，遍历top3_agent
        ]
    },
    "question2": {
        "title": "Top 3 Model Architectures by Multimodal Capability Ratio",
        "data": [
            {
                "name": row['model_architecture'],
                "ratio": float(row['ratio']),
                "multimodal_count": int(row['multimodal_count']),
                "total_count": int(row['total_count'])
            }
            for idx, row in top3_model.iterrows()
        ]
    },
    "question3": {
        "title": "Top 3 Task Categories by Median Bias Detection Score",
        "data": [
            {
                "name": row['task_category'],
                "median_score": float(row['median_bias_score']),
                "count": int(row['count'])
            }
            for idx, row in top3_task.iterrows()
        ]
    }
}

# 将Python字典保存为JSON文件
# open() 打开文件，'w'表示写入模式，encoding='utf-8'支持中文
# json.dump() 将字典写入文件，indent=2表示格式化输出（便于阅读）
with open('results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("分析完成！结果已保存到 results.json")
print("\n现在可以用浏览器打开 dashboard.html 查看可视化结果")
