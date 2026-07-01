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

## 实验结果

### MSRA + bert-base-chinese

**最佳验证集 F1：0.9353**

测试集详细结果：

| 类别 | Precision | Recall | F1 | Support |
|------|-----------|--------|-----|---------|
| B-LOC | 0.98 | 0.95 | 0.97 | 643 |
| B-ORG | 0.97 | 0.91 | 0.94 | 323 |
| B-PER | 0.99 | 0.98 | 0.99 | 307 |
| I-LOC | 0.97 | 0.95 | 0.96 | 967 |
| I-ORG | 0.97 | 0.95 | 0.96 | - |
| I-PER | 0.99 | 0.99 | 0.99 | 558 |
| **Micro Avg** | **0.98** | **0.96** | **0.97** | **4141** |

训练曲线：

![训练loss](./images/train_loss.png)
![验证loss](./images/eval_loss.png)
![验证F1](./images/eval_f1.png)

**分析：**
- 人名（PER）识别效果最好，F1 达到 0.99
- 组织名（ORG）召回稍低（0.91），部分组织名被漏标
- 验证集 F1 稳定在 0.93 以上，没有明显过拟合

**配置：**
- 学习率：2e-5
- Dropout：0.2
- 训练轮数：30
- 对齐策略：ignore
