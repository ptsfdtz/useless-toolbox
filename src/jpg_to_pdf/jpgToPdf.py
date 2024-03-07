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
        self.master.geometry("420x260")

        self.create_widgets()

    def create_widgets(self):
        self.folder_path = tk.StringVar()
        self.message_var = tk.StringVar()
        self.progress_var = tk.DoubleVar()
        self.pdf_path_var = tk.StringVar()

        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#ccc")
        style.configure("TEntry", padding=6, relief="flat", background="#eee")
        style.configure("TLabel", background="#fff")

        self.label = tk.Label(self.master, text="选择图片文件夹:")
        self.label.grid(row=0, column=0, padx=20, pady=(20, 0), sticky=tk.W)

        self.entry = ttk.Entry(self.master, textvariable=self.folder_path, width=30, style="TEntry")
        self.entry.grid(row=1, column=0, padx=20, pady=5, sticky=tk.W)

        self.browse_button = ttk.Button(self.master, text="浏览", command=self.browse, style="TButton")
        self.browse_button.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        self.convert_button = ttk.Button(self.master, text="一键转换", command=self.convert_to_pdf, width=15, style="TButton")
        self.convert_button.grid(row=2, column=0, padx=20, pady=10, sticky=tk.W)

        self.progress_bar = ttk.Progressbar(self.master, variable=self.progress_var, orient=tk.HORIZONTAL, length=380, mode='determinate')
        self.progress_bar.grid(row=3, column=0, columnspan=2, pady=10, padx=20, sticky=tk.W)

        self.pdf_path_label = ttk.Label(self.master, textvariable=self.pdf_path_var, wraplength=380, justify=tk.LEFT, style="TLabel", foreground="blue")
        self.pdf_path_label.grid(row=4, column=0, columnspan=2, pady=(0, 20), padx=20, sticky=tk.W)

        self.message_label = ttk.Label(self.master, textvariable=self.message_var, style="TLabel", foreground="red")
        self.message_label.grid(row=5, column=0, columnspan=2, pady=(0, 10), padx=20, sticky=tk.W)

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

        message = f"Conversion completed. PDF saved in the 'output' folder."
        self.pdf_path_var.set(f"PDF Path: {os.path.abspath(pdf_path)}")
        self.show_message(message)

    def show_message(self, message):
        self.message_var.set(message)
        self.master.update_idletasks()
        self.master.after(2000, self.clear_message)

    def clear_message(self):
        self.message_var.set("")
        self.pdf_path_var.set("")

def main():
    root = tk.Tk()
    app = ImageToPDFConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
