# 寻脉方言系统 - API 文档

服务地址：`http://localhost:5000`（默认端口 5000）

## 页面路由
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | 首页 |
| GET | `/map` | 方言分布地图 |
| GET | `/statistics` | 统计分析 |
| GET | `/evolution` | 语言演变模拟 |
| GET | `/migration` | 人口迁移与方言演变 |
| GET | `/detail/<city>` | 地区详情（如 `/detail/北京`） |
| GET | `/game` | 方言词汇游戏 |
| GET | `/game-test` | 游戏测试页 |

## 数据 API
### GET `/api/dialects`
返回全部方言点位记录（JSON 数组），字段与清洗 CSV 对齐：
```json
[
  {
    "city": "广州",
    "dialect_area": "粤语",
    "province": "广东",
    "longitude": 113.2644,
    "latitude": 23.1291,
    "population_10k": ...,
    "youth_usage_rate": ...,
    "endanger_index": ...,
    "endanger_level": ...
  }
]
```

### GET `/api/statistics`
返回统计汇总数据（JSON 数组）。

### GET `/api/cache-stats`
返回缓存命中统计，用于监控命中率：
```json
{ "hits": 100, "misses": 1, "hit_rate": "99.01%", "memory_entries": 3 }
```

## 静态资源
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/static/<file>` | 前端静态资源（css/js） |
| GET | `/outputs/<file>` | 分析产物（图表、清洗 CSV、地图 HTML） |

## 缓存头
- `/static/*`、`/outputs/*`：`Cache-Control: public, max-age=604800`（7 天）
- `/api/*`：`Cache-Control: public, max-age=300`
- 其余 GET：`Cache-Control: no-cache`