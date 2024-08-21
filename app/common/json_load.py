import json
from ..common.setting import DATA_FILE

def jsonLoad(new_data: dict):
    # 尝试追加单个 JSON 对象到文件
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            originalData = json.load(file)  # 加载现有数据

        # 直接向 originalData 的 "data" 键对应的列表追加新数据
        originalData["data"].append(new_data["data"])

        # 写回文件
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(originalData, file, ensure_ascii=False)

    except FileNotFoundError:
        print(f"文件 {DATA_FILE} 未找到。创建新文件并写入数据。")

    except json.JSONDecodeError:
        print(f"文件 {DATA_FILE} 不是有效的 JSON 格式。创建新数据结构。")
