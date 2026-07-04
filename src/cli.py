"""
命令行界面 (CLI)
支持命令行参数和交互模式
"""

import argparse
import sys
from .converter import TemperatureConverter


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description='温度转换工具 - 支持摄氏、华氏、开尔文之间的转换',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python -m src.cli 25 -f C -t F        # 25°C → °F
  python -m src.cli 77 -f F -t C        # 77°F → °C
  python -m src.cli 300 -f K -t C       # 300K → °C
  python -m src.cli -i                  # 交互模式
  python -m src.cli 25 -f C -t F -v    # 详细输出
        '''
    )

    parser.add_argument(
        'value',
        type=float,
        nargs='?',
        help='温度值'
    )
    parser.add_argument(
        '-f', '--from',
        dest='from_unit',
        choices=['C', 'F', 'K'],
        default='C',
        help='输入单位 (C:摄氏, F:华氏, K:开尔文)'
    )
    parser.add_argument(
        '-t', '--to',
        dest='to_unit',
        choices=['C', 'F', 'K'],
        default='F',
        help='输出单位 (C:摄氏, F:华氏, K:开尔文)'
    )
    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='交互模式'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='详细输出'
    )

    args = parser.parse_args()

    # 交互模式
    if args.interactive:
        interactive_mode()
        return

    # 单次转换模式
    if args.value is None:
        parser.print_help()
        return

    try:
        converter = TemperatureConverter()
        result = converter.convert(args.value, args.from_unit, args.to_unit)

        from_symbol = converter.get_unit_symbol(args.from_unit)
        to_symbol = converter.get_unit_symbol(args.to_unit)

        if args.verbose:
            print(f"输入: {args.value:.2f} {from_symbol}")
            print(f"单位: {args.from_unit} → {args.to_unit}")
            print(f"公式: {get_formula(args.from_unit, args.to_unit)}")
            print(f"结果: {result:.2f} {to_symbol}")
        else:
            print(f"{args.value:.2f}{from_symbol} = {result:.2f}{to_symbol}")

    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


def interactive_mode():
    """交互式转换模式"""
    converter = TemperatureConverter()

    print("\n" + "=" * 50)
    print("🌡️  温度转换器 - 交互模式")
    print("=" * 50)
    print("支持单位: C(摄氏), F(华氏), K(开尔文)")
    print("输入 'q' 退出, 'h' 查看历史, 'c' 清空历史")
    print("=" * 50 + "\n")

    history = []

    while True:
        try:
            # 输入温度值
            value_input = input("请输入温度值: ").strip()
            if value_input.lower() in ['q', 'quit', 'exit']:
                print("\n感谢使用，再见！")
                break
            if value_input.lower() == 'h':
                show_history(history)
                continue
            if value_input.lower() == 'c':
                history.clear()
                print("✅ 历史已清空\n")
                continue

            value = float(value_input)

            # 输入单位
            from_unit = input("输入单位 (C/F/K): ").strip().upper()
            if from_unit.lower() == 'q':
                break
            if not converter.is_valid_unit(from_unit):
                print("❌ 无效的单位，请使用 C、F 或 K\n")
                continue

            # 输出单位
            to_unit = input("输出单位 (C/F/K): ").strip().upper()
            if to_unit.lower() == 'q':
                break
            if not converter.is_valid_unit(to_unit):
                print("❌ 无效的单位，请使用 C、F 或 K\n")
                continue

            # 执行转换
            result = converter.convert(value, from_unit, to_unit)

            from_symbol = converter.get_unit_symbol(from_unit)
            to_symbol = converter.get_unit_symbol(to_unit)

            # 显示结果
            print(f"\n✅ 结果: {value:.2f}{from_symbol} = {result:.2f}{to_symbol}")
            print(f"📝 公式: {get_formula(from_unit, to_unit)}\n")

            # 添加到历史
            history.append({
                'value': value,
                'from_unit': from_unit,
                'to_unit': to_unit,
                'result': result
            })

        except ValueError:
            print("❌ 请输入有效的数字\n")
        except KeyboardInterrupt:
            print("\n\n程序已中断")
            break
        except Exception as e:
            print(f"❌ 错误: {e}\n")


def show_history(history):
    """显示转换历史"""
    if not history:
        print("📭 暂无历史记录\n")
        return

    print("\n📜 转换历史:")
    print("-" * 40)
    for i, record in enumerate(history, 1):
        from_symbol = TemperatureConverter.get_unit_symbol(record['from_unit'])
        to_symbol = TemperatureConverter.get_unit_symbol(record['to_unit'])
        print(f"{i:2d}. {record['value']:.2f}{from_symbol} → {record['result']:.2f}{to_symbol}")
    print("-" * 40 + "\n")


def get_formula(from_unit: str, to_unit: str) -> str:
    """获取转换公式"""
    formulas = {
        ('C', 'F'): '°F = °C × 9/5 + 32',
        ('F', 'C'): '°C = (°F - 32) × 5/9',
        ('C', 'K'): 'K = °C + 273.15',
        ('K', 'C'): '°C = K - 273.15',
        ('F', 'K'): 'K = (°F + 459.67) × 5/9',
        ('K', 'F'): '°F = K × 9/5 - 459.67',
    }
    return formulas.get((from_unit.upper(), to_unit.upper()), '未知公式')


if __name__ == "__main__":
    main()