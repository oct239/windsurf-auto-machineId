# Windsurf 机器码修改工具

一个简单的 Python 程序，用于自动修改 Windsurf 编辑器的机器标识信息。

## 功能特性

-   🎯 自动定位 Windsurf 配置文件
-   🔧 随机生成新的机器标识
-   🔒 修改完成后设置文件为只读
-   ✅ 完整的错误处理和用户反馈

## 修改的字段

程序会修改以下三个字段：

-   `telemetry.machineId`: 32 位十六进制字符串
-   `telemetry.sqmId`: 标准 UUID 格式（带大括号）
-   `telemetry.devDeviceId`: 32 位十六进制字符串

## 系统要求

-   Windows 操作系统
-   Python 3.6+
-   已安装 Windsurf 编辑器

## 使用方法

直接运行 Python 脚本：

```bash
python main.py
```

## 程序流程

1. **环境检查**: 验证操作系统和文件路径
2. **文件备份**: 创建原始文件的备份
3. **读取配置**: 解析 JSON 配置文件
4. **生成随机值**: 为三个字段生成新的随机标识
5. **保存修改**: 将修改后的配置写回文件
6. **设置只读**: 防止软件自动恢复配置

## 文件位置

-   **目标文件**: `%APPDATA%\Windsurf\User\globalStorage\storage.json`
-   **备份文件**: `%APPDATA%\Windsurf\User\globalStorage\storage.json.backup`

## 安全特性

-   ✅ 完整的错误处理机制
-   ✅ 修改后设置文件为只读
-   ✅ 详细的操作日志输出

## 注意事项

1. **运行前请确保 Windsurf 编辑器已关闭**
2. 程序会自动备份原始文件，如需恢复可使用备份文件
3. 修改完成后文件会被设置为只读，如需再次修改请先取消只读属性
4. 建议在修改前手动备份整个 Windsurf 配置目录

## 错误处理

程序包含以下错误处理：

-   操作系统兼容性检查
-   文件存在性验证
-   JSON 格式验证
-   文件权限检查
-   备份操作验证

## 示例输出

```
🚀 Windsurf 机器码修改工具启动
==================================================
🔍 检查运行环境...
✅ APPDATA路径: C:\Users\Username\AppData\Roaming
🎯 目标文件: C:\Users\Username\AppData\Roaming\Windsurf\User\globalStorage\storage.json
✅ 目标文件存在
📖 读取配置文件...
✅ 配置文件读取成功
🔧 生成新的机器标识...

📋 原始值:
  telemetry.machineId: abc123def456...
  telemetry.sqmId: {12345678-1234-1234-1234-123456789012}
  telemetry.devDeviceId: def456abc123...

🆕 新值:
  telemetry.machineId: 9f8e7d6c5b4a3928374650192837465a
  telemetry.sqmId: {A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
  telemetry.devDeviceId: 1a2b3c4d5e6f7890abcdef1234567890

💾 保存修改后的配置...
✅ 配置文件保存成功
🔒 设置文件为只读...
✅ 文件已设置为只读

==================================================
🎉 机器码修改完成！
⚠️  注意：文件已设置为只读，如需再次修改请先取消只读属性

按任意键退出...
```

## 许可证

本项目仅供学习和研究使用。

## 免责声明

使用本工具修改软件配置文件可能违反软件的使用条款。请在使用前仔细阅读相关软件的许可协议，并自行承担使用风险。
