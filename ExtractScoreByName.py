import os
import pdfplumber
import tools
import re
import csv
from PyPDF2 import PdfReader, PdfWriter

print("""
Extract score and manage them into a scv file
select file next
""")

# 读取 PDF 文件
input_path = tools.selectFile()

# 确保输出目录存在
output_dir = f"{os.path.splitext(input_path)[0]}"
# 写入 CSV 文件
with open(f'{output_dir}.csv', mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # 写入列标题
    writer.writerow(['Name', 'Subject', 'Score'])


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
                for rowIndex, row in enumerate(table):
                    if row[0] == "CANDIDATE No. AND NAME":
                        name = str(row[2]).replace(": ", " ")
                        score = table[rowIndex + 2][0].replace("RESULT TYPE EXAM SESSION SUBJECT TITLE RESULT", "")\
                                                      .replace("AWARD ", "").replace("4CH1", "").replace("4CN1", "")\
                                                      .replace("4ES1", "").replace("4PH1", "").replace("4EC1", "")\
                                                      .replace("END", "")\
                                                      .split(" ")
                        for i, item in enumerate(score):
                            if "/" in item:
                                score.remove(score[i])
                            score[i] = score[i].replace("\n", "")
                            score[i] = re.sub(r'\(.*?\)', '', score[i])
                        score = list(filter(None, score))
                        # print(score)
                        
                        # 保存csv
                        # 定义需要合并的字段片段
                        merge_patterns = [
                            (['ENGLISH', 'AS', 'A', 'SECOND', 'LANG.'], 'ENGLISH AS A SECOND LANG.'),  # 合并 ENGLISH AS A SECOND LANG.
                            (['SPOKEN', 'LANGUAGE'], 'SPOKEN LANGUAGE')                                # 合并 SPOKEN LANGUAGE
                        ]


                        # 合并数据
                        score = tools.merge_fields(score, merge_patterns)
                        # 将成绩整理为 (科目, 成绩) 的形式
                        subjects_scores = [(score[i], score[i+1]) for i in range(0, len(score), 2)]

                        # 写入 CSV 文件
                        with open(f'{output_dir}.csv', mode='a', newline='', encoding='utf-8') as file:
                            writer = csv.writer(file)
                            # 遍历整理好的科目和成绩，写入 CSV 文件
                            for idx, (subject, subject_score) in enumerate(subjects_scores):
                                if idx == 0:
                                    # 第一行写入学生姓名、科目、成绩
                                    writer.writerow([name, subject, subject_score])
                                else:
                                    # 后续行不写入学生姓名，保持空白
                                    writer.writerow(['', subject, subject_score])
                                                    

        else:
            print(f"在第 {page_num + 1} 页未找到表格。")

print("PDF 提取完成")
os.system("pause")
