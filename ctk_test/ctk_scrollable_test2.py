import customtkinter as ctk

app = ctk.CTk()
app.geometry("500x400")
app.title("CTkTabview + 滚动示例")

# ✅ 固定尺寸的 Tabview
tabview = ctk.CTkTabview(app, width=450, height=300,fg_color="black",bg_color="white")
tabview.place(x=25, y=30)

tabview.add("文本内容")
tabview.add("按钮列表")

# ✅ 标签页 1：加入滚动框，用于长文本显示
scroll1 = ctk.CTkScrollableFrame(tabview.tab("文本内容"), width=300, height=100, fg_color="green")
scroll1.place(x=20, y=20)

# for i in range(30):
#     ctk.CTkLabel(scroll1, text=f"第 {i+1} 段内容", font=("微软雅黑", 14)).pack(anchor="w", pady=2)

# ✅ 标签页 2：加入滚动框，显示很多按钮
scroll2 = ctk.CTkScrollableFrame(tabview.tab("按钮列表"), width=420, height=260)
scroll2.pack(padx=10, pady=10)

for i in range(20):
    ctk.CTkButton(scroll2, text=f"按钮 {i+1}").pack(pady=5)

app.mainloop()
