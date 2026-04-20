---
name: daily-market-report
description: 每日A股收盘交易汇总报告生成流程 — 数据采集、资金流向分析、板块热点分析、技术面与消息面综合分析
category: data-science
---

# 每日A股收盘汇总报告

## 触发条件
每个交易日15:30收盘后自动执行，或用户要求查看当日/历史市场汇总时使用。

## 数据源

⚠️ 东方财富 push2 API (push2.eastmoney.com) 已失效（2026-04-20 确认），不要使用。
所有数据通过 **AKShare** 库获取，数据源为 Sina + 同花顺。

## 数据采集流程

### Step 1: 主要指数数据（日线）
```python
import akshare as ak

index_symbols = {
    'sh000001': '上证指数', 'sz399001': '深证成指', 'sz399006': '创业板指',
    'sh000688': '科创50',   'sh000016': '上证50',   'sh000300': '沪深300',
    'sh000905': '中证500',  'sh000852': '中证1000', 'bj899050': '北证50',
}
for sym, name in index_symbols.items():
    df = ak.stock_zh_index_daily(symbol=sym)
    latest = df.iloc[-1]
    prev = df.iloc[-2]
    close = latest['close']
    change_pct = (close - prev['close']) / prev['close'] * 100
```
- 数据源：Sina
- 字段：close=收盘价, open/high/low, volume=成交量
- 注意：这是日线数据（非实时），收盘后获取即可

### Step 2: 行业板块数据（同花顺）
```python
df_sector = ak.stock_board_industry_summary_ths()
# 包含：板块名称、涨跌幅、涨跌额、总成交量、总成交额、净流入、上涨家数、下跌家数、领涨股
```
- 涨跌幅排行：`df.nlargest(10, '涨跌幅')` / `df.nsmallest(5, '涨跌幅')`
- 资金净流入排行：`df.nlargest(10, '净流入')` / `df.nsmallest(5, '净流入')`

### Step 3: 概念板块（同花顺）
```python
df_concept = ak.stock_board_concept_summary_ths()
# 包含：概念名称、成分股数量、驱动事件、龙头股
```

### Step 4: 全市场个股行情（Sina）
```python
df_all = ak.stock_zh_a_spot()
# 全市场 ~5500 只股票，耗时约 35 秒
# 统计：上涨/下跌/平盘/涨停/跌停家数，涨幅/跌幅 TOP5
```

### Step 5: 市场消息面
使用 `web_search` 搜索：
- `"YYYY年M月D日 A股收盘 板块 热点"`
- `"A股今日涨停 资金流向"`

## 报告结构

```
# A股每日交易汇总报告 — YYYY年M月D日（星期X）

## 📊 主要指数收盘
| 指数 | 收盘 | 涨跌幅 |
（9个主要指数）

**成交额：X.XX万亿（两市合计）**

## 📈 行业板块涨跌排行
**涨幅 TOP10** / **跌幅 TOP5**

## 💰 行业板块资金净流入
**净流入 TOP10** / **净流出 TOP5**

## 🔥 近期热门概念板块

## 📊 个股涨跌统计
全市场涨跌家数、涨停跌停数、涨幅/跌幅 TOP5

## 💡 市场总结
（AI 根据数据自动补充：核心主线、弱势方向、关键信号）

---

*数据来源：AKShare (Sina + 同花顺) | 数据时间：YYYY-MM-DD*
```

## 保存路径
- 日报：`/Users/huidge/market-reports/daily/YYYY-MM-DD.md`
- 周报：`/Users/huidge/market-reports/weekly/YYYY-WXX.md`
- 美股：`/Users/huidge/market-reports/us-stock/daily/YYYY-MM-DD.md`
- 保存后执行 `python3 /Users/huidge/market-reports/report.py` 生成 HTML + 微信版
- 然后执行 `bash ~/.hermes/scripts/sync-reports.sh` 同步到 GitHub

## 周报生成逻辑（每周五自动触发）
1. 读取本周所有日报文件
2. 汇总：指数周涨跌、资金流向周变化、板块轮动趋势
3. 保存：`/Users/huidge/market-reports/YYYY-MM-DD-A股周报.md`

## 辅助脚本
`~/.hermes/scripts/a-share-daily-report.py` — 自动生成报告初稿（不含市场总结）
```bash
python3 ~/.hermes/scripts/a-share-daily-report.py /path/to/output.md
```

## PITFALLS
- 沙箱环境有代理问题，AKShare 需在宿主机执行（用 terminal 工具，不用 execute_code 的沙箱）
- `stock_zh_a_spot()` 下载全市场数据约 35 秒，属正常
- 同花顺板块接口需翻页加载，约 5-10 秒
- 非交易日需跳过（检查涨跌幅是否全为0）
