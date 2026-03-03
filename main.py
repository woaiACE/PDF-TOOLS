import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt6.QtGui import QIcon

from ui.home_page import HomePage
from ui.merge_page import MergePage
from ui.split_page import SplitPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF爱好者的在线工具")
        self.resize(1000, 700)
        self.setStyleSheet("background-color: #fafafa; font-family: 'Microsoft YaHei';")

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Initialize pages
        self.home_page = HomePage()
        self.merge_page = MergePage()
        self.split_page = SplitPage()

        # Add to stacked widget
        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.merge_page)
        self.stacked_widget.addWidget(self.split_page)

        # Connect signals
        self.home_page.request_navigate.connect(self.navigate)
        self.merge_page.request_back.connect(self.go_home)
        self.split_page.request_back.connect(self.go_home)

    def navigate(self, page_id):
        if page_id == "merge":
            self.stacked_widget.setCurrentWidget(self.merge_page)
        elif page_id == "split":
            self.stacked_widget.setCurrentWidget(self.split_page)

    def go_home(self):
        self.stacked_widget.setCurrentWidget(self.home_page)

def main():
    app = QApplication(sys.argv)

    # Optional: Set global font
    font = app.font()
    font.setFamily("Microsoft YaHei")
    app.setFont(font)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
