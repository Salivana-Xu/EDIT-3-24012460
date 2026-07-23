# 第10天：模型比较（完成版）

本项目使用同一训练集和测试集比较最低参照线、逻辑回归、决策树与随机森林，并选择随机森林生成用户流失预测、高风险名单和特征重要性结果。

## 运行环境检查

在项目根目录运行：

```bash
python validate_day10_environment.py
```

## 重新执行 Notebook

```bash
jupyter nbconvert --to notebook --execute notebooks/day10_model_comparison_student.ipynb \
  --output day10_model_comparison_student.ipynb \
  --output-dir notebooks \
  --ExecutePreprocessor.timeout=300
```

也可以启动 Jupyter Notebook 后按任务 0～9 顺序运行全部单元格。

## 提交检查

```bash
python validate_day10_submission.py
```

成果文件位于 `output/`，包括模型比较、混淆矩阵、测试用户预测、高风险名单、特征重要性、已保存模型、元数据和文字说明。


