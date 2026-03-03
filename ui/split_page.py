import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QFileDialog, QMessageBox, QRadioButton, QLineEdit, QButtonGroup)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont, QCursor

from utils.pdf_utils import split_pdf_pages, extract_pdf_pages

class SplitPage(QWidget):
    request_back = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.input_pdf_path = None
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)

        # Top Bar (Back button)
        top_layout = QHBoxLayout()
        self.back_btn = QPushButton("← 返回主页")
        self.back_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #555555;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: #ff4d4f;
            }
        """)
        self.back_btn.clicked.connect(self.request_back.emit)
        top_layout.addWidget(self.back_btn)
        top_layout.addStretch()
        main_layout.addLayout(top_layout)

        # Title
        title_label = QLabel("拆分 PDF 文件")
        title_font = QFont("Microsoft YaHei", 24, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # Subtitle
        subtitle_label = QLabel("选择或拖拽一个PDF文件，然后选择拆分方式。")
        subtitle_font = QFont("Microsoft YaHei", 11)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: #666666;")
        main_layout.addWidget(subtitle_label)

        main_layout.addSpacing(10)

        # File Selection Area
        self.file_label = QLabel("未选择文件")
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.file_label.setStyleSheet("""
            QLabel {
                border: 2px dashed #cccccc;
                border-radius: 8px;
                background-color: #fcfcfc;
                font-size: 16px;
                color: #999999;
                padding: 40px;
            }
        """)
        main_layout.addWidget(self.file_label)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self.select_btn = QPushButton("选择 PDF 文件")
        self.select_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 1px solid #cccccc;
                border-radius: 5px;
                color: #333333;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                border: 1px solid #ff4d4f;
                color: #ff4d4f;
            }
        """)
        self.select_btn.clicked.connect(self.select_file)
        btn_layout.addWidget(self.select_btn)
        btn_layout.addStretch()
        main_layout.addLayout(btn_layout)

        main_layout.addSpacing(20)

        # Options Area
        options_layout = QVBoxLayout()
        self.radio_group = QButtonGroup(self)

        self.radio_all = QRadioButton("将所有页面拆分为独立PDF")
        self.radio_all.setFont(QFont("Microsoft YaHei", 12))
        self.radio_all.setChecked(True)
        self.radio_group.addButton(self.radio_all)
        options_layout.addWidget(self.radio_all)

        custom_layout = QHBoxLayout()
        self.radio_custom = QRadioButton("提取特定页码（或范围）:")
        self.radio_custom.setFont(QFont("Microsoft YaHei", 12))
        self.radio_group.addButton(self.radio_custom)
        custom_layout.addWidget(self.radio_custom)

        self.page_input = QLineEdit()
        self.page_input.setPlaceholderText("例如: 1,3,5-7")
        self.page_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 5px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #ff4d4f;
            }
        """)
        self.page_input.setEnabled(False)
        self.radio_custom.toggled.connect(self.page_input.setEnabled)
        custom_layout.addWidget(self.page_input)

        options_layout.addLayout(custom_layout)

        main_layout.addLayout(options_layout)

        main_layout.addSpacing(30)

        # Split Button
        split_layout = QHBoxLayout()
        split_layout.addStretch()
        self.split_btn = QPushButton("开始拆分")
        self.split_btn.setFixedSize(200, 50)
        self.split_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff4d4f;
                color: white;
                border-radius: 25px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff7875;
            }
            QPushButton:disabled {
                background-color: #ffb3b3;
            }
        """)
        self.split_btn.clicked.connect(self.do_split)
        self.split_btn.setEnabled(False)
        split_layout.addWidget(self.split_btn)
        split_layout.addStretch()
        main_layout.addLayout(split_layout)

        main_layout.addStretch()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if path.lower().endswith(".pdf"):
                self.set_file(path)
                break # Only take the first one

    def select_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "选择待拆分的 PDF", "", "PDF Files (*.pdf)")
        if file:
            self.set_file(file)

    def set_file(self, filepath):
        self.input_pdf_path = filepath
        self.file_label.setText(f"已选择文件：\n{os.path.basename(filepath)}")
        self.file_label.setStyleSheet("""
            QLabel {
                border: 2px solid #ff4d4f;
                border-radius: 8px;
                background-color: #fff0f0;
                font-size: 16px;
                color: #333333;
                padding: 40px;
                font-weight: bold;
            }
        """)
        self.split_btn.setEnabled(True)

    def do_split(self):
        if not self.input_pdf_path:
            return

        if self.radio_all.isChecked():
            output_dir = QFileDialog.getExistingDirectory(self, "选择保存目录")
            if output_dir:
                try:
                    split_pdf_pages(self.input_pdf_path, output_dir)
                    QMessageBox.information(self, "成功", "拆分成功，所有页面已保存为独立的 PDF 文件！")
                except Exception as e:
                    QMessageBox.critical(self, "错误", f"拆分过程中发生错误：\n{e}")
        else:
            pages_str = self.page_input.text().strip()
            if not pages_str:
                QMessageBox.warning(self, "警告", "请输入要提取的页码！")
                return

            output_path, _ = QFileDialog.getSaveFileName(self, "保存提取后的 PDF", "", "PDF Files (*.pdf)")
            if output_path:
                try:
                    extract_pdf_pages(self.input_pdf_path, output_path, pages_str)
                    QMessageBox.information(self, "成功", "提取成功！")
                except ValueError as ve:
                    QMessageBox.warning(self, "警告", str(ve))
                except Exception as e:
                    QMessageBox.critical(self, "错误", f"提取过程中发生错误：\n{e}")
