# LexiFact — 个保合规审计平台

个人信息保护合规审计（PIPL / GB-T 46903）AI 辅助审计平台。

## 前置依赖

- **Docker** 24+
- **Docker Compose** v2（通常随 Docker 一起安装）
- **uv**（运行管理脚本需要，`curl -LsSf https://astral.sh/uv/install.sh | sh`）

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/xutianyi1999/lexifact-deploy.git
cd lexifact-deploy
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env，填写所有必填变量
```

必填变量：

| 变量 | 说明 |
|------|------|
| `NGINX_PORT` | nginx 监听端口（如 `80`） |
| `JWT_SECRET` | JWT 签名密钥，随机字符串 |
| `LLM_BASE_URL` | LLM API 地址（如 `https://api.deepseek.com`） |
| `LLM_API_KEY` | LLM API 密钥 |
| `LLM_MODEL` | 模型名（如 `deepseek-v4-flash`） |
| `LLM_REASONING_EFFORT` | 推理深度（minimal/low/default/high/max） |
| `VOICE_ARK_API_KEY` | 火山引擎 ARK 语音识别 API 密钥 |
| `MIDSCENE_MODEL_BASE_URL` | Midscene 视觉模型 API 地址 |
| `MIDSCENE_MODEL_API_KEY` | Midscene 视觉模型 API 密钥 |
| `MIDSCENE_MODEL_NAME` | Midscene 模型名（如 `doubao-seed-2-1-turbo-260628`） |
| `MIDSCENE_MODEL_FAMILY` | Midscene 模型系列（如 `doubao-seed`） |
| `MIDSCENE_MODEL_EXTRA_BODY_JSON` | Midscene 附加请求体参数 |
| `MINERU_TOKEN` | MinerU 文档解析 API Token |
| `LICENSE_KEY` | 激活码 |

### 3. 启动

```bash
./scripts/lexifact.py up
```

或者直接用 docker compose：

```bash
docker compose pull
docker compose up -d
```

浏览器打开 `http://localhost:<NGINX_PORT>`。

### 4. 首次初始化

```bash
./scripts/lexifact.py init
```

浏览器打开 `http://localhost:<NGINX_PORT>`，按页面指引创建租户并登录。

## 更新

```bash
git pull
docker compose pull
docker compose up -d
```

更新前建议查看 [CHANGELOG.md](./CHANGELOG.md) 了解变更。

## 回滚

```bash
git tag --list                        # 查看有哪些版本
git checkout v0.2.0-alpha.1           # 回滚到指定版本（compose 文件会 pin 对应版本 tag）
docker compose pull
docker compose up -d
```

## 管理命令

```bash
./scripts/lexifact.py check   # 运行环境检查
./scripts/lexifact.py up      # 启动所有服务
./scripts/lexifact.py down    # 停止所有服务
./scripts/lexifact.py logs    # 查看日志
./scripts/lexifact.py ps      # 查看容器状态
./scripts/lexifact.py pull    # 拉取最新镜像
```

## 数据结构

所有数据存储在宿主机 `~/.lexifact/` 目录，包括：

- SQLite 数据库
- 项目文件
- 审计记录

备份该目录即可完成数据备份。
