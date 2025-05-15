# import customtkinter as ctk
#
# # 初始化应用窗口
# app = ctk.CTk()
# app.geometry("500x300")
# app.title("CTkTabview 示例")
#
# # 创建 Tabview 控件
# tabview = ctk.CTkTabview(app, width=460, height=240)
# tabview.pack(padx=20, pady=20)
#
# # 添加标签页（你可以添加任意数量）
# tabview.add("主页")
# tabview.add("设置")
# tabview.add("关于")
#
# # ✅ 往“主页”标签页添加控件
# ctk.CTkLabel(tabview.tab("主页"), text="欢迎来到主页！").pack(pady=10)
# ctk.CTkEntry(tabview.tab("主页"), placeholder_text="请输入你的名字").pack()
#
# # ✅ 设置页内容
# ctk.CTkCheckBox(tabview.tab("设置"), text="启用功能 A").pack(pady=5)
# ctk.CTkSwitch(tabview.tab("设置"), text="夜间模式").pack(pady=5)
#
# # ✅ 关于页
# ctk.CTkLabel(tabview.tab("关于"), text="版本：v1.0\n作者：你自己").pack(pady=20)
#
# # ✅ 获取当前标签页的名称（可以用按钮触发）
# def show_selected_tab():
#     current_tab = tabview.get()
#     print("当前标签页是：", current_tab)
#
# btn = ctk.CTkButton(app, text="获取当前标签页", command=show_selected_tab)
# btn.pack()
#
# app.mainloop()

import customtkinter as ctk

app = ctk.CTk()
app.geometry("500x400")

tabview = ctk.CTkTabview(app, width=480, height=350)
tabview.pack(padx=10, pady=10)

tabview.add("内容页")
tabview.add("设置页")

# ✅ 在第一个标签页中添加滚动框
scroll_frame = ctk.CTkScrollableFrame(tabview.tab("内容页"), width=460, height=320)
scroll_frame.pack(x=10, y=10, fill="both", expand=True)

# 向滚动框中添加多个控件
for i in range(30):
    ctk.CTkLabel(scroll_frame, text=f"项目 {i+1}").pack(anchor="w", pady=2)

# 第二个页签正常使用
ctk.CTkLabel(tabview.tab("设置页"), text="设置内容").pack(pady=20)

app.mainloop()


