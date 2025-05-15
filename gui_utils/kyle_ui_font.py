# 创建字体字典
dky_fonts = {}

# 字体列表及其适用系统和用途
font_info = [
    "Times New Roman",  # Windows, macOS, 文本
    "Microsoft YaHei",  # Windows, 文本和控件
    "SF Pro",  # macOS, 文本和控件
    "Roboto",  # Windows, macOS, 文本和控件
    "Helvetica",  # macOS, 文本和控件
    "Open Sans",  # Windows, macOS, 文本和控件
    "Avenir",  # macOS, 文本和控件
    "PingFang SC",  # macOS, 文本和控件
    "Source Han Sans",  # Windows, macOS, 文本和控件
    "Arial",  # Windows, macOS, 文本和控件
    "DIN",  # Windows, macOS, 文本和控件
    "Futura",  # Windows, macOS, 文本和控件
    "Garamond",  # Windows, macOS, 文本
    "Segoe UI Symbol" # Symbol
]

# 使用循环创建 10 到 40 号字体
for font_name in font_info:
    for size in range(10, 51):
        # font_name = font_name.replace(' ', '_') # 替换空格
        font_name_key = font_name.split(" ")[0]
        font_key = f"{font_name_key}_{size}"
        dky_fonts[font_key] = (font_name, size)  # 加入填充字典
        # 添加注释说明
        # print(f"# {font_key}使用")

# 示例：访问某个字体
# print(dky_fonts["Times_25"])  # 输出: ('Times New Roman', 25)

