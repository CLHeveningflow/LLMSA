#!/usr/bin/env python3
import os
import sys
import platform
import shutil
from pathlib import Path

def get_platform_specifics():
    """获取平台特定信息"""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    # 确定平台目录和可执行文件后缀
    if system == "windows":
        return {
            "platform_dir": "Windows",
            "exe_suffix": ".exe",
            "script_suffix": ".bat"
        }
    elif system == "linux":
        return {
            "platform_dir": f"Linux_{machine}",
            "exe_suffix": "",
            "script_suffix": ".sh"
        }
    elif system == "darwin":
        return {
            "platform_dir": f"macOS_{machine}",
            "exe_suffix": "",
            "script_suffix": ".command"
        }
    else:
        raise NotImplementedError(f"Unsupported platform: {system}")

def generate_executable(src_file: Path, output_dir: Path, exe_name: str, platform_info: dict):
    """生成可执行文件"""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 目标路径
    exe_path = output_dir / f"{exe_name}{platform_info['exe_suffix']}"
    script_path = output_dir / f"{exe_name}{platform_info['script_suffix']}"
    
    # 尝试使用PyInstaller
    try:
        import PyInstaller.__main__
        
        print(f"正在使用PyInstaller生成 {platform_info['platform_dir']} 平台的可执行文件...")
        
        temp_dir = output_dir / "build_temp"
        temp_dir.mkdir(exist_ok=True)
        
        PyInstaller.__main__.run([
            '--onefile',
            '--distpath', str(output_dir),
            '--workpath', str(temp_dir),
            '--specpath', str(temp_dir),
            '--name', exe_name,
            str(src_file)
        ])
        
        shutil.rmtree(temp_dir)
        print(f"可执行文件已生成: {exe_path}")
        return exe_path
        
    except ImportError:
        # 回退方案：创建平台特定的启动脚本
        print(f"PyInstaller未安装，将创建{platform_info['script_suffix']}启动脚本")
        
        # 复制源文件
        dest_file = output_dir / src_file.name
        shutil.copy2(src_file, dest_file)
        
        # 创建启动脚本
        if platform_info['script_suffix'] == ".bat":
            script_content = f'@python "%~dp0{dest_file.name}" %*\n'
        elif platform_info['script_suffix'] == ".sh":
            script_content = f'#!/bin/bash\npython3 "$(dirname "$0")/{dest_file.name}" "$@"\n'
            os.chmod(script_path, 0o755)  # 添加执行权限
        elif platform_info['script_suffix'] == ".command":
            script_content = f'#!/bin/bash\npython3 "$(dirname "$0")/{dest_file.name}" "$@"\n'
            os.chmod(script_path, 0o755)  # 添加执行权限
        
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        print(f"启动脚本已生成: {script_path}")
        return script_path

def setup_environment(src_file:str, base_dir=str):
    """
    设置跨平台环境
    
    参数:
        src_file (str/Path): 源Python文件路径
        base_dir (str/Path): 基础输出目录
    """
    src_file = Path(src_file)
    if not src_file.exists():
        raise FileNotFoundError(f"源文件不存在: {src_file}")
    
    platform_info = get_platform_specifics()
    output_dir = Path(base_dir) / platform_info["platform_dir"] / "bin"
    
    exe_name = src_file.stem

    # 生成可执行文件
    exe_path = generate_executable(
        src_file=src_file,
        output_dir=output_dir,
        exe_name=exe_name,
        platform_info=platform_info
    )
    
    print("\n环境设置完成!")
    print(f"平台: {platform_info['platform_dir']}")
    print(f"可执行文件/脚本: {exe_path}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='跨平台环境设置工具')
    parser.add_argument('--src-file', default="Analysis.py",
                       help='源Python文件路径 (默认: src/Analysis.py)')
    parser.add_argument('--base-dir', default="env_test",
                       help='输出基础目录 (默认: env_test)')
    
    args = parser.parse_args()
    
    setup_environment(
        src_file="src/"+args.src_file,
        base_dir=args.base_dir
    )