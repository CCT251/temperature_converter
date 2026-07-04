"""
温度转换核心逻辑
"""


class TemperatureConverter:
    """温度转换器核心类"""

    # 温度单位常量
    CELSIUS = 'C'
    FAHRENHEIT = 'F'
    KELVIN = 'K'

    @staticmethod
    def celsius_to_fahrenheit(celsius: float) -> float:
        """
        摄氏转华氏
        公式: °F = °C × 9/5 + 32

        Args:
            celsius: 摄氏温度值

        Returns:
            华氏温度值，保留两位小数
        """
        return round(celsius * 9 / 5 + 32, 2)

    @staticmethod
    def fahrenheit_to_celsius(fahrenheit: float) -> float:
        """
        华氏转摄氏
        公式: °C = (°F - 32) × 5/9

        Args:
            fahrenheit: 华氏温度值

        Returns:
            摄氏温度值，保留两位小数
        """
        return round((fahrenheit - 32) * 5 / 9, 2)

    @staticmethod
    def celsius_to_kelvin(celsius: float) -> float:
        """
        摄氏转开尔文
        公式: K = °C + 273.15

        Args:
            celsius: 摄氏温度值

        Returns:
            开尔文温度值，保留两位小数
        """
        return round(celsius + 273.15, 2)

    @staticmethod
    def kelvin_to_celsius(kelvin: float) -> float:
        """
        开尔文转摄氏
        公式: °C = K - 273.15

        Args:
            kelvin: 开尔文温度值

        Returns:
            摄氏温度值，保留两位小数
        """
        return round(kelvin - 273.15, 2)

    @staticmethod
    def fahrenheit_to_kelvin(fahrenheit: float) -> float:
        """
        华氏转开尔文
        公式: K = (°F + 459.67) × 5/9

        Args:
            fahrenheit: 华氏温度值

        Returns:
            开尔文温度值，保留两位小数
        """
        return round((fahrenheit + 459.67) * 5 / 9, 2)

    @staticmethod
    def kelvin_to_fahrenheit(kelvin: float) -> float:
        """
        开尔文转华氏
        公式: °F = K × 9/5 - 459.67

        Args:
            kelvin: 开尔文温度值

        Returns:
            华氏温度值，保留两位小数
        """
        return round(kelvin * 9 / 5 - 459.67, 2)

    @staticmethod
    def convert(value: float, from_unit: str, to_unit: str) -> float:
        """
        通用转换方法

        Args:
            value: 温度值
            from_unit: 输入单位 ('C', 'F', 'K')
            to_unit: 输出单位 ('C', 'F', 'K')

        Returns:
            转换后的温度值

        Raises:
            ValueError: 不支持的温度单位或转换路径
        """
        from_unit = from_unit.upper()
        to_unit = to_unit.upper()

        # 如果单位相同，直接返回
        if from_unit == to_unit:
            return round(value, 2)

        # 直接转换路径
        conversion_map = {
            ('C', 'F'): TemperatureConverter.celsius_to_fahrenheit,
            ('F', 'C'): TemperatureConverter.fahrenheit_to_celsius,
            ('C', 'K'): TemperatureConverter.celsius_to_kelvin,
            ('K', 'C'): TemperatureConverter.kelvin_to_celsius,
            ('F', 'K'): TemperatureConverter.fahrenheit_to_kelvin,
            ('K', 'F'): TemperatureConverter.kelvin_to_fahrenheit,
        }

        key = (from_unit, to_unit)
        if key in conversion_map:
            return conversion_map[key](value)
        else:
            raise ValueError(f"不支持的温度单位转换: {from_unit} → {to_unit}")

    @staticmethod
    def get_unit_symbol(unit: str) -> str:
        """获取温度单位符号"""
        symbols = {
            'C': '°C',
            'F': '°F',
            'K': 'K'
        }
        return symbols.get(unit.upper(), unit)

    @staticmethod
    def is_valid_unit(unit: str) -> bool:
        """检查温度单位是否有效"""
        return unit.upper() in ['C', 'F', 'K']