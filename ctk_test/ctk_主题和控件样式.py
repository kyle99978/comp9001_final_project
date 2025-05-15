import customtkinter as ctk


for xx in {"Light","Dark"}:

    for theme in ["blue", "dark-blue", "green"]:
        ctk.set_appearance_mode(xx)  # 或 "Light"
        ctk.set_default_color_theme(theme)

        app = ctk.CTk()
        app.title(f"Theme: {theme}")
        app.geometry("300x200")

        label = ctk.CTkLabel(app, text=f"This is {theme} theme")
        label.pack(pady=10)

        btn = ctk.CTkButton(app, text="Click Me")
        btn.pack(pady=10)

        app.mainloop()





'''
ctk.set_default_color_theme("my_red_theme.json")

文件内容：示例
{
  "CTkButton": {
    "fg_color": ["#FF4C4C", "#FF4C4C"],
    "hover_color": ["#CC0000", "#CC0000"],
    "text_color": ["#FFFFFF", "#FFFFFF"]
  }
}

完整：
{
  "CTk": {
    "fg_color": ["#1e1e2f", "#1e1e2f"]  // 主窗口背景
  },
  "CTkButton": {
    "fg_color": ["#4C4CFF", "#4C4CFF"],
    "hover_color": ["#6666FF", "#6666FF"],
    "text_color": ["#FFFFFF", "#FFFFFF"],
    "corner_radius": 10,
    "border_width": 1,
    "border_color": ["#999999", "#999999"]
  },
  "CTkLabel": {
    "text_color": ["#FFFFFF", "#FFFFFF"],
    "fg_color": "transparent"
  },
  "CTkEntry": {
    "fg_color": ["#2C2C3C", "#2C2C3C"],
    "border_color": ["#6666FF", "#6666FF"],
    "text_color": ["#FFFFFF", "#FFFFFF"],
    "placeholder_text_color": ["#888888", "#888888"]
  }
}



属性名	说明
fg_color	主背景色（按钮、输入框等）
bg_color	背景色（嵌套用，一般自动继承）
text_color	文本颜色
hover_color	鼠标悬停时的颜色
border_color	边框颜色
border_width	边框宽度（数值）
text_color_disabled	禁用状态下文字颜色
fg_color_disabled	禁用状态下的背景色
hover_color_disabled	禁用状态下的悬停色


✅ 特定控件额外支持：
📦 CTkButton
所有通用属性
corner_radius：圆角程度
text_color、hover_color、border_width

🧾 CTkEntry
fg_color：输入框背景色
border_color、text_color、placeholder_text_color

🧩 CTkFrame
fg_color：框体颜色
border_color、corner_radius

🔘 CTkRadioButton / CTkCheckBox
border_color、fg_color、checkmark_color

📍 CTkSlider
progress_color：滑动进度条颜色
button_color：圆点按钮颜色





'''