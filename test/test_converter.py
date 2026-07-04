"""
温度转换器单元测试
"""

import unittest
from src.converter import TemperatureConverter


class TestTemperatureConverter(unittest.TestCase):
    """测试温度转换功能"""

    def setUp(self):
        """测试前准备"""
        self.converter = TemperatureConverter()

    def test_celsius_to_fahrenheit(self):
        """测试摄氏转华氏"""
        test_cases = [
            (0, 32),
            (100, 212),
            (-40, -40),
            (37, 98.6),
            (25, 77),
        ]
        for celsius, expected in test_cases:
            with self.subTest(celsius=celsius):
                result = self.converter.celsius_to_fahrenheit(celsius)
                self.assertAlmostEqual(result, expected, places=1)

    def test_fahrenheit_to_celsius(self):
        """测试华氏转摄氏"""
        test_cases = [
            (32, 0),
            (212, 100),
            (-40, -40),
            (98.6, 37),
            (77, 25),
        ]
        for fahrenheit, expected in test_cases:
            with self.subTest(fahrenheit=fahrenheit):
                result = self.converter.fahrenheit_to_celsius(fahrenheit)
                self.assertAlmostEqual(result, expected, places=1)

    def test_celsius_to_kelvin(self):
        """测试摄氏转开尔文"""
        test_cases = [
            (0, 273.15),
            (100, 373.15),
            (-273.15, 0),
            (25, 298.15),
        ]
        for celsius, expected in test_cases:
            with self.subTest(celsius=celsius):
                result = self.converter.celsius_to_kelvin(celsius)
                self.assertAlmostEqual(result, expected, places=2)

    def test_kelvin_to_celsius(self):
        """测试开尔文转摄氏"""
        test_cases = [
            (273.15, 0),
            (373.15, 100),
            (0, -273.15),
            (298.15, 25),
        ]
        for kelvin, expected in test_cases:
            with self.subTest(kelvin=kelvin):
                result = self.converter.kelvin_to_celsius(kelvin)
                self.assertAlmostEqual(result, expected, places=2)

    def test_fahrenheit_to_kelvin(self):
        """测试华氏转开尔文"""
        self.assertAlmostEqual(
            self.converter.fahrenheit_to_kelvin(32),
            273.15,
            places=2
        )
        self.assertAlmostEqual(
            self.converter.fahrenheit_to_kelvin(212),
            373.15,
            places=2
        )

    def test_kelvin_to_fahrenheit(self):
        """测试开尔文转华氏"""
        self.assertAlmostEqual(
            self.converter.kelvin_to_fahrenheit(273.15),
            32,
            places=2
        )
        self.assertAlmostEqual(
            self.converter.kelvin_to_fahrenheit(373.15),
            212,
            places=2
        )

    def test_convert_general(self):
        """测试通用转换方法"""
        test_cases = [
            (25, 'C', 'F', 77),
            (77, 'F', 'C', 25),
            (0, 'C', 'K', 273.15),
            (273.15, 'K', 'C', 0),
            (32, 'F', 'K', 273.15),
            (273.15, 'K', 'F', 32),
            (25, 'C', 'C', 25),  # 相同单位
            (77, 'F', 'F', 77),
        ]
        for value, from_unit, to_unit, expected in test_cases:
            with self.subTest(value=value, from_unit=from_unit, to_unit=to_unit):
                result = self.converter.convert(value, from_unit, to_unit)
                self.assertAlmostEqual(result, expected, places=2)

    def test_invalid_unit(self):
        """测试无效单位"""
        with self.assertRaises(ValueError):
            self.converter.convert(100, 'X', 'C')
        with self.assertRaises(ValueError):
            self.converter.convert(100, 'C', 'X')
        with self.assertRaises(ValueError):
            self.converter.convert(100, 'X', 'Y')

    def test_get_unit_symbol(self):
        """测试获取单位符号"""
        self.assertEqual(self.converter.get_unit_symbol('C'), '°C')
        self.assertEqual(self.converter.get_unit_symbol('F'), '°F')
        self.assertEqual(self.converter.get_unit_symbol('K'), 'K')
        self.assertEqual(self.converter.get_unit_symbol('X'), 'X')

    def test_is_valid_unit(self):
        """测试单位验证"""
        self.assertTrue(self.converter.is_valid_unit('C'))
        self.assertTrue(self.converter.is_valid_unit('F'))
        self.assertTrue(self.converter.is_valid_unit('K'))
        self.assertFalse(self.converter.is_valid_unit('X'))
        self.assertFalse(self.converter.is_valid_unit(''))

    def test_edge_cases(self):
        """测试边界情况"""
        # 绝对零度
        self.assertEqual(self.converter.celsius_to_kelvin(-273.15), 0)
        self.assertEqual(self.converter.kelvin_to_celsius(0), -273.15)

        # 大数值
        self.assertIsInstance(
            self.converter.celsius_to_fahrenheit(1e6),
            float
        )

        # 小数值
        self.assertIsInstance(
            self.converter.fahrenheit_to_celsius(-1e6),
            float
        )


class TestUtils(unittest.TestCase):
    """测试工具函数"""

    def test_validate_temperature(self):
        """测试温度验证"""
        from src.utils import validate_temperature

        # 合理温度
        self.assertTrue(validate_temperature(25, 'C'))
        self.assertTrue(validate_temperature(77, 'F'))
        self.assertTrue(validate_temperature(300, 'K'))

        # 绝对零度
        self.assertTrue(validate_temperature(-273.15, 'C'))
        self.assertTrue(validate_temperature(-459.67, 'F'))
        self.assertTrue(validate_temperature(0, 'K'))

        # 低于绝对零度
        self.assertFalse(validate_temperature(-300, 'C'))
        self.assertFalse(validate_temperature(-500, 'F'))
        self.assertFalse(validate_temperature(-10, 'K'))

        # 无效单位
        self.assertFalse(validate_temperature(25, 'X'))

    def test_format_temperature(self):
        """测试温度格式化"""
        from src.utils import format_temperature

        self.assertEqual(format_temperature(25, 'C'), '25.00°C')
        self.assertEqual(format_temperature(77, 'F'), '77.00°F')
        self.assertEqual(format_temperature(300, 'K'), '300.00K')
        self.assertEqual(format_temperature(25.5, 'C', 1), '25.5°C')


if __name__ == '__main__':
    unittest.main(verbosity=2)