from bs4 import BeautifulSoup
import html


def extract_code_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    code_lines = []

    # 定位所有包含代码行的span标签（通过line属性识别）
    for line_span in soup.find_all('span', {'line': True}):
        line_content = []
        # 提取该行内所有子节点的文本（包括嵌套span）
        for elem in line_span.next_siblings:
            if elem.name == 'span' and 'line' in elem.attrs:
                break  # 遇到下一行时停止
            if elem.name == 'span':
                line_content.append(elem.get_text())
        # 拼接并处理HTML转义字符
        full_line = ''.join(line_content).strip()
        if full_line:
            code_lines.append(html.unescape(full_line))

    return '\n'.join(code_lines)


import sys


def extract_code_full(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    code_lines = []

    for line_span in soup.find_all('span', {'line': True}):
        line_content = []
        current = line_span.next_sibling
        while current and not (current.name == 'span'
                               and 'line' in current.attrs):
            if isinstance(current, str):
                line_content.append(current)
            elif current.name == 'span':
                line_content.append(
                    current.get_text(strip=False, separator=' '))
            current = current.next_sibling
        decoded_line = html.unescape(''.join(line_content).strip())
        code_lines.append(decoded_line)

    # 确保输出终端支持UTF-8
    sys.stdout.reconfigure(encoding='utf-8')
    return '\n'.join(code_lines)


def extract_code_from_html2(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    code_lines = []

    # 查找所有包含code-span类的span标签作为起始标记
    code_spans = soup.find_all('span',
                               {'class': lambda x: x and 'code-span' in x})

    for i, span in enumerate(code_spans):
        line_content = []
        current = span

        # 遍历后续兄弟节点直到遇到下一个代码块标记
        while current:
            # 处理当前节点内容
            if current.name == 'span':
                # 保留原始空白和格式
                line_content.append(
                    current.get_text(strip=False, separator=' '))
            else:
                # 处理文本节点
                line_content.append(str(current).replace('\n', ' '))

            # 检查下一个兄弟节点
            next_sib = current.next_sibling
            if next_sib and next_sib.name == 'span' and 'code-span' in next_sib.get(
                    'class', []):
                break
            current = next_sib  # 修正变量名

        # 合并并清理代码行
        decoded_line = html.unescape(''.join(line_content).strip())
        if decoded_line:
            # 处理行末换行符
            if i != len(code_spans) - 1 and not decoded_line.endswith('\n'):
                decoded_line += '\n'
            code_lines.append(decoded_line)

    return '\n'.join(code_lines)


# 示例用法
html_content = """<code class="code-block-content code-block-theme-style"><span class="code-block-line no-hit ProseMirror-widget" line="1" contenteditable="false"></span><span class="hljs-meta">#</span><span class="hljs-meta hljs-meta-keyword">ifndef</span><span class="hljs-meta"> __KX_HTTP_REQUEST_MANAGER_H_</span><span class="code-span">
</span><span class="code-block-line no-hit ProseMirror-widget" line="2" contenteditable="false"></span><span class="hljs-meta">#</span><span class="hljs-meta hljs-meta-keyword">define</span><span class="hljs-meta"> __KX_HTTP_REQUEST_MANAGER_H_</span><span class="code-span">
</span><span class="code-block-line no-hit ProseMirror-widget" line="3" contenteditable="false"></span><span class="code-span">
</span><span class="code-block-line no-hit ProseMirror-widget" line="4" contenteditable="false"></span><span class="hljs-meta">#</span><span class="hljs-meta hljs-meta-keyword">include</span><span class="hljs-meta"> </span><span class="hljs-meta hljs-meta-string">&lt;QObject&gt;</span><span class="code-span">
</span><span class="code-block-line no-hit ProseMirror-widget" line="5" contenteditable="false"></span><span class="hljs-meta">#</span><span class="hljs-meta hljs-meta-keyword">include</span><span class="hljs-meta"> </span><span class="hljs-meta hljs-meta-string">&lt;QNetworkAccessManager&gt;</span><span class="code-span">
</span><span class="code-block-line no-hit ProseMirror-widget" line="6" contenteditable="false"></span><span class="hljs-meta">#</span><span class="hljs-meta hljs-meta-keyword">include</span><span class="hljs-meta"> </span><span class="hljs-meta hljs-meta-string">&lt;QNetworkRequest&gt;</span><span class="code-span">
</span><span class="code-block-line no-hit ProseMirror-widget" line="7" contenteditable="false"></span><span class="hljs-meta">#</span><span class="hljs-meta hljs-meta-keyword">include</span><span class="hljs-meta"> </span><span class="hljs-meta hljs-meta-string">&lt;QNetworkReply&gt;</span><span class="code-span">
</span><span class="code-block-line no-hit ProseMirror-widget" line="8" contenteditable="false"></span><span class="code-span">
</span><span class="code-block-line no-hit ProseMirror-widget" line="9" contenteditable="false"></span><span class="hljs-class hljs-keyword">class</span><span class="hljs-class"> </span><span class="hljs-class hljs-title">KxHttpRequestManager</span><span class="hljs-class"> :</span><span class="code-span"> </span><span class="hljs-keyword">public</span><span class="code-span"> QObject
</span><span class="code-block-line no-hit ProseMirror-widget" line="10" contenteditable="false"></span><span class="code-span">{
</span><span class="code-block-line no-hit ProseMirror-widget" line="11" contenteditable="false"></span><span class="code-span">    Q_OBJECT
</span><span class="code-block-line no-hit ProseMirror-widget" line="12" contenteditable="false"></span><span class="code-span">
</span><span class="code-block-line no-hit ProseMirror-widget" line="13" contenteditable="false"></span><span class="hljs-keyword">public</span><span class="code-span">:
</span><span class="code-block-line no-hit ProseMirror-widget" line="14" contenteditable="false"></span><span class="code-span">    </span><span class="hljs-built_in">KxHttpRequestManager</span><span class="code-span">(QObject *parent = </span><span class="hljs-literal">nullptr</span><span class="code-span">);
</span><span class="code-block-line no-hit ProseMirror-widget" line="15" contenteditable="false"></span><span class="code-span">    ~</span><span class="hljs-built_in">KxHttpRequestManager</span><span class="code-span">();
</span><span class="code-block-line no-hit ProseMirror-widget" line="16" contenteditable="false"></span><span class="code-span">    </span><span class="hljs-function hljs-keyword">void</span><span class="hljs-function"> </span><span class="hljs-function hljs-title">sendGetRequest</span><span class="hljs-function hljs-params">(</span><span class="hljs-function hljs-params hljs-keyword">const</span><span class="hljs-function hljs-params"> QUrl&amp; url)</span><span class="code-span">;</span><span class="hljs-comment">// 发送 get 请求</span><span class="code-span">
</span><span class="code-block-line no-hit ProseMirror-widget" line="17" contenteditable="false"></span><span class="code-span">    </span><span class="hljs-function hljs-keyword">void</span><span class="hljs-function"> </span><span class="hljs-function hljs-title">sendPostRequest</span><span class="hljs-function hljs-params">(</span><span class="hljs-function hljs-params hljs-keyword">const</span><span class="hljs-function hljs-params"> QUrl&amp; url, </span><span class="hljs-function hljs-params hljs-keyword">const</span><span class="hljs-function hljs-params"> QByteArray&amp; data)</span><span class="code-span">; </span><span class="hljs-comment">// 发送 post 请求</span><span class="code-span">
</span><span class="code-block-line no-hit ProseMirror-widget" line="18" contenteditable="false"></span><span class="code-span">
</span><span class="code-block-line no-hit ProseMirror-widget" line="19" contenteditable="false"></span><span class="code-span">signals:
</span><span class="code-block-line no-hit ProseMirror-widget" line="20" contenteditable="false"></span><span class="code-span">    </span><span class="hljs-function hljs-keyword">void</span><span class="hljs-function"> </span><span class="hljs-function hljs-title">requestFinished</span><span class="hljs-function hljs-params">(QNetworkReply* reply)</span><span class="code-span">;
</span><span class="code-block-line no-hit ProseMirror-widget" line="21" contenteditable="false"></span><span class="code-span">
</span><span class="code-block-line no-hit ProseMirror-widget" line="22" contenteditable="false"></span><span class="hljs-keyword">private</span><span class="code-span">:
</span><span class="code-block-line no-hit ProseMirror-widget" line="23" contenteditable="false"></span><span class="code-span">    QNetworkAccessManager m_manager;
</span><span class="code-block-line no-hit ProseMirror-widget" line="24" contenteditable="false"></span><span class="code-span">};
</span><span class="code-block-line no-hit ProseMirror-widget" line="25" contenteditable="false"></span><span class="code-span">
</span><span class="code-block-line no-hit ProseMirror-widget" line="26" contenteditable="false"></span><span class="hljs-meta">#</span><span class="hljs-meta hljs-meta-keyword">endif</span></code>"""
source_code = extract_code_from_html2(html_content)
print(source_code)
