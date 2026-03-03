import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget

# 确保能正确导入内部模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.views.home_view import HomeView
from ui.views.merge_view import MergeView
from ui.views.split_view import SplitView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF工具集")
        self.resize(1024, 768)
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.home_view = HomeView()
        self.merge_view = MergeView()
        self.split_view = SplitView()

        self.stacked_widget.addWidget(self.home_view)
        self.stacked_widget.addWidget(self.merge_view)
        self.stacked_widget.addWidget(self.split_view)

        self.home_view.go_to_merge.connect(self.show_merge)
        self.home_view.go_to_split.connect(self.show_split)
        self.merge_view.go_back.connect(self.show_home)
        self.split_view.go_back.connect(self.show_home)

        self.load_stylesheet()
        self.show_home()

    def load_stylesheet(self):
        style_path = os.path.join(os.path.dirname(__file__), 'assets', 'style.qss')
        if os.path.exists(style_path):
            with open(style_path, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())

    def show_home(self): self.stacked_widget.setCurrentWidget(self.home_view)
    def show_merge(self): self.stacked_widget.setCurrentWidget(self.merge_view)
    def show_split(self): self.stacked_widget.setCurrentWidget(self.split_view)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
