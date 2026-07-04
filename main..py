#!/usr/bin/env python3
"""
温度转换器 - 主程序入口
支持GUI和CLI两种模式
"""

import sys
import argparse
from src.ui import ConverterUI
from src.cli import main as cli_main


def main():
    """主程序入口"""
    parser = argparse.ArgumentParser(
        description='温度转换器 - 支持摄氏、华氏、开尔文转换',
        usage='python main.py [options]'
    )
    parser.add_argument(
        '-g', '--gui',
        action='store_true',
        help='启动图形界面 (默认)'
    )
    parser.add_argument(
        '-c', '--cli',
        action='store_true',
        help='启动命令行界面'
    )
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='温度转换器 v1.0.0'
    )

    # 解析参数
    args, remaining = parser.parse_known_args()

    # 如果使用CLI模式
    if args.cli:
        # 将剩余参数传递给CLI
        sys.argv = [sys.argv[0]] + remaining
        cli_main()
    else:
        # 默认启动GUI
        try:
            app = ConverterUI()
            app.run()
        except KeyboardInterrupt:
            print("\n程序已退出")
            sys.exit(0)
        except Exception as e:
            print(f"启动GUI失败: {e}")
            print("尝试使用命令行模式: python main.py -c")
            sys.exit(1)


if __name__ == "__main__":
    main()