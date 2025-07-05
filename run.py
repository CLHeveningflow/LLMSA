#!/usr/bin/env python3
import os
import json
import platform
import subprocess
from pathlib import Path

def find_json_files(config_dir="configs"):
    """查找指定目录下的所有JSON配置文件"""
    config_dir = Path(config_dir)
    if not config_dir.exists():
        raise FileNotFoundError(f"配置目录不存在: {config_dir}")
    
    return list(config_dir.glob("*.json"))

def get_executable_path(script_name, base_dir="env"):
    """获取跨平台可执行文件路径"""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if system == "windows":
        platform_dir = "Windows"
        exe_suffix = ".exe"
    elif system == "linux":
        platform_dir = f"Linux_{machine}"
        exe_suffix = ""
    elif system == "darwin":
        platform_dir = f"macOS_{machine}"
        exe_suffix = ""
    else:
        raise NotImplementedError(f"不支持的操作系统: {system}")
    
    exe_path = Path(base_dir) / platform_dir / "bin" / f"{script_name}{exe_suffix}"
    
    # 检查备用脚本文件
    if not exe_path.exists():
        if system == "windows":
            alt_path = exe_path.with_suffix(".bat")
        elif system == "linux":
            alt_path = exe_path.with_suffix(".sh")
        elif system == "darwin":
            alt_path = exe_path.with_suffix(".command")
        
        if alt_path.exists():
            return alt_path
    
    return exe_path if exe_path.exists() else None

def run_command(config_name, config_data, base_dir="env"):
    """根据配置运行命令"""
    exe_path = get_executable_path(config_name, base_dir)
    if not exe_path:
        print(f"错误: 找不到 {config_name} 的可执行文件")
        return False
    
    # 构建命令参数
    args = [str(exe_path)]
    
    if isinstance(config_data, dict):
        # 如果是字典，转换为命令行参数
        for k, v in config_data.items():
            args.append(f"--{k}")
            if v is not None and v != "":  # 忽略空值
                args.append(str(v))
    elif isinstance(config_data, list):
        # 如果是列表，直接作为参数
        args.extend(str(arg) for arg in config_data)
    
    print(f"执行命令: {' '.join(args)}")
    
    try:
        result = subprocess.run(args, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e}")
        return False
    except Exception as e:
        print(f"运行时错误: {e}")
        return False

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='跨平台任务运行器')
    parser.add_argument('--config-dir', default="configs",
                       help='配置文件目录 (默认: configs)')
    parser.add_argument('--base-dir', default="env",
                       help='可执行文件基础目录 (默认: env)')
    parser.add_argument('--list', action='store_true',
                       help='列出所有可用配置')
    parser.add_argument('config', nargs='?',
                       help='要运行的配置名称(不带.json扩展名)')
    
    args = parser.parse_args()
    
    # 查找所有JSON配置文件
    json_files = find_json_files(args.config_dir)
    
    if args.list:
        print("可用配置:")
        for f in json_files:
            print(f"  - {f.stem}")
        return
    
    if not args.config:
        parser.print_help()
        print("\n请指定要运行的配置名称")
        return
    
    # 查找匹配的配置文件
    config_file = None
    for f in json_files:
        if f.stem.lower() == args.config.lower():
            config_file = f
            break
    
    if not config_file:
        print(f"错误: 找不到 {args.config} 的配置文件")
        return
    
    # 读取配置文件
    try:
        with open(config_file, 'r') as f:
            config_data = json.load(f)
    except json.JSONDecodeError:
        print(f"错误: 配置文件 {config_file} 格式无效")
        return
    
    # 运行命令
    success = run_command(args.config, config_data, args.base_dir)
    
    if not success:
        exit(1)

if __name__ == "__main__":
    main()