"""
图形用户界面 (GUI)
使用 tkinter 实现
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
from .converter import TemperatureConverter


class ConverterUI:
    """温度转换器图形界面"""

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("温度转换器 v1.0")
        self.window.geometry("500x450")
        self.window.resizable(False, False)

        # 设置窗口图标和样式
        self.window.configure(bg='#f0f0f0')

        self.converter = TemperatureConverter()
        self.history = []
        self.max_history = 20

        self.setup_ui()
        self.bind_events()

    def setup_ui(self):
        """设置界面组件"""
        # 使用ttk样式
        style = ttk.Style()
        style.theme_use('clam')

        # 主框架
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 标题
        title_label = ttk.Label(
            main_frame,
            text="🌡️ 温度转换器",
            font=('Arial', 16, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # 输入区域
        ttk.Label(main_frame, text="输入温度值:", font=('Arial', 10)).grid(
            row=1, column=0, sticky='w', pady=5
        )
        self.input_value = ttk.Entry(main_frame, width=20, font=('Arial', 12))
        self.input_value.grid(row=1, column=1, pady=5, padx=10, sticky='w')
        self.input_value.focus()  # 自动聚焦

        # 单位选择 - 从
        ttk.Label(main_frame, text="从:", font=('Arial', 10)).grid(
            row=2, column=0, sticky='w', pady=5
        )
        self.from_unit = ttk.Combobox(
            main_frame,
            values=['摄氏 (°C)', '华氏 (°F)', '开尔文 (K)'],
            width=15,
            state='readonly'
        )
        self.from_unit.grid(row=2, column=1, pady=5, padx=10, sticky='w')
        self.from_unit.set('摄氏 (°C)')

        # 单位选择 - 到
        ttk.Label(main_frame, text="到:", font=('Arial', 10)).grid(
            row=3, column=0, sticky='w', pady=5
        )
        self.to_unit = ttk.Combobox(
            main_frame,
            values=['摄氏 (°C)', '华氏 (°F)', '开尔文 (K)'],
            width=15,
            state='readonly'
        )
        self.to_unit.grid(row=3, column=1, pady=5, padx=10, sticky='w')
        self.to_unit.set('华氏 (°F)')

        # 转换按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=20)

        self.convert_btn = ttk.Button(
            button_frame,
            text="🔄 转换",
            command=self.convert,
            width=15
        )
        self.convert_btn.pack(side=tk.LEFT, padx=5)

        self.clear_btn = ttk.Button(
            button_frame,
            text="🗑️ 清空",
            command=self.clear_all,
            width=15
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)

        self.swap_btn = ttk.Button(
            button_frame,
            text="⇄ 交换",
            command=self.swap_units,
            width=15
        )
        self.swap_btn.pack(side=tk.LEFT, padx=5)

        # 结果区域
        result_frame = ttk.LabelFrame(main_frame, text="转换结果", padding="10")
        result_frame.grid(row=5, column=0, columnspan=3, pady=10, sticky='ew')

        self.result_label = ttk.Label(
            result_frame,
            text="等待输入...",
            font=('Arial', 18, 'bold'),
            foreground='#0066cc'
        )
        self.result_label.pack(pady=10)

        # 详细信息
        self.detail_label = ttk.Label(
            result_frame,
            text="",
            font=('Arial', 10),
            foreground='#666'
        )
        self.detail_label.pack()

        # 历史记录
        history_frame = ttk.LabelFrame(main_frame, text="转换历史", padding="10")
        history_frame.grid(row=6, column=0, columnspan=3, pady=10, sticky='nsew')

        # 创建带滚动条的历史列表
        history_container = ttk.Frame(history_frame)
        history_container.pack(fill=tk.BOTH, expand=True)

        self.history_list = tk.Listbox(
            history_container,
            height=5,
            font=('Courier', 10),
            bg='white',
            selectmode=tk.SINGLE
        )
        self.history_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        history_scrollbar = ttk.Scrollbar(
            history_container,
            orient=tk.VERTICAL,
            command=self.history_list.yview
        )
        history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_list.config(yscrollcommand=history_scrollbar.set)

        # 配置网格权重
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(6, weight=1)

        # 状态栏
        self.status_label = ttk.Label(
            self.window,
            text="就绪 | 按 Enter 快速转换",
            relief=tk.SUNKEN,
            padding=(5, 2)
        )
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def bind_events(self):
        """绑定事件"""
        self.input_value.bind('<Return>', lambda e: self.convert())
        self.window.bind('<Escape>', lambda e: self.clear_all())

    def convert(self):
        """执行转换"""
        try:
            # 获取输入值
            value_str = self.input_value.get().strip()
            if not value_str:
                messagebox.showwarning("警告", "请输入温度值")
                self.status_label.config(text="请输入温度值")
                return

            value = float(value_str)

            # 获取单位
            from_unit = self.get_unit_code(self.from_unit.get())
            to_unit = self.get_unit_code(self.to_unit.get())

            # 执行转换
            result = self.converter.convert(value, from_unit, to_unit)

            # 获取单位符号
            from_symbol = self.converter.get_unit_symbol(from_unit)
            to_symbol = self.converter.get_unit_symbol(to_unit)

            # 显示结果
            result_text = f"{result:.2f} {to_symbol}"
            self.result_label.config(text=result_text, foreground='#0066cc')

            # 显示详细信息
            detail = f"{value:.2f} {from_symbol}  →  {result:.2f} {to_symbol}"
            self.detail_label.config(text=detail)

            # 添加到历史
            timestamp = datetime.now().strftime("%H:%M:%S")
            history_entry = f"[{timestamp}] {value:.2f}{from_symbol} = {result:.2f}{to_symbol}"
            self.history_list.insert(0, history_entry)

            # 限制历史记录数量
            if self.history_list.size() > self.max_history:
                self.history_list.delete(self.max_history)

            # 更新状态
            self.status_label.config(text=f"转换成功: {detail}")

        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字")
            self.status_label.config(text="输入无效，请输入数字")
            self.input_value.select_range(0, tk.END)
            self.input_value.focus()
        except Exception as e:
            messagebox.showerror("错误", str(e))
            self.status_label.config(text=f"错误: {str(e)}")

    def get_unit_code(self, unit_text: str) -> str:
        """从显示文本获取单位代码"""
        mapping = {
            '摄氏 (°C)': 'C',
            '华氏 (°F)': 'F',
            '开尔文 (K)': 'K'
        }
        return mapping.get(unit_text, 'C')

    def clear_all(self):
        """清空所有输入和结果"""
        self.input_value.delete(0, tk.END)
        self.result_label.config(text="等待输入...", foreground='#0066cc')
        self.detail_label.config(text="")
        self.status_label.config(text="已清空")
        self.input_value.focus()

    def swap_units(self):
        """交换单位"""
        from_unit = self.from_unit.get()
        to_unit = self.to_unit.get()
        self.from_unit.set(to_unit)
        self.to_unit.set(from_unit)
        self.status_label.config(text="单位已交换")
        # 自动转换
        if self.input_value.get().strip():
            self.convert()

    def run(self):
        """运行应用程序"""
        # 设置窗口居中
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')

        self.window.mainloop()