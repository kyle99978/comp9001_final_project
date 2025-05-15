import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CTkScrollableFrame 示例")
        self.geometry("500x400")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ✅ 创建滚动框，并设置 label
        self.scrollable_frame = ctk.CTkScrollableFrame(
            master=self,
            # label_text="模型选择",
            width=300,
            height=300,
            corner_radius=10
        )
        self.scrollable_frame.place(x=0, y=0)

        # ✅ 设置内容列可扩展
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        # ✅ 添加多个开关控件
        self.scrollable_frame_switches = []
        for i in range(100):
            switch = ctk.CTkSwitch(
                master=self.scrollable_frame,
                text=f"模型 {i+1}",
                font=("微软雅黑", 14)
            )
            switch.grid(row=i, column=0, padx=10, pady=(0, 10), sticky="w")
            self.scrollable_frame_switches.append(switch)

if __name__ == "__main__":
    app = App()
    app.mainloop()
