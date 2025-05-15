import customtkinter as ctk
from markdown import markdown
from tkhtmlview import HTMLLabel  # 用于渲染HTML格式的内容
# from tkinterweb import HtmlFrame
import tkinterweb as TKweb

# tkinterweb 和 tkhtmlview区别：
# tkhtmlview： 有内置的字体style，不需要后面去添加css美化，但是不能复制编辑
# tkinterweb可以复制，但是需要自定义css

from transfer_md_textfont.webframe_css import get_html_style, get_scroll_fix_css

# 初始化CustomTkinter应用
ctk.set_appearance_mode("System")  # Appearance: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Theme color: "blue", "dark-blue", "green"

# 创建主窗口
root0 = ctk.CTk()
root0.withdraw()

root = ctk.CTkToplevel()
root.title("Markdown 转换工具")
root.geometry("800x500")

root.grid_rowconfigure(0, weight=2)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)





# 上面的：HTML渲染窗口
output_frame = ctk.CTkFrame(root,corner_radius=10, fg_color="#999999")
output_frame.grid(row=0, column=0, columnspan=8,sticky="nsew", padx=10, pady=10)

# HTMLLabel
output_html_frame = HTMLLabel(output_frame, )

# 默认用 CSS 控制溢出行为，必须显式指定 overflow-x: auto 才有效果
# 没有水平滚动条，内部机制的问题,horizontal_scrollbar="auto" 这个参数目前 没有被 HtmlFrame 真正实现
# Overflow behaviour is controlled by CSS by default, overflow-x: auto must be explicitly specified to have any effect.
# No horizontal scrollbar, internal mechanism, horizontal_scrollbar="auto" parameter is not implemented by HtmlFrame.

output_html_frame.pack(fill="both", expand=True, padx=10, pady=10)
# output_html_frame = TKweb.HtmlFrame(output_frame, messages_enabled=True,
#                                     vertical_scrollbar="auto",
# 默认用 CSS 控制溢出行为，必须显式指定 overflow-x: auto 才有效果
# 没有水平滚动条，内部机制的问题,horizontal_scrollbar="auto" 这个参数目前 没有被 HtmlFrame 真正实现
# Overflow behaviour is controlled by CSS by default, overflow-x: auto must be explicitly specified to have any effect.
# No horizontal scrollbar, internal mechanism, horizontal_scrollbar="auto" parameter is not implemented by HtmlFrame.
#                                     )
# output_html_frame.pack(fill="both", expand=True, padx=10, pady=10)

def convert_markdown(index:str="test"):
    if index ==1:
        html = markdown("", extensions=["fenced_code", "tables", "codehilite", "nl2br"])
        # style = get_html_style(scale=2) + get_scroll_fix_css()
        # styled_html = style + html
        output_html_frame.set_html(html)
    else:
        markdown_text = input_text.get("1.0", "end").strip()

        if markdown_text:
            html = markdown(markdown_text, extensions=["fenced_code", "tables", "codehilite", "nl2br"])
            # style = get_html_style(scale=2) + get_scroll_fix_css()
            # styled_html = style + html
            output_html_frame.set_html(html)



# 下面：Markdown输入窗口
input_text = ctk.CTkTextbox(root, wrap="none",)
input_text.insert("1.0", "# 在这里输入\n例如，`Hello World`")
input_text.grid(row=1, column=0, columnspan=8, sticky="nsew", padx=10, pady=10)
convert_markdown(index="test")


def xxx(choice):
    if choice == 1:
        var2.set(0)  # 取消第二个复选框
    elif choice == 2:
        var1.set(0)  # 取消第一个复选框

# 添加两个变量
var1 = ctk.IntVar()
var2 = ctk.IntVar()

# 修改复选框 Modify checkbox
convert_button1 = ctk.CTkCheckBox(root, text="text", variable=var1,
                                  command=lambda val=1: xxx(val), width=50, height=30)
convert_button1.grid(row=3, column=1, padx=5, pady=10)

convert_button2 = ctk.CTkCheckBox(root, text="md text", variable=var2,
                                  command=lambda val=2: xxx(val), width=50, height=30)
convert_button2.grid(row=3, column=2, padx=5, pady=10)




# 中部：转换按钮
convert_button = ctk.CTkButton(root, text="save as", command=convert_markdown,width=80,height=30)
convert_button.grid(row=3, column=5, padx=10, pady=10)

# 中部：转换按钮
convert_button = ctk.CTkButton(root, text="转换", command=convert_markdown,width=80,height=30)
convert_button.grid(row=3, column=6, padx=10, pady=10)

# 运行主程序循环
root.mainloop()
