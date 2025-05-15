# import customtkinter
#
# # 定义一个包含复选框的自定义框架
# class MyCheckboxFrame(customtkinter.CTkFrame):
#     def __init__(self, master, values):
#         super().__init__(master)
#         self.values = values
#         self.checkboxes = []
#
#         # 创建并放置复选框
#         for i, value in enumerate(self.values):
#             checkbox = customtkinter.CTkCheckBox(self, text=value)
#             checkbox.grid(row=i, column=0, padx=10, pady=(10, 0), sticky="w")
#             self.checkboxes.append(checkbox)
#
#     # 获取选中复选框的文本
#     def get(self):
#         checked_checkboxes = []
#         for checkbox in self.checkboxes:
#             if checkbox.get() == 1:
#                 checked_checkboxes.append(checkbox.cget("text"))
#         return checked_checkboxes
#
# # 定义一个可滚动的包含复选框的框架
# class MyScrollableCheckboxFrame(customtkinter.CTkScrollableFrame):
#     def __init__(self, master, title, values):
#         super().__init__(master, label_text=title)
#         self.grid_columnconfigure(0, weight=1)
#         self.values = values
#         self.checkboxes = []
#
#         # 创建并放置复选框
#         for i, value in enumerate(self.values):
#             checkbox = customtkinter.CTkCheckBox(self, text=value)
#             checkbox.grid(row=i, column=0, padx=10, pady=(10, 0), sticky="w")
#             self.checkboxes.append(checkbox)
#
#     # 获取选中复选框的文本
#     def get(self):
#         checked_checkboxes = []
#         for checkbox in self.checkboxes:
#             if checkbox.get() == 1:
#                 checked_checkboxes.append(checkbox.cget("text"))
#         return checked_checkboxes
#
# # 定义主应用程序类
# class App(customtkinter.CTk):
#     def __init__(self):
#         super().__init__()
#
#         self.title("我的应用程序")
#         self.geometry("400x220")
#         self.grid_columnconfigure(0, weight=1)
#         self.grid_rowconfigure(0, weight=1)
#
#         values = ["值 1", "值 2", "值 3", "值 4", "值 5", "值 6"]
#         self.scrollable_checkbox_frame = MyScrollableCheckboxFrame(self, title="值", values=values)
#         self.scrollable_checkbox_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")
#
#         self.button = customtkinter.CTkButton(self, text="我的按钮", command=self.button_callback)
#         self.button.grid(row=3, column=0, padx=10, pady=10, sticky="ew", columnspan=2)
#
#     # 按钮的回调函数
#     def button_callback(self):
#         print("checkbox_frame:", self.scrollable_checkbox_frame.get())
#
# # 创建并运行应用程序
# app = App()
# app.mainloop()

import customtkinter

# 定义主应用程序类
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("我的应用程序")
        self.geometry("400x220")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 创建一个可滚动的框架
        scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="值")
        scrollable_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")

        # 添加复选框到可滚动框架中
        values = ["值 1", "值 2", "值 3", "值 4", "值 5", "值 6"]
        self.checkboxes = []
        for i, value in enumerate(values):
            checkbox = customtkinter.CTkCheckBox(scrollable_frame, text=value)
            checkbox.grid(row=i, column=0, padx=10, pady=(10, 0), sticky="w")
            self.checkboxes.append(checkbox)

        # 创建一个按钮
        self.button = customtkinter.CTkButton(self, text="我的按钮", command=self.button_callback)
        self.button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    # 按钮的回调函数
    def button_callback(self):
        checked_values = [checkbox.cget("text") for checkbox in self.checkboxes if checkbox.get() == 1]
        print("选中的值:", checked_values)

# 创建并运行应用程序
app = App()
app.mainloop()

