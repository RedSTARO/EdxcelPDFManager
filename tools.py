import tkinter as tk
from tkinter import filedialog

def selectFile():
    root = tk.Tk()
    root.withdraw()

    directory_path = filedialog.askopenfilename()
    return directory_path
# 合并字段的函数
def merge_fields(data, merge_patterns):
    i = 0
    result = []
    while i < len(data):
        merged = False
        for pattern, replacement in merge_patterns:
            if data[i:i+len(pattern)] == pattern:
                result.append(replacement)  # 添加合并后的字段
                i += len(pattern)           # 跳过已合并的部分
                merged = True
                break
        if not merged:
            result.append(data[i])          # 未匹配合并模式，直接添加原字段
            i += 1
    return result