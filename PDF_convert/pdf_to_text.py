# pdf 读取后的格式
# 元素类型	要求
# text	保留为字符串
# images	整页中真实嵌入的图片内容，以 图像数据 存储，⚠️ 可以还原为图片（不是路径）
# tables	表格本身不要结构数据，而是直接截图为图像，⚠️ 后续也可转为图片
# [
#   {
#     "page_num": 1,
#     "text": "...",
#     "images": [PIL.Image, PIL.Image, ...],      # 可保存
#     "tables": [PIL.Image, PIL.Image, ...]       # 可保存
#   },
#   ...
# ]
import os

import pdfplumber
from PIL import Image
from io import BytesIO

import warnings
warnings.filterwarnings("ignore", category=UserWarning)


def extract_pdf_as_images(file_path,text:bool=True,image:bool=True,table:bool=True):

    results = []
    with pdfplumber.open(file_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):

            page_data = {
                "page_num": page_num,
                "text": "",
                "images": [],
                "tables": [],
            }
            if text:
                page_data["text"] = page.extract_text() or ""

            if image or table:
                page_image = page.to_image(resolution=200)  # 先渲染整页成PIL图片

            if image:
            # 提取嵌入图片（bitmap图片）
                for img in page.images:
                    bbox = (img["x0"], img["top"], img["x1"], img["bottom"])
                    cropped = page_image.original.crop(bbox)  # ✅ 使用 PIL.Image.crop
                    page_data["images"].append(cropped)

            if table:
                # 提取表格截图
                for table in page.find_tables():
                    table_bbox = table.bbox  # (x0, top, x1, bottom)
                    table_img = page_image.original.crop(table_bbox)  # ✅ 也是使用 PIL.Image.crop
                    page_data["tables"].append(table_img)

            results.append(page_data)

    return results


def get_text_from_pdf():
    content = extract_pdf_as_images("info.pdf")
    all_text = ""
    for page in content:
        print(page['text'])
        all_text += page['text']
    return all_text

if __name__ == "__main__":
    content = extract_pdf_as_images("info.pdf")

    output_dir = "output"
    images_dir = os.path.join(output_dir, "images")
    tables_dir = os.path.join(output_dir, "tables")
    texts_dir = os.path.join(output_dir, "texts")

    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(tables_dir, exist_ok=True)
    os.makedirs(texts_dir, exist_ok=True)

    for page in content:
        page_num = page["page_num"]

        # 保存文本到 texts/
        text_filename = f"page{page_num}.txt"
        with open(os.path.join(texts_dir, text_filename), "w", encoding="utf-8") as f:
            f.write(page['text'])

        # 保存普通图片到 images/
        for i, img in enumerate(page['images']):
            img_filename = f"page{page_num}_img{i + 1}.png"
            img.save(os.path.join(images_dir, img_filename))

        # 保存表格截图到 tables/
        for i, table_img in enumerate(page['tables']):
            table_filename = f"page{page_num}_table{i + 1}.png"
            table_img.save(os.path.join(tables_dir, table_filename))

    print(f"✅ 所有内容保存完成，目录：{output_dir}/")