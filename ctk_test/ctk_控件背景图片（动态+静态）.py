# import itertools
#
# import customtkinter as ctk
# from PIL import Image
# from pathlib import Path

# class App(ctk.CTk):
#     def __init__(self):
#         super().__init__()
#         self.geometry("400x300")
#         self.title("CTkButton 背景图示例")
#
#         # ✅ 加载并缩放图片
#         # img_path = Path(__file__).parent / "c1.png"  # 确保路径对（你可以放到当前目录）
#         image = Image.open("c1.png")
#         self.bg_image = ctk.CTkImage(light_image=image, size=(180, 60))  # 必须用 light_image
#
#         # ✅ 创建按钮
#         self.btn = ctk.CTkButton(
#             self,
#             text="",  # 先不显示文字，避免遮挡图像
#             image=self.bg_image,
#             width=180,
#             height=60,
#             fg_color="transparent",  # 设置为透明，图像才会显示完整
#             hover_color="gray90",    # 可加悬停效果测试按钮是否存在
#         )
#         self.btn.place(x=110, y=100)
#
# if __name__ == "__main__":
#     app = App()
#     app.mainloop()




# 加载 GIF 动图： 使用 PIL 库的 Image.open() 方法打开 GIF 动图，并逐帧加载。
#
# 处理帧： 使用 ImageTk.PhotoImage 将每一帧转换为可以在 tkinter 中显示的图像对象，并存储在一个列表中。
#
# 更新帧： 创建一个函数来更新 Label 控件的图像，并使用 tkinter 的 after() 方法定时调用该函数，以实现动画效果。

import customtkinter as ctk
import os
from PIL import Image, ImageTk
import tkinter as tk

# 检查 GIF 文件是否存在
gif_path = "B1.gif"
if not os.path.exists(gif_path):
    raise FileNotFoundError(f"GIF 文件未找到: {gif_path}")

# 创建主窗口
root = ctk.CTk()
root.geometry("800x800")
root.title("CTk Button with GIF Background")

# 加载 GIF 动图
gif_image = Image.open(gif_path)
frames = []
try:
    while True:
        frames.append(ImageTk.PhotoImage(gif_image.copy().convert("RGBA")))
        gif_image.seek(len(frames))  # 移动到下一帧
except EOFError:
    pass  # 处理完所有帧

# 获取 GIF 动图的尺寸
gif_width, gif_height = frames[0].width(), frames[0].height()

# 更新 GIF 动画的函数
def update_gif(frame_index):
    frame = frames[frame_index]
    gif_label.configure(image=frame)
    root.after(100, update_gif, (frame_index + 1) % len(frames))

# 创建按钮
button = ctk.CTkButton(root, text="Click Me")
button.pack(pady=20)

# 创建用于显示 GIF 的 Label，并设置其大小
gif_label = tk.Label(root, width=gif_width, height=gif_height)
gif_label.pack()

# 启动 GIF 动画
update_gif(0)

# 运行主循环
root.mainloop()

