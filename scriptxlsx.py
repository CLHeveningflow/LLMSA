import pandas as pd

# 读取文件‘Saga全量模板.xlsx’，获取‘深度分析（SAGA）全量模板’这个sheet的内容并输出
file_path = 'Saga全量模板.xlsx'
sheet_name = '深度分析（SAGA）全量模板'

# 使用pandas读取Excel文件
df = pd.read_excel(file_path, sheet_name=sheet_name)

# 提取所需列并转换为字典
result_dict = {}
for index, row in df.iterrows():
    rule_id = row['规则ID']
    rule_name = row['规则名称']
    description = row['规则描述']
    if not isinstance(description, str):
        continue
    result_dict[rule_id] = [rule_name, description]

# 将字典保存到json文件
import json
with open('rules.json', 'w', encoding='utf-8') as json_file:
    json.dump(result_dict, json_file, ensure_ascii=False, indent=4)
