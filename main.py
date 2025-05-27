#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windsurf 机器码修改工具
自动修改 Windsurf 配置文件中的机器标识信息
"""

import os
import json
import uuid
import random
import string
import stat
from pathlib import Path
import sys
import subprocess
import time


class WindsurfMachineIdModifier:
    """Windsurf 机器码修改器"""

    def __init__(self):
        self.appdata_path = os.getenv('APPDATA')
        self.storage_file_path = None

    def check_environment(self):
        """检查运行环境"""
        print("🔍 检查运行环境...")

        # 检查操作系统
        if os.name != 'nt':
            print("❌ 错误：此程序仅支持Windows系统")
            return False

        # 检查APPDATA环境变量
        if not self.appdata_path:
            print("❌ 错误：无法获取APPDATA环境变量")
            return False

        print(f"✅ APPDATA路径: {self.appdata_path}")

        # 构建目标文件路径
        self.storage_file_path = Path(self.appdata_path) / "Windsurf" / "User" / "globalStorage" / "storage.json"

        print(f"🎯 目标文件: {self.storage_file_path}")

        # 检查文件是否存在
        if not self.storage_file_path.exists():
            print(f"❌ 错误：目标文件不存在: {self.storage_file_path}")
            return False

        print("✅ 目标文件存在")
        return True

    def detect_windsurf_processes(self):
        """检测 Windsurf 相关进程"""
        print("🔍 扫描 Windsurf 相关进程...")
        windsurf_processes = []
        process_names = ['Windsurf.exe', 'Code.exe', 'code.exe']

        for process_name in process_names:
            try:
                result = subprocess.run(
                    ['tasklist', '/FI', f'IMAGENAME eq {process_name}'],
                    capture_output=True, text=True, check=True
                )
                # 检查输出中是否包含进程名（忽略大小写）
                if process_name.lower() in result.stdout.lower() and "INFO: No tasks" not in result.stdout:
                    windsurf_processes.append(process_name)
                    print(f"  🔍 发现进程: {process_name}")
            except subprocess.CalledProcessError:
                continue

        return windsurf_processes

    def kill_windsurf_processes(self, process_list):
        """终止 Windsurf 进程"""
        print("🔄 正在关闭 Windsurf 进程...")
        success_count = 0

        for process_name in process_list:
            try:
                subprocess.run(
                    ['taskkill', '/F', '/IM', process_name],
                    capture_output=True, text=True, check=True
                )
                print(f"  ✅ 已终止进程: {process_name}")
                success_count += 1
            except subprocess.CalledProcessError:
                print(f"  ❌ 终止进程失败: {process_name}")
                continue

        return success_count == len(process_list)

    def check_and_close_windsurf(self):
        """检查并关闭 Windsurf 进程"""
        processes = self.detect_windsurf_processes()

        if not processes:
            print("✅ 未发现 Windsurf 进程")
            return True

        print(f"⚠️  发现运行中的 Windsurf 进程: {', '.join(processes)}")

        if self.kill_windsurf_processes(processes):
            print("✅ 所有 Windsurf 进程已关闭")
            print("⏳ 等待文件锁释放...")
            time.sleep(3)  # 等待文件锁释放
            return True
        else:
            print("❌ 部分进程关闭失败，请手动关闭后重试")
            return False

    def generate_machine_id(self):
        """生成32位十六进制机器ID"""
        return ''.join(random.choices(string.hexdigits.lower(), k=32))

    def generate_sqm_id(self):
        """生成标准UUID格式的SQM ID（带大括号）"""
        return "{" + str(uuid.uuid4()).upper() + "}"

    def generate_dev_device_id(self):
        """生成32位十六进制设备ID"""
        return ''.join(random.choices(string.hexdigits.lower(), k=32))



    def read_storage_file(self):
        """读取storage.json文件"""
        print("📖 读取配置文件...")
        try:
            with open(self.storage_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print("✅ 配置文件读取成功")
            return data
        except json.JSONDecodeError as e:
            print(f"❌ JSON格式错误: {e}")
            return None
        except Exception as e:
            print(f"❌ 读取文件失败: {e}")
            return None

    def modify_machine_ids(self, data):
        """修改机器标识信息"""
        print("🔧 生成新的机器标识...")

        # 生成新的随机值
        new_machine_id = self.generate_machine_id()
        new_sqm_id = self.generate_sqm_id()
        new_dev_device_id = self.generate_dev_device_id()

        # 显示原始值（如果存在）
        print("\n📋 原始值:")
        print(f"  telemetry.machineId: {data.get('telemetry.machineId', '未设置')}")
        print(f"  telemetry.sqmId: {data.get('telemetry.sqmId', '未设置')}")
        print(f"  telemetry.devDeviceId: {data.get('telemetry.devDeviceId', '未设置')}")

        # 修改值
        data['telemetry.machineId'] = new_machine_id
        data['telemetry.sqmId'] = new_sqm_id
        data['telemetry.devDeviceId'] = new_dev_device_id

        # 显示新值
        print("\n🆕 新值:")
        print(f"  telemetry.machineId: {new_machine_id}")
        print(f"  telemetry.sqmId: {new_sqm_id}")
        print(f"  telemetry.devDeviceId: {new_dev_device_id}")

        return data

    def write_storage_file(self, data):
        """写入修改后的数据到文件"""
        print("\n💾 保存修改后的配置...")
        try:
            # 先移除只读属性（如果有）
            if self.storage_file_path.exists():
                os.chmod(self.storage_file_path, stat.S_IWRITE | stat.S_IREAD)

            with open(self.storage_file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print("✅ 配置文件保存成功")
            return True
        except Exception as e:
            print(f"❌ 保存文件失败: {e}")
            return False

    def set_readonly(self):
        """设置文件为只读"""
        print("🔒 设置文件为只读...")
        try:
            os.chmod(self.storage_file_path, stat.S_IREAD)
            print("✅ 文件已设置为只读")
            return True
        except Exception as e:
            print(f"❌ 设置只读失败: {e}")
            return False

    def run(self):
        """运行主程序"""
        print("🚀 Windsurf 机器码修改工具启动")
        print("=" * 50)

        # 检查环境
        if not self.check_environment():
            return False

        # 检查并关闭 Windsurf 进程
        if not self.check_and_close_windsurf():
            return False

        # 读取配置文件
        data = self.read_storage_file()
        if data is None:
            return False

        # 修改机器标识
        modified_data = self.modify_machine_ids(data)

        # 保存修改
        if not self.write_storage_file(modified_data):
            return False

        # 设置只读
        if not self.set_readonly():
            return False

        print("\n" + "=" * 50)
        print("🎉 机器码修改完成！")
        print("⚠️  注意：文件已设置为只读，如需再次修改请先取消只读属性")

        return True


def main():
    """主函数"""
    try:
        modifier = WindsurfMachineIdModifier()
        success = modifier.run()

        if success:
            print("\n按任意键退出...")
            input()
            sys.exit(0)
        else:
            print("\n程序执行失败，按任意键退出...")
            input()
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n用户中断程序执行")
        sys.exit(1)
    except Exception as e:
        print(f"\n程序执行出错: {e}")
        print("按任意键退出...")
        input()
        sys.exit(1)


if __name__ == "__main__":
    main()