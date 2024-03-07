from PIL import Image
from reportlab.pdfgen import canvas
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from threading import Thread

class ImageToPDFConverter:
    def __init__(self, master):
        self.master = master
        master.title("Image to PDF Converter")
        self.master.geometry("400x200")
        
        self.folder_path = tk.StringVar()
        self.message_var = tk.StringVar()
        self.progress_var = tk.DoubleVar()

        self.label = tk.Label(master, text="选择图片文件夹:")
        self.label.pack(padx=20)

        self.entry = tk.Entry(master, textvariable=self.folder_path,width=40)
        self.entry.pack(padx=20)

        self.browse_button = tk.Button(master, text="浏览", command=self.browse,width=15)
        self.browse_button.pack(padx=20)

        self.convert_button = tk.Button(master, text="一键转换", command=self.convert_to_pdf,width=15)
        self.convert_button.pack(padx=20)

        self.progress_bar = ttk.Progressbar(master, variable=self.progress_var, orient=tk.HORIZONTAL, length=200, mode='determinate')
        self.progress_bar.pack(pady=10)

        self.message_label = tk.Label(master, textvariable=self.message_var)
        self.message_label.pack()

    def browse(self):
        folder_selected = filedialog.askdirectory(title="选择文件夹")
        self.folder_path.set(folder_selected)

    def convert_to_pdf(self):
        folder_path = self.folder_path.get()

        if not folder_path:
            self.show_message("No folder selected. Exiting.")
            return

        output_pdf_path = "output"
        os.makedirs(output_pdf_path, exist_ok=True)

        Thread(target=self.images_to_pdf, args=(folder_path, output_pdf_path)).start()

    def images_to_pdf(self, image_folder, output_pdf):
        images = [img for img in os.listdir(image_folder) if img.lower().endswith((".png", ".jpg"))]

        if not images:
            self.show_message("No images found in the selected folder.")
            return

        images.sort()

        pdf_path = os.path.join(output_pdf, "output.pdf")
        c = canvas.Canvas(pdf_path)

        total_images = len(images)
        for i, image in enumerate(images):
            img_path = os.path.join(image_folder, image)
            img = Image.open(img_path)
            width, height = img.size
            c.setPageSize((width, height))
            c.drawInlineImage(img_path, 0, 0, width, height)

            if i != len(images) - 1:
                c.showPage()

            progress_value = (i + 1) / total_images * 100
            self.progress_var.set(progress_value)
            self.master.update()

        c.save()

        message = f"Conversion completed. PDF saved in the 'output' folder.\nPath: {os.path.abspath(pdf_path)}"
        self.show_message(message)

    def show_message(self, message):
        self.message_var.set(message)
        self.master.update_idletasks()  
        self.master.after(2000, self.clear_message)  

    def clear_message(self):
        self.message_var.set("")  

def main():
    root = tk.Tk()
    app = ImageToPDFConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
