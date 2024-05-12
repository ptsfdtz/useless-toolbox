import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog, QProgressBar
from PyQt5.QtCore import Qt
from datetime import datetime
import exifread
import shutil
import threading

class PhotoOrganizer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('图片分类')
        self.setGeometry(100, 100, 400, 200)

        self.btn_select_input_folder = QPushButton('选择输入文件夹', self)
        self.btn_select_input_folder.clicked.connect(self.selectInputFolder)

        self.btn_select_output_folder = QPushButton('选择输出文件夹', self)
        self.btn_select_output_folder.clicked.connect(self.selectOutputFolder)

        self.btn_start = QPushButton('开始', self)
        self.btn_start.clicked.connect(self.organizePhotos)

        self.progress_label = QLabel('进度:', self)
        self.progress_bar = QProgressBar(self)

        layout = QVBoxLayout()
        layout.addWidget(self.btn_select_input_folder)
        layout.addWidget(self.btn_select_output_folder)
        layout.addWidget(self.btn_start)
        layout.addWidget(self.progress_label)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

    def selectInputFolder(self):
        self.input_folder = QFileDialog.getExistingDirectory(self, 'Select Input Folder')

    def selectOutputFolder(self):
        self.output_folder = QFileDialog.getExistingDirectory(self, 'Select Output Folder')

    def organizePhotos(self):
        if not hasattr(self, 'input_folder') or not hasattr(self, 'output_folder'):
            return

        jpg_output_folder = os.path.join(self.output_folder, 'JPEG')
        raw_output_folder = os.path.join(self.output_folder, 'raw')

        if not os.path.exists(jpg_output_folder):
            os.makedirs(jpg_output_folder)
        if not os.path.exists(raw_output_folder):
            os.makedirs(raw_output_folder)

        jpg_files = [os.path.join(root, file) for root, _, files in os.walk(self.input_folder) for file in files if file.lower().endswith('.jpg')]
        total_files = len(jpg_files)
        
        def moveAndOrganize():
            for idx, jpg_file in enumerate(jpg_files):
                taken_date = self.get_photo_taken_time(jpg_file)
                if taken_date:
                    destination_subdir = os.path.join(jpg_output_folder, str(taken_date))
                    if not os.path.exists(destination_subdir):
                        os.makedirs(destination_subdir)
                    destination_file_path = os.path.join(destination_subdir, os.path.basename(jpg_file))
                    shutil.move(jpg_file, destination_file_path)
                self.updateProgress(int((idx + 1) / total_files * 100))
            
            for root, _, files in os.walk(self.input_folder):
                for file in files:
                    os.remove(os.path.join(root, file))

        threading.Thread(target=moveAndOrganize).start()

    def get_photo_taken_time(self, photo_path):
        with open(photo_path, 'rb') as f:
            tags = exifread.process_file(f, stop_tag="DateTimeOriginal")
            if 'EXIF DateTimeOriginal' in tags:
                taken_time = tags['EXIF DateTimeOriginal']
                taken_time = datetime.strptime(str(taken_time), '%Y:%m:%d %H:%M:%S')
                return taken_time.date()
            else:
                return None

    def updateProgress(self, value):
        self.progress_bar.setValue(value)
def main():
    app = QApplication(sys.argv)
    photo_organizer = PhotoOrganizer()
    photo_organizer.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()
