import csv

# 定义要写入的数据
data = [
    ['firstname', 'lastname', 'studentid'],
    ['Olivia', 'Smith', 57384926],
    ['Ethan', 'Johnson', 21873654],
    ['Ava', 'Brown', 69581237],
    ['Liam', 'Patel', 38492017],
    ['Sophia', 'Kim', 12659843],
    ['Jackson', 'James', 75982134],
    ['Isabella', 'Lee', 48273615],
    ['Lucas', 'Davis', 93746521],
    ['Mia', 'Singh', 65321847],
    ['Aiden', 'Garcia', 12345678],
    ['Harper', 'Chen', 59836214],
    ['Noah', 'Anderson', 23147568],
    ['Amelia', 'Martinez', 87654321],
    ['Mason', 'Wilson', 35968472],
    ['Evelyn', 'Nguyen', 76542139],
    ['Logan', 'Taylor', 14327586],
    ['William', 'Thomas', 62738495],
    ['Oliver', 'Hernandez', 91827346],
    ['Lily', 'Jackson', 54637218],
    ['Elijah', 'Moore', 48261735],
    ['Charlotte', 'White', 29584763],
    ['Carter', 'Harris', 71359482],
    ['Grace', 'Martin', 36478125],
    ['Lucas', 'Hall', 92867354],
    ['Zoe', 'Turner', 63721584],
    ['Caleb', 'Adams', 15483629],
    ['Scarlett', 'Scott', 87415932],
    ['Henry', 'King', 42658371],
    ['Madison', 'Baker', 59136248],
    ['Alexander', 'Perez', 38472659],
    ['Abigail', 'Jones', 17485932],
    ['Williams', 'James', 12345678]
]

# 指定要创建的CSV文件路径
csv_file_path = 'info.csv'

# 使用 'w' 模式打开文件，newline='' 用于避免写入的行之间出现额外的空行
with open(csv_file_path, mode='w', newline='') as file:
    # 创建CSV写入器
    csv_writer = csv.writer(file)

    # 使用 writerows 方法写入多行数据
    csv_writer.writerows(data)

print(f"CSV文件已创建并成功写入：{csv_file_path}")
