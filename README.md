# RSNA Knee Abnormality Detection

2026 RSNA 膝关节 MRI 异常检测比赛的可复现实验项目。当前已完成**阶段 0：准备环境与理解比赛**和**阶段 1：CSV 探索分析**，下一步进入阶段 2 DICOM 与 MRI 序列管线。

## 当前进度

### 阶段 0：环境与项目准备——已完成

- [x] 建立可复现项目骨架与 Git 工作流
- [x] 验证 Python、PyTorch 和 Apple MPS
- [x] 建立配置、实验记录与基础测试
- [x] 整理比赛目标、约束和最低成功标准

### 阶段 1：CSV 探索分析——已完成

- [x] 将5个原始 CSV 放入 `data/raw/`，并确认不会提交到 Git
- [x] 检查病例ID、序列ID、重复记录、缺失值及表间关联
- [x] 分析12类人工标签的阳性数、阳性率和缺失率
- [x] 分析标签共现次数和 Phi 相关性
- [x] 在 `notebooks/01_eda.ipynb` 中保存图表与文字结论
- [x] 分析每病例序列数和 Sagittal、Coronal、Axial 覆盖情况
- [x] 分析 `Anatomical_Plane × Fluid_Sensitive × Fat_Suppression`
- [x] 比较人工标注病例与无人工标签病例
- [x] 分析报告长度、语言、重复及否定/不确定表达
- [x] 汇总10条会影响验证、采样或建模的核心结论
- [x] 从空内核完整执行31个代码单元格，确认无错误输出

### 已确认的数据事实

- `train.csv` 包含4,407个唯一病例，`train_series.csv` 包含24,371个唯一序列，所有训练病例都能关联到序列。
- 只有58个病例拥有完整的12类人工标签；其余4,349个病例的12类标签全部缺失，没有部分缺失病例。
- 12类已标注值只有0和1，因此缺失标签不能填充为0。
- 人工标注病例中，Effusion 阳性最多（35/58，60.3%），MCL 阳性最少（9/58，15.5%）。
- 人工标签覆盖率仅1.32%，后续验证必须固定病例级多标签分层 fold，并逐折检查各类阳性数。
- 每病例包含3–14个序列，三种解剖平面覆盖率均为100%；`Fluid_Sensitive`与`Fat_Suppression`在当前数据中完全一致。
- 全部病例都有报告，共检测到9种语言；标准化后有54组重复报告模板，涉及204个病例。
- 约76.95%的报告包含初步否定表达，22.99%包含不确定表达，弱标签必须保留作用域和Unknown状态。
- 当前测试 CSV 只有3个示例病例；Kaggle Code Competition 正式推理时会使用隐藏测试集。

## 阶段 0 状态

- [x] 建立标准项目目录和 Git 仓库
- [x] 复用并验证现有 Anaconda Python 环境
- [x] 验证 PyTorch 与本机加速后端
- [x] 固定基础配置、随机种子和路径
- [x] 建立实验记录模板
- [x] 记录算力、时间预算和最低成功标准
- [x] 登录 Kaggle、接受比赛规则并取得官方 CSV 数据
- [ ] 每次提交前重新逐项复核 Overview、Data、Rules

最后一项是贯穿比赛的提交前检查，不影响阶段 0 的工程验收。

## 比赛理解

### 已从官方公开页面确认

- 任务是利用膝关节 MRI 检测异常。
- 训练数据结合 MRI 影像与原始放射学报告，是 RSNA 首次采用影像与报告文本的 AI Challenge。
- 官方介绍称数据包含超过 5,000 例膝关节 MRI，来自多家机构，报告覆盖 9 种语言。
- 比赛在 2026 年启动并于 10 月结束。

官方入口：

- [Kaggle 比赛页面](https://www.kaggle.com/competitions/rsna-knee-abnormality-detection)
- [RSNA Knee MRI AI Challenge](https://www.rsna.org/artificial-intelligence/ai-image-challenge/knee-mri-ai-challenge)

### 来自项目行动指南、需在 Kaggle 登录后复核

- 预测目标为 12 个异常标签，属于病例级多标签分类。
- 指标为 12 类 ROC-AUC 的宏平均。
- 同一 `StudyInstanceUID` 的不同序列不得跨训练集和验证集。
- 报告可以辅助训练，但测试集没有报告，最终推理必须能够只使用影像。
- 指南按 Kaggle Code Competition 的离线推理和 9 小时预算规划。

若 Kaggle 当前页面与 `guide.docx` 不一致，以 Kaggle 的 Overview、Data 和 Rules 为准，并同步更新本 README。

## 关键概念

- **多标签分类**：同一病例可能同时存在多个异常，每个标签独立输出概率。
- **ROC-AUC**：衡量模型把阳性病例排在阴性病例之前的能力；类别极不平衡时仍需同时报告阳性数和有效样本数。
- **病例级防泄漏**：所有属于同一 `StudyInstanceUID` 的序列必须进入同一个 fold。
- **弱监督**：报告中的描述只能作为训练信号；“报告未提及”不能自动当作阴性。

## 项目结构

```text
configs/                 实验配置
experiments/             实验记录模板与说明
notebooks/               EDA 和探索性分析
outputs/                 日志、OOF、权重等生成物（不提交 Git）
scripts/                 环境检查等入口脚本
src/data/                数据读取与预处理
src/models/              模型定义
tests/                   自动化检查
guide.docx               八周行动指南
requirements.txt         阶段 0–1 的直接依赖
```

比赛数据统一放在 `data/`，该目录不会被 Git 跟踪。Kaggle 密钥同样禁止提交。

## 环境设置

本机已验证的解释器为 `/opt/anaconda3/bin/python`（Python 3.13.9）。它已经包含 `requirements.txt` 中的全部直接依赖，无须重复安装。VS Code 已配置为默认使用该解释器。

每次开始工作时运行：

```bash
/opt/anaconda3/bin/python scripts/check_environment.py
/opt/anaconda3/bin/python -m pytest
```

只有环境检查提示缺包时才安装依赖：

```bash
/opt/anaconda3/bin/python -m pip install -r requirements.txt
```

当前验证结果：

```text
Python 3.13.9
PyTorch 2.13.0
MPS available: True
Tensor smoke test: PASS
```

也可以先激活 Anaconda base 环境，再使用简短命令：

```bash
source /opt/anaconda3/bin/activate base
python scripts/check_environment.py
pytest
```

如果 VS Code 没有自动切换，执行 “Python: Select Interpreter” 并选择 `/opt/anaconda3/bin/python`。

## 资源计划

- **本地设备**：Apple M5、16 GB 内存（arm64）；PyTorch MPS 已通过实际张量测试。模型训练是否转到 Kaggle GPU，由后续小样本测试决定。
- **本地磁盘**：阶段 0 检查时项目所在磁盘约有 221 GiB 可用；下载完整数据前再次确认容量。
- **时间预算假设**：每周 6–10 小时。若实际课业安排不同，直接修改本节。
- **实验纪律**：正式实验必须使用固定 fold，保存配置、OOF 概率、每类 AUC、运行时间和 Git commit。
- **资源纪律**：阶段 1 只分析 CSV；阶段 2 先用 20–50 个病例开发 DICOM 管线，再扩大数据量。

## 最低成功标准

排名不是唯一目标。项目至少完成以下七项：

1. 一份带结论的 EDA。
2. 可靠的 DICOM 读取模块。
3. 固定的病例级交叉验证。
4. 一个可复现的多标签 baseline。
5. OOF 预测及每类指标分析。
6. 一次格式正确的 Kaggle 有效提交。
7. 完整的 README、实验记录与复现说明。

## 实验纪律

每次正式实验先复制 `experiments/template.csv` 的表头或新增一行，并确保只改变一个关键因素。实验产物保存在 `outputs/`，有价值的结论写回实验记录或 README，不能只留在终端日志里。

## 当前下一步

进入阶段 2：先选择20–50个病例，开发可复用的 DICOM 读取、切片排序、灰度处理、固定切片采样和三平面可视化模块。随机抽查仍存在乱序、解码失败或灰度异常时，不进入模型训练。
