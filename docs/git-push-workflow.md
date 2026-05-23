# Maker-Mods 分支开发与推送流程

> 本文档记录了如何基于 [Maker-Mods/lerobot-MakerMods](https://github.com/Maker-Mods/lerobot-MakerMods) 的 `main` 分支创建功能分支、添加自定义代码并推送的完整流程。
> 以 `lekiwi-chassis` 和 `Elrobot_MakerMods` 两个分支为例。

## 前置条件

- 本地已配置 SSH Key 并添加到 GitHub（用于 `git@github.com` 推送）
- 已安装 `git`、`sshpass`（如需从 Jetson 复制文件）

---

## 第一步：克隆仓库

```bash
cd ~
git clone https://github.com/Maker-Mods/lerobot-MakerMods.git
cd lerobot-MakerMods
```

> 如果克隆后 remote 是 HTTPS，改为 SSH 以便推送：
>
> ```bash
> git remote set-url origin git@github.com:Maker-Mods/lerobot-MakerMods.git
> ```

设置本仓库的 git 用户信息（仅首次）：

```bash
git config user.email "你的邮箱@example.com"
git config user.name "你的用户名"
```

---

## 第二步：从 main 创建新分支

```bash
git checkout main
git pull origin main
git checkout -b 你的分支名
```

**关键原则：新分支必须从 `main` 创建，这样才能与 `main` 共享完整的 git 历史，避免出现 "N commits behind" 无法合并的问题。**

---

## 第三步：添加你的代码

根据需求不同，有两种方式：

### 方式 A：添加全新的模块文件

适用于添加新的 robot/teleoperator 等独立模块。

**示例：lekiwi-chassis 分支**

```bash
# 创建目录
mkdir -p src/lerobot/robots/xlerobot

# 把你的文件复制进来（可从其他机器 scp，或本地复制）
cp /path/to/your/xlerobot/*.py src/lerobot/robots/xlerobot/

# 也可以从远程机器复制
sshpass -p '密码' scp -o StrictHostKeyChecking=no \
    user@192.168.x.x:~/源路径/文件.py \
    src/lerobot/robots/xlerobot/
```

### 方式 B：添加模块 + 修改注册文件 + 修复已有代码

适用于添加新 robot 类型并需要集成到框架中。

**示例：Elrobot_MakerMods 分支**

1. 复制 robot 和 teleoperator 文件：

```bash
mkdir -p src/lerobot/robots/elrobot_follower
mkdir -p src/lerobot/teleoperators/elrobot_leader

# 从 Jetson 复制
sshpass -p '密码' scp -o StrictHostKeyChecking=no \
    jetson@192.168.x.x:~/Elrobot_lerobot/src/lerobot/robots/elrobot_follower/*.py \
    src/lerobot/robots/elrobot_follower/

sshpass -p '密码' scp -o StrictHostKeyChecking=no \
    jetson@192.168.x.x:~/Elrobot_lerobot/src/lerobot/teleoperators/elrobot_leader/*.py \
    src/lerobot/teleoperators/elrobot_leader/
```

2. 在 `src/lerobot/robots/utils.py` 中注册新 robot：

```python
# 在 make_robot_from_config 函数中，mock_robot 之前添加：
elif config.type == "elrobot_follower":
    from .elrobot_follower import ElrobotFollower
    return ElrobotFollower(config)
```

3. 在 `src/lerobot/teleoperators/utils.py` 中注册新 teleoperator：

```python
# 在 make_teleoperator_from_config 函数中，else 之前添加：
elif config.type == "elrobot_leader":
    from .elrobot_leader import ElrobotLeader
    return ElrobotLeader(config)
```

4. 如有需要，修复依赖的底层驱动代码（如 feetech）

---

## 第四步：检查变更

```bash
# 查看所有变更
git status

# 查看修改的文件差异
git diff --stat
```

确认：
- 新增的文件夹/文件都在列表中
- 修改的注册文件（utils.py）变更正确
- 没有误改其他文件

---

## 第五步：提交

```bash
# 暂存所有变更
git add src/lerobot/robots/elrobot_follower/
git add src/lerobot/teleoperators/elrobot_leader/
git add src/lerobot/robots/utils.py
git add src/lerobot/teleoperators/utils.py
git add src/lerobot/motors/feetech/feetech.py   # 如果有修改

# 提交（用中文写清楚改了什么）
git commit -m "feat: 添加 Elrobot 七自由度机械臂支持

新增 elrobot_follower 和 elrobot_leader 模块
修复 feetech Homing_Offset 溢出问题"
```

---

## 第六步：推送到远程

```bash
git push origin 你的分支名
```

如果分支之前已存在且需要覆盖（比如之前推错了）：

```bash
git push origin 你的分支名 --force
```

> **注意：`--force` 会覆盖远程分支，只在你确定要替换旧内容时使用。**

---

## 完整流程速查

```bash
# 1. 克隆 & 进入
git clone https://github.com/Maker-Mods/lerobot-MakerMods.git
cd lerobot-MakerMods
git remote set-url origin git@github.com:Maker-Mods/lerobot-MakerMods.git
git config user.email "your@email.com"
git config user.name "YourName"

# 2. 创建分支
git checkout main && git pull origin main
git checkout -b 新分支名

# 3. 添加/修改代码
#    ... 复制文件、编辑 utils.py 等 ...

# 4. 检查
git status
git diff --stat

# 5. 提交
git add .
git commit -m "feat: 你的功能描述"

# 6. 推送
git push origin 新分支名
```

---

## 已有分支参考

| 分支名 | 用途 | 基于 | 新增文件 |
|--------|------|------|----------|
| `lekiwi-chassis` | LeKiwi 底盘控制 + XLerobot 架构 | `main` | `robots/lekiwi/` 下 4 个脚本, `robots/xlerobot/` 整个模块 |
| `Elrobot_MakerMods` | Elrobot 七自由度机械臂 | `main` | `robots/elrobot_follower/`, `teleoperators/elrobot_leader/`, feetech 修复 |

---

## 常见错误与解决

### "N commits behind, M commits ahead" 且无法合并

**原因**：分支不是从 `main` 创建的，没有共享 git 历史。

**解决**：重新从 `main` 创建分支，把代码复制过来，force-push 覆盖：

```bash
git checkout main && git pull
git checkout -b 分支名-fix main

# 从旧分支提取你的文件
git checkout origin/旧分支名 -- src/lerobot/robots/你的模块/

git add . && git commit -m "你的提交信息"
git push origin 分支名-fix:分支名 --force
```

### "fatal: could not read Username" 推送失败

**原因**：remote 使用 HTTPS 但未配置凭证。

**解决**：切换到 SSH：

```bash
git remote set-url origin git@github.com:Maker-Mods/lerobot-MakerMods.git
```

### "作者身份未知" 提交失败

**解决**：

```bash
git config user.email "你的邮箱"
git config user.name "你的用户名"
```
