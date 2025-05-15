'''
ctk 没有原生 Tooltip 工具提示，如需可手动用 Toplevel 模拟

Tooltip（工具提示）是当鼠标悬停在一个控件上时，会弹出一个小气泡说明，比如：

    悬停在 🛠️按钮上弹出：“保存项目”

    悬停在 📤上弹出：“上传文件”

'''


import customtkinter as ctk
import tkinter as tk


class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None

        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        if self.tip_window or not self.text:
            return
        x = self.widget.winfo_rootx() + 40
        y = self.widget.winfo_rooty() + 30

        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)  # 无边框
        tw.wm_geometry(f"+{x}+{y}")

        label = tk.Label(tw, text=self.text, justify='left',
                         background="lightyellow", relief='solid', borderwidth=1,
                         font=("Microsoft YaHei", 10))
        label.pack(ipadx=5, ipady=2)

    def hide_tooltip(self, event=None):
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()


class TooltipDemo(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CustomTkinter Tooltip 示例")
        self.geometry("400x200")

        btn = ctk.CTkButton(self, text="悬停查看提示")
        btn.pack(pady=40)

        # 添加 tooltip
        Tooltip(btn, "我是一个提示文本 tooltip！")


if __name__ == "__main__":
    app = TooltipDemo()
    app.mainloop()
