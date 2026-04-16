---
name: eastmoney-scraper
description: Scrape A-share market data, fund rankings, and sector fund flows from East Money (东方财富) internal APIs
category: data-science
version: 1.0
---

# East Money (东方财富) Financial Data Scraper

## Trigger
When the user asks for A-share market data, fund rankings, sector fund flows, index quotes, or any financial data from Chinese markets that East Money covers.

## Context
East Money renders most financial data dynamically via JavaScript. Standard web scraping (web_extract) won't capture the data. Use the internal API endpoints instead.

## Key API Endpoints

### 1. Real-time Index Quotes
```
https://push2.eastmoney.com/api/qt/ulist.np/get?fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17,f18&secids=1.000001,0.399001,0.399006,0.399106,0.000688
```
- `1.000001` = Shanghai Composite, `0.399001` = Shenzhen Component, `0.399006` = ChiNext, `0.000688` = STAR 50
- Key fields: `f2`=price(x100), `f3`=change%(+500 means 5.00%), `f4`=change(x100), `f14`=name, `f15`=high, `f16`=low, `f17`=open, `f18`=prev_close
- **Important**: Values are scaled by 100. Divide f2/f15/f16/f17/f18 by 100 for actual prices.

### 2. Sector Fund Flow (Industry Sectors)
```
https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=60&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f62&fs=m:90+t:2&fields=f12,f14,f2,f3,f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f204,f205
```
- `fs=m:90+t:2` = industry sectors, `m:90+t:3` = concept sectors
- `po=1` = descending (top inflows), `po=0` = ascending (top outflows)
- `fid=f62` = sort by net inflow
- Key fields:
  - `f62` = daily net inflow (元), `f184` = large order inflow%
  - `f66` = super large order inflow, `f72` = large order inflow
  - `f78` = medium order inflow, `f84` = small order inflow
  - `f204` = representative stock, `f205` = stock code

### 3. Fund Rankings
```
https://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=TYPE&rs=&gs=0&sc=SORT&st=ORDER&sd=START&ed=END&qdii=&tabSubtype=,,,,,&pi=1&pn=20&dx=1
```
- `ft=` all/gp/zs/hh/zq/qdii/fof
- `sc=` zzf(daily)/1yzf(1-month)/3yzf(3-month)/1nzf(1-year)/0nzf(YTD)
- `st=` desc/asc
- Requires `Referer: https://fund.eastmoney.com/data/fundranking.html` header
- Response: `var rankData = {datas:["code,name,pinyin,date,nav,totalNav,dailyChange,1w,1m,3m,6m,1y,2y,3y,ytd,sinceInception,..."]}`

## Step-by-Step Approach

1. **Index data**: Use `push2.eastmoney.com` API, divide prices by 100
2. **Sector flows**: Use `clist` API with `m:90+t:2` (industry) or `m:90+t:3` (concept)
3. **Fund rankings**: Use rankhandler API via `terminal/curl` with Referer header
4. **Never rely on browser_snapshot** for data — content is JS-rendered and incomplete
5. **Prefer `terminal/curl`** over browser fetch() for reliability (CORS issues)

## 4. East Money News Search (for market context)
```
https://so.eastmoney.com/news/s?keyword=KEYWORD&pageindex=1&searchrange=8&channelid=
```
- `searchrange=8` = recent news, `1000000` = all time
- Returns page titles and snippets — useful for gathering sector catalysts, analyst views, and market sentiment
- Navigate via `browser_navigate` and parse `browser_snapshot` for article links

## 5. Sector Historical Fund Flow (大盘资金流向)
```
https://data.eastmoney.com/zjlx/dpzjlx.html
```
- Navigate via browser, then use `browser_console` with JS to extract table data
- Shows daily index closes + fund flow history (super/large/medium/small orders)
- The data loaded via `browser_snapshot` from the `zbjlx` page includes a table `#tb_1` with daily market fund flow records

## Step-by-Step Approach

1. **Index data**: Use `push2.eastmoney.com` API, divide prices by 100
2. **Sector flows**: Use `clist` API with `m:90+t:2` (industry) or `m:90+t:3` (concept)
3. **Fund rankings**: Use rankhandler API via `terminal/curl` with Referer header
4. **Market news/context**: Use East Money search (`so.eastmoney.com/news/s`)
5. **Never rely on browser_snapshot** for data — content is JS-rendered and incomplete
6. **Prefer `terminal/curl`** over browser fetch() for reliability (CORS issues)

## Pitfalls
- All price values from push2 API are x100 — always divide f2/f15/f16/f17/f18 by 100
- `f3` for sectors is plain % (1.52 = 1.52%), but for indexes it's x100 (6 = 0.06%)
- `f62` is in 元 (yuan), divide by 1e8 for 亿元
- Fund API requires `Referer: https://fund.eastmoney.com/data/fundranking.html` header or returns empty
- QDII funds may have stale NAV dates (e.g., 04-10 vs 04-13) due to timezone/trading day differences
- Fund ranking response is JSONP-wrapped CSV — strip `var rankData = {datas:[...]}` and parse comma-separated fields
  - Fields: `code,name,pinyin,date,nav,totalNav,dailyChange,1w,1m,3m,6m,1y,2y,3y,ytd,sinceInception,foundingDate,...`
- **CORS blocks fetch()** from browser console when calling East Money APIs directly — use `terminal/curl` instead
- When `terminal` is blocked (API auth issues), fall back to `browser_navigate` + `browser_console` JS evaluation
- Concept sector filter `m:90+t:3` returns 200+ results — filter client-side by keywords (e.g., 航天, 卫星, AI, 军工)
- For individual stock quotes via API: `secid=1.600760` (Shanghai) or `secid=0.002594` (Shenzhen)
