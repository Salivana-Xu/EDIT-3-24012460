from pathlib import Path

import pandas as pd


def _read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, encoding="utf-8-sig")


def load_dashboard_data(
    base_dir: Path,
    selected_category: str = "全部"
) -> dict:
    data_dir = base_dir / "data"

    # 读取三个数据文件
    metrics_df = _read_csv(data_dir / "overall_metrics.csv")
    category_df = _read_csv(data_dir / "category_analysis.csv")
    segment_df = _read_csv(data_dir / "segment_analysis.csv")

    # 将总体指标转换成字典
    metric_map = dict(zip(metrics_df["指标"], metrics_df["数值"]))

    #  2-1：增加“总体流失率”和“平均订单数”
    metrics = [
        {
            "label": "总用户数",
            "value": f"{int(metric_map['用户数']):,}",
            "note": "人",
        },
        {
            "label": "流失用户",
            "value": f"{int(metric_map['流失人数']):,}",
            "note": "人",
        },
        {
            "label": "总体流失率",
            "value": f"{float(metric_map['流失率']):.1%}",
            "note": "",
        },
        {
            "label": "平均订单数",
            "value": f"{float(metric_map['平均订单数']):.2f}",
            "note": "单/人",
        },
    ]

    # 下拉框中的全部品类
    categories = [
        "全部",
        *category_df["PreferedOrderCat"].tolist(),
    ]

    table_df = category_df.copy()

    # 3-1：根据用户选择的品类筛选表格
    if selected_category != "全部":
        table_df = table_df[
            table_df["PreferedOrderCat"] == selected_category
        ]

    # 修改表格列名
    table_df = table_df.rename(
        columns={
            "PreferedOrderCat": "偏好品类",
            "用户数": "用户数",
            "流失率": "流失率",
            "平均订单数": "平均订单数",
        }
    )[
        [
            "偏好品类",
            "用户数",
            "流失率",
            "平均订单数",
        ]
    ]

    # 格式化表格数据
    table_df["流失率"] = table_df["流失率"].map(
        lambda value: f"{value:.1%}"
    )
    table_df["平均订单数"] = table_df["平均订单数"].map(
        lambda value: f"{value:.2f}"
    )

    # 2-2：找出流失率最高的生命周期阶段
    highest_risk_row = segment_df.loc[
        segment_df["流失率"].idxmax()
    ]

    # 默认使用segment_analysis.csv的第一列作为阶段名称列
    segment_column = segment_df.columns[0]
    segment_name = highest_risk_row[segment_column]
    highest_churn_rate = float(highest_risk_row["流失率"])

    insight = (
        f"{segment_name}阶段的流失率最高，"
        f"达到{highest_churn_rate:.1%}，"
        "建议重点关注该阶段用户并制定针对性的用户挽留措施。"
    )

    return {
        "metrics": metrics,
        "categories": categories,
        "category_rows": table_df.to_dict("records"),
        "insight": insight,
    }