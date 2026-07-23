from pathlib import Path

import pandas as pd


def answer_question(base_dir: Path, question: str) -> str:
    data_dir = base_dir / "data"

    metrics_df = pd.read_csv(
        data_dir / "overall_metrics.csv",
        encoding="utf-8-sig"
    )

    category_df = pd.read_csv(
        data_dir / "category_analysis.csv",
        encoding="utf-8-sig"
    )

    segment_df = pd.read_csv(
        data_dir / "segment_analysis.csv",
        encoding="utf-8-sig"
    )

    metrics = dict(zip(metrics_df["指标"], metrics_df["数值"]))
    normalized = question.replace(" ", "").lower()

    # 总用户数
    if any(word in normalized for word in [
        "多少用户",
        "用户数",
        "总用户",
        "一共有多少用户"
    ]):
        return f"数据集中共有{int(metrics['用户数']):,}名用户。"

    # 总体流失率
    if any(word in normalized for word in [
        "总体流失率",
        "总流失率",
        "流失率是多少"
    ]):
        return f"数据集的总体流失率为{float(metrics['流失率']):.1%}。"

    # 用户最多的偏好品类
    if any(word in normalized for word in [
        "哪个偏好品类用户最多",
        "用户最多的品类",
        "最多用户的品类",
        "偏好品类"
    ]):
        max_category_row = category_df.loc[
            category_df["用户数"].idxmax()
        ]

        category_name = max_category_row["PreferedOrderCat"]
        user_count = int(max_category_row["用户数"])

        return (
            f"用户数量最多的偏好品类是{category_name}，"
            f"共有{user_count:,}名用户。"
        )

    # 生命周期阶段风险
    if any(word in normalized for word in [
        "生命周期风险",
        "哪个生命周期阶段风险最高",
        "风险最高的阶段",
        "生命周期阶段"
    ]):
        max_segment_row = segment_df.loc[
            segment_df["流失率"].idxmax()
        ]

        segment_name = max_segment_row["生命周期阶段"]
        churn_rate = float(max_segment_row["流失率"])

        return (
            f"流失风险最高的生命周期阶段是{segment_name}，"
            f"该阶段流失率为{churn_rate:.1%}。"
        )

    # 平均订单数
    if any(word in normalized for word in [
        "平均订单数",
        "平均下单数",
        "平均多少订单",
        "订单数"
    ]):
        return (
            f"每名用户的平均订单数为"
            f"{float(metrics['平均订单数']):.2f}单。"
        )

    return (
        "暂时无法识别这个问题。"
        "你可以询问总用户数、总体流失率、偏好品类、"
        "生命周期风险或平均订单数。"
    )