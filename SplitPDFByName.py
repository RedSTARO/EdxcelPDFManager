import os
import pdfplumber
import tools
from PyPDF2 import PdfReader, PdfWriter

print("""
Split a large pdf into pages by name
Select file that you want to process
""")

# 读取 PDF 文件
input_path = tools.selectFile()

# 确保输出目录存在
output_dir = f"{os.path.splitext(input_path)[0]}"

print(input_path, output_dir)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 打开 PDF 文件
with pdfplumber.open(input_path) as pdf:
    # 使用 PyPDF2 打开 PDF 文件
    pdf_reader = PdfReader(input_path)

    # 遍历每一页
    for page_num, page in enumerate(pdf.pages):
        # 尝试提取表格数据
        tables = page.extract_tables()

        # 确保表格存在
        if tables:
            for table in tables:
                # 查找 "CANDIDATE No. AND NAME" 列的匹配项
                for row in table:
                    if row[0] == "CANDIDATE No. AND NAME":
                        # 提取名字并替换非法字符
                        name = str(row[2]).replace(": ", "_")
                        output_filename = f"{output_dir}/{name}.pdf"

                        # 使用 PyPDF2 创建新的 PDF 文件
                        pdf_writer = PdfWriter()

                        # 使用 PyPDF2 从原始 PDF 文件中获取页面
                        pdf_writer.add_page(pdf_reader.pages[page_num])

                        # 保存文件
                        with open(output_filename, 'wb') as output_file:
                            pdf_writer.write(output_file)

                        print(f"保存文件：{output_filename}")
        else:
            print(f"在第 {page_num + 1} 页未找到表格。")

print("PDF 拆分并命名完成！")
os.system("pause")
