---
name: us-stock-daily-report
description: 每日美股收盘行情汇总 — 主要指数、板块轮动、个股亮点、宏观消息面、技术分析
category: data-science
---

# 每日美股行情汇总

## 触发条件
每天早上6:00（北京时间）自动执行，汇总前一交易日美股收盘数据。

## 数据源
- **指数日线**：AKShare `index_us_stock_sina`（Sina 源，稳定可靠）
- **板块/个股/宏观**：`web_search` 搜索聚合

## 数据采集流程

### Step 1: 主要指数数据（AKShare）
```python
import akshare as ak

index_symbols = {
    '.DJI':  '道琼斯工业指数',
    '.IXIC': '纳斯达克综合指数',
    '.INX':  '标普500指数',
    '.SOX':  '费城半导体指数',
}
for sym, name in index_symbols.items():
    df = ak.index_us_stock_sina(symbol=sym)
    latest = df.iloc[-1]
    prev = df.iloc[-2]
    close = latest['close']
    change_pct = (close - prev['close']) / prev['close'] * 100
    change = close - prev['close']
    print(f'{name}: {close:.2f} ({change_pct:+.2f}%)')
```
- 数据源：Sina，日线数据
- 支持指数：DJI、IXIC（Nasdaq）、INX（S&P 500）、SOX（半导体）
- 字段：date/open/high/low/close/volume

### Step 2: 板块/行业表现（web_search）
- `web_search("S&P 500 sector performance today")`
- `web_search("美股 板块表现 科技 能源 金融 今日")`

S&P 500 十一大板块：
1. 信息技术 (XLK)  2. 医疗保健 (XLV)  3. 金融 (XLF)
4. 可选消费 (XLY)  5. 通信服务 (XLC)  6. 工业 (XLI)
7. 必需消费 (XLP)  8. 能源 (XLE)  9. 公用事业 (XLU)
10. 房地产 (XLRE)  11. 原材料 (XLB)

### Step 3: 个股亮点（web_search）
- `web_search("美股今日涨幅最大个股 大盘股")`
- `web_search("US stock biggest gainers today")`
- 涨幅最大 TOP5、跌幅最大 TOP5、成交额最大个股

### Step 4: 大宗商品与外汇（web_search）
- `web_search("今日WTI原油 黄金价格 美元指数")`
- `web_search("US 10 year treasury yield today")`
- WTI/Brent 原油、黄金、美元指数(DXY)、10年期美债收益率、BTC/ETH

### Step 5: 宏观消息面（web_search）
- `web_search("美股今日 驱动因素 美联储 财报")`
- 经济数据（CPI/PPI/非农/PMI）、美联储动态、地缘政治、重点公司财报

### Step 6: 分析展望
- 技术面：S&P 500 关键支撑/阻力位、均线排列
- 消息面：驱动因素分析
- 情绪面：VIX 恐慌指数（web_search 单独获取）
- 对 A 股/港股次日影响判断

## 报告模板

```
# 美股每日行情汇总 — YYYY年M月D日（美东时间）

## 📊 主要指数收盘
| 指数 | 收盘价 | 涨跌点 | 涨跌幅 |
（DJI、S&P 500、Nasdaq、SOX）

## 📈 板块表现
（S&P 500 十一大板块涨跌排行）

## 🏆 个股亮点
（涨幅/跌幅 TOP5、成交额最大个股）

## 💰 大宗商品与外汇
（原油、黄金、美元指数、美债收益率）

## 📰 重要消息面
（经济数据、美联储、财报、地缘政治）

## 💡 技术面与情绪分析
（关键点位、VIX、对亚太市场影响）

---

*数据来源：AKShare (Sina) + web_search | 数据时间：YYYY-MM-DD*
```

## 保存路径
- 日报：`/Users/huidge/market-reports/YYYY-MM-DD-美股收盘汇总.md`
- 保存后执行 `bash ~/.hermes/scripts/sync-reports.sh` 同步到 GitHub

## 辅助脚本
如需自动化，可用 AKShare 批量获取指数数据：
```bash
python3 -c "
import akshare as ak
for sym, name in [('.DJI','道琼斯'),('.IXIC','纳斯达克'),('.INX','标普500'),('.SOX','半导体')]:
    df = ak.index_us_stock_sina(symbol=sym)
    l, p = df.iloc[-1], df.iloc[-2]
    pct = (l['close']-p['close'])/p['close']*100
    print(f'{name}: {l[\"close\"]:.2f} ({pct:+.2f}%) date={l[\"date\"]}')
"
```

## PITFALLS
- 美股收盘时间为北京时间凌晨 4:00（夏令时）/ 5:00（冬令时）
- AKShare 的美股个股接口（stock_us_spot 等）在沙箱中有代理问题，需在宿主机执行
- `stock_us_spot()` 全量扫描约 860 只股票需 20+ 分钟，不实用，改用 web_search
- 财报季（1/4/7/10月）需特别关注大型科技公司财报
- VIX 和美债收益率需单独 web_search 获取
- RUT（罗素2000）在 AKShare 中可能获取失败，可跳过
