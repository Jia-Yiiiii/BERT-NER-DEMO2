# BERT-NER-DEMO2
基于BERT的中文命名实体识别

---

## 数据分析

### MSRA 样本（新闻）

![MSRA数据样本](https://github.com/user-attachments/assets/54886593-1432-4c90-8653-c545491e2a62)

### Weibo 样本（微博）

![Weibo数据样本](https://github.com/user-attachments/assets/05fd8b16-5314-4161-91ac-4b05b4e72a2b)

### 两个数据集的区别

MSRA 只分 3 种实体（人名、地名、组织名），标签 7 种。

Weibo 分得更细，多出了 `.NAM`（具体名称）和 `.NOM`（指代）的区别，标签 17 种。

比如"马化腾"是 PER.NAM，"小马哥"是 PER.NOM。


![MSRA标签分布](https://github.com/user-attachments/assets/d9f893de-1136-4056-b433-4b5b35d4366b)


![Weibo标签分布](https://github.com/user-attachments/assets/8189df4a-7717-42f2-bc44-998c42e4379d)


