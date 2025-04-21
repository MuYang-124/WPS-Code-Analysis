import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from bs4 import BeautifulSoup
import html
import pyperclip
import re


def paste_from_clipboard():
    try:
        clipboard_content = pyperclip.paste()
        if is_valid_html(clipboard_content):
            input_text.delete('1.0', tk.END)
            input_text.insert(tk.END, clipboard_content)
            parse_html()
        else:
            output_text.delete('1.0', tk.END)
            status_bar.config(text="剪贴板内容不是有效HTML", foreground="gray")
    except Exception as e:
        messagebox.showerror("剪贴板错误", f"无法读取剪贴板内容：{str(e)}")


def is_valid_html(content):
    try:
        BeautifulSoup(content, 'html.parser')
        return True
    except:
        return False


def parse_html():
    output_text.delete('1.0', tk.END)
    status_bar.config(text="")

    html_content = input_text.get('1.0', tk.END)

    if not html_content.strip():
        status_bar.config(text="输入内容为空", foreground="gray")
        return

    try:
        parsed_code = extract_code_from_html(html_content)
        if parsed_code.strip():
            output_text.insert(tk.END, parsed_code)
            status_bar.config(text="解析成功", foreground="green")
        else:
            status_bar.config(text="未找到有效代码", foreground="orange")
    except Exception as e:
        output_text.insert(tk.END, "")
        status_bar.config(text=f"解析错误：{str(e)}", foreground="red")


def extract_code_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    code_lines = []
    current_line = []

    # 查找所有代码相关元素
    for element in soup.find_all(['span', 'br']):
        if element.name == 'br':
            # 处理换行符
            if current_line:
                code_lines.append(''.join(current_line))
                current_line = []
            continue

        if 'code-span' in element.get('class', []):
            text = element.get_text(strip=False, separator=' ')
            # 处理特殊换行情况
            if text.strip().endswith(('{', '}', ';', '//')):
                current_line.append(text)
                code_lines.append(''.join(current_line))
                current_line = []
            else:
                current_line.append(text)
        else:
            # 处理非代码内容
            current_line.append(element.get_text(strip=False, separator=' '))

    # 添加最后一行
    if current_line:
        code_lines.append(''.join(current_line))

    # 合并处理
    formatted_code = html.unescape('\n'.join(code_lines))

    # 二次格式处理
    formatted_code = formatted_code.replace(' )', ')').replace('( ', '(')
    formatted_code = re.sub(r'\n{3,}', '\n\n', formatted_code)  # 压缩多余空行
    formatted_code = re.sub(r'([\{\}])\n *', r'\1\n',
                            formatted_code)  # 花括号换行优化

    return formatted_code


# 创建主窗口
root = tk.Tk()
root.title("智能WPS代码解析器")
root.geometry("1100x650")

# 菜单栏
menubar = tk.Menu(root)
action_menu = tk.Menu(menubar, tearoff=0)
action_menu.add_command(label="从剪贴板粘贴", command=paste_from_clipboard)
action_menu.add_separator()
action_menu.add_command(label="退出", command=root.quit)
menubar.add_cascade(label="操作", menu=action_menu)
root.config(menu=menubar)

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
                                       height=28)
input_text.pack()

# 操作按钮
button_frame = ttk.Frame(main_frame)
button_frame.grid(row=0, column=1, sticky='ns', padx=10)

parse_btn = ttk.Button(button_frame, text="解析代码", command=parse_html, width=15)
parse_btn.pack(pady=5)

paste_btn = ttk.Button(button_frame,
                       text="粘贴剪贴板",
                       command=paste_from_clipboard,
                       width=15)
paste_btn.pack(pady=5)

# 输出面板
output_frame = ttk.Frame(main_frame)
output_frame.grid(row=0, column=2, sticky='nsew', padx=5)

output_label = ttk.Label(output_frame, text="解析结果:")
output_label.pack(anchor='w')

output_text = scrolledtext.ScrolledText(output_frame,
                                        wrap=tk.WORD,
                                        width=60,
                                        height=28)
output_text.pack()

# 状态栏
status_bar = ttk.Label(root, text="就绪", relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# 配置网格权重
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(2, weight=1)
main_frame.rowconfigure(0, weight=1)

# 启动程序
root.mainloop()
