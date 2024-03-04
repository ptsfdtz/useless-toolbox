from PIL import Image
from reportlab.pdfgen import canvas
import os
import tkinter as tk
from tkinter import filedialog

class ImageToPDFConverter:
    def __init__(self, master):
        self.master = master
        master.title("Image to PDF Converter")
        self.master.geometry("400x200")
        
        self.folder_path = tk.StringVar()
        self.message_var = tk.StringVar()

        self.label = tk.Label(master, text="Select Image Folder:")
        self.label.pack()

        self.entry = tk.Entry(master, textvariable=self.folder_path)
        self.entry.pack()

        self.browse_button = tk.Button(master, text="Browse", command=self.browse)
        self.browse_button.pack()

        self.convert_button = tk.Button(master, text="Convert to PDF", command=self.convert_to_pdf)
        self.convert_button.pack()

        self.message_label = tk.Label(master, textvariable=self.message_var)
        self.message_label.pack()

    def browse(self):
        folder_selected = filedialog.askdirectory(title="Select A Folder")
        self.folder_path.set(folder_selected)

    def convert_to_pdf(self):
        folder_path = self.folder_path.get()

        if not folder_path:
            self.show_message("No folder selected. Exiting.")
            return

        output_pdf_path = "output"
        os.makedirs(output_pdf_path, exist_ok=True)

        self.images_to_pdf(folder_path, output_pdf_path)
        message = f"Conversion completed. PDF saved in the 'output' folder.\nPath: {os.path.abspath(output_pdf_path)}"
        self.show_message(message)

    def images_to_pdf(self, image_folder, output_pdf):
        images = [img for img in os.listdir(image_folder) if img.lower().endswith((".png", ".jpg"))]

        if not images:
            self.show_message("No images found in the selected folder.")
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

    def show_message(self, message):
        self.message_var.set(message)

def main():
    root = tk.Tk()
    app = ImageToPDFConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
