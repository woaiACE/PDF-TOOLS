import os
from pypdf import PdfReader, PdfWriter

def merge_pdfs(input_paths, output_path):
    """
    Merge a list of PDF files into a single output file.
    """
    writer = PdfWriter()
    for path in input_paths:
        try:
            reader = PdfReader(path)
            for page in reader.pages:
                writer.add_page(page)
        except Exception as e:
            print(f"Error reading {path}: {e}")
            raise e

    with open(output_path, "wb") as out_file:
        writer.write(out_file)

def split_pdf_pages(input_path, output_dir):
    """
    Split a PDF into single-page PDF files.
    Output files will be named like: original_name_page_1.pdf, original_name_page_2.pdf
    """
    reader = PdfReader(input_path)
    base_name = os.path.splitext(os.path.basename(input_path))[0]

    for i in range(len(reader.pages)):
        writer = PdfWriter()
        writer.add_page(reader.pages[i])
        output_filename = os.path.join(output_dir, f"{base_name}_page_{i+1}.pdf")
        with open(output_filename, "wb") as out_file:
            writer.write(out_file)

def extract_pdf_pages(input_path, output_path, pages_str):
    """
    Extract specific pages from a PDF.
    pages_str can be like "1,3,5-7" (1-based indexing).
    """
    reader = PdfReader(input_path)
    total_pages = len(reader.pages)
    writer = PdfWriter()

    pages_to_extract = set()
    parts = pages_str.split(',')
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if '-' in part:
            try:
                start, end = part.split('-')
                start_idx = int(start)
                end_idx = int(end)
                if start_idx <= end_idx:
                    pages_to_extract.update(range(start_idx, end_idx + 1))
            except ValueError:
                pass
        else:
            try:
                pages_to_extract.add(int(part))
            except ValueError:
                pass

    # Sort and filter valid pages
    sorted_pages = sorted([p for p in pages_to_extract if 1 <= p <= total_pages])

    for page_num in sorted_pages:
        # 1-based to 0-based
        writer.add_page(reader.pages[page_num - 1])

    if len(sorted_pages) > 0:
        with open(output_path, "wb") as out_file:
            writer.write(out_file)
    else:
        raise ValueError("未选择有效的页面。")
