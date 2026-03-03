import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem, QFileDialog, QMessageBox, QAbstractItemView)
from PySide6.QtCore import Qt, Signal
from utils.pdf_utils import merge_pdfs

class MergeView(QWidget):
    go_back = Signal()
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        header_layout = QHBoxLayout()
        back_btn = QPushButton("← 返回首页")
        back_btn.clicked.connect(self.go_back.emit)
        title = QLabel("合并PDF文件")
        title.setObjectName("headerTitle")
        header_layout.addWidget(back_btn)
        header_layout.addStretch()
        header_layout.addWidget(title)
        header_layout.addStretch()
        spacer = QWidget()
        spacer.setFixedWidth(back_btn.sizeHint().width())
        header_layout.addWidget(spacer)
        main_layout.addLayout(header_layout)

        subtitle = QLabel("请添加需要合并的PDF文件。您可以拖拽列表项来调整合并顺序。")
        subtitle.setObjectName("headerSubtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle)

        content_layout = QHBoxLayout()
        list_layout = QVBoxLayout()
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.list_widget.setDragDropMode(QAbstractItemView.InternalMove)
        list_layout.addWidget(self.list_widget)

        list_btn_layout = QHBoxLayout()
        add_btn = QPushButton("+ 添加文件")
        add_btn.clicked.connect(self.add_files)
        remove_btn = QPushButton("- 移除选定文件")
        remove_btn.clicked.connect(self.remove_files)
        list_btn_layout.addWidget(add_btn)
        list_btn_layout.addWidget(remove_btn)
        list_layout.addLayout(list_btn_layout)
        content_layout.addLayout(list_layout, 3)

        controls_layout = QVBoxLayout()
        up_btn = QPushButton("↑ 上移")
        up_btn.clicked.connect(self.move_up)
        down_btn = QPushButton("↓ 下移")
        down_btn.clicked.connect(self.move_down)
        merge_btn = QPushButton("合并PDF")
        merge_btn.setProperty("class", "PrimaryButton")
        merge_btn.setMinimumHeight(50)
        merge_btn.clicked.connect(self.perform_merge)
        controls_layout.addWidget(up_btn)
        controls_layout.addWidget(down_btn)
        controls_layout.addStretch()
        controls_layout.addWidget(merge_btn)
        content_layout.addLayout(controls_layout, 1)
        main_layout.addLayout(content_layout)

    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "选择PDF文件", "", "PDF Files (*.pdf)")
        if files:
            for file in files:
                item = QListWidgetItem(os.path.basename(file))
                item.setData(Qt.UserRole, file)
                self.list_widget.addItem(item)

    def remove_files(self):
        for item in self.list_widget.selectedItems():
            self.list_widget.takeItem(self.list_widget.row(item))

    def move_up(self):
        row = self.list_widget.currentRow()
        if row > 0:
            item = self.list_widget.takeItem(row)
            self.list_widget.insertItem(row - 1, item)
            self.list_widget.setCurrentRow(row - 1)

    def move_down(self):
        row = self.list_widget.currentRow()
        if row < self.list_widget.count() - 1 and row != -1:
            item = self.list_widget.takeItem(row)
            self.list_widget.insertItem(row + 1, item)
            self.list_widget.setCurrentRow(row + 1)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if path.lower().endswith(".pdf"):
                # Check for duplicates before adding
                is_duplicate = False
                for i in range(self.list_widget.count()):
                    item = self.list_widget.item(i)
                    if item.data(Qt.UserRole) == path:
                        is_duplicate = True
                        break
                if not is_duplicate:
                    item = QListWidgetItem(os.path.basename(path))
                    item.setData(Qt.UserRole, path)
                    self.list_widget.addItem(item)

    def perform_merge(self):
        if self.list_widget.count() < 2:
            return QMessageBox.warning(self, "提示", "请至少添加2个PDF文件进行合并。")
        output_file, _ = QFileDialog.getSaveFileName(self, "保存合并后的PDF", "merged.pdf", "PDF Files (*.pdf)")
        if not output_file: return
        pdf_list = [self.list_widget.item(i).data(Qt.UserRole) for i in range(self.list_widget.count())]
        success, msg = merge_pdfs(pdf_list, output_file)
        if success: QMessageBox.information(self, "成功", msg)
        else: QMessageBox.critical(self, "错误", msg)
