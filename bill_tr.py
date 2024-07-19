import csv
import uuid
import json
import argparse

# 定义要提取的列的索引
column_indices = [0, 2, 3, 5]

# 存储提取的数据的数组
data_array = []

# UUID 生成函数
def generate_uuid():
    return str(uuid.uuid4()).upper()

# 定义匹配规则的数组，每个规则包含关键字和对应类别
match_rules = [
    {"keywords": ["滴滴","中铁网络","火车票"], "category": "交通"},
    {"keywords": ["停车"], "category": "车"},
    {"keywords": ["中国石化"], "category": "车"},
    {"keywords": ["明哥"], "category": "车"},
    {"keywords": ["汽车"], "category": "车"},
    {"keywords": ["电费"], "category": "水电煤费"},
    {"keywords": ["京东","拼多多","Jd Health"], "category": "网购"},
    {"keywords": ["开市客"], "category": "购物"},
    {"keywords": ["宜得利"], "category": "购物"},
    {"keywords": ["逸刻"], "category": "餐饮"},
    {"keywords": ["餐饮店"], "category": "餐饮"},
    {"keywords": ["顾村煎饼"], "category": "餐饮"},
    {"keywords": ["汐尘弄日本料理"], "category": "餐饮"},
    {"keywords": ["小碗菜"], "category": "餐饮"},
    {"keywords": ["卓驿"], "category": "餐饮"},
    {"keywords": ["咖啡馆"], "category": "餐饮"},
    {"keywords": ["馬記永"], "category": "餐饮"},
    {"keywords": ["溢香源"], "category": "餐饮"},
    {"keywords": ["石膳家"], "category": "餐饮"},
    {"keywords": ["川流不息"], "category": "餐饮"},
    {"keywords": ["肥田仔"], "category": "餐饮"},
    {"keywords": ["大米先生"], "category": "餐饮"},
    {"keywords": ["老乡鸡"], "category": "餐饮"},
    {"keywords": ["杨国福"], "category": "餐饮"},
    {"keywords": ["酷味乐"], "category": "餐饮"},
    {"keywords": ["LAWSON"], "category": "餐饮"},
    {"keywords": ["慕名沙龙"], "category": "服务"},
    {"keywords": ["顺丰速运"], "category": "服务"},
    {"keywords": ["喜欢作者"], "category": "文体娱"},
    {"keywords": ["医院"], "category": "医疗"},
    # 可以根据需要添加更多规则
]

# 自定义的用于确定类别的子函数
def determine_category(detail, cost):
    if "餐" in detail and float(cost) < 100:
        return "餐饮"
    if "大众点评" in detail and float(cost) < 100:
        return "餐饮"
    for rule in match_rules:
        if any(keyword in detail for keyword in rule["keywords"]):
            return rule["category"]
    return "支付"  # 默认类别


# 解析命令行参数
parser = argparse.ArgumentParser(description='Process CSV and output JSON.')

parser.add_argument('input_file', type=str, help='The input CSV file path')
parser.add_argument('output_file', type=str, help='The output JSON file path')

args = parser.parse_args()

with open(args.input_file, encoding='utf-8') as f:
    reader = csv.reader(f)
    # 跳过前17行
    for _ in range(17):
        next(reader)

    header = next(reader)  # 跳过表头
    
    for row in reader:
        # 提取指定列的数据并存储到数组
        selected_data = [row[i].replace('¥', '') if i == 5 else row[i] for i in column_indices]
        data_array.append(selected_data)

# 构建JSON数组
expenses = []

for data in data_array:

    detail = f"{data[1]} {data[2]}"
    category = determine_category(detail,data[3])

    expense = {
        "uuid": generate_uuid(),
        "timezone": "Asia/Shanghai",
        "detail": detail,
        "datetime": data[0],
        "category": category,
        "cost": f"{data[3]}"
    }
    expenses.append(expense)

# 构建最终的JSON格式
final_output = {
    "version": "1.1",
    "expenses": expenses
}

# 写入 JSON 文件
with open(args.output_file, 'w', encoding='utf-8') as f:
    json.dump(final_output, f, indent=2, ensure_ascii=False)

print(f"JSON data has been written to {args.output_file}")
