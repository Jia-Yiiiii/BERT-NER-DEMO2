# BERT-NER-DEMO2
基于BERT的中文命名实体识别

---

## 数据分析

### MSRA 样本（新闻）
| 标签 | 数量 |
|------|------|
| O | 206412 |
| I-ORG | 9141 |
| I-LOC | 5313 |
| B-LOC | 3952 |
| I-PER | 3612 |
| B-ORG | 2158 |
| B-PER | 1850 |

### Weibo 样本（微博）
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

### 两个数据集的区别
MSRA 只分 3 种实体（人名、地名、组织名），标签 7 种。
Weibo 分得更细，多出了 `.NAM`（具体名称）和 `.NOM`（指代）的区别，标签 17 种。


## 数据处理
### 1. 两个数据集格式不一样
MSRA 用 `0` 分隔句子，Weibo 用空行。代码里同时判断 `line == '' or line == '0'`。
### 2. 标签不一样
MSRA 是 `B-LOC`，Weibo 是 `B-LOC.NAM`，所以分别建 label2id。
![MSRA标签分布](https://github.com/user-attachments/assets/d9f893de-1136-4056-b433-4b5b35d4366b)
![Weibo标签分布](https://github.com/user-attachments/assets/8189df4a-7717-42f2-bc44-998c42e4379d)

### 3. 子词对齐
BERT 会把词分的很细，因此只保留第一个子词的标签，其余标 O 忽略。


