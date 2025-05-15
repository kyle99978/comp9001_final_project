import customtkinter as ctk


class CustomDropdown(ctk.CTkFrame):
    def __init__(self, master, options, width=150, height=200, button_text="Select", **kwargs):
        super().__init__(master, **kwargs)

        self.master = master
        self.options = options
        self.dropdown_width = width
        self.dropdown_height = height

        self.button = ctk.CTkButton(self, text=button_text, command=self.toggle_dropdown)
        self.button.pack(fill="x", padx=10, pady=10)

        self.dropdown_window = None  # 使用 Toplevel 显示下拉内容

    def create_dropdown_window(self):
        """创建下拉框窗口"""
        self.dropdown_window = ctk.CTkToplevel(self)
        self.dropdown_window.overrideredirect(True)  # 去掉边框
        self.dropdown_window.geometry(f"{self.dropdown_width}x{self.dropdown_height}")
        self.dropdown_window.configure(fg_color="#FFFFFF")
        self.dropdown_window.configure(corner_radius=10)

        # 滚动区域
        self.scrollable = ctk.CTkScrollableFrame(self.dropdown_window,
                                                 width=self.dropdown_width,
                                                 bg_color="#F0F0F0",
                                                 corner_radius=10,
                                                 fg_color="#F0F0F0",
                                                 height=self.dropdown_height)
        self.scrollable.pack(expand=True, fill="both")

        for option in self.options:
            button = ctk.CTkButton(
                self.scrollable,
                text=option,
                corner_radius=10,
                command=lambda opt=option: self.select_option(opt),
                fg_color="#F0F0F0",
                text_color="black",
                hover_color="#C0C0C0",
            )
            button.pack(fill="x", padx=0, pady=0)

    def toggle_dropdown(self):
        if self.dropdown_window and self.dropdown_window.winfo_exists():
            self.dropdown_window.destroy()
            self.dropdown_window = None
        else:
            self.create_dropdown_window()

            # 获取按钮相对于屏幕的位置
            button_x = self.winfo_rootx()
            button_y = self.winfo_rooty()
            button_height = self.button.winfo_height()

            # 设置下拉窗口位置在按钮下方
            x = button_x
            y = button_y + button_height
            self.dropdown_window.geometry(f"+{x}+{y}")

    def select_option(self, option):
        self.button.configure(text=option)
        if self.dropdown_window:
            self.dropdown_window.destroy()
            self.dropdown_window = None


if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("400x400")

    options = [f"Option {i}" for i in range(1, 21)]

    dropdown = CustomDropdown(app, options=options, width=200, height=150, button_text="Choose an option")
    dropdown.pack(pady=20, padx=20)

    app.mainloop()
