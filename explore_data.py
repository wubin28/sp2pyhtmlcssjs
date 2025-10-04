import pandas as pd

# Read and process the Excel file
df = pd.read_excel('first-80-rows-agentic_ai_performance_dataset_20250622.xlsx')
new_header = df.iloc[0]
df = df[1:]
df.columns = new_header
df = df.reset_index(drop=True)

print("Dataset shape:", df.shape)
print("Total records processed:", len(df))

# Convert data types
df['multimodal_capability'] = df['multimodal_capability'].astype(bool)
df['bias_detection_score'] = pd.to_numeric(df['bias_detection_score'], errors='coerce')

print("\n" + "="*80)
print("QUESTION 1: Top 3 agent_type with highest multimodal_capability ratio")
print("="*80)

# Filter agents with multimodal capability
multimodal_agents = df[df['multimodal_capability'] == True]
print(f"\nTotal agents with multimodal_capability: {len(multimodal_agents)}")

# Calculate ratio for each agent_type
agent_type_stats = df.groupby('agent_type').agg({
    'multimodal_capability': ['sum', 'count']
}).reset_index()
agent_type_stats.columns = ['agent_type', 'multimodal_count', 'total_count']
agent_type_stats['ratio'] = agent_type_stats['multimodal_count'] / agent_type_stats['total_count']
agent_type_stats = agent_type_stats.sort_values('ratio', ascending=False)

print("\nAll agent_type multimodal ratios:")
print(agent_type_stats.to_string(index=False))

print("\nTop 3 agent_type with highest multimodal_capability ratio:")
top3_agent = agent_type_stats.head(3)
print(top3_agent.to_string(index=False))

print("\n" + "="*80)
print("QUESTION 2: Top 3 model_architecture with highest multimodal_capability ratio")
print("="*80)

# Calculate ratio for each model_architecture
model_stats = df.groupby('model_architecture').agg({
    'multimodal_capability': ['sum', 'count']
}).reset_index()
model_stats.columns = ['model_architecture', 'multimodal_count', 'total_count']
model_stats['ratio'] = model_stats['multimodal_count'] / model_stats['total_count']
model_stats = model_stats.sort_values('ratio', ascending=False)

print("\nAll model_architecture multimodal ratios:")
print(model_stats.to_string(index=False))

print("\nTop 3 model_architecture with highest multimodal_capability ratio:")
top3_model = model_stats.head(3)
print(top3_model.to_string(index=False))

print("\n" + "="*80)
print("QUESTION 3: Top 3 task_category with highest median bias_detection_score")
print("="*80)

# Calculate median bias_detection_score for each task_category
task_bias_stats = df.groupby('task_category')['bias_detection_score'].agg([
    'median', 'count', 'mean'
]).reset_index()
task_bias_stats.columns = ['task_category', 'median_bias_score', 'count', 'mean_bias_score']
task_bias_stats = task_bias_stats.sort_values('median_bias_score', ascending=False)

print("\nAll task_category bias detection median scores:")
print(task_bias_stats.to_string(index=False))

print("\nTop 3 task_category with highest median bias_detection_score:")
top3_task = task_bias_stats.head(3)
print(top3_task.to_string(index=False))

print("\n" + "="*80)
print("SUMMARY OF ANSWERS")
print("="*80)
print(f"\nTotal data records processed: {len(df)}")
print("\nQ1 - Top 3 agent_type by multimodal ratio:")
for idx, row in top3_agent.iterrows():
    print(f"  {idx+1}. {row['agent_type']}: {row['ratio']:.2%} ({int(row['multimodal_count'])}/{int(row['total_count'])})")

print("\nQ2 - Top 3 model_architecture by multimodal ratio:")
for idx, row in top3_model.iterrows():
    print(f"  {idx+1}. {row['model_architecture']}: {row['ratio']:.2%} ({int(row['multimodal_count'])}/{int(row['total_count'])})")

print("\nQ3 - Top 3 task_category by median bias_detection_score:")
for idx, row in top3_task.iterrows():
    print(f"  {idx+1}. {row['task_category']}: {row['median_bias_score']:.4f}")
