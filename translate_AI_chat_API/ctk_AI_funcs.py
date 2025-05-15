import os

from markdown import markdown
from transfer_md_textfont.webframe_css import get_html_style, get_scroll_fix_css
import customtkinter as ctk

def create_toplevel_with_icon(top, icon_path):
    icon_abs = os.path.abspath(icon_path)
    top.iconbitmap(icon_abs)
    # 自动监听窗口恢复或更新后再设置图标（只做一次绑定）
    # Automatically listen for windows to be restored or updated before setting icons (only one binding)
    def reapply_icon(event=None):
        try:
            top.iconbitmap(icon_abs)
        except:
            pass

    # 绑定窗口显示、激活等事件     # Bind events for window display, activation, etc.
    top.bind("<Map>", reapply_icon)         # 窗口出现
    top.bind("<Visibility>", reapply_icon)  # 窗口变为可见
    top.bind("<FocusIn>", reapply_icon)     # 获取焦点
    top.update()
    return top



def text_or_mdtext1(root, output_frame, output_frame2,var2):

        var2.set(0)  # 取消第二个复选框  Cancel the second checkbox
        output_frame.grid_remove()
        output_frame2.grid(row=0, rowspan=2, column=0, columnspan=8, sticky="nsew", padx=10, pady=10)
        root.update()

def text_or_mdtext2(root, output_frame, output_frame2,var1):

        var1.set(0)  # 取消第二个复选框  Cancel the second checkbox
        output_frame2.grid_remove()
        output_frame.grid()
        root.update()




def get_text_from_user(root,input_text):
    usr_input = input_text.get("1.0", "end").strip()
    input_text.delete("1.0", "end")
    root.update()  # 不加刷新的话，显示会延迟
    # "1.0"` 表示从文本的第一行、第0列位置开始提取文本（行和列都是从 1 和 0 开始数的）。
    # "end"` 表示提取到文本的末尾（包括结尾的换行符 `\n`，如果有
    # "1.0"` means that the text is extracted from the first line of the text, from the 0th column position (lines and columns are counted from 1 and 0).
    # "end"` means extract to the end of the text (including the line break `\n` at the end, if any).
    if usr_input !="":
        return usr_input
    else:
        return ""


def convert_markdown(root, output_html_frame,outputframe2, ai_answer, index: int = 0, ):
    if index == 1:
        t1 = '''
#The free version provides:
##gpt-4o, gpt-4.1 for 5 times a day,
##deepseek-r1, deepseek-v3 for 30 times a day,
##gpt-4o-mini, gpt-3.5-turbo, gpt-4.1-mini, gpt-4.1-nano for 200 times a day.
'''
        outputframe2.insert("0.0",t1)
        root.update()
        html = markdown(t1, extensions=["fenced_code", "tables", "codehilite", "nl2br"])
        style = get_html_style(scale=1) + get_scroll_fix_css()
        styled_html = style + html
        output_html_frame.load_html(styled_html)
        root.update()
    else:
        outputframe2.delete("0.0", "end")
        markdown_text = ai_answer
        outputframe2.insert("0.0", ai_answer)
        root.update()
        if markdown_text:
            html = markdown(markdown_text, extensions=["fenced_code", "tables", "codehilite", "nl2br"])
            style = get_html_style(scale=1.5) + get_scroll_fix_css()
            styled_html = style + html
            output_html_frame.load_html(styled_html)
        root.update()







