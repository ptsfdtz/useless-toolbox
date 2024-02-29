from PIL import Image
from reportlab.pdfgen import canvas
import os

def images_to_pdf(image_folder, output_pdf):
    images = [img for img in os.listdir(image_folder) if img.endswith(".png") or img.endswith(".jpg") or img.endswith(".JPG")]

    if not images:
        print("没有找到图片文件！")
        return

    images.sort()

    pdf_path = os.path.join(output_pdf, "output.pdf")
    c = canvas.Canvas(pdf_path)

    for image in images:
        img_path = os.path.join(image_folder, image)
        img = Image.open(img_path)
        width, height = img.size
        c.setPageSize((width, height))
        c.drawInlineImage(img_path, 0, 0, width, height)

        if image != images[-1]:
            c.showPage()

    c.save()
    print(f"PDF已生成:{pdf_path}")

if __name__ == "__main__":
    # 指定包含图片的文件夹路径
    image_folder_path = "jpg_to_pdf/image"

    # 指定输出PDF的文件夹路径
    output_pdf_path = "jpg_to_pdf/output"

    # 创建输出文件夹（如果不存在）
    os.makedirs(output_pdf_path, exist_ok=True)

    # 执行转换
    images_to_pdf(image_folder_path, output_pdf_path)
