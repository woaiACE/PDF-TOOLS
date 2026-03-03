import os
from pypdf import PdfWriter, PdfReader

def merge_pdfs(pdf_list, output_path):
    merger = PdfWriter()
    try:
        for pdf in pdf_list:
            merger.append(pdf)
        with open(output_path, "wb") as f:
            merger.write(f)
        return True, "合并成功！"
    except Exception as e:
        return False, f"合并失败: {str(e)}"
    finally:
        merger.close()

def parse_page_ranges(range_str, total_pages):
    pages = set()
    parts = [p.strip() for p in range_str.split(',') if p.strip()]
    for part in parts:
        if '-' in part:
            try:
                start, end = map(int, part.split('-'))
                if start > end:
                    start, end = end, start
                for p in range(start, end + 1):
                    if 1 <= p <= total_pages:
                        pages.add(p - 1)
            except ValueError:
                raise ValueError(f"无效的页码范围格式: {part}")
        else:
            try:
                p = int(part)
                if 1 <= p <= total_pages:
                    pages.add(p - 1)
            except ValueError:
                raise ValueError(f"无效的页码格式: {part}")
    return sorted(list(pages))

def split_pdf_extract(pdf_path, output_path, range_str):
    try:
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)
        pages_to_extract = parse_page_ranges(range_str, total_pages)
        if not pages_to_extract:
            return False, "没有选中任何有效的页面。"
        writer = PdfWriter()
        for p in pages_to_extract:
            writer.add_page(reader.pages[p])
        with open(output_path, "wb") as f:
            writer.write(f)
        return True, "提取成功！"
    except Exception as e:
        return False, f"提取失败: {str(e)}"

def split_pdf_all(pdf_path, output_dir):
    try:
        reader = PdfReader(pdf_path)
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        for i, page in enumerate(reader.pages):
            writer = PdfWriter()
            writer.add_page(page)
            output_path = os.path.join(output_dir, f"{base_name}_page_{i+1}.pdf")
            with open(output_path, "wb") as f:
                writer.write(f)
        return True, "拆分成功！"
    except Exception as e:
        return False, f"拆分失败: {str(e)}"
