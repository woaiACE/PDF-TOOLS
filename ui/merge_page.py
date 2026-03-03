import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QListWidget, QListWidgetItem, QFileDialog, QMessageBox, QAbstractItemView)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont, QIcon

from utils.pdf_utils import merge_pdfs

class MergePage(QWidget):
    request_back = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
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
        title_label = QLabel("合并 PDF 文件")
        title_font = QFont("Microsoft YaHei", 24, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # Subtitle
        subtitle_label = QLabel("请选择或拖拽PDF文件至列表，您可以在列表中拖拽调整顺序。")
        subtitle_font = QFont("Microsoft YaHei", 11)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: #666666;")
        main_layout.addWidget(subtitle_label)

        main_layout.addSpacing(10)

        # Buttons (Add, Move Up, Move Down, Delete)
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.add_btn = QPushButton("+ 添加文件")
        self.add_btn.setStyleSheet(self.get_btn_style())
        self.add_btn.clicked.connect(self.add_files)
        btn_layout.addWidget(self.add_btn)

        self.up_btn = QPushButton("↑ 上移")
        self.up_btn.setStyleSheet(self.get_btn_style())
        self.up_btn.clicked.connect(self.move_up)
        btn_layout.addWidget(self.up_btn)

        self.down_btn = QPushButton("↓ 下移")
        self.down_btn.setStyleSheet(self.get_btn_style())
        self.down_btn.clicked.connect(self.move_down)
        btn_layout.addWidget(self.down_btn)

        self.del_btn = QPushButton("🗑️ 删除")
        self.del_btn.setStyleSheet(self.get_btn_style(danger=True))
        self.del_btn.clicked.connect(self.delete_selected)
        btn_layout.addWidget(self.del_btn)

        btn_layout.addStretch()
        main_layout.addLayout(btn_layout)

        # List Widget for files
        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.file_list.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.file_list.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.file_list.setStyleSheet("""
            QListWidget {
                border: 2px dashed #cccccc;
                border-radius: 8px;
                background-color: #fcfcfc;
                font-size: 14px;
                padding: 10px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #eeeeee;
            }
            QListWidget::item:selected {
                background-color: #ffe6e6;
                color: #333333;
            }
        """)
        main_layout.addWidget(self.file_list)

        # Merge Button
        merge_layout = QHBoxLayout()
        merge_layout.addStretch()
        self.merge_btn = QPushButton("开始合并")
        self.merge_btn.setFixedSize(200, 50)
        self.merge_btn.setStyleSheet("""
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
        """)
        self.merge_btn.clicked.connect(self.do_merge)
        merge_layout.addWidget(self.merge_btn)
        merge_layout.addStretch()
        main_layout.addLayout(merge_layout)

    def get_btn_style(self, danger=False):
        color = "#ff4d4f" if danger else "#333333"
        hover_color = "#ff7875" if danger else "#555555"
        return f"""
            QPushButton {{
                background-color: white;
                border: 1px solid #cccccc;
                border-radius: 5px;
                color: {color};
                padding: 8px 15px;
            }}
            QPushButton:hover {{
                border: 1px solid {hover_color};
                color: {hover_color};
            }}
        """

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if path.lower().endswith(".pdf"):
                self.add_file_to_list(path)

    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "选择 PDF 文件", "", "PDF Files (*.pdf)")
        for f in files:
            self.add_file_to_list(f)

    def add_file_to_list(self, filepath):
        # Check if already in list
        for i in range(self.file_list.count()):
            item = self.file_list.item(i)
            if item.data(Qt.ItemDataRole.UserRole) == filepath:
                return # Skip duplicate

        filename = os.path.basename(filepath)
        item = QListWidgetItem(filename)
        item.setData(Qt.ItemDataRole.UserRole, filepath)
        self.file_list.addItem(item)

    def move_up(self):
        row = self.file_list.currentRow()
        if row > 0:
            item = self.file_list.takeItem(row)
            self.file_list.insertItem(row - 1, item)
            self.file_list.setCurrentRow(row - 1)

    def move_down(self):
        row = self.file_list.currentRow()
        if row >= 0 and row < self.file_list.count() - 1:
            item = self.file_list.takeItem(row)
            self.file_list.insertItem(row + 1, item)
            self.file_list.setCurrentRow(row + 1)

    def delete_selected(self):
        row = self.file_list.currentRow()
        if row >= 0:
            self.file_list.takeItem(row)

    def do_merge(self):
        count = self.file_list.count()
        if count < 2:
            QMessageBox.warning(self, "警告", "请至少添加 2 个 PDF 文件进行合并。")
            return

        input_paths = []
        for i in range(count):
            item = self.file_list.item(i)
            input_paths.append(item.data(Qt.ItemDataRole.UserRole))

        output_path, _ = QFileDialog.getSaveFileName(self, "保存合并后的 PDF", "", "PDF Files (*.pdf)")
        if output_path:
            try:
                merge_pdfs(input_paths, output_path)
                QMessageBox.information(self, "成功", "PDF 合并成功！")
                self.file_list.clear()
            except Exception as e:
                QMessageBox.critical(self, "错误", f"合并过程中发生错误：\n{e}")
