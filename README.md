# LexiFact — 个保合规审计平台

个人信息保护合规审计（PIPL / GB-T 46903）AI 辅助审计平台。

## 前置依赖

- **Docker** 24+
- **Docker Compose** v2（通常随 Docker 一起安装）

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
| `MIDSCENE_MODEL_*` | Midscene UI 自动化模型配置 |
| `MINERU_TOKEN` | MinerU 文档解析 API Token |
| `LICENSE_KEY` | 激活码 |

### 3. 启动

```bash
# 首次启动前先登录 GHCR 拉取镜像
docker login ghcr.io -u YOUR_GITHUB_USERNAME
# 输入 GitHub Token（需要 read:packages 权限）

# 启动所有服务
./scripts/manage.py up
```

或者直接用 docker compose：

```bash
docker compose pull
docker compose up -d
```

浏览器打开 `http://localhost:<NGINX_PORT>`。

### 4. 创建租户

```bash
./scripts/manage.py init
# 然后访问前端页面，按指引创建租户
```

## 更新

```bash
cd /opt/lexifact  # 你的部署目录
git pull
docker compose pull
docker compose up -d
```

更新前建议查看 [CHANGELOG.md](./CHANGELOG.md) 了解变更。

## 管理命令

```bash
./scripts/manage.py check   # 运行环境检查
./scripts/manage.py up      # 启动所有服务
./scripts/manage.py down    # 停止所有服务
./scripts/manage.py logs    # 查看日志
./scripts/manage.py ps      # 查看容器状态
./scripts/manage.py pull    # 拉取最新镜像
```

## 数据结构

所有数据存储在宿主机 `~/.lexifact/` 目录，包括：

- SQLite 数据库
- 项目文件
- 审计记录

备份该目录即可完成数据备份。
