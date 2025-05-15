import customtkinter as ctk
import ttkbootstrap as ttk
from ttkbootstrap.widgets import Meter

class MixedApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CTk + ttkbootstrap 混用示例")
        self.geometry("400x300")
        ctk.set_appearance_mode("light")

        # CTk Button 示例
        ctk.CTkButton(self, text="CTk 按钮").place(x=20, y=20)

        # ttkbootstrap Meter 放入 CTk 窗口中
        meter = Meter(
            master=self,
            metersize=200,
            amountused=55,
            amounttotal=100,
            metertype="semi",
            subtext="系统状态",
            interactive=False,
            bootstyle="success"
        )
        meter.place(x=100, y=80)

if __name__ == "__main__":
    app = MixedApp()
    app.mainloop()
