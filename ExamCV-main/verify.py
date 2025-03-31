import csv
import Levenshtein

def calculate_accuracy(reference, target):
    max_length = max(len(reference), len(target))
    distance = Levenshtein.distance(reference.lower(), target.lower())
    accuracy = 1 - (distance / max_length)
    return accuracy

def find_best_match(firstname, lastname, studentid):
    best_match = None
    result = []
    results = []
    csv_file_path = "info.csv"  # 替换为你的CSV文件路径
    # 打开CSV文件
    with open(csv_file_path, mode='r', encoding='utf-8-sig') as file:
        # 创建CSV读取器
        csv_reader = csv.DictReader(file)
        # 将CSV数据存储为列表，以便多次使用
        csv_data = list(csv_reader)    
        #print(csv_reader.fieldnames)
        best_average_accuracy = 0.1
        for row in csv_data:
            accuracy1 = calculate_accuracy(row["firstname"], firstname)
            accuracy2 = calculate_accuracy(row["lastname"], lastname)
            accuracy3 = calculate_accuracy(row["studentid"], studentid)

            average_accuracy = (accuracy1 + accuracy2 + accuracy3) / 3

            if average_accuracy > best_average_accuracy:
                best_match = [
                    row["firstname"],
                    row["lastname"],
                    row["studentid"]
                ]
                best_average_accuracy = average_accuracy

    return best_match
    

def verify(scores):
    total = 0
    for i in scores[:-1]:
        total = total + i
    if total == scores[-1]:
        return True
    else:
        return False