# 寻脉方言系统 - 架构说明

## 概述
“寻脉——方言地理分布与语言演变可视化教学平台”采用 Flask 前后端分离结构：
后端负责业务与数据，前端独立存放模板与静态资源，通过 HTTP 交互。

## 目录结构
```
寻脉方言系统/
├── backend/                  # 后端根目录
│   ├── app/                  # Flask 应用包
│   │   ├── __init__.py       # 应用工厂 create_app()：注册蓝图/初始化缓存/缓存钩子
│   │   ├── config.py         # 集中配置：动态路径、端口、缓存参数
│   │   ├── routes/           # 路由层（只做参数接收与响应返回）
│   │   │   ├── pages_bp.py   # 页面路由：/ /map /statistics /evolution /migration /detail/<city> /game /game-test
│   │   │   ├── api_bp.py     # API 路由：/api/dialects /api/statistics /api/cache-stats
│   │   │   └── static_bp.py  # 静态文件：/outputs/ /static/
│   │   ├── services/         # 服务层（业务逻辑，数据均经缓存读取）
│   │   │   ├── dialect_service.py
│   │   │   ├── statistics_service.py
│   │   │   └── evolution_service.py
│   │   ├── models/           # 数据模型层 (dataclass / TypedDict)
│   │   │   └── dialect.py
│   │   ├── data/             # 内嵌静态数据（方言详情字典，约 1300 行）
│   │   │   └── dialect_info.py
│   │   ├── cache/            # 缓存层（多级缓存 + 命中率统计）
│   │   │   └── cache_manager.py
│   │   └── utils/            # 工具层
│   │       └── helpers.py
│   ├── data/                 # 原始数据文件
│   ├── outputs/              # 分析产物（清洗 CSV、图表、地图）
│   ├── analysis_scripts/     # 数据分析流水线（1-9 步）
│   ├── requirements.txt
│   └── run.py                # 后端唯一启动入口
├── frontend/                 # 前端根目录
│   ├── templates/            # Jinja2 模板（base.html + 各页面继承）
│   └── static/               # 静态资源（css/js/assets）
├── scripts/                  # 项目级脚本（bat）
├── docs/                     # 文档
├── .gitignore
├── README.md
└── 启动系统.bat              # 根目录快捷入口（调用 scripts/start.bat）
```

## 分层职责
- **路由层**：接收请求、传参给服务层、渲染模板/返回 JSON，不含业务。
- **服务层**：方言查询、详情获取、相关城市推荐、统计加载、演变数据准备。**所有数据读取都经 CacheManager**，禁止直接读文件。
- **数据层**：内嵌的方言详情静态字典，提供 `get_dialect_info_dict()`（模块级单例缓存）。
- **缓存层**：`CacheManager` 一级内存缓存（TTL）+ 二级文件缓存（可选），统计命中/未命中，目标命中率 ≥ 98%。
- **模型层**：静态类型定义，便于维护。
- **工具层**：路径、格式化、相关城市计算等通用函数。

## 应用工厂
`backend/app/__init__.py` 的 `create_app(config_name)`：
- 从 `config.py` 加载配置（development/production）
- `Flask(static_folder=None)`，静态资源统一由 `static_bp` 提供（/static、/outputs）
- Jinja2 模板路径指向 `frontend/templates`
- 注册三个蓝图，初始化缓存单例
- `before_request`/`after_request` 挂载缓存钩子并设置 HTTP 缓存头

## 缓存设计
- 服务层用 `cache.get_or_set(key, loader, ttl)` 包裹数据加载（全部方言、统计、演变数据）。
- 静态资源 HTTP 头长缓存（7 天），API 缓存 300s，页面 no-cache。
- 命中率通过 `/api/cache-stats` 或日志监控，目标 ≥ 98%。

## 启动方式
见 `README.md`。

## 数据分析流水线
`backend/analysis_scripts/` 按编号执行：数据整理→清洗→统计→空间分析→可视化→地图→相似度→演变模拟→TTS。配置在 `analysis_scripts/config.py`，输入 `backend/data`、输出 `backend/outputs`。