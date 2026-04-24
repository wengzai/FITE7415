# VS Code Copilot “无人模式”配置说明

## 目标

在你主动手动关停前，默认自动批准 Copilot Agent 的大部分工具调用，减少编译、测试、终端命令、编辑文件等操作中的反复 Allow 确认。

## 一次性全局配置（跨项目生效）

编辑用户级设置文件 `C:\Users\ZHT\AppData\Roaming\Code\User\settings.json`，加入或确认如下配置：

```json
{
	"chat.tools.global.autoApprove": true,
	"chat.tools.edits.autoApprove": {
		"**/*": true,
		"**/.git/**": false
	}
}
```

说明：

- `chat.tools.global.autoApprove: true` 是总开关，开启后自动批准工具调用。
- `chat.tools.edits.autoApprove` 控制文件编辑的自动批准范围。当前配置表示：
	- 除 `.git` 目录外，编辑默认自动批准。
	- `.git` 目录保留保护，不自动改。

## 开启方法

1. 打开用户设置 JSON。
2. 设置 `"chat.tools.global.autoApprove": true`。
3. 首次启用时，如果 VS Code 弹出全局确认，点击 Allow（一次性确认）。
4. 之后在其他项目中也会保持自动批准（用户级生效）。

## 关闭方法

### 方式 A：永久关闭（全局）

将用户设置改为：

```json
"chat.tools.global.autoApprove": false
```

### 方式 B：当前会话临时关闭

在 Copilot Chat 输入：

```text
/disableAutoApprove
```

需要恢复当前会话自动批准时，输入：

```text
/autoApprove
```

## 推荐使用习惯

- 日常开发保持全局开启，减少打断。
- 做敏感操作（例如大规模删除、发布前关键改动）时，临时执行 `/disableAutoApprove`。
- 完成后执行 `/autoApprove` 恢复“无人模式”。
