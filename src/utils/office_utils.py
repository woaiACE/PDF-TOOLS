import os
import platform

def word_to_pdf(input_path, output_path):
    """
    Windows 下使用 docx2pdf (依赖本地 Office)。
    """
    if platform.system() != "Windows":
        return False, "当前功能仅支持 Windows 操作系统 (需安装 Microsoft Word)。"
    try:
        from docx2pdf import convert
        convert(input_path, output_path)
        return True, "Word成功转换为PDF文件！"
    except Exception as e:
        return False, f"转换失败 (请确保已安装Microsoft Word): {str(e)}"

def excel_to_pdf(input_path, output_path):
    """
    Windows 下使用 comtypes 调用本地 Excel。
    """
    if platform.system() != "Windows":
        return False, "当前功能仅支持 Windows 操作系统 (需安装 Microsoft Excel)。"
    try:
        import comtypes.client
        # 参数: 0 对应 xlTypePDF
        excel = comtypes.client.CreateObject("Excel.Application")
        excel.Visible = False
        wb = excel.Workbooks.Open(os.path.abspath(input_path))
        wb.ExportAsFixedFormat(0, os.path.abspath(output_path))
        wb.Close(False)
        excel.Quit()
        return True, "Excel成功转换为PDF文件！"
    except Exception as e:
        return False, f"转换失败 (请确保已安装Microsoft Excel): {str(e)}"

def ppt_to_pdf(input_path, output_path):
    """
    Windows 下使用 comtypes 调用本地 PowerPoint。
    """
    if platform.system() != "Windows":
        return False, "当前功能仅支持 Windows 操作系统 (需安装 Microsoft PowerPoint)。"
    try:
        import comtypes.client
        # 参数: 32 对应 ppSaveAsPDF
        powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
        # powerpoint.Visible = True # 有时需设为True避免挂起，但为了静默保持默认或处理COM错误
        presentation = powerpoint.Presentations.Open(os.path.abspath(input_path), WithWindow=False)
        presentation.SaveAs(os.path.abspath(output_path), 32)
        presentation.Close()
        powerpoint.Quit()
        return True, "PowerPoint成功转换为PDF文件！"
    except Exception as e:
        return False, f"转换失败 (请确保已安装Microsoft PowerPoint): {str(e)}"
