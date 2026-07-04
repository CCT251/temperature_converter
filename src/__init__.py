"""
温度转换器核心模块
"""
from .converter import TemperatureConverter
from .ui import ConverterUI
from .cli import main as cli_main

__version__ = "1.0.0"
__all__ = ['TemperatureConverter', 'ConverterUI', 'cli_main']