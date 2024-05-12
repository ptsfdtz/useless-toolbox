import os
from docx2pdf import convert
import openpyxl
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QFileDialog

class ConverterApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("转PDF")
        self.setGeometry(100, 100, 400, 200)

        self.input_label = QLabel("输入文件")
        self.input_line_edit = QLineEdit()
        self.input_button = QPushButton("选择")
        self.input_button.clicked.connect(self.browse_input_folder)

        self.output_label = QLabel("输出文件")
        self.output_line_edit = QLineEdit()
        self.output_button = QPushButton("选择")
        self.output_button.clicked.connect(self.browse_output_folder)

        self.convert_button = QPushButton("确定")
        self.convert_button.clicked.connect(self.convert_files)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_line_edit)
        input_layout.addWidget(self.input_button)

        output_layout = QHBoxLayout()
        output_layout.addWidget(self.output_line_edit)
        output_layout.addWidget(self.output_button)

        layout = QVBoxLayout()
        layout.addWidget(self.input_label)
        layout.addLayout(input_layout)
        layout.addWidget(self.output_label)
        layout.addLayout(output_layout)
        layout.addWidget(self.convert_button)

        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def browse_input_folder(self):
        folder = str(QFileDialog.getExistingDirectory(self, "Select Input Folder"))
        self.input_line_edit.setText(folder)

    def browse_output_folder(self):
        folder = str(QFileDialog.getExistingDirectory(self, "Select Output Folder"))
        self.output_line_edit.setText(folder)

    def convert_files(self):
        input_folder = self.input_line_edit.text()
        output_folder = self.output_line_edit.text()

        if not os.path.exists(input_folder) or not os.path.exists(output_folder):
            QtWidgets.QMessageBox.warning(self, "Error", "Input or Output folder does not exist.")
            return

        convert_docx_to_pdf(input_folder, output_folder)
        convert_excel_to_pdf(input_folder, output_folder)
        QtWidgets.QMessageBox.information(self, "Success", "Conversion complete.")

def convert_docx_to_pdf(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    files = os.listdir(input_folder)

    for file in files:
        if file.endswith('.docx'):
            input_file = os.path.join(input_folder, file)
            output_file = os.path.join(output_folder, os.path.splitext(file)[0] + '.pdf')
            convert(input_file, output_file)

def convert_excel_to_pdf(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    files = os.listdir(input_folder)

    for file in files:
        if file.endswith('.xlsx'):
            input_file = os.path.join(input_folder, file)
            output_file = os.path.join(output_folder, os.path.splitext(file)[0] + '.pdf')

            workbook = openpyxl.load_workbook(input_file)
            sheets = workbook.sheetnames

            for sheet_name in sheets:
                ws = workbook[sheet_name]
                ws.title = sheet_name
                pdf_file = output_file[:-4] + "_" + sheet_name + ".pdf"
                ws.sheet_view.showGridLines = False  
                ws.page_setup.orientation = ws.ORIENTATION_LANDSCAPE  
                ws.page_setup.fitToHeight = False
                ws.page_setup.fitToWidth = True
                ws.page_margins.left = 0.2
                ws.page_margins.right = 0.2
                ws.page_margins.top = 0.2
                ws.page_margins.bottom = 0.2
                ws.page_margins.header = 0
                ws.page_margins.footer = 0
                ws.page_setup.paperSize = ws.PAPERSIZE_A4

                ws.print_options.horizontalCentered = True
                ws.print_options.verticalCentered = True

                workbook.save(output_file)
                os.remove(output_file)

def main():
    app = QApplication([])
    window = ConverterApp()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
