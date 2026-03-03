import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                               QFileDialog, QMessageBox, QGroupBox, QListWidget, QListWidgetItem, QAbstractItemView)
from PySide6.QtCore import Qt, Signal

class SingleFileActionView(QWidget):
    """
    通用单文件处理视图，适用于“单文件进 -> 单文件出” 或 “单文件进 -> 目录出”的场景
    """
    go_back = Signal()

    def __init__(self, title, subtitle, file_filter, action_btn_text, action_func, is_dir_output=False, default_ext=""):
        super().__init__()
        self.title_text = title
        self.subtitle_text = subtitle
        self.file_filter = file_filter
        self.action_btn_text = action_btn_text
        self.action_func = action_func
        self.is_dir_output = is_dir_output
        self.default_ext = default_ext
        self.selected_file = None
        self.setAcceptDrops(True)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        # Header
        header_layout = QHBoxLayout()
        back_btn = QPushButton("← 返回首页")
        back_btn.clicked.connect(self.go_back.emit)
        title = QLabel(self.title_text)
        title.setObjectName("headerTitle")
        header_layout.addWidget(back_btn)
        header_layout.addStretch()
        header_layout.addWidget(title)
        header_layout.addStretch()
        spacer = QWidget()
        spacer.setFixedWidth(back_btn.sizeHint().width())
        header_layout.addWidget(spacer)
        main_layout.addLayout(header_layout)

        # Subtitle
        subtitle = QLabel(self.subtitle_text)
        subtitle.setObjectName("headerSubtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle)

        content_layout = QVBoxLayout()
        content_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        # File Selection
        file_group = QGroupBox("选择文件")
        file_layout = QHBoxLayout()
        self.file_label = QLabel("未选择文件 (支持拖拽)")
        select_btn = QPushButton("浏览...")
        select_btn.clicked.connect(self.select_file)
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(select_btn)
        file_group.setLayout(file_layout)
        content_layout.addWidget(file_group)

        # Action Button
        action_btn = QPushButton(self.action_btn_text)
        action_btn.setProperty("class", "PrimaryButton")
        action_btn.setMinimumHeight(50)
        action_btn.clicked.connect(self.perform_action)
        content_layout.addWidget(action_btn)

        main_layout.addLayout(content_layout)

    def select_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "选择文件", "", self.file_filter)
        if file:
            self.set_file(file)

    def set_file(self, filepath):
        self.selected_file = filepath
        self.file_label.setText(os.path.basename(filepath))

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            # Basic extension check based on filter string
            ext = os.path.splitext(path)[1].lower()
            if ext in self.file_filter.lower():
                self.set_file(path)
                break

    def perform_action(self):
        if not self.selected_file:
            return QMessageBox.warning(self, "提示", "请先选择一个文件。")

        if self.is_dir_output:
            output_path = QFileDialog.getExistingDirectory(self, "选择保存目录")
            if not output_path: return
        else:
            # Create a suggested default filename
            base = os.path.splitext(os.path.basename(self.selected_file))[0]
            suggested_name = f"{base}_converted{self.default_ext}"
            filter_str = f"*{self.default_ext}" if self.default_ext else ""
            output_path, _ = QFileDialog.getSaveFileName(self, "保存文件", suggested_name, filter_str)
            if not output_path: return

        # call the function
        # action_func must take (input_path, output_path) and return (success, msg)
        success, msg = self.action_func(self.selected_file, output_path)
        if success:
            QMessageBox.information(self, "成功", msg)
        else:
            QMessageBox.critical(self, "错误", msg)


class MultiFileActionView(QWidget):
    """
    通用多文件处理视图，适用于“多文件进 -> 单文件出”场景 (例如 JPG转PDF)
    基于 MergeView 修改
    """
    go_back = Signal()

    def __init__(self, title, subtitle, file_filter, action_btn_text, action_func, default_ext=""):
        super().__init__()
        self.title_text = title
        self.subtitle_text = subtitle
        self.file_filter = file_filter
        self.action_btn_text = action_btn_text
        self.action_func = action_func
        self.default_ext = default_ext
        self.setAcceptDrops(True)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        # Header
        header_layout = QHBoxLayout()
        back_btn = QPushButton("← 返回首页")
        back_btn.clicked.connect(self.go_back.emit)
        title = QLabel(self.title_text)
        title.setObjectName("headerTitle")
        header_layout.addWidget(back_btn)
        header_layout.addStretch()
        header_layout.addWidget(title)
        header_layout.addStretch()
        spacer = QWidget()
        spacer.setFixedWidth(back_btn.sizeHint().width())
        header_layout.addWidget(spacer)
        main_layout.addLayout(header_layout)

        subtitle = QLabel(self.subtitle_text)
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
        action_btn = QPushButton(self.action_btn_text)
        action_btn.setProperty("class", "PrimaryButton")
        action_btn.setMinimumHeight(50)
        action_btn.clicked.connect(self.perform_action)

        controls_layout.addWidget(up_btn)
        controls_layout.addWidget(down_btn)
        controls_layout.addStretch()
        controls_layout.addWidget(action_btn)
        content_layout.addLayout(controls_layout, 1)
        main_layout.addLayout(content_layout)

    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "选择文件", "", self.file_filter)
        if files:
            for file in files:
                self.add_file_to_list(file)

    def add_file_to_list(self, filepath):
        is_duplicate = False
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item.data(Qt.UserRole) == filepath:
                is_duplicate = True
                break
        if not is_duplicate:
            item = QListWidgetItem(os.path.basename(filepath))
            item.setData(Qt.UserRole, filepath)
            self.list_widget.addItem(item)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            ext = os.path.splitext(path)[1].lower()
            if ext in self.file_filter.lower() or '.*' in self.file_filter:
                 self.add_file_to_list(path)

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

    def perform_action(self):
        if self.list_widget.count() < 1:
            return QMessageBox.warning(self, "提示", "请至少添加1个文件。")

        filter_str = f"*{self.default_ext}" if self.default_ext else ""
        output_file, _ = QFileDialog.getSaveFileName(self, "保存文件", f"converted{self.default_ext}", filter_str)
        if not output_file: return

        file_list = [self.list_widget.item(i).data(Qt.UserRole) for i in range(self.list_widget.count())]
        success, msg = self.action_func(file_list, output_file)
        if success:
            QMessageBox.information(self, "成功", msg)
        else:
            QMessageBox.critical(self, "错误", msg)
