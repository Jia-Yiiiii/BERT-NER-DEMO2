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

### 2.1 MSRA + bert-base-chinese

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

**训练曲线**

<img width="602" height="338" alt="训练loss" src="https://github.com/user-attachments/assets/f2e5dac1-a160-48ca-b562-7a064ea601b6" />
<img width="1112" height="383" alt="验证曲线" src="https://github.com/user-attachments/assets/d161ba4b-4d08-45b3-9092-a1c0262afc42" />
<img width="686" height="416" alt="测试F1" src="https://github.com/user-attachments/assets/8529cbc0-c9e0-44cb-af13-ae77ebe75dc9" />

**结果分析**

- 人名（PER）识别效果最好，F1 达到 0.99，说明模型对名称类实体学习充分。
- 验证集 F1 稳定在 0.93 以上，训练过程中没有明显的过拟合现象。
- 组织名（ORG）召回率相对较低（0.91），部分组织名称可能被漏标，这是后续可以优化的方向。

---

### 2.2 MSRA + chinese-bert-wwm

**最佳验证集 F1：0.9332**

测试集详细结果：

| 类别 | Precision | Recall | F1 | Support |
|------|-----------|--------|-----|---------|
| B-LOC | 0.99 | 0.96 | 0.98 | 643 |
| B-ORG | 0.98 | 0.96 | 0.97 | 323 |
| B-PER | 0.99 | 0.98 | 0.99 | 307 |
| I-LOC | 0.99 | 0.94 | 0.97 | 967 |
| I-ORG | 0.99 | 0.91 | 0.95 | 1343 |
| I-PER | 0.99 | 0.99 | 0.99 | 558 |
| **Micro Avg** | **0.99** | **0.96** | **0.97** | **4141** |

**训练曲线**

<img width="498" height="312" alt="训练loss" src="https://github.com/user-attachments/assets/358ac79f-2790-4b06-9cd2-202f18a2f6eb" />
<img width="1011" height="321" alt="验证曲线" src="https://github.com/user-attachments/assets/86f9a963-df91-471f-bb79-b6a4a7d31b78" />
<img width="502" height="313" alt="测试F1" src="https://github.com/user-attachments/assets/48fe5a89-952a-47d2-aa3c-03cc9baeaaa8" />

**结果分析**

- 与 bert-base-chinese（0.9123）相比，chinese-bert-wwm 在 MSRA 上略高 0.0011。
- 全词掩码在规范的新闻文本上优势不明显。
- B-ORG 的召回稍有下降，但整体保持稳定。

---

### 2.3 Weibo + chinese-bert-wwm (align_type='ignore')

**最佳验证集 F1：0.7282**

测试集详细结果：

| 类别 | Precision | Recall | F1 | Support |
|------|-----------|--------|-----|---------|
| B-GPE.NAM | 0.84 | 0.89 | 0.86 | 46 |
| B-GPE.NOM | 0.00 | 0.00 | 0.00 | 2 |
| B-LOC.NAM | 0.58 | 0.37 | 0.45 | 19 |
| B-LOC.NOM | 1.00 | 0.44 | 0.62 | 9 |
| B-ORG.NAM | 0.58 | 0.54 | 0.56 | 39 |
| B-ORG.NOM | 0.85 | 0.69 | 0.76 | 16 |
| B-PER.NAM | 0.85 | 0.80 | 0.83 | 110 |
| B-PER.NOM | 0.93 | 0.77 | 0.85 | 167 |
| I-GPE.NAM | 0.87 | 0.87 | 0.87 | 60 |
| I-GPE.NOM | 0.00 | 0.00 | 0.00 | 2 |
| I-LOC.NAM | 0.76 | 0.36 | 0.48 | 45 |
| I-LOC.NOM | 0.75 | 0.40 | 0.52 | 15 |
| I-ORG.NAM | 0.69 | 0.61 | 0.65 | 100 |
| I-ORG.NOM | 0.67 | 0.67 | 0.67 | 21 |
| I-PER.NAM | 0.89 | 0.74 | 0.81 | 200 |
| I-PER.NOM | 0.89 | 0.83 | 0.86 | 213 |
| **Micro Avg** | **0.68** | **0.70** | **0.69** | **1072** |

**训练曲线**

<img width="497" height="317" alt="训练loss" src="https://github.com/user-attachments/assets/6a51f42b-171d-48e9-b50b-7eb07ddbd97b" />
<img width="1017" height="321" alt="验证曲线" src="https://github.com/user-attachments/assets/ab949485-427e-42e6-a7e4-00455e4c0e1b" />
<img width="498" height="318" alt="测试F1" src="https://github.com/user-attachments/assets/f1eff8c2-cb24-4055-9b93-29a3a1779523" />

**结果分析**

- GPE.NAM 识别最好（F1 0.86-0.87），地名和组织名（LOC.NAM、ORG.NAM）效果较差。
- GPE.NOM 和 I-GPE.NOM 为 0，因为测试集分别只有 2 个样本，模型学不到。
- 整体 F1 比 MSRA 低约 23 个点，说明 Weibo 口语化、标签细、数据少，难度大。

---

### 2.4 Weibo + bert-base-chinese (align_type='ignore')

**最佳验证集 F1：0.7259**

测试集详细结果：

| 类别 | Precision | Recall | F1 | Support |
|------|-----------|--------|-----|---------|
| B-GPE.NAM | 0.85 | 0.89 | 0.87 | 46 |
| B-GPE.NOM | 0.00 | 0.00 | 0.00 | 2 |
| B-LOC.NAM | 0.42 | 0.42 | 0.42 | 19 |
| B-LOC.NOM | 0.80 | 0.44 | 0.57 | 9 |
| B-ORG.NAM | 0.67 | 0.46 | 0.55 | 39 |
| B-ORG.NOM | 0.86 | 0.38 | 0.52 | 16 |
| B-PER.NAM | 0.84 | 0.77 | 0.81 | 110 |
| B-PER.NOM | 0.93 | 0.73 | 0.82 | 167 |
| I-GPE.NAM | 0.89 | 0.92 | 0.90 | 60 |
| I-GPE.NOM | 0.00 | 0.00 | 0.00 | 2 |
| I-LOC.NAM | 0.59 | 0.38 | 0.46 | 45 |
| I-LOC.NOM | 0.57 | 0.27 | 0.36 | 15 |
| I-ORG.NAM | 0.75 | 0.58 | 0.66 | 100 |
| I-ORG.NOM | 0.64 | 0.33 | 0.44 | 21 |
| I-PER.NAM | 0.87 | 0.71 | 0.78 | 200 |
| I-PER.NOM | 0.90 | 0.83 | 0.86 | 213 |
| **Micro Avg** | **0.67** | **0.66** | **0.66** | **1064** |

**训练曲线**

<img width="500" height="321" alt="训练loss" src="https://github.com/user-attachments/assets/6b1dbca4-7454-45b6-9801-b4f78df4eea0" />
<img width="1003" height="315" alt="验证曲线" src="https://github.com/user-attachments/assets/415cab02-1325-449e-8d41-5a2d03b84540" />
<img width="500" height="325" alt="测试F1" src="https://github.com/user-attachments/assets/6e5c8702-3f0a-47f1-aa89-96d8d3f0c920" />

**结果分析**

- GPE.NAM 识别最好（F1 0.87-0.90），地理实体相对规范。
- GPE.NOM 为 0，测试集仅 2 个样本，无法学习。
- 整体 F1 0.66，与 chinese-bert-wwm（0.69）接近，两个模型在 Weibo 上差距不大。

---

### 2.5 Weibo + chinese-bert-wwm (align_type='other')

**最佳验证集 F1：0.7259**

测试集详细结果：

| 类别 | Precision | Recall | F1 | Support |
|------|-----------|--------|-----|---------|
| B-GPE.NAM | 0.85 | 0.89 | 0.87 | 46 |
| B-GPE.NOM | 0.00 | 0.00 | 0.00 | 2 |
| B-LOC.NAM | 0.42 | 0.42 | 0.42 | 19 |
| B-LOC.NOM | 0.80 | 0.44 | 0.57 | 9 |
| B-ORG.NAM | 0.67 | 0.46 | 0.55 | 39 |
| B-ORG.NOM | 0.86 | 0.38 | 0.52 | 16 |
| B-PER.NAM | 0.84 | 0.77 | 0.81 | 110 |
| B-PER.NOM | 0.93 | 0.73 | 0.82 | 167 |
| I-GPE.NAM | 0.89 | 0.92 | 0.90 | 60 |
| I-GPE.NOM | 0.00 | 0.00 | 0.00 | 2 |
| I-LOC.NAM | 0.59 | 0.38 | 0.46 | 45 |
| I-LOC.NOM | 0.57 | 0.27 | 0.36 | 15 |
| I-ORG.NAM | 0.75 | 0.58 | 0.66 | 100 |
| I-ORG.NOM | 0.64 | 0.33 | 0.44 | 21 |
| I-PER.NAM | 0.87 | 0.71 | 0.78 | 200 |
| I-PER.NOM | 0.90 | 0.83 | 0.86 | 213 |
| **Micro Avg** | **0.67** | **0.66** | **0.66** | **1064** |

**训练曲线**

<img width="495" height="317" alt="训练loss" src="https://github.com/user-attachments/assets/93f392fb-2ca9-47d0-b319-ed4317dacd66" />
<img width="1007" height="317" alt="验证曲线" src="https://github.com/user-attachments/assets/85779d5d-9b18-4113-a5ad-339fca163cbf" />
<img width="497" height="317" alt="测试F1" src="https://github.com/user-attachments/assets/3e09bb9b-b28b-488c-85f9-d10c03ec3cee" />

**结果分析**

- 与 align_type='ignore'（0.69）相比，other 策略（0.66）略低，说明在数据量小的情况下，保守的 ignore 策略更好。
## 三、总结

实验表明，在规范新闻语料（MSRA）上，BERT 系列模型能达到很高的 F1，且不同模型间差距很小。在口语化的社交媒体文本（Weibo）上，性能显著下降至 0.66-0.69。此外，对比 `ignore` 和 `other` 两种子词对齐策略，后者在 Weibo 上有微弱提升，但整体影响有限。
