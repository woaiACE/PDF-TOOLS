from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QFrame, QMessageBox)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor

class FeatureCard(QFrame):
    clicked = Signal()
    def __init__(self, title, description, icon_text, is_active=True, parent=None):
        super().__init__(parent)
        self.is_active = is_active
        self.setFixedSize(240, 180)
        self.setProperty("class", "FeatureCard")
        self.setCursor(QCursor(Qt.PointingHandCursor))
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        icon_label = QLabel(icon_text)
        icon_label.setStyleSheet("font-size: 32px; color: #e53e3e;")
        title_label = QLabel(title)
        title_label.setProperty("class", "CardTitle")
        title_label.setWordWrap(True)
        desc_label = QLabel(description)
        desc_label.setProperty("class", "CardDesc")
        desc_label.setWordWrap(True)
        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        layout.addStretch()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.is_active: self.clicked.emit()
            else: QMessageBox.information(self, "敬请期待", f"功能即将上线，敬请期待！")
        super().mousePressEvent(event)

class HomeView(QWidget):
    go_to_merge = Signal()
    go_to_split = Signal()
    go_to_compress = Signal()
    go_to_p2w = Signal()
    go_to_p2p = Signal()
    go_to_p2e = Signal()
    go_to_w2p = Signal()
    go_to_p2p2 = Signal()
    go_to_e2p = Signal()
    go_to_p2j = Signal()
    go_to_j2p = Signal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(40)

        header_layout = QVBoxLayout()
        title = QLabel("PDF爱好者的在线工具")
        title.setObjectName("headerTitle")
        title.setAlignment(Qt.AlignCenter)
        subtitle = QLabel("完全免费、易于使用、丰富的PDF处理工具，包括：合并、拆分、压缩、转换、旋转和解锁PDF文件，\n以及给PDF文件添加水印的工具等。仅需几秒钟即可完成。")
        subtitle.setObjectName("headerSubtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        main_layout.addLayout(header_layout)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)
        cards_data = [
            {"title": "合并PDF", "desc": "合并PDF文件，并按照您的喜好排序，简单又快速！", "icon": "📄➕", "active": True, "action": self.go_to_merge.emit},
            {"title": "拆分 PDF", "desc": "拆分出1个页面，或者所有页面，以便将这些页面转换为独立的PDF文件。", "icon": "📄✂️", "active": True, "action": self.go_to_split.emit},
            {"title": "压缩PDF", "desc": "减小PDF文件的尺寸，但同时保持最佳质量。优化您的PDF文件。", "icon": "🗜️", "active": True, "action": self.go_to_compress.emit},
            {"title": "PDF 转换至 Word", "desc": "轻松地把PDF转换为可编辑的DOC和DOCX文件。转换后的WORD文件几乎100%正确。", "icon": "📝", "active": True, "action": self.go_to_p2w.emit},
            {"title": "PDF 转换至 PowerPoint", "desc": "将你的PDF转换为可编辑的PPT和PPTX幻灯片文件。", "icon": "📊", "active": True, "action": self.go_to_p2p.emit},
            {"title": "PDF 转换至 Excel", "desc": "只需几秒钟，即可将数据直接从PDF文件提取至Excel电子表格中。", "icon": "📈", "active": True, "action": self.go_to_p2e.emit},
            {"title": "Word转换至PDF文件", "desc": "将你的DOC或DOCX文件转换为PDF，以方便查看。", "icon": "🔄", "active": True, "action": self.go_to_w2p.emit},
            {"title": "PowerPoint 转换至 PDF", "desc": "将PPT转换为PDF文件，与原来的PPT或PPTX文件完全一样，并保持最佳质量。", "icon": "🔄", "active": True, "action": self.go_to_p2p2.emit},
            {"title": "Excel 转换至 PDF", "desc": "把EXCEL表格转换为PDF文件，以方便查看。", "icon": "🔄", "active": True, "action": self.go_to_e2p.emit},
            {"title": "编辑PDF文件", "desc": "给PDF文件添加文本、图片、形状或手写的注释。编辑已添加内容的大小、字体和颜色。", "icon": "✏️", "active": False},
            {"title": "PDF转JPG", "desc": "提取PDF文件中的所有图片，或将每一页转换为JPG图片。", "icon": "🖼️", "active": True, "action": self.go_to_p2j.emit},
            {"title": "JPG转PDF", "desc": "将您的图片转换为PDF文件，还可以调整方向和边距。", "icon": "🖼️", "active": True, "action": self.go_to_j2p.emit},
        ]
        row, col = 0, 0
        for data in cards_data:
            card = FeatureCard(data["title"], data["desc"], data["icon"], data["active"])
            if data["active"] and "action" in data:
                card.clicked.connect(data["action"])
            grid_layout.addWidget(card, row, col)
            col += 1
            if col >= 5: col, row = 0, row + 1
        main_layout.addLayout(grid_layout)
