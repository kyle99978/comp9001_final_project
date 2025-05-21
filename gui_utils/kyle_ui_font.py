# 创建字体字典 # Create  font
dky_fonts = {}

# List of fonts and their applicable systems and uses
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

# Use loops to create fonts from size 10 to 40
for font_name in font_info:
    for size in range(10, 51):
        # font_name = font_name.replace(' ', '_') # 替换空格
        font_name_key = font_name.split(" ")[0]
        font_key = f"{font_name_key}_{size}"
        dky_fonts[font_key] = (font_name, size)  # 加入填充字典
        # 添加注释说明
        # print(f"# {font_key}使用")

# Example: Accessing a fontExample: Accessing a font
# print(dky_fonts["Times_25"])  # 输出: ('Times New Roman', 25)

