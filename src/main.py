import sys
import os
import re
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PySide6.QtGui import QScreen

# 确保能正确导入内部模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.views.home_view import HomeView
from ui.views.merge_view import MergeView
from ui.views.split_view import SplitView
from ui.views.generic_view import SingleFileActionView, MultiFileActionView
from utils import pdf_utils, office_utils

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF工具集")
        self.resize(1024, 768)
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Instantiate base views
        self.home_view = HomeView()
        self.merge_view = MergeView()
        self.split_view = SplitView()

        # Instantiate newly requested views
        self.compress_view = SingleFileActionView("压缩 PDF", "选择需要压缩的PDF文件进行体积优化。", "PDF Files (*.pdf)", "执行压缩", pdf_utils.compress_pdf, default_ext=".pdf")
        self.p2w_view = SingleFileActionView("PDF 转 Word", "将PDF转换为可编辑的DOCX文档。", "PDF Files (*.pdf)", "开始转换", pdf_utils.pdf_to_word, default_ext=".docx")
        self.p2e_view = SingleFileActionView("PDF 转 Excel", "提取PDF表格并保存为XLSX电子表格。", "PDF Files (*.pdf)", "开始转换", pdf_utils.pdf_to_excel, default_ext=".xlsx")
        self.p2p_view = SingleFileActionView("PDF 转 PowerPoint", "将PDF各页转为PPTX幻灯片。", "PDF Files (*.pdf)", "开始转换", pdf_utils.pdf_to_ppt, default_ext=".pptx")
        self.p2j_view = SingleFileActionView("PDF 转 JPG", "将PDF的每一页导出为JPG图片目录。", "PDF Files (*.pdf)", "导出图片目录", pdf_utils.pdf_to_jpg, is_dir_output=True)
        self.j2p_view = MultiFileActionView("JPG 转 PDF", "将多张图片合成一个PDF文件。","Images (*.png *.jpg *.jpeg)", "合成 PDF", pdf_utils.jpg_to_pdf, default_ext=".pdf")

        self.w2p_view = SingleFileActionView("Word 转 PDF", "将DOC/DOCX文件转换为PDF (需Windows下安装Word)。", "Word Files (*.doc *.docx)", "开始转换", office_utils.word_to_pdf, default_ext=".pdf")
        self.e2p_view = SingleFileActionView("Excel 转 PDF", "把XLS/XLSX表格转换为PDF (需Windows下安装Excel)。", "Excel Files (*.xls *.xlsx)", "开始转换", office_utils.excel_to_pdf, default_ext=".pdf")
        self.p2p2_view = SingleFileActionView("PowerPoint 转 PDF", "将PPT/PPTX转换为PDF (需Windows下安装PowerPoint)。", "PPT Files (*.ppt *.pptx)", "开始转换", office_utils.ppt_to_pdf, default_ext=".pdf")

        # Add to stack
        for view in [self.home_view, self.merge_view, self.split_view,
                     self.compress_view, self.p2w_view, self.p2e_view, self.p2p_view,
                     self.p2j_view, self.j2p_view, self.w2p_view, self.e2p_view, self.p2p2_view]:
            self.stacked_widget.addWidget(view)

        # Connect Navigation
        self.home_view.go_to_merge.connect(lambda: self.stacked_widget.setCurrentWidget(self.merge_view))
        self.home_view.go_to_split.connect(lambda: self.stacked_widget.setCurrentWidget(self.split_view))
        self.home_view.go_to_compress.connect(lambda: self.stacked_widget.setCurrentWidget(self.compress_view))
        self.home_view.go_to_p2w.connect(lambda: self.stacked_widget.setCurrentWidget(self.p2w_view))
        self.home_view.go_to_p2e.connect(lambda: self.stacked_widget.setCurrentWidget(self.p2e_view))
        self.home_view.go_to_p2p.connect(lambda: self.stacked_widget.setCurrentWidget(self.p2p_view))
        self.home_view.go_to_p2j.connect(lambda: self.stacked_widget.setCurrentWidget(self.p2j_view))
        self.home_view.go_to_j2p.connect(lambda: self.stacked_widget.setCurrentWidget(self.j2p_view))
        self.home_view.go_to_w2p.connect(lambda: self.stacked_widget.setCurrentWidget(self.w2p_view))
        self.home_view.go_to_e2p.connect(lambda: self.stacked_widget.setCurrentWidget(self.e2p_view))
        self.home_view.go_to_p2p2.connect(lambda: self.stacked_widget.setCurrentWidget(self.p2p2_view))

        # Back buttons
        for view in [self.merge_view, self.split_view,
                     self.compress_view, self.p2w_view, self.p2e_view, self.p2p_view,
                     self.p2j_view, self.j2p_view, self.w2p_view, self.e2p_view, self.p2p2_view]:
            view.go_back.connect(self.show_home)

        self.load_stylesheet()
        self.show_home()

    def load_stylesheet(self):
        style_path = os.path.join(os.path.dirname(__file__), 'assets', 'style.qss')
        if os.path.exists(style_path):
            with open(style_path, "r", encoding="utf-8") as f:
                qss_content = f.read()

            # --- 方案 A：自动缩放逻辑 ---
            # 1. 获取主屏幕的逻辑 DPI
            screen = QApplication.primaryScreen()
            dpi = screen.logicalDotsPerInch()
            # 2. 以 96 DPI 为基准计算缩放比例
            scale = dpi / 96.0

            # 3. 使用正则替换 QSS 中的所有数字 px，按比例放大
            # 例如: "font-size: 16px;" -> "font-size: 20px;" (假设 scale 为 1.25)
            def scale_match(match):
                original_value = float(match.group(1))
                scaled_value = int(original_value * scale)
                return f"{scaled_value}px"

            scaled_qss = re.sub(r'(\d+(?:\.\d+)?)\s*px', scale_match, qss_content)

            # 应用缩放后的样式
            self.setStyleSheet(scaled_qss)

    def show_home(self): self.stacked_widget.setCurrentWidget(self.home_view)
    def show_merge(self): self.stacked_widget.setCurrentWidget(self.merge_view)
    def show_split(self): self.stacked_widget.setCurrentWidget(self.split_view)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
