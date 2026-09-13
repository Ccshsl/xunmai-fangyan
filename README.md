# 寻脉 —— 方言地理分布与语言演变可视化教学平台

基于 Flask + Jinja2 的方言教学可视化系统，展示中国方言的地理分布、统计分析、语言演变模拟、人口迁移探究与方言词汇游戏。

## 目录结构（前后端分离）

```
寻脉方言系统/
├── backend/               # 后端（Flask）
│   ├── app/               # 应用包：routes(路由) / services(服务) / models(模型) / data(数据) / cache(缓存) / utils(工具)
│   ├── data/              # 原始数据
│   ├── outputs/           # 分析产物
│   ├── analysis_scripts/  # 数据分析流水线（1-9 步）
│   ├── requirements.txt
│   └── run.py             # 后端入口
├── frontend/              # 前端
│   ├── templates/         # Jinja2 模板（base.html + 各页面）
│   └── static/            # 静态资源（css / js / webfonts / images，全部本地化，零 CDN 依赖）
├── scripts/               # 启动 / 分析 bat 脚本
├── docs/                  # 架构与 API 文档
└── 启动系统.bat           # 一键启动（根目录快捷入口）
```

> 详见 [docs/architecture.md](docs/architecture.md) 与 [docs/api.md](docs/api.md)。

## 环境要求
- Python 3.10+（已装 Flask、pandas）
- 数据分析流水线还需 numpy、matplotlib、seaborn、scipy、folium

## 一键启动
双击根目录 **`启动系统.bat`**（或 `scripts\start.bat`），将自动：
1. 启动后端服务（端口 5000）
2. 打开浏览器访问 `http://localhost:5000`

## 其他脚本
| 脚本 | 说明 |
|------|------|
| `scripts\start.bat` | 一键启动后端并打开浏览器（根目录 `启动系统.bat` 调用此脚本） |
| `scripts\run_analysis.bat` | 运行数据分析流水线（产出到 `backend\outputs`） |

## 手动启动后端
```bat
cd backend
python run.py
```

## 说明
- 服务层数据读取均经过多级缓存（内存 + 文件），命中率目标 ≥ 98%，可通过 `/api/cache-stats` 查看。
- `寻脉方言系统111.zip` 为历史备份，可自行删除。
- 根目录旧的单文件 `app.py` 已拆分至 `backend/app/` 各模块。