from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QProgressBar
from PyQt5.QtCore import Qt, pyqtSlot, QThread, pyqtSignal, QTimer, QCoreApplication
from PyQt5.QtGui import QPixmap
from PIL import Image
from reportlab.pdfgen import canvas
import os

class ImageToPDFConverter(QWidget):
    def __init__(self):
        super().__init__()

        self.folder_path = QLineEdit()
        self.message_label = QLabel()
        self.progress_bar = QProgressBar()
        self.pdf_path_label = QLabel()

        self.worker = None  # Initialize worker instance

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("选择图片文件夹:"))
        layout.addWidget(self.folder_path)

        browse_button = QPushButton("浏览", clicked=self.browse)
        layout.addWidget(browse_button)

        convert_button = QPushButton("一键转换", clicked=self.convert_to_pdf)
        layout.addWidget(convert_button)

        layout.addWidget(self.progress_bar)
        layout.addWidget(self.pdf_path_label)
        layout.addWidget(self.message_label)

        self.setLayout(layout)
        self.setWindowTitle("Image to PDF Converter")
        self.setGeometry(100, 100, 420, 260)

    @pyqtSlot()
    def browse(self):
        folder_selected = QFileDialog.getExistingDirectory(self, "选择文件夹")
        self.folder_path.setText(folder_selected)

    @pyqtSlot()
    def convert_to_pdf(self):
        folder_path = self.folder_path.text()

        if not folder_path:
            self.show_message("未选择文件夹。退出。")
            return

        output_pdf_path = "output"
        os.makedirs(output_pdf_path, exist_ok=True)

        self.worker = ImageToPDFWorker(folder_path, output_pdf_path)
        self.worker.finished.connect(self.show_conversion_result)
        self.worker.update_progress.connect(self.update_progress_bar)
        self.worker.start()

    @pyqtSlot(str)
    def show_message(self, message):
        self.message_label.setStyleSheet("")  # Reset to default
        self.message_label.setText(message)
        self.message_label.repaint()

    @pyqtSlot(str)
    def show_conversion_result(self, result):
        if result.startswith("Error: "):
            self.show_message(result)
        else:
            self.pdf_path_label.setText(f"PDF Path: {os.path.abspath(result)}")
            self.progress_bar.setValue(100)
            self.show_message("Conversion completed.")
        self.worker.deleteLater()

    @pyqtSlot(int)
    def update_progress_bar(self, value):
        self.progress_bar.setValue(value)
        QCoreApplication.processEvents()  # Allow the GUI to update

class ImageToPDFWorker(QThread):
    finished = pyqtSignal(str)
    update_progress = pyqtSignal(int)

    def __init__(self, image_folder, output_pdf):
        super().__init__()
        self.image_folder = image_folder
        self.output_pdf = output_pdf

    def run(self):
        try:
            images = [img for img in os.listdir(self.image_folder) if img.lower().endswith((".png", ".jpg"))]

            if not images:
                raise ValueError("No images found in the selected folder.")

            images.sort()

            pdf_path = os.path.join(self.output_pdf, "output.pdf")
            c = canvas.Canvas(pdf_path)

            total_images = len(images)
            for i, image in enumerate(images):
                img_path = os.path.join(self.image_folder, image)
                img = Image.open(img_path)
                width, height = img.size
                c.setPageSize((width, height))
                c.drawInlineImage(img_path, 0, 0, width, height)

                if i != len(images) - 1:
                    c.showPage()

                progress_value = (i + 1) / total_images * 100
                self.update_progress.emit(int(progress_value))

            c.save()

            self.finished.emit(pdf_path)

        except Exception as e:
            error_message = f"Error: {str(e)}"
            self.finished.emit(error_message)

def main():
    app = QApplication([])
    window = ImageToPDFConverter()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
