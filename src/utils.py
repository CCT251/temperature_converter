"""
工具函数模块
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class HistoryManager:
    """历史记录管理类"""

    def __init__(self, filename: str = "history.json"):
        self.filename = filename
        self.history: List[Dict] = []
        self.load()

    def add_record(self, value: float, from_unit: str, to_unit: str, result: float) -> None:
        """添加转换记录"""
        record = {
            'timestamp': datetime.now().isoformat(),
            'value': value,
            'from_unit': from_unit,
            'to_unit': to_unit,
            'result': result
        }
        self.history.append(record)
        self.save()

    def get_all(self) -> List[Dict]:
        """获取所有历史记录"""
        return self.history

    def clear(self) -> None:
        """清空历史记录"""
        self.history.clear()
        self.save()

    def get_last(self, n: int = 10) -> List[Dict]:
        """获取最近n条记录"""
        return self.history[-n:]

    def save(self) -> None:
        """保存历史到文件"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存历史失败: {e}")

    def load(self) -> None:
        """从文件加载历史"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
        except Exception as e:
            print(f"加载历史失败: {e}")
            self.history = []


def validate_temperature(value: float, unit: str) -> bool:
    """
    验证温度值是否物理合理

    Args:
        value: 温度值
        unit: 单位 (C, F, K)

    Returns:
        True 如果温度值在物理合理范围内
    """
    # 绝对零度
    abs_zero = {
        'C': -273.15,
        'F': -459.67,
        'K': 0
    }

    min_value = abs_zero.get(unit.upper())
    if min_value is None:
        return False

    return value >= min_value


def format_temperature(value: float, unit: str, decimals: int = 2) -> str:
    """
    格式化温度显示

    Args:
        value: 温度值
        unit: 单位符号
        decimals: 小数位数

    Returns:
        格式化后的字符串
    """
    symbols = {
        'C': '°C',
        'F': '°F',
        'K': 'K'
    }
    symbol = symbols.get(unit.upper(), unit)
    return f"{value:.{decimals}f}{symbol}"


def batch_convert(input_file: str, output_file: str, from_unit: str, to_unit: str) -> int:
    """
    批量转换文件中的温度值

    Args:
        input_file: 输入文件路径
        output_file: 输出文件路径
        from_unit: 输入单位
        to_unit: 输出单位

    Returns:
        转换的记录数
    """
    from .converter import TemperatureConverter

    converter = TemperatureConverter()
    count = 0

    try:
        with open(input_file, 'r', encoding='utf-8') as f_in, \
                open(output_file, 'w', encoding='utf-8') as f_out:

            for line in f_in:
                line = line.strip()
                if not line:
                    continue

                try:
                    value = float(line)
                    result = converter.convert(value, from_unit, to_unit)
                    f_out.write(f"{value},{result}\n")
                    count += 1
                except ValueError:
                    # 跳过无效行
                    continue

    except Exception as e:
        raise Exception(f"批量转换失败: {e}")

    return count