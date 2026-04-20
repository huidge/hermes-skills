---
name: a-share-report-akshare
description: A股每日/每周收盘行情汇总报告生成 — 使用 AKShare (Sina + 同花顺) 替代已失效的东方财富 push2 API
---

# A股行情报告 (AKShare)

## 背景
东方财富 push2 API (`push2.eastmoney.com`) 已全面返回空响应 (curl exit code 52)，无法使用。
本技能使用 **AKShare** 库通过 **Sina** 和 **同花顺** 数据源替代。

## 数据源

| 数据类型 | AKShare 接口 | 数据源 |
|---------|-------------|--------|
| 主要指数日线 | `stock_zh_index_daily(symbol)` | Sina |
| 全市场个股行情 | `stock_zh_a_spot()` | Sina |
| 行业板块排行 | `stock_board_industry_summary_ths()` | 同花顺 |
| 概念板块排行 | `stock_board_concept_summary_ths()` | 同花顺 |

## 使用方式

### 运行脚本
```bash
python3 ~/.hermes/scripts/a-share-daily-report.py
# 保存到文件:
python3 ~/.hermes/scripts/a-share-daily-report.py /path/to/output.md
```

### 在 cron job 中使用
在 cron job 的 prompt 中引用此技能，使用 `execute_code` 调用脚本：
```
执行 A 股收盘汇总报告：
1. 运行: python3 ~/.hermes/scripts/a-share-daily-report.py
2. 读取输出，格式化为 Markdown 报告
3. 投递到微信
```

## 指数代码映射
- sh000001 = 上证指数
- sz399001 = 深证成指
- sz399006 = 创业板指
- sh000688 = 科创50
- sh000016 = 上证50
- sh000300 = 沪深300
- sh000905 = 中证500
- sh000852 = 中证1000

## 注意事项
- `stock_zh_a_spot()` 下载全市场 ~5500 只股票需约 35 秒
- 同花顺板块接口需翻页加载，耗时约 5-10 秒
- Sina 指数接口仅提供日线数据（非实时）
- 如需实时指数数据，可尝试 `ak.stock_zh_index_spot_em()`（依赖东方财富，可能失败）
- 沙箱环境有代理问题，需要在宿主机运行

## 报告格式
报告包含 5 个部分：
1. 主要指数表现
2. 行业板块涨跌排行
3. 行业板块资金净流入
4. 近期热门概念
5. 个股涨跌统计（涨跌家数、涨跌停、TOP10）
