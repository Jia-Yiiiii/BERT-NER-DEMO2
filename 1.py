from collections import Counter


def read_data(file_path):
    data = []
    tokens, labels = [], []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line == '' or line == '0':
                if tokens:
                    data.append((tokens, labels))
                    tokens, labels = [], []
                continue
            parts = line.split()
            if len(parts) >= 2:
                tokens.append(parts[0])
                labels.append(parts[1] if parts[1] != '0' else 'O')
    if tokens:
        data.append((tokens, labels))
    return data


def analyze_dataset(file_path, name):
    data = read_data(file_path)
    all_labels = []
    for tokens, labels in data:
        all_labels.extend(labels)

    print(f"{name}:")
    print(f"  句子数: {len(data)}")
    print(f"  标签种类: {len(set(all_labels))}")
    print("  标签分布:")
    for label, count in Counter(all_labels).most_common():
        print(f"    {label}: {count}")

    # 打印前3个样本
    print("\n  前3个样本:")
    for i in range(min(3, len(data))):
        tokens, labels = data[i]
        print(f"    样本{i + 1}: {''.join(tokens)}")
        print(f"      词数: {len(tokens)}")
        for j in range(min(10, len(tokens))):
            print(f"        {tokens[j]} -> {labels[j]}")
        if len(tokens) > 10:
            print("        ...")
    print()


msra_path = "D:/4c/实战 Demo 指南/数据集/1.demo2实体识别/MSRA/train_5k.txt"
weibo_path = "D:/4c/实战 Demo 指南/数据集/1.demo2实体识别/weibo/train.txt"

analyze_dataset(msra_path, "MSRA 训练集")
analyze_dataset(weibo_path, "Weibo 训练集")