from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QGridLayout, QFrame, QSizePolicy, QSpacerItem)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QCursor, QFont

class CardWidget(QFrame):
    clicked = pyqtSignal(str)

    def __init__(self, card_id, title, description, is_active=True, icon_text="📄", parent=None):
        super().__init__(parent)
        self.card_id = card_id
        self.is_active = is_active

        # Style
        self.setObjectName("CardWidget")
        if self.is_active:
            self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.setStyleSheet("""
                #CardWidget {
                    background-color: white;
                    border-radius: 12px;
                    border: 1px solid #e0e0e0;
                }
                #CardWidget:hover {
                    border: 1px solid #ff4d4f;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                }
            """)
        else:
            self.setStyleSheet("""
                #CardWidget {
                    background-color: #f9f9f9;
                    border-radius: 12px;
                    border: 1px solid #e0e0e0;
                    color: #999999;
                }
            """)

        self.setFixedSize(280, 160)

        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Icon
        self.icon_label = QLabel(icon_text)
        self.icon_label.setFont(QFont("Arial", 24))
        self.icon_label.setStyleSheet("color: #ff4d4f;" if is_active else "color: #cccccc;")
        layout.addWidget(self.icon_label)

        # Title
        self.title_label = QLabel(title)
        title_font = QFont("Microsoft YaHei", 12, QFont.Weight.Bold)
        self.title_label.setFont(title_font)
        if not is_active:
            self.title_label.setStyleSheet("color: #999999;")
        layout.addWidget(self.title_label)

        # Description
        self.desc_label = QLabel(description)
        self.desc_label.setFont(QFont("Microsoft YaHei", 9))
        self.desc_label.setStyleSheet("color: #666666;" if is_active else "color: #b0b0b0;")
        self.desc_label.setWordWrap(True)
        self.desc_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.desc_label)

        # Make the layout stretch from bottom
        layout.addStretch()

    def mousePressEvent(self, event):
        if self.is_active and event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.card_id)
        super().mousePressEvent(event)


class HomePage(QWidget):
    request_navigate = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)

        # Header Title
        title_label = QLabel("PDF爱好者的在线工具")
        title_font = QFont("Microsoft YaHei", 24, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # Subtitle
        subtitle_label = QLabel("完全免费、易于使用、丰富的PDF处理工具，包括：合并、拆分等。仅需几秒钟即可完成。")
        subtitle_font = QFont("Microsoft YaHei", 11)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: #666666;")
        main_layout.addWidget(subtitle_label)

        main_layout.addSpacing(30)

        # Grid Layout for Cards
        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Active Cards
        self.card_merge = CardWidget(
            "merge",
            "合并PDF",
            "合并PDF文件，并按照您的喜好排序，简单又快速！",
            is_active=True,
            icon_text="📥"
        )
        self.card_split = CardWidget(
            "split",
            "拆分 PDF",
            "拆分出1个页面，或者所有页面，以便将这些页面转换为独立的PDF文件。",
            is_active=True,
            icon_text="✂️"
        )

        self.card_merge.clicked.connect(self.on_card_clicked)
        self.card_split.clicked.connect(self.on_card_clicked)

        # Placeholders
        self.card_compress = CardWidget(
            "compress",
            "压缩PDF",
            "减小PDF文件的尺寸，但同时保持最佳质量。(敬请期待)",
            is_active=False,
            icon_text="🗜️"
        )
        self.card_to_word = CardWidget(
            "to_word",
            "PDF 转换至 Word",
            "轻松地把PDF转换为可编辑的DOC和DOCX文件。(敬请期待)",
            is_active=False,
            icon_text="📝"
        )
        self.card_to_ppt = CardWidget(
            "to_ppt",
            "PDF 转换至 PowerPoint",
            "将你的PDF转换为可编辑的PPT和PPTX幻灯片文件。(敬请期待)",
            is_active=False,
            icon_text="📊"
        )
        self.card_to_excel = CardWidget(
            "to_excel",
            "PDF 转换至 Excel",
            "只需几秒钟，即可将数据直接从PDF文件提取至Excel电子表格中。(敬请期待)",
            is_active=False,
            icon_text="📈"
        )

        # Add to grid
        grid_layout.addWidget(self.card_merge, 0, 0)
        grid_layout.addWidget(self.card_split, 0, 1)
        grid_layout.addWidget(self.card_compress, 0, 2)
        grid_layout.addWidget(self.card_to_word, 0, 3)
        grid_layout.addWidget(self.card_to_ppt, 1, 0)
        grid_layout.addWidget(self.card_to_excel, 1, 1)

        # Add a stretch container to center the grid
        grid_container = QWidget()
        grid_container.setLayout(grid_layout)

        h_layout = QHBoxLayout()
        h_layout.addStretch()
        h_layout.addWidget(grid_container)
        h_layout.addStretch()

        main_layout.addLayout(h_layout)
        main_layout.addStretch()

    def on_card_clicked(self, card_id):
        self.request_navigate.emit(card_id)
