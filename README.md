# 基于 BERT 的中文命名实体识别

本项目使用 BERT 模型在 **MSRA** 和 **Weibo** 两个中文数据集上进行命名实体识别（NER）实验，并对比了不同模型和标签对齐策略的效果。

---

## 一、数据分析

### 1.1 数据格式

MSRA 用 `0` 分隔句子，Weibo 用空行。代码中通过判断 `line == '' or line == '0'` 同时兼容两种格式。

两个数据集的标签体系不同：

- **MSRA**：标签为 `B-LOC` 形式，共 7 种。
- **Weibo**：标签为 `B-LOC.NAM` 形式，增加了 `.NAM`（具体名称）和 `.NOM`（指代）的区分，共 17 种。

因此，在代码中为两个数据集**分别建立了独立的 `label2id` 映射**，不共用标签体系。

### 1.2 标签分布

**MSRA 训练集标签分布**

| 标签 | 数量 |
|------|------|
| O | 206412 |
| I-ORG | 9141 |
| I-LOC | 5313 |
| B-LOC | 3952 |
| I-PER | 3612 |
| B-ORG | 2158 |
| B-PER | 1850 |

**Weibo 训练集标签分布**

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

### 1.3 数据处理

<img width="832" height="327" alt="image" src="https://github.com/user-attachments/assets/8facc656-a167-4d23-aa6a-984fbd225345" />
<img width="617" height="330" alt="image" src="https://github.com/user-attachments/assets/c9db921c-50a5-4b22-b3d2-8df0a501a530" />

1. 读取时兼容 MSRA（`0` 分隔）和 Weibo（空行分隔）两种格式。
2. 自动从数据中构建标签映射。MSRA 和 Weibo 标签体系不同，代码分别生成各自的 label2id，不共用。
3. BERT 分词会产生子词，导致标签数量对不上。使用 `word_ids` 对齐，只保留每个词首个子词的原始标签，后续子词标 `O` 忽略。同时也支持标签传播策略（`other`），用于对比实验。

---

## 二、实验结果

### 整体结果对比

| 模型 | 数据集 | 对齐策略 | 最佳验证 F1 | 测试集 F1 |
|------|--------|----------|-------------|-----------|
| bert-base-chinese | MSRA | ignore | 0.9263| 0.9192 |
| chinese-bert-wwm | MSRA | ignore | 0.9403 | 0.9095 |
| bert-base-chinese | Weibo | ignore | 0.7268 | 0.6594 |
| chinese-bert-wwm | Weibo | ignore | 0.7270 | 0.6745 |
| chinese-bert-wwm | Weibo | other | 0.7270 | 0.6745 |

### 2.1 MSRA + bert-base-chinese

测试集详细结果：

| 实体类型 | Precision | Recall | F1-score | Support |
|----------|-----------|--------|----------|---------|
| LOC      | 94.52%    | 93.93% | 94.23%   | 643     |
| ORG      | 80.54%    | 92.26% | 86.00%   | 323     |
| PER      | 96.14%    | 97.39% | 96.76%   | 307     |
| micro avg | 90.98%   | 94.34% | 92.63%   | 1273    |
| macro avg | 90.40%   | 94.53% | 92.33%   | 1273    |
| weighted avg | 91.37% | 94.34% | 92.75% | 1273    |

**训练曲线**

<img width="467" height="392" alt="image" src="https://github.com/user-attachments/assets/13d9e893-6456-4800-9753-94b4d6a82027" />
<img width="972" height="398" alt="image" src="https://github.com/user-attachments/assets/60285f6a-9f89-4c78-b8f9-18adc9c0685d" />
<img width="653" height="441" alt="image" src="https://github.com/user-attachments/assets/04c449bf-3ba4-4228-b5dd-c077e5712272" />


---

### 2.2 MSRA + chinese-bert-wwm

测试集详细结果：



| 实体类型 | Precision | Recall | F1-score | Support |
|----------|-----------|--------|----------|---------|
| LOC（地点） | 95.72% | 93.93% | 94.82% | 643 |
| ORG（组织） | 87.24% | 91.02% | 89.09% | 323 |
| PER（人名） | 97.41% | 98.05% | 97.73% | 307 |
| **micro avg** | **93.89%** | **94.19%** | **94.04%** | **1273** |
| **macro avg** | **93.46%** | **94.33%** | **93.88%** | **1273** |
| **weighted avg** | **93.98%** | **94.19%** | **94.07%** | **1273** |

**训练曲线**

<img width="468" height="386" alt="image" src="https://github.com/user-attachments/assets/701595da-3848-40a5-9c30-1727fbdf2616" />
<img width="971" height="407" alt="image" src="https://github.com/user-attachments/assets/9b01558d-ff2b-4d9a-a4f8-711f84cacd34" />
<img width="560" height="458" alt="image" src="https://github.com/user-attachments/assets/841072a6-d4a4-4657-88fc-532e31f28cbd" />



---

### 2.3 Weibo + chinese-bert-wwm (align_type='ignore')

测试集详细结果：

| 标签 | precision | recall | f1-score | support |
|------|-----------|--------|----------|---------|
| B-GPE.NAM | 0.79 | 0.88 | 0.84 | 26 |
| B-GPE.NOM | 1.00 | 1.00 | 1.00 | 1 |
| B-LOC.NAM | 0.62 | 0.83 | 0.71 | 6 |
| B-LOC.NOM | 0.75 | 0.50 | 0.60 | 6 |
| B-ORG.NAM | 0.81 | 0.45 | 0.58 | 47 |
| B-ORG.NOM | 0.57 | 0.80 | 0.67 | 5 |
| B-PER.NAM | 0.95 | 0.83 | 0.89 | 89 |
| B-PER.NOM | 0.97 | 0.84 | 0.90 | 208 |
| I-GPE.NAM | 0.74 | 0.84 | 0.79 | 31 |
| I-GPE.NOM | 1.00 | 1.00 | 1.00 | 1 |
| I-LOC.NAM | 0.70 | 0.88 | 0.78 | 16 |
| I-LOC.NOM | 0.75 | 0.43 | 0.55 | 7 |
| I-ORG.NAM | 0.89 | 0.47 | 0.61 | 126 |
| I-ORG.NOM | 0.67 | 0.80 | 0.73 | 5 |
| I-PER.NAM | 0.99 | 0.80 | 0.89 | 155 |
| I-PER.NOM | 0.92 | 0.90 | 0.91 | 239 |
| O | 0.00 | 0.00 | 0.00 | 0 |
| **accuracy** | | | **0.78** | **968** |
| **macro avg** | **0.77** | **0.72** | **0.73** | **968** |
| **weighted avg** | **0.92** | **0.78** | **0.83** | **968** |

**训练曲线**

<img width="475" height="381" alt="image" src="https://github.com/user-attachments/assets/7bca32f2-f647-406f-b5ed-d4ec0839ea0c" />
<img width="942" height="383" alt="image" src="https://github.com/user-attachments/assets/47424f8b-807b-4541-8d08-cdd5c8ba041f" />
<img width="491" height="373" alt="image" src="https://github.com/user-attachments/assets/b9dd3ff8-5f00-4a9a-829d-db09132428ca" />


---

### 2.4 Weibo + bert-base-chinese (align_type='ignore')

测试集详细结果：

| 标签 | precision | recall | f1-score | support |
|------|-----------|--------|----------|---------|
| B-GPE.NAM | 0.88 | 0.88 | 0.88 | 26 |
| B-GPE.NOM | 1.00 | 1.00 | 1.00 | 1 |
| B-LOC.NAM | 0.45 | 0.83 | 0.59 | 6 |
| B-LOC.NOM | 1.00 | 0.83 | 0.91 | 6 |
| B-ORG.NAM | 0.71 | 0.47 | 0.56 | 47 |
| B-ORG.NOM | 0.80 | 0.80 | 0.80 | 5 |
| B-PER.NAM | 0.95 | 0.82 | 0.88 | 89 |
| B-PER.NOM | 0.95 | 0.82 | 0.88 | 208 |
| I-GPE.NAM | 0.91 | 0.94 | 0.92 | 31 |
| I-GPE.NOM | 0.00 | 0.00 | 0.00 | 1 |
| I-LOC.NAM | 0.54 | 0.88 | 0.67 | 16 |
| I-LOC.NOM | 1.00 | 1.00 | 1.00 | 7 |
| I-ORG.NAM | 0.91 | 0.48 | 0.62 | 126 |
| I-ORG.NOM | 1.00 | 0.80 | 0.89 | 5 |
| I-PER.NAM | 0.96 | 0.79 | 0.87 | 155 |
| I-PER.NOM | 0.93 | 0.87 | 0.90 | 239 |
| O | 0.00 | 0.00 | 0.00 | 0 |
| **accuracy** | | | **0.77** | **968** |
| **macro avg** | **0.76** | **0.72** | **0.73** | **968** |
| **weighted avg** | **0.92** | **0.77** | **0.83** | **968** |

**训练曲线**

<img width="495" height="396" alt="image" src="https://github.com/user-attachments/assets/60df5fc1-a1e4-43a1-bf9e-7332aba2f018" />
<img width="982" height="400" alt="image" src="https://github.com/user-attachments/assets/0af548b3-7218-442a-9fb9-6291acb60734" />
<img width="476" height="387" alt="image" src="https://github.com/user-attachments/assets/17797a7b-e6fc-455a-8bd9-3cbd2334a6a8" />


### 2.5 Weibo + chinese-bert-wwm (align_type='other')

测试集详细结果：

| 标签 | precision | recall | f1-score | support |
|------|-----------|--------|----------|---------|
| B-GPE.NAM | 0.79 | 0.88 | 0.84 | 26 |
| B-GPE.NOM | 1.00 | 1.00 | 1.00 | 1 |
| B-LOC.NAM | 0.62 | 0.83 | 0.71 | 6 |
| B-LOC.NOM | 0.75 | 0.50 | 0.60 | 6 |
| B-ORG.NAM | 0.81 | 0.45 | 0.58 | 47 |
| B-ORG.NOM | 0.57 | 0.80 | 0.67 | 5 |
| B-PER.NAM | 0.95 | 0.83 | 0.89 | 89 |
| B-PER.NOM | 0.97 | 0.84 | 0.90 | 208 |
| I-GPE.NAM | 0.74 | 0.84 | 0.79 | 31 |
| I-GPE.NOM | 1.00 | 1.00 | 1.00 | 1 |
| I-LOC.NAM | 0.70 | 0.88 | 0.78 | 16 |
| I-LOC.NOM | 0.75 | 0.43 | 0.55 | 7 |
| I-ORG.NAM | 0.89 | 0.47 | 0.61 | 126 |
| I-ORG.NOM | 0.67 | 0.80 | 0.73 | 5 |
| I-PER.NAM | 0.99 | 0.80 | 0.89 | 155 |
| I-PER.NOM | 0.92 | 0.90 | 0.91 | 239 |
| O | 0.00 | 0.00 | 0.00 | 0 |
| **accuracy** | | | **0.78** | **968** |
| **macro avg** | **0.77** | **0.72** | **0.73** | **968** |
| **weighted avg** | **0.92** | **0.78** | **0.83** | **968** |

**训练曲线**

<img width="462" height="377" alt="image" src="https://github.com/user-attachments/assets/41141296-a92d-4e58-b5f3-c0ef497add41" />
<img width="955" height="380" alt="image" src="https://github.com/user-attachments/assets/7acdb971-ee0a-4d90-87af-c6ecf3d1636d" />
<img width="523" height="397" alt="image" src="https://github.com/user-attachments/assets/f8b23c98-1dee-4934-a5bf-828f36ecfb99" />


---

## 三、总结

从结果看，在规范的MSRA数据集上，bert-base-chinese和chinese-bert-wwm的表现都很好，测试F1都在0.91以上。但在Weibo数据上，性能下降很明显，F1值普遍在0.66-0.69之间，说明社交媒体文本的NER任务难度大很多。

对比模型，chinese-bert-wwm在Weibo上的表现比bert-base-chinese好一些，说明全词掩码在非规范文本上可能有点帮助。ignore和other两个方式结果完全一样，可能在这个场景下影响不大。

## 项目结构

```text
BERT-NER-DEMO2/
├── DATA/
│ ├── MSRA/
│ │ ├── train.txt
│ │ ├── dev.txt
│ │ └── test.txt
│ └── weibo/
│ ├── train.txt
│ ├── dev.txt
│ └── test.txt
├── configs/
│ └── Bert_Config_exp1.json
├── data.py
├── model.py
├── trainer.py
├── utils.py
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
