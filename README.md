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
| bert-base-chinese | MSRA | ignore | 0.9352 | 0.9218 |
| chinese-bert-wwm | MSRA | ignore | 0.9331 | 0.9134 |
| bert-base-chinese | Weibo | ignore | 0.7258 | 0.66172 |
| chinese-bert-wwm | Weibo | ignore | 0.7281 | 0.6875 |
| chinese-bert-wwm | Weibo | other | 0.7281 | 0.6875 |

### 2.1 MSRA + bert-base-chinese

测试集详细结果：

| 标签 | precision | recall | f1-score | support |
|:---|:---:|:---:|:---:|:---:|
| B-LOC | 0.98 | 0.95 | 0.97 | 643 |
| B-ORG | 0.97 | 0.91 | 0.94 | 323 |
| B-PER | 0.99 | 0.98 | 0.99 | 307 |
| I-LOC | 0.97 | 0.95 | 0.96 | 967 |
| I-ORG | 0.97 | 0.95 | 0.96 | 1343 |
| I-PER | 0.99 | 0.99 | 0.99 | 558 |
| 0 | 0.00 | 0.00 | 0.00 | 0 |
| **accuracy** | | | **0.96** | **4141** |
| **macro avg** | **0.84** | **0.82** | **0.83** | **4141** |
| **weighted avg** | **0.98** | **0.96** | **0.97** | **4141** |

**训练曲线**
<img width="481" height="383" alt="image" src="https://github.com/user-attachments/assets/a36917a5-33f9-4735-9546-9e6912c82ed1" />
<img width="1025" height="390" alt="image" src="https://github.com/user-attachments/assets/47321c13-7018-4b6b-bec6-ef209b0b5f68" />
<img width="492" height="372" alt="image" src="https://github.com/user-attachments/assets/ede39df5-406a-462f-809a-0c108cfffc41" />


---

### 2.2 MSRA + chinese-bert-wwm

测试集详细结果：
| 标签 | precision | recall | f1-score | support |
|:---|:---:|:---:|:---:|:---:|
| B-LOC | 0.99 | 0.96 | 0.98 | 643 |
| B-ORG | 0.98 | 0.96 | 0.97 | 323 |
| B-PER | 0.99 | 0.98 | 0.99 | 307 |
| I-LOC | 0.99 | 0.94 | 0.97 | 967 |
| I-ORG | 0.99 | 0.91 | 0.95 | 1343 |
| I-PER | 0.99 | 0.99 | 0.99 | 558 |
| 0 | 0.00 | 0.00 | 0.00 | 0 |
| **accuracy** | | | **0.95** | **4141** |
| **macro avg** | **0.85** | **0.82** | **0.83** | **4141** |
| **weighted avg** | **0.99** | **0.95** | **0.97** | **4141** |
**训练曲线**
<img width="467" height="372" alt="image" src="https://github.com/user-attachments/assets/764070a6-1ed2-4ef8-aecb-2130cd993853" />
<img width="947" height="377" alt="image" src="https://github.com/user-attachments/assets/6e9e9a20-96f7-4a1c-9a25-808296d73ad0" />
<img width="553" height="401" alt="image" src="https://github.com/user-attachments/assets/6882a6f8-e7a9-47d9-afde-ff346b23bfa1" />


---

### 2.3 Weibo + chinese-bert-wwm (align_type='ignore')


测试集详细结果：

| 标签 | precision | recall | f1-score | support |
|:---|:---:|:---:|:---:|:---:|
| B-GPE.NAM | 0.88 | 0.88 | 0.88 | 26 |
| B-GPE.NOM | 1.00 | 1.00 | 1.00 | 1 |
| B-LOC.NAM | 0.62 | 0.83 | 0.71 | 6 |
| B-LOC.NOM | 1.00 | 0.50 | 0.67 | 6 |
| B-ORG.NAM | 0.83 | 0.62 | 0.71 | 47 |
| B-ORG.NOM | 0.67 | 0.80 | 0.73 | 5 |
| B-PER.NAM | 0.97 | 0.85 | 0.91 | 89 |
| B-PER.NOM | 0.97 | 0.79 | 0.87 | 208 |
| I-GPE.NAM | 0.90 | 0.84 | 0.87 | 31 |
| I-GPE.NOM | 1.00 | 1.00 | 1.00 | 1 |
| I-LOC.NAM | 0.88 | 0.88 | 0.88 | 16 |
| I-LOC.NOM | 0.67 | 0.29 | 0.40 | 7 |
| I-ORG.NAM | 0.88 | 0.65 | 0.75 | 126 |
| I-ORG.NOM | 0.50 | 0.80 | 0.62 | 5 |
| I-PER.NAM | 0.96 | 0.85 | 0.90 | 155 |
| I-PER.NOM | 0.92 | 0.86 | 0.89 | 239 |
| 0 | 0.00 | 0.00 | 0.00 | 0 |
| **accuracy** | | | **0.80** | **968** |
| **macro avg** | **0.80** | **0.73** | **0.75** | **968** |
| **weighted avg** | **0.92** | **0.80** | **0.85** | **968** |

**训练曲线**
<img width="462" height="377" alt="image" src="https://github.com/user-attachments/assets/44a968a3-2ca8-4b7e-b377-350e9bc5478d" />
<img width="942" height="382" alt="image" src="https://github.com/user-attachments/assets/6913cb3d-9244-43ef-8528-45864da7226c" />
<img width="522" height="395" alt="image" src="https://github.com/user-attachments/assets/b9a63cd6-1b1e-434b-826c-0ff843a99148" />


---

### 2.4 Weibo + bert-base-chinese (align_type='ignore')

测试集详细结果：

| 标签 | precision | recall | f1-score | support |
|:---|:---:|:---:|:---:|:---:|
| B-GPE.NAM | 0.89 | 0.92 | 0.91 | 26 |
| B-GPE.NOM | 1.00 | 1.00 | 1.00 | 1 |
| B-LOC.NAM | 0.45 | 0.83 | 0.59 | 6 |
| B-LOC.NOM | 1.00 | 0.50 | 0.67 | 6 |
| B-ORG.NAM | 0.76 | 0.47 | 0.58 | 47 |
| B-ORG.NOM | 0.67 | 0.80 | 0.73 | 5 |
| B-PER.NAM | 0.96 | 0.79 | 0.86 | 89 |
| B-PER.NOM | 0.97 | 0.80 | 0.87 | 208 |
| I-GPE.NAM | 0.90 | 0.87 | 0.89 | 31 |
| I-GPE.NOM | 0.00 | 0.00 | 0.00 | 1 |
| I-LOC.NAM | 0.54 | 0.88 | 0.67 | 16 |
| I-LOC.NOM | 0.80 | 0.57 | 0.67 | 7 |
| I-ORG.NAM | 0.88 | 0.50 | 0.64 | 126 |
| I-ORG.NOM | 0.67 | 0.80 | 0.73 | 5 |
| I-PER.NAM | 0.97 | 0.82 | 0.89 | 155 |
| I-PER.NOM | 0.94 | 0.85 | 0.89 | 239 |
| 0 | 0.00 | 0.00 | 0.00 | 0 |
| **accuracy** | | | **0.76** | **968** |
| **macro avg** | **0.73** | **0.68** | **0.68** | **968** |
| **weighted avg** | **0.93** | **0.76** | **0.83** | **968** |
**训练曲线**
<img width="468" height="372" alt="image" src="https://github.com/user-attachments/assets/2d1e31d1-e25b-4546-94fd-42456c9fda0d" />
<img width="947" height="377" alt="image" src="https://github.com/user-attachments/assets/24b76e60-a82d-4110-b22c-51f82a374d7c" />
<img width="552" height="386" alt="image" src="https://github.com/user-attachments/assets/df065412-3cc5-4bdf-94a8-b753649e6f0e" />

### 2.5 Weibo + chinese-bert-wwm (align_type='other')

测试集详细结果：
| 标签 | precision | recall | f1-score | support |
|:---|:---:|:---:|:---:|:---:|
| B-GPE.NAM | 0.88 | 0.88 | 0.88 | 26 |
| B-GPE.NOM | 1.00 | 1.00 | 1.00 | 1 |
| B-LOC.NAM | 0.62 | 0.83 | 0.71 | 6 |
| B-LOC.NOM | 1.00 | 0.50 | 0.67 | 6 |
| B-ORG.NAM | 0.83 | 0.62 | 0.71 | 47 |
| B-ORG.NOM | 0.67 | 0.80 | 0.73 | 5 |
| B-PER.NAM | 0.97 | 0.85 | 0.91 | 89 |
| B-PER.NOM | 0.97 | 0.79 | 0.87 | 208 |
| I-GPE.NAM | 0.90 | 0.84 | 0.87 | 31 |
| I-GPE.NOM | 1.00 | 1.00 | 1.00 | 1 |
| I-LOC.NAM | 0.88 | 0.88 | 0.88 | 16 |
| I-LOC.NOM | 0.67 | 0.29 | 0.40 | 7 |
| I-ORG.NAM | 0.88 | 0.65 | 0.75 | 126 |
| I-ORG.NOM | 0.50 | 0.80 | 0.62 | 5 |
| I-PER.NAM | 0.96 | 0.85 | 0.90 | 155 |
| I-PER.NOM | 0.92 | 0.86 | 0.89 | 239 |
| 0 | 0.00 | 0.00 | 0.00 | 0 |
| **accuracy** | | | **0.80** | **968** |
| **macro avg** | **0.80** | **0.73** | **0.75** | **968** |
| **weighted avg** | **0.92** | **0.80** | **0.85** | **968** |
**训练曲线**
<img width="470" height="372" alt="image" src="https://github.com/user-attachments/assets/c62f9d85-50f3-480f-ad31-7f39bbf0ede7" />
<img width="942" height="377" alt="image" src="https://github.com/user-attachments/assets/800d260f-762c-41d7-a052-1969c333a541" />
<img width="611" height="360" alt="image" src="https://github.com/user-attachments/assets/c78a1cca-d624-4570-9183-738db04355b4" />


## 三、总结
从结果看，在规范的MSRA数据集上，bert-base-chinese和chinese-bert-wwm的表现都很好，测试F1都在0.91以上。但在Weibo数据上，性能下降很明显，F1值普遍在0.66-0.69之间，说明社交媒体文本的NER任务难度大很多。
对比模型，chinese-bert-wwm在Weibo上的表现比bert-base-chinese好一些，说明全词掩码在非规范文本上可能有点帮助。ignore和other两个方式结果完全一样，可能在这个场景下影响不大。
## 项目结构
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
