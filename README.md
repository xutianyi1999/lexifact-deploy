# LexiFact — 个保合规审计平台

个人信息保护合规审计（PIPL / GB-T 46903）AI 辅助审计平台。

## 前置依赖

- **Docker** 24+
- **Docker Compose** v2（通常随 Docker 一起安装）
- **uv**（运行管理脚本需要，`curl -LsSf https://astral.sh/uv/install.sh | sh`）
- **文件系统** ext4（需 `prjquota` 挂载选项）或 XFS，支持磁盘配额

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

### 3. 创建租户

```bash
./scripts/lexifact.py create-tenant "公司名称"
```

输出中的 `API Key`（`lf-...`）是登录凭证，保存它。

### 4. 启动

```bash
./scripts/lexifact.py up
```

或者直接用 docker compose：

```bash
docker compose --profile image pull
docker compose up -d
```

### 5. 登录

浏览器打开 `http://localhost:<NGINX_PORT>`，输入上一步获取的 API Key。

## 更新

```bash
git pull
docker compose --profile image pull
docker compose up -d
```

更新前建议查看 [CHANGELOG.md](./CHANGELOG.md) 了解变更。

## 回滚

```bash
git tag --list                        # 查看有哪些版本
git checkout v0.2.0-alpha.1           # 回滚到指定版本（compose 文件会 pin 对应版本 tag）
docker compose --profile image pull
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
./scripts/lexifact.py create-tenant   # 创建租户 API Key
```

## PC 端隧道代理

`lexifact-tunnel` 是 ADB 隧道代理，运行在用户 PC 上，通过 WebSocket 连接后端，将本地 ADB 和 scrcpy 端口暴露给 sandbox 容器中的 agent，实现远程手机操控。

### 下载

从 [Releases](https://github.com/xutianyi1999/lexifact-deploy/releases) 下载对应平台的二进制：

| 平台 | 文件 |
|------|------|
| Linux x86_64 | `lexifact-tunnel-*-x86_64-unknown-linux-gnu.tar.gz` |
| macOS ARM | `lexifact-tunnel-*-aarch64-apple-darwin.tar.gz` |
| Windows x86_64 | `lexifact-tunnel-*-x86_64-pc-windows-msvc.zip` |

解压后得到 `lexifact-tunnel`（或 `lexifact-tunnel.exe`）单个二进制文件。

### 手机准备

1. 开启 **开发者选项**：设置 → 关于手机 → 连续点击「版本号」7 次
2. 开启 **USB 调试**：设置 → 系统 → 开发者选项 → USB 调试
3. 用数据线连接电脑，选择 **传输文件** 模式
4. 首次连接会弹出 RSA 指纹确认，勾选「一律允许」→ 确定

### 前置依赖

- **ADB** — Android Debug Bridge
  - Windows：程序会自动下载安装
  - macOS/Linux：手动安装 [platform-tools](https://developer.android.com/tools/releases/platform-tools)，确保 `adb` 在 `PATH` 中

### 用法

```bash
# 查看帮助
./lexifact-tunnel --help

# 启动 PC 模式
./lexifact-tunnel \
  --base-url https://your-server.com \
  --api-key lf-xxxxxxxxxxxxxxxx \
  --mode pc
```

参数说明：

| 参数 | 说明 |
|------|------|
| `--base-url` | 后端服务地址，如 `http://localhost:8080` 或 `https://your-server.com` |
| `--api-key` | 租户 API Key（`lf-...`），通过 `create-tenant` 获取 |
| `--mode` | `pc`（绑定 ADB+scrcpy）或 `docker`（仅转发 ADB） |

程序会：

1. 用 API Key 向服务端获取 JWT
2. 通过 WebSocket 建立隧道连接
3. 绑定本地 ADB（5037）端口，后端通过 ADB 自动推送 scrcpy-server 到手机并启动屏幕镜像
4. 断线自动重连（3 秒间隔）

## 数据结构

所有数据存储在宿主机 `~/.lexifact/` 目录，包括：

- SQLite 数据库
- 项目文件
- 审计记录

备份该目录即可完成数据备份。
