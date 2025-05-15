import customtkinter as ctk

class WidgetDemoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CustomTkinter 控件演示面板")
        self.geometry("700x500")
        ctk.set_appearance_mode("light")  # 或 'dark'
        ctk.set_default_color_theme("blue")

        self.create_widgets()

    def create_widgets(self):
        # 标题标签
        ctk.CTkLabel(self, text="🎨 控件演示区", font=("微软雅黑", 18)).pack(pady=10)

        # 主题切换按钮
        self.theme_mode = ctk.StringVar(value="light")
        self.theme_switch = ctk.CTkSwitch(self, text="切换暗色模式",
                                          variable=self.theme_mode, onvalue="dark", offvalue="light",
                                          command=self.toggle_theme)
        self.theme_switch.pack(pady=10)

        # Entry + Label 同步
        self.entry_var = ctk.StringVar()
        self.entry = ctk.CTkEntry(self, placeholder_text="请输入内容...", textvariable=self.entry_var)
        self.entry.pack(pady=10)
        self.display_label = ctk.CTkLabel(self, text="你输入了：")
        self.display_label.pack()
        ctk.CTkButton(self, text="同步显示", command=self.sync_label).pack(pady=5)

        # OptionMenu 下拉菜单
        self.option = ctk.StringVar(value="选择一个选项")
        self.option_menu = ctk.CTkOptionMenu(self, variable=self.option, values=["选项 A", "选项 B", "选项 C"])
        self.option_menu.pack(pady=10)

        # CheckBox + 状态展示
        self.check_var = ctk.BooleanVar()
        self.checkbox = ctk.CTkCheckBox(self, text="我同意条款", variable=self.check_var)
        self.checkbox.pack(pady=10)

        # Switch + 状态反馈
        self.switch_var = ctk.BooleanVar()
        self.switch = ctk.CTkSwitch(self, text="开关按钮", variable=self.switch_var)
        self.switch.pack(pady=10)

        # Slider + 进度条联动
        self.slider_val = ctk.DoubleVar(value=0.5)
        self.slider = ctk.CTkSlider(self, from_=0, to=1, number_of_steps=100,
                                    variable=self.slider_val, command=self.update_progress)
        self.slider.pack(pady=10)
        self.progress = ctk.CTkProgressBar(self, orientation="horizontal", width=200, height=15,
                                           progress_color="green", variable=self.slider_val)
        self.progress.pack(pady=5)

    def sync_label(self):
        self.display_label.configure(text=f"你输入了：{self.entry_var.get()}")

    def toggle_theme(self):
        mode = self.theme_mode.get()
        ctk.set_appearance_mode(mode)

    def update_progress(self, value):
        self.progress.set(float(value))


if __name__ == "__main__":
    app = WidgetDemoApp()
    app.mainloop()
