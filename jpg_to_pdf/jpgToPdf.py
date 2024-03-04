from PIL import Image
from reportlab.pdfgen import canvas
import os
import tkinter as tk

def images_to_pdf(image_folder, output_pdf):
    images = [img for img in os.listdir(image_folder) if img.lower().endswith((".png", ".jpg"))]

    if not images:
        return

    images.sort()

    pdf_path = os.path.join(output_pdf, "output.pdf")
    c = canvas.Canvas(pdf_path)

    for i, image in enumerate(images):
        img_path = os.path.join(image_folder, image)
        img = Image.open(img_path)
        width, height = img.size
        c.setPageSize((width, height))
        c.drawInlineImage(img_path, 0, 0, width, height)

        if i != len(images) - 1:
            c.showPage()

    c.save()

def main():
    image_folder_path = "jpg_to_pdf/images"
    output_pdf_path = "jpg_to_pdf/output"

    os.makedirs(output_pdf_path, exist_ok=True)
    images_to_pdf(image_folder_path, output_pdf_path)

    window = tk.Tk()
    window.title("jpg to pdf")

    label = tk.Label(window, text="PDF转换完成", font=("Arial", 16))
    label.pack()

    window.mainloop()

if __name__ == "__main__":
    main()
