# 基于 BERT 的中文命名实体识别

本项目使用 BERT 模型在 **MSRA** 和 **Weibo** 两个中文数据集上进行命名实体识别（NER）实验，并对比了不同模型和标签对齐策略的效果。

## 数据分析

### 数据格式
MSRA 用 `0` 分隔句子，Weibo 用空行。代码中通过判断 `line == '' or line == '0'` 同时兼容两种格式。

两个数据集的标签体系不同：
*   **MSRA**：标签为 `B-LOC` 形式，共 7 种。
*   **Weibo**：标签为 `B-LOC.NAM` 形式，增加了 `.NAM`（具体名称）和 `.NOM`（指代）的区分，共 17 种。

因此，在代码中为两个数据集**分别建立了独立的 `label2id` 映射**，不共用标签体系。

### 标签分布

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

## 数据处理特点

1.  **兼容不同数据格式**：统一的数据读取函数同时处理 MSRA（`0` 分隔）和 Weibo（空行分隔）的数据格式。
2.  **独立标签映射**：由于标签体系不同，MSRA 和 Weibo 分别构建自己的 `label2id` 映射表。
3.  **子词对齐策略**：针对 BERT 分词器将词切分为子词（subtoken）的问题，采用 **“忽略策略”**。即仅保留每个词第一个子词的原始标签，其余子词标注为 `O`（在损失计算中被忽略），避免标签冲突。

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
### 训练曲线
<img width="602" height="338" alt="16e51ab98de36d90c1c3829a86061ce4" src="https://github.com/user-attachments/assets/f2e5dac1-a160-48ca-b562-7a064ea601b6" />
<img width="1112" height="383" alt="78dc19eaa75e60db649ea489df90982d" src="https://github.com/user-attachments/assets/d161ba4b-4d08-45b3-9092-a1c0262afc42" />
<img width="686" height="416" alt="93be1c039abd130067117a65abd1afc6" src="https://github.com/user-attachments/assets/8529cbc0-c9e0-44cb-af13-ae77ebe75dc9" />

### 结果分析
*   **人名（PER）识别效果最好**，F1 达到 0.99，说明模型对名称类实体学习充分。
*   **验证集 F1 稳定在 0.93 以上**，训练过程中没有明显的过拟合现象。
*   **组织名（ORG）召回率相对较低**（0.91），部分组织名称可能被漏标，这是后续可以优化的方向。

### MSRA + chinese-bert-wwm

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

**训练曲线：**
<img width="498" height="312" alt="156b0daf00097be9ba7ef68cf9e55f5e" src="https://github.com/user-attachments/assets/358ac79f-2790-4b06-9cd2-202f18a2f6eb" />
<img width="1011" height="321" alt="e28d5a82a684d654be008529677c2ae7" src="https://github.com/user-attachments/assets/86f9a963-df91-471f-bb79-b6a4a7d31b78" />
<img width="502" height="313" alt="2f54946235817c25238570981e938870" src="https://github.com/user-attachments/assets/48fe5a89-952a-47d2-aa3c-03cc9baeaaa8" />

**分析：**
- 与 bert-base-chinese（0.9123）相比，chinese-bert-wwm 在 MSRA 上略高 0.0011
- 全词掩码在规范的新闻文本上优势不明显
- B-ORG 的召回稍有下降，但整体保持稳定
## 待完成实验
- [ ] MSRA + chinese-bert-wwm
- [ ] Weibo + bert-base-chinese
- [ ] Weibo + chinese-bert-wwm
- [ ] 尝试标签传播策略（`align_type='other'`）对比效果
