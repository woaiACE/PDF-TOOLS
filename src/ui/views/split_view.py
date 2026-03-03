import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox, QRadioButton, QLineEdit, QGroupBox)
from PySide6.QtCore import Qt, Signal
from utils.pdf_utils import split_pdf_extract, split_pdf_all

class SplitView(QWidget):
    go_back = Signal()
    def __init__(self):
        super().__init__()
        self.selected_file = None
        self.setAcceptDrops(True)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        header_layout = QHBoxLayout()
        back_btn = QPushButton("← 返回首页")
        back_btn.clicked.connect(self.go_back.emit)
        title = QLabel("拆分PDF文件")
        title.setObjectName("headerTitle")
        header_layout.addWidget(back_btn)
        header_layout.addStretch()
        header_layout.addWidget(title)
        header_layout.addStretch()
        spacer = QWidget()
        spacer.setFixedWidth(back_btn.sizeHint().width())
        header_layout.addWidget(spacer)
        main_layout.addLayout(header_layout)

        content_layout = QVBoxLayout()
        content_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        file_group = QGroupBox("1. 选择文件")
        file_layout = QHBoxLayout()
        self.file_label = QLabel("未选择文件")
        select_btn = QPushButton("浏览...")
        select_btn.clicked.connect(self.select_file)
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(select_btn)
        file_group.setLayout(file_layout)
        content_layout.addWidget(file_group)

        options_group = QGroupBox("2. 拆分方式")
        options_layout = QVBoxLayout()
        self.radio_extract = QRadioButton("按页码提取 (保存为一个PDF)")
        self.radio_extract.setChecked(True)
        self.radio_all = QRadioButton("将所有页面拆分为独立的PDF")
        options_layout.addWidget(self.radio_extract)

        extract_layout = QHBoxLayout()
        extract_label = QLabel("页码范围 (例如: 1, 3, 5-7):")
        self.range_input = QLineEdit()
        self.range_input.setPlaceholderText("请输入页码，用逗号或连字符分隔")
        extract_layout.addWidget(extract_label)
        extract_layout.addWidget(self.range_input)
        options_layout.addLayout(extract_layout)
        options_layout.addWidget(self.radio_all)
        options_group.setLayout(options_layout)
        content_layout.addWidget(options_group)

        split_btn = QPushButton("执行拆分")
        split_btn.setProperty("class", "PrimaryButton")
        split_btn.setMinimumHeight(50)
        split_btn.clicked.connect(self.perform_split)
        content_layout.addWidget(split_btn)
        main_layout.addLayout(content_layout)

    def select_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "选择PDF文件", "", "PDF Files (*.pdf)")
        if file:
            self.selected_file = file
            self.file_label.setText(os.path.basename(file))

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if path.lower().endswith(".pdf"):
                self.selected_file = path
                self.file_label.setText(os.path.basename(path))
                break # Only accept the first dragged PDF

    def perform_split(self):
        if not self.selected_file: return QMessageBox.warning(self, "提示", "请先选择一个PDF文件。")
        if self.radio_extract.isChecked():
            range_str = self.range_input.text().strip()
            if not range_str: return QMessageBox.warning(self, "提示", "请输入有效的页码范围。")
            output_file, _ = QFileDialog.getSaveFileName(self, "保存提取后的PDF", "extracted.pdf", "PDF Files (*.pdf)")
            if not output_file: return
            success, msg = split_pdf_extract(self.selected_file, output_file, range_str)
            if success: QMessageBox.information(self, "成功", msg)
            else: QMessageBox.critical(self, "错误", msg)
        elif self.radio_all.isChecked():
            output_dir = QFileDialog.getExistingDirectory(self, "选择保存目录")
            if not output_dir: return
            success, msg = split_pdf_all(self.selected_file, output_dir)
            if success: QMessageBox.information(self, "成功", msg)
            else: QMessageBox.critical(self, "错误", msg)
