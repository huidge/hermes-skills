---
name: a-share-report-akshare
description: A股每日/每周收盘行情汇总报告生成 — 东方财富 API 为主，AKShare (Sina + 同花顺) 兜底
---

# A股行情报告 (东方财富 + AKShare)

## 数据源优先级

| 数据类型 | 主数据源 (东方财富) | 兜底数据源 |
|---------|-------------------|-----------|
| 主要指数实时 | `stock_zh_index_spot_em()` — 东财实时 | Sina 日线 `stock_zh_index_daily()` (深证成指/创业板指/北证50) |
| 行业板块+资金流向 | `stock_sector_fund_flow_rank()` — 东财板块资金 | 同花顺 `stock_board_industry_summary_ths()` |
| 全市场个股行情 | — | Sina `stock_zh_a_spot()` |
| 概念板块 | — | 同花顺 `stock_board_concept_summary_ths()` |

### 已知限制
- 东方财富 `push2.eastmoney.com` 已全面不可用 (curl exit 52)，不再尝试
- `stock_zh_index_spot_em()` 缺失深证成指(399001)和创业板指(399006)，需 Sina 兜底
- **⚠️ `stock_zh_index_daily()` Sina 日线数据更新有延迟**：cron 在 15:30 运行时，日线接口可能仍返回前一日数据，导致指数重复。必须使用 `stock_zh_index_spot_em()` 获取实时行情，Sina 日线仅用于北证50兜底（东财列表不含）
- `stock_sector_fund_flow_rank()` 不含涨跌家数，仅含主力净流入数据
- Sina `stock_zh_a_spot()` 全市场加载约 90-100 秒

## 完整工作流 (cron job)

每次执行应完成 3 步：
1. **生成报告** — 运行脚本并保存到本地文件
2. **同步 GitHub** — 推送到远程仓库
3. **投递** — 格式化报告推送到微信/其他平台

### 步骤 1: 生成并保存
```bash
python3 ~/.hermes/scripts/a-share-daily-report.py /Users/huidge/market-reports/$(date +%Y-%m-%d)-A股收盘汇总.md
```

### 步骤 2: 同步到 GitHub
```bash
bash ~/.hermes/scripts/sync-reports.sh
```
同步脚本会自动检测变更、commit 并 push 到 `huidge/market-reports` 仓库。

### 步骤 3: 投递
读取报告文件内容，格式化为 Markdown，通过 deliver 机制推送到目标平台。

## 文件路径约定

```
market-reports/
├── report.py                # Markdown → HTML/微信 转换器
├── daily/                   # A股日报
│   ├── YYYY-MM-DD.md        # Markdown 源文件
│   ├── YYYY-MM-DD.html      # 网页版
│   └── YYYY-MM-DD.wechat.html  # 微信公众号版
├── weekly/                  # A股周报
│   ├── YYYY-WXX.md
│   ├── YYYY-WXX.html
│   └── YYYY-WXX.wechat.html
└── us-stock/
    └── daily/               # 美股日报
        └── YYYY-MM-DD.md
```

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

| 指数 | 东财代码 | Sina 代码 | 备注 |
|------|---------|-----------|------|
| 上证指数 | 000001 | sh000001 | 东财可用 |
| 深证成指 | 399001 | sz399001 | 东财缺失，Sina兜底 |
| 创业板指 | 399006 | sz399006 | 东财缺失，Sina兜底 |
| 科创50 | 000688 | sh000688 | 东财可用 |
| 上证50 | 000016 | sh000016 | 东财可用 |
| 沪深300 | 000300 | sh000300 | 东财可用 |
| 中证500 | 000905 | sh000905 | 东财可用 |
| 中证1000 | 000852 | sh000852 | 东财可用 |
| 北证50 | — | bj899050 | 东财无，仅Sina |

## 注意事项
- `stock_zh_a_spot()` 下载全市场 ~5500 只股票需约 90-100 秒
- 东方财富板块资金流向接口需加载 5 页，耗时约 20-25 秒
- 同花顺概念板块接口需加载 39 页，耗时约 10-12 秒
- **脚本总耗时约 120-150 秒，terminal 超时必须设 ≥300 秒**（120s 会超时截断）
- 沙箱环境有代理问题，需要在宿主机运行

## 已知间歇性故障及兜底方案

| 故障接口 | 错误表现 | 兜底方案 |
|---------|---------|---------|
| `stock_zh_index_spot_em()` | 深证成指/创业板指返回 "--" | Sina 日线自动兜底 |
| `stock_sector_fund_flow_rank()` | 接口异常或超时 | 回退到同花顺板块 |
| `stock_board_industry_summary_ths()` | `'NoneType' object has no attribute 'text'` | 用 `web_search` 搜"A股收盘 板块 涨幅居前"获取板块涨跌 |
| `stock_board_concept_summary_ths()` | 同上 | 用 `web_search` 搜"热门概念 板块"获取 |

**兜底操作：** 当脚本部分数据获取失败时，用 `web_search` 获取财经媒体收盘报道，手动补全报告对应章节。在报告中标注数据来源为"财经媒体收盘报道"。

## 完整 cron job 流程（含 AI 补充）

```
执行步骤：
1. 运行: python3 ~/.hermes/scripts/a-share-daily-report.py /path/to/daily/YYYY-MM-DD.md
   （terminal 超时设 300 秒）
2. 检查输出，如有数据缺失用 web_search 兜底补全
3. 用 AI 补充"市场总结"章节（核心主线、弱势方向、关键信号）
4. 生成 HTML 和微信版: python3 /Users/huidge/market-reports/report.py -f all /path/to/daily/YYYY-MM-DD.md
5. 同步到 GitHub: bash ~/.hermes/scripts/sync-reports.sh
6. 投递到微信
```

## 报告格式
报告包含 5 个部分：
1. 主要指数表现
2. 行业板块涨跌排行
3. 行业板块资金净流入
4. 近期热门概念
5. 个股涨跌统计（涨跌家数、涨跌停、TOP10）
