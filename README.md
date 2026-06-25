# BERT-NER-DEMO2
基于BERT的中文命名实体识别

---

## 数据分析

### MSRA 样本（新闻）

![MSRA数据样本](https://github.com/user-attachments/assets/54886593-1432-4c90-8653-c545491e2a62)
"北戴河"是地名，标成 B-LOC、I-LOC、I-LOC。

### Weibo 样本（微博）

![Weibo数据样本](https://github.com/user-attachments/assets/05fd8b16-5314-4161-91ac-4b05b4e72a2b)
女 B-PER.NOM
人 I-PER.NOM

text

"女人"是人称指代，标 B-PER.NOM、I-PER.NOM。

### 两个数据集的区别

MSRA 只分 3 种实体（人名、地名、组织名），标签 7 种。

Weibo 分得更细，多出了 `.NAM`（具体名称）和 `.NOM`（指代）的区别，标签 17 种。

比如"马化腾"是 PER.NAM，"小马哥"是 PER.NOM。

### 标签分布

![MSRA标签分布](https://github.com/user-attachments/assets/d9f893de-1136-4056-b433-4b5b35d4366b)

| 标签 | 数量 |
|------|------|
| O | 206412 |
| I-ORG | 9141 |
| I-LOC | 5313 |
| B-LOC | 3952 |
| I-PER | 3612 |
| B-ORG | 2158 |
| B-PER | 1850 |

MSRA 的 O 占绝大多数，实体里 I-ORG 最多，B-PER 最少。

![Weibo标签分布](https://github.com/user-attachments/assets/8189df4a-7717-42f2-bc44-998c42e4379d)

| 标签 | 数量 |
|------|------|
| O | 68777 |
| I-PER.NOM | 1043 |
| I-PER.NAM | 1041 |
| B-PER.NOM | 766 |
| B-PER.NAM | 574 |
| I-ORG.NAM | 477 |
| I-GPE.NAM | 241 |
| B-GPE.NAM | 205 |
| B-ORG.NAM | 183 |
| I-LOC.NAM | 129 |
| I-LOC.NOM | 66 |
| I-ORG.NOM | 61 |
| B-LOC.NAM | 56 |
| B-LOC.NOM | 51 |
| B-ORG.NOM | 42 |
| B-GPE.NOM | 8 |
| I-GPE.NOM | 8 |

Weibo 也是 O 最多，实体里 I-PER.NOM 最多，B-GPE.NOM 和 I-GPE.NOM 最少（各 8 个），说明地点指代很少。
