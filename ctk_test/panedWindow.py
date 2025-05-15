# # 在 tkinter 的 PanedWindow 控件中，默认情况下，子控件是从左到右（对于水平分隔）或从上到下（对于垂直分隔）依次添加的。
# # 如果你想添加四个子控件，可以使用两个嵌套的 PanedWindow 来实现。
# #
# # 以下是一个示例，展示如何在 PanedWindow 中添加四个子控件，并使它们均匀分布：
#
# import tkinter as tk
# import customtkinter
#
# # 创建主应用程序窗口
# root = tk.Tk()
# root.title("PanedWindow 示例")
# root.geometry("600x400")
#
# # 创建主 PanedWindow 控件（水平分隔）
# main_paned_window = tk.PanedWindow(root, orient=tk.HORIZONTAL)
# main_paned_window.pack(fill=tk.BOTH, expand=True)
#
# # 创建左侧 PanedWindow 控件（垂直分隔）
# left_paned_window = tk.PanedWindow(main_paned_window, orient=tk.VERTICAL)
# main_paned_window.add(left_paned_window)
#
# # 创建右侧 PanedWindow 控件（垂直分隔）
# right_paned_window = tk.PanedWindow(main_paned_window, orient=tk.VERTICAL)
# main_paned_window.add(right_paned_window)
#
# # 创建并添加左上框架
# left_top_frame = customtkinter.CTkFrame(left_paned_window, fg_color="lightblue")
# left_paned_window.add(left_top_frame)
#
# # 创建并添加左下框架
# left_bottom_frame = customtkinter.CTkFrame(left_paned_window, fg_color="lightgreen")
# left_paned_window.add(left_bottom_frame)
#
# # 创建并添加右上框架
# right_top_frame = customtkinter.CTkFrame(right_paned_window, fg_color="lightyellow")
# right_paned_window.add(right_top_frame)
#
# # 创建并添加右下框架
# right_bottom_frame = customtkinter.CTkFrame(right_paned_window, fg_color="lightcoral")
# right_paned_window.add(right_bottom_frame)
#
# # 在每个框架中添加一些控件以示例
# customtkinter.CTkLabel(left_top_frame, text="左上").pack(padx=20, pady=20)
# customtkinter.CTkLabel(left_bottom_frame, text="左下").pack(padx=20, pady=20)
# customtkinter.CTkLabel(right_top_frame, text="右上").pack(padx=20, pady=20)
# customtkinter.CTkLabel(right_bottom_frame, text="右下").pack(padx=20, pady=20)
#
# # 运行应用程序
# root.mainloop()


import tkinter as tk
import customtkinter

# 创建主应用程序窗口
root = tk.Tk()
root.title("PanedWindow 示例")
root.geometry("600x400")

# 创建主 PanedWindow 控件（水平分隔）
main_paned_window = tk.PanedWindow(root, orient=tk.HORIZONTAL)
main_paned_window.pack(fill=tk.BOTH, expand=True)

# 创建左侧垂直分隔的框架
left_frame = tk.PanedWindow(main_paned_window, orient=tk.VERTICAL)
main_paned_window.add(left_frame)

# 创建右侧垂直分隔的框架
right_frame = tk.PanedWindow(main_paned_window, orient=tk.VERTICAL)
main_paned_window.add(right_frame)

# 创建并添加左上框架
left_top_frame = customtkinter.CTkFrame(left_frame, fg_color="lightblue")
left_frame.add(left_top_frame)

# 创建并添加左下框架
left_bottom_frame = customtkinter.CTkFrame(left_frame, fg_color="lightgreen")
left_frame.add(left_bottom_frame)

# 创建并添加右上框架
right_top_frame = customtkinter.CTkFrame(right_frame, fg_color="lightyellow")
right_frame.add(right_top_frame)

# 创建并添加右下框架
right_bottom_frame = customtkinter.CTkFrame(right_frame, fg_color="lightcoral")
right_frame.add(right_bottom_frame)

# 在每个框架中添加一些控件以示例
customtkinter.CTkLabel(left_top_frame, text="左上").pack(padx=20, pady=20)
customtkinter.CTkLabel(left_bottom_frame, text="左下").pack(padx=20, pady=20)
customtkinter.CTkLabel(right_top_frame, text="右上").pack(padx=20, pady=20)
customtkinter.CTkLabel(right_bottom_frame, text="右下").pack(padx=20, pady=20)

# 运行应用程序
root.mainloop()

