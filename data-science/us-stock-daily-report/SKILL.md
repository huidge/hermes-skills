---
name: us-stock-daily-report
description: 每日美股收盘行情汇总 — 主要指数、板块轮动、个股亮点、宏观消息面、技术分析
category: data-science
---

# 每日美股行情汇总

## 触发条件
每天早上6:00（北京时间）自动执行，汇总前一交易日美股收盘数据。

## 数据采集流程

### Step 1: 主要指数数据
使用 web_search 搜索当日美股收盘：
- `web_search("美股收盘 YYYY年M月D日 S&P500 纳斯达克 道琼斯 行情")`
- `web_search("US stock market close today S&P 500 Nasdaq Dow Jones")`

必须包含指数：
- 道琼斯工业平均指数 (Dow Jones / DJIA)
- 标普500指数 (S&P 500)
- 纳斯达克综合指数 (Nasdaq Composite)
- 罗素2000 (Russell 2000) — 如有数据
- 费城半导体指数 (PHLX Semiconductor / SOX) — 如有数据

记录：收盘价、涨跌点数、涨跌幅、当日高低点

### Step 2: 板块/行业表现
- `web_search("S&P 500 sector performance today")`
- `web_search("美股 板块表现 科技 能源 金融 今日")`

S&P 500 十一大板块：
1. 信息技术 (XLK)
2. 医疗保健 (XLV)
3. 金融 (XLF)
4. 可选消费 (XLY)
5. 通信服务 (XLC)
6. 工业 (XLI)
7. 必需消费 (XLP)
8. 能源 (XLE)
9. 公用事业 (XLU)
10. 房地产 (XLRE)
11. 原材料 (XLB)

### Step 3: 个股亮点
- 涨幅最大个股 TOP5（大盘股）
- 跌幅最大个股 TOP5
- 成交额最大个股
- 盘后异动个股

### Step 4: 大宗商品与外汇
- WTI/Brent 原油价格
- 黄金价格
- 美元指数 (DXY)
- 美国10年期国债收益率
- BTC/ETH（如有）

### Step 5: 宏观消息面
- 经济数据（CPI/PPI/非农/PMI等）
- 美联储动态
- 地缘政治（中东、贸易政策等）
- 企业财报（重点公司）

### Step 6: 分析展望
- 技术面：S&P 500 关键支撑/阻力位、均线排列
- 消息面：驱动因素分析
- 情绪面：VIX恐慌指数、Put/Call ratio
- 对A股/港股次日影响判断

## 报告模板

```
# 美股每日行情汇总
## 日期：YYYY年M月D日（美东时间）

### 一、主要指数收盘
### 二、板块表现
### 三、个股亮点
### 四、大宗商品与外汇
### 五、重要消息面
### 六、技术面与情绪分析
### 七、对亚太市场影响
### 八、免责声明
```

## 保存路径
日报：`~/market-reports/us-stock/daily/YYYY-MM-DD.md`

## 数据来源
- MarketWatch, Yahoo Finance, Investing.com
- 新浪财经美股, 华尔街见闻
- CNBC, Bloomberg（web_search）

## PITFALLS
- 无直接API，主要依赖 web_search 和 web_extract
- 美股收盘时间为北京时间凌晨4:00（夏令时）/ 5:00（冬令时）
- 财报季（1/4/7/10月）需特别关注大型科技公司财报
- VIX 和美债收益率需单独搜索获取
