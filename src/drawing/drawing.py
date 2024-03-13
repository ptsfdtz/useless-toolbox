import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtCore import QTimer, Qt
import pandas as pd
import random
from collections import Counter

class DrawingApp(QWidget):
    def __init__(self, app):
        super().__init__()

        self.app = app  # Store the reference to the QApplication instance

        self.setWindowTitle("抽签程序")
        self.setGeometry(0, 0, 800, 400)  # Set dimensions to 800x400
        self.center_on_screen()  # Center the window on the screen
        self.setStyleSheet("background-color: #f0f0f0;")

        self.label = QLabel("点击按钮选择文件", self)
        self.label.setGeometry(20, 20, 760, 40)

        self.choose_file_button = QPushButton("选择文件", self)
        self.choose_file_button.setGeometry(20, 80, 760, 40)
        self.choose_file_button.clicked.connect(self.choose_file)

        self.draw_button = QPushButton("抽签", self)
        self.draw_button.setGeometry(20, 140, 760, 40)
        self.draw_button.setEnabled(False)
        self.draw_button.clicked.connect(self.draw)

        self.selected_file = None

    def center_on_screen(self):
        screen_geometry = self.app.desktop().availableGeometry()
        x_position = (screen_geometry.width() - self.width()) // 2
        y_position = (screen_geometry.height() - self.height()) // 2
        self.move(x_position, y_position)

    def choose_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Excel files (*.xlsx)")
        file_dialog.setOptions(options)

        if file_dialog.exec_() == QFileDialog.Accepted:
            self.selected_file = file_dialog.selectedFiles()[0]
            self.label.setText(f"已选择文件：{self.selected_file}")
            self.draw_button.setEnabled(True)

    def drawing(self, file_path):
        data = pd.read_excel(file_path)

        output_dict = {}

        for index, row in data.iterrows():
            name = row['姓名']
            output_dict[str(index)] = name
    
        return output_dict

    def draw(self):
        if not self.selected_file:
            QMessageBox.warning(self, "警告", "请选择一个有效的Excel文件。")
            return

        iterations = 1 
        result_dict = {}
        
        result_dict[self.selected_file] = self.drawing(self.selected_file)

        selected_list = [random.choice(list(result_dict[self.selected_file].values())) for _ in range(iterations)]

        most_common_person, _ = Counter(selected_list).most_common(1)[0]

        message = f"恭喜你 {most_common_person} 被抽中了！"
        self.label.setText(message)

        QTimer.singleShot(2000, self.fade_out)
        QMessageBox.information(self, "恭喜", message)

    def fade_out(self):
        current_color = self.label.palette().color(self.label.foregroundRole()).name()
        new_color = self.palette().color(self.backgroundRole()).name()

        self.label.setStyleSheet(f"color: {new_color};")

def main():
    app = QApplication(sys.argv)
    window = DrawingApp(app)  # Pass the QApplication instance to DrawingApp
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
