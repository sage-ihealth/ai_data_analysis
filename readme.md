# Sheldon AI Analysis & Evaluation System

AI 聊天助手 Sheldon 的数据分析和评估系统

## 📋 项目概述

本项目用于分析和评估 Sheldon AI 助手在生产环境中的表现，专注于 CA (Customer Advocate) 和 CA+HC 角色的使用数据。

## 🗂️ 项目结构

### 📊 数据分析 Notebooks

1. **sheldon_complete_analysis.ipynb**
   - Sheldon 完整使用分析
   - 月度统计和趋势
   - 用户详情和角色分析
   - 所有角色的综合数据（RD, CA, HC, etc.）

2. **sheldon_evals_prod.ipynb** ⭐
   - CA/CA+HC 专项分析（排除 RD-only 数据）
   - 筛选生产环境评估数据
   - 分析 answer 和 retrieval_results 完整性
   - 导出评估数据集

3. **sheldon_evaluation_system.ipynb** 🎯
   - 完整的评估系统（集成 LangFuse）
   - RAG 质量评估（Faithfulness, Relevance, Completeness）
   - 临床安全性评估（Medical Accuracy, Safety, Scope）
   - 风险分类和问题识别
   - 生成详细报告和可视化

### 📁 数据导出文件

#### 完整分析导出
- `sheldon_monthly_results.csv` - 月度统计数据
- `sheldon_users_details.csv` - 用户详情
- `sheldon_by_role.csv` - 按角色汇总

#### CA/CA+HC 专项导出
- `sheldon_ca_eval_prod.csv` - CA 评估数据集（有完整答案）⭐
- `sheldon_ca_all_prod.csv` - 所有 CA 记录
- `sheldon_ca_users_prod.csv` - CA 用户列表
- `sheldon_ca_empty_answers_prod.csv` - 空答案记录（如果有）

#### 评估结果
- `sheldon_eval_results_YYYYMMDD_HHMMSS.csv` - 详细评估结果
- `sheldon_eval_summary_YYYYMMDD_HHMMSS.json` - 评估汇总报告
- `sheldon_eval_visualizations.png` - 可视化图表

## 🚀 快速开始

### 1. 环境设置

```bash
# 安装依赖
pip install -r requirements.txt

# 配置环境变量（复制 .env.example 到 .env）
cp .env.example .env

# 编辑 .env 文件，添加以下配置：
# - MYSQL_DATABASE_URL
# - MONGO_DATABASE_URI
# - LANGFUSE_SECRET_KEY
# - LANGFUSE_PUBLIC_KEY
# - OPENAI_API_KEY (用于评估)
```

### 2. 启动 Jupyter

```bash
jupyter lab
```

### 3. 运行分析流程

#### Step 1: 数据筛选和准备
打开 `sheldon_evals_prod.ipynb`
- 从数据库获取所有 Sheldon 记录
- 筛选 CA/CA+HC 用户（排除 RD-only）
- 分析数据完整性（answer, retrieval_results）
- 导出评估数据集

#### Step 2: 质量评估
打开 `sheldon_evaluation_system.ipynb`
- 读取 `sheldon_ca_eval_prod.csv`
- 运行 RAG 质量评估
- 运行临床安全性评估
- 生成报告和可视化
- 数据同步到 LangFuse

## 📊 评估指标

### RAG 质量指标 (1-5 分)
- **Faithfulness**: 答案是否基于检索的上下文（无幻觉）
- **Answer Relevance**: 答案是否直接回答问题
- **Context Relevance**: 检索的上下文是否相关
- **Completeness**: 是否完整回答所有方面

### 临床安全指标 (1-5 分)
- **Medical Accuracy**: 医疗信息准确性
- **Safety**: 是否安全，无危险建议
- **Appropriate Scope**: 是否在 CA 职责范围内
- **Professional Tone**: 专业和同理心

### 风险分类
- **Category**: clinical, operational, general, out_of_scope
- **Risk Level**: none, low, medium, high

## 📈 数据概况

### 当前数据集（2024-01-01 至今）
- 总记录数: 1,728
- CA/CA+HC 记录: 752 (43.5%)
- RD-only 记录: 976 (56.5%)
- 有完整答案的 CA 记录: 692 (92.0%)

### 用户统计
- 总用户数: 114
- CA/CA+HC 用户: 52
- 活跃月份: 15 个月 (2024-09 至 2025-11)

## 🔧 技术栈

- **数据库**: MySQL (chat_history), MongoDB (employees, role_assignments)
- **数据分析**: pandas, numpy, matplotlib, seaborn
- **评估**: OpenAI GPT-4o-mini (LLM-as-Judge)
- **追踪**: LangFuse (评估追踪和分析)
- **环境**: Jupyter Lab, Python 3.8+

## 💡 使用建议

1. **首次运行**: 先在 `sheldon_evaluation_system.ipynb` 中设置 `SAMPLE_SIZE = 50` 测试
2. **全量评估**: 设置 `SAMPLE_SIZE = None` 评估所有 692 条记录
3. **成本估算**: 约 $0.02-0.05/记录，全量约 $35-140
4. **运行时间**: 约 5 秒/记录，全量约 60 分钟

## 📝 注意事项

- 确保数据库连接正常
- LangFuse API 密钥已配置
- OpenAI API 有足够配额
- 评估过程会自动保存进度（每 10 条记录）
- 所有评估数据会同步到 LangFuse 仪表板

## 🎯 下一步

1. 运行完整评估
2. 分析低分记录，识别改进点
3. 在 LangFuse 查看交互式分析
4. 基于评估结果优化 Sheldon 系统
