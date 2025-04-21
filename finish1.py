import tkinter as tk
from tkinter import ttk, scrolledtext
from bs4 import BeautifulSoup
import html


def parse_html():
    # 清空输出框
    output_text.delete('1.0', tk.END)

    # 获取输入内容
    html_content = input_text.get('1.0', tk.END)

    try:
        # 解析代码
        parsed_code = extract_code_from_html(html_content)
        # 插入结果（带语法高亮占位）
        output_text.insert(tk.END, parsed_code)
    except Exception as e:
        output_text.insert(tk.END, f"解析错误: {str(e)}")


def extract_code_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    code_lines = []

    # 修改查找条件：查找包含code-span类的span标签
    for line_span in soup.find_all(
            'span', {'class': lambda x: x and 'code-span' in x}):
        line_content = []
        current = line_span

        # 遍历所有相邻节点直到遇到下一个代码块标记
        while current:
            # 获取元素内容时保留原始格式
            if current.name == 'span':
                line_content.append(
                    current.get_text(strip=False, separator=' '))
            else:
                line_content.append(str(current))

            # 检测下一个同层级元素是否为代码块标记
            next_sib = current.next_sibling
            if next_sib and next_sib.name == 'span' and 'code-span' in next_sib.get(
                    'class', []):
                break
            current = next_sibling

        # 合并并清理代码行
        decoded_line = html.unescape(''.join(line_content).replace(
            '\n', ' ').strip())
        if decoded_line:
            code_lines.append(decoded_line)

    return '\n'.join(code_lines)


# 创建主窗口
root = tk.Tk()
root.title("WPS网页代码解析器")
root.geometry("1000x600")

# 界面布局
main_frame = ttk.Frame(root, padding=10)
main_frame.pack(fill=tk.BOTH, expand=True)

# 输入面板
input_frame = ttk.Frame(main_frame)
input_frame.grid(row=0, column=0, sticky='nsew', padx=5)

input_label = ttk.Label(input_frame, text="输入HTML代码:")
input_label.pack(anchor='w')

input_text = scrolledtext.ScrolledText(input_frame,
                                       wrap=tk.WORD,
                                       width=60,
                                       height=30)
input_text.pack()

# 操作按钮
button_frame = ttk.Frame(main_frame)
button_frame.grid(row=0, column=1, sticky='ns', padx=10)

parse_btn = ttk.Button(button_frame, text="解析代码 →", command=parse_html)
parse_btn.pack(pady=20)

# 输出面板
output_frame = ttk.Frame(main_frame)
output_frame.grid(row=0, column=2, sticky='nsew', padx=5)

output_label = ttk.Label(output_frame, text="解析结果:")
output_label.pack(anchor='w')

output_text = scrolledtext.ScrolledText(output_frame,
                                        wrap=tk.WORD,
                                        width=60,
                                        height=30)
output_text.pack()

# 配置网格权重
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(2, weight=1)
main_frame.rowconfigure(0, weight=1)

# 启动程序
root.mainloop()
