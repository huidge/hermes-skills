---
name: daily-market-report
description: 每日A股收盘交易汇总报告生成流程 — 数据采集、资金流向分析、板块热点分析、技术面与消息面综合分析
category: data-science
---

# 每日A股收盘汇总报告

## 触发条件
每个交易日15:30收盘后自动执行，或用户要求查看当日/历史市场汇总时使用。

## 数据采集流程

### Step 1: 主要指数数据（必须包含以下9个指数）
```bash
curl -s "https://push2.eastmoney.com/api/qt/ulist.np/get?fields=f2,f3,f4,f12,f14&secids=1.000001,0.399001,0.399006,1.000688,1.000300,1.000016,0.899050,1.000510"
```
- 1.000001=上证指数, 0.399001=深证成指, 0.399006=创业板指, 1.000688=科创50
- 1.000300=沪深300, 1.000016=上证50, 0.899050=北证50
- 1.000510=中证A500, 中证A50 secid待确认
- f2/f4 需除以100，f3 对指数需除以100
- **备用方案**：如API返回空，用 web_search 搜索当日指数收盘数据

### Step 2: 行业板块资金流向
```bash
# 资金流入TOP
curl -s "https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=60&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f62&fs=m:90+t:2&fields=f2,f3,f12,f14,f62,f184,f66,f69,f72,f75,f204,f205"

# 资金流出TOP（po=0 升序）
curl -s "https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=60&po=0&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f62&fs=m:90+t:2&fields=f2,f3,f12,f14,f62,f184,f66,f69,f72,f75,f204,f205"
```
- f62 = 净流入（元），除以1e8转换为亿元
- f66 = 超大单流入

### Step 3: 市场消息面
使用 web_search 搜索：
- "YYYY年M月D日 A股收盘 板块 资金流向"
- "A股今日涨停 热点"

### Step 4: 成交量数据
从证券时报等来源获取两市成交额和涨跌家数比。

## 报告结构模板

```
# A股每日交易汇总报告
## 日期：YYYY年M月D日（星期X）

### 一、主要指数收盘数据
### 二、资金流向数据
### 三、市场热点与板块分析
### 四、重要消息面
### 五、技术面分析
### 六、市场情绪分析
### 七、市场展望与分析
### 八、免责声明
```

## 保存路径
- 日报：`~/market-reports/daily/YYYY-MM-DD.md`
- 周报：`~/market-reports/weekly/YYYY-WXX.md`

## 周报生成逻辑（每周五自动触发）
1. 读取本周所有 `~/market-reports/daily/*.md`
2. 汇总：指数周涨跌、资金流向周变化、板块轮动趋势、热点演变
3. 分析：技术面周线形态、周度资金面总结
4. 展望：下周重点关注方向、风险提示
5. 保存：`~/market-reports/weekly/YYYY-WXX.md`

## PITFALLS
- 概念板块API `m:90+t:3` 可能返回空数据，使用 web_search 替代获取热点
- 北向资金API数据可能异常（全为0），如异常则从新闻搜索中补充
- 非交易日需跳过执行（可通过检查涨跌幅是否全为0判断）
