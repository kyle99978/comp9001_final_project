# 高级 GUI 翻译器（customtkinter） - 绝对定位 + 弹出菜单选择音频来源

import customtkinter as ctk
import tkinter as tk

class TranslatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("高级翻译器 GUI - customtkinter 版")
        self.geometry("1200x200+200+100")
        self.resizable(False, False)
        ctk.set_appearance_mode("light")  # 可选 dark / system
        ctk.set_default_color_theme("blue")

        self.audio_sources = [
            "麦克风 Mic",
            "系统音频 System",
            "蓝牙设备 Bluetooth",
            "虚拟音频 Virtual",
            "外部输入 External",
            "网络流 Network"
        ]
        self.current_audio = tk.StringVar(value=self.audio_sources[0])

        self.setup_ui()

    def setup_ui(self):
        # 文本区域
        self.textbox = ctk.CTkTextbox(self, font=("Microsoft YaHei", 13), wrap="none",
                                      width=850, height=130)
        self.textbox.place(x=20, y=20)

        # 滚动条（customtkinter 内置支持）
        self.textbox_scroll_x = ctk.CTkScrollbar(self, orientation="horizontal", command=self.textbox.xview,
                                                 width=850)
        self.textbox_scroll_y = ctk.CTkScrollbar(self, orientation="vertical", command=self.textbox.yview,
                                                 height=130)
        self.textbox.configure(xscrollcommand=self.textbox_scroll_x.set, yscrollcommand=self.textbox_scroll_y.set)
        self.textbox_scroll_y.place(x=870, y=20)
        self.textbox_scroll_x.place(x=20, y=150)

        self.create_buttons()

    def create_buttons(self):
        # 功能按钮
        func_labels = ["转", "翻", "存", "改"]
        for i, text in enumerate(func_labels):
            btn = ctk.CTkButton(self, text=text, corner_radius=8, width=60, height=40)
            btn.place(x=900 + i * 70, y=20)

        # 导航按钮
        nav_labels = ["top", "up", "bottom", "down"]
        positions = [(0, 0), (0, 1), (1, 0), (1, 1)]
        for i, (text, (r, c)) in enumerate(zip(nav_labels, positions)):
            btn = ctk.CTkButton(self, text=text, corner_radius=8, width=70, height=40)
            btn.place(x=900 + c * 80, y=70 + r * 50)

        # 音频输入按钮（自定义弹出菜单）
        self.input_button = ctk.CTkButton(self, text=self.current_audio.get(), corner_radius=8,
                                          width=150, height=30, command=self.show_audio_menu)
        self.input_button.place(x=900, y=170)

        # 退出按钮
        exit_btn = ctk.CTkButton(self, text="退出", corner_radius=8, width=100, height=30,
                                 fg_color="red", hover_color="#b22222", command=self.quit)
        exit_btn.place(x=1060, y=170)

    def show_audio_menu(self):
        menu = tk.Menu(self, tearoff=0, font=("Microsoft YaHei", 10))
        for source in self.audio_sources:
            menu.add_command(label=source, command=lambda s=source: self.select_audio_source(s))
        menu.tk_popup(self.input_button.winfo_rootx(), self.input_button.winfo_rooty() + self.input_button.winfo_height())

    def select_audio_source(self, source):
        self.current_audio.set(source)
        self.input_button.configure(text=source)


if __name__ == '__main__':
    app = TranslatorApp()
    app.mainloop()