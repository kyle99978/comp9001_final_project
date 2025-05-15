# HTML 标签	Python 渲染逻辑（HTMLLabel）	已转为 CSS
# <h1> ~ <h6>	使用 Defs.HEADINGS_FONT_SIZE 设置字体大小	✅ 对应 font-size
# <p> / <div>	设置下间距	✅ margin-bottom
# <code> / <pre>	用 Courier 字体 + 灰背景 + padding + 边框圆角	✅ 完全还原
# <ul> / <ol> / <li>	使用 tab 缩进 + bullet	✅ 使用 padding-left 和 list-style 效果一致
# <a href>	蓝色字体 + underline + 鼠标悬停变色	✅ 用 CSS 完美模拟
# <strong> / <b>	加粗（font-weight: bold）	✅ 有
# <em> / <i>	斜体（font-style: italic）	✅ 有




# 改进点	效果
# pre 自动换行 + 横向滚动兼容	保留滚动条的同时，在较窄窗口也能换行
# 多级 li 缩进清晰	嵌套结构看得更明白
# 表格默认样式增强	加边框 + 表头浅灰底，更好看
# code 与 pre 分开设置	更符合 Markdown 语义差异

# ✅ 白天模式：黑字白底
# ✅ 夜间模式：白字深灰底
# ✅ 自动跟随 CustomTkinter 当前主题（ctk.get_appearance_mode()）
# ✅ 样式包含标题、段落、列表、代码块、表格、链接
# ✅ 使用方式简单（只调用一个函数）

# from markdown import markdown
#
# # 获取当前主题对应的 CSS 样式
# style = get_html_style()
#
# # 转换 Markdown 内容
# html = markdown(markdown_text, extensions=["fenced_code", "tables"])
#
# # 拼接样式并显示
# output_html_frame.load_html(style + html)


import customtkinter as ctk

def get_scroll_fix_css():
    return """
    <style>
        pre, code, table {
            display: block;
            overflow-x: auto;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        body {
            overflow-x: auto;
        }
    </style>
    """


def get_html_style(mode="System", scale=1.0) -> str:
    """
    生成自适应暗/亮主题 + 支持视觉缩放的 HTML 样式
    参数:
        mode: "Light" | "Dark" | "System"
        scale: 视觉放大倍率（默认1.0）
    """
    if mode == "System":
        mode = ctk.get_appearance_mode()

    # 颜色方案
    if mode == "Dark":
        background = "#1e1e1e"
        foreground = "#eeeeee"
        code_bg = "#2d2d2d"
        table_border = "#444"
        table_header = "#333"
        link_color = "#4ea1ff"
    else:
        background = "#ffffff"
        foreground = "#000000"
        code_bg = "#f4f4f4"
        table_border = "#ccc"
        table_header = "#f0f0f0"
        link_color = "blue"

    # 字号基准
    base = 16 * scale
    h1 = int(base * 2.0)
    h2 = int(base * 1.6)
    h3 = int(base * 1.4)
    h4 = int(base * 1.2)
    h5 = int(base * 1.0)
    h6 = int(base * 0.9)
    code_font = int(base * 0.95)
    pre_font = int(base * 0.95)
    line_height = round(1.6 * scale, 2)
    pad = int(12 * scale)
    cell_pad = int(8 * scale)

    return f"""
<style> 
    body {{
        font-family: 'Segoe UI', 'Calibri', 'Helvetica', sans-serif;
        font-size: {base}px;
        color: {foreground};
        background-color: {background};
        line-height: {line_height};
        padding: {pad}px;
    }}

    h1 {{ font-size: {h1}px; font-weight: bold; }}
    h2 {{ font-size: {h2}px; font-weight: bold; }}
    h3 {{ font-size: {h3}px; font-weight: bold; }}
    h4 {{ font-size: {h4}px; font-weight: bold; }}
    h5 {{ font-size: {h5}px; font-weight: bold; }}
    h6 {{ font-size: {h6}px; font-weight: bold; }}

    p, div {{ margin-bottom: {int(1.0 * scale)}em; }}

    code {{
        font-size: {code_font}px;
        font-family: 'Courier New', monospace;
        background-color: {code_bg};
        padding: 2px 5px;
        border-radius: 4px;
    }}

    pre {{
        font-size: {pre_font}px;
        font-family: 'Courier New', monospace;
        background-color: {code_bg};
        padding: {pad}px;
        border-radius: 5px;
        overflow-x: auto;
        white-space: pre-wrap;
        word-wrap: break-word;
    }}

    ul, ol {{
        padding-left: {24 * scale}px;
        margin-bottom: 1em;
    }}

    li {{
        margin: 4px 0;
    }}

    ul ul, ol ul, ul ol, ol ol {{
        margin-left: 20px;
    }}

    a {{
        color: {link_color};
        text-decoration: underline;
    }}

    table {{
        border-collapse: collapse;
        margin: 1em 0;
        width: 100%;
        overflow-x: auto;
       /* display: block;*/
    }}

    th, td {{
        border: 1px solid {table_border};
        padding: {cell_pad}px {cell_pad + 2}px;
        text-align: left;
        white-space: pre-line; /* ✅ 这里加，保证 <br>和换行符有效 */
        word-break: break-word; /* ✅ 防止单词太长撑爆表格 */
    }}

    th {{
        background-color: {table_header};
    }}
</style>
"""
