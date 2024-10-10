from bs4 import BeautifulSoup

html_content = """
<div class="content">
<p id="introText">
    <span class="english" data-start="0.00" data-end="0.90">Long,</span>
    <span class="english" data-start="0.90" data-end="2.53">long ago,</span>
    <span class="english" data-start="2.53" data-end="7.58">there were no boys or girls.</span>
    <span class="english" data-start="7.58" data-end="13.54">There were no mothers or fathers.</span>
    <span class="english" data-start="13.54" data-end="20.95">There was no earth with rivers and trees.</span>
    <span class="english" data-start="20.95" data-end="24.02">No one was there,</span>
    <span class="english" data-start="24.02" data-end="26.19">but God.<br></span>
    <span class="english" data-start="26.19" data-end="29.80">God has always been.</span>
    <span class="english" data-start="29.80" data-end="33.23">God will always be.</span>
    <span class="english" data-start="33.23" data-end="37.56">There is God the Father.</span>
    <span class="english" data-start="37.56" data-end="41.36">There is God the Son.</span>
    <span class="english" data-start="41.36" data-end="44.61">We call Him Jesus.</span>
    <span class="english" data-start="44.61" data-end="50.57">And there is God the Holy Spirit.</span>
    <span class="english" data-start="50.57" data-end="57.61">There is one God but three persons.<br></span>
    <span class="english" data-start="57.61" data-end="65.02">God family is a little like our families.</span>
    <span class="english" data-start="65.02" data-end="69.17">A family is one family,</span>
    <span class="english" data-start="69.17" data-end="77.30">but there are different people in the family.</span>
    <span class="english" data-start="77.30" data-end="82.90">There is a father and a mother.</span>
    <span class="english" data-start="82.90" data-end="87.78">And there are children.<br></span>
    <span class="english" data-start="87.78" data-end="96.45">God made many angels to live with Him in heaven,</span>
    <span class="english" data-start="96.45" data-end="100.24">and to work with Him.</span>
    <span class="english" data-start="100.24" data-end="107.46">He made this world and put people in it.</span>
    <span class="english" data-start="107.46" data-end="107.46">God wanted angels and people to be His friends.</span>
</p>
</div>
"""

# 使用BeautifulSoup解析HTML
soup = BeautifulSoup(html_content, 'html.parser')

# 遍历所有的<span class="english">
for span in soup.find_all('span', class_='english'):
    # 获取 data-start 和 data-end 的值
    start = span['data-start']
    end = span['data-end']

    # 交换属性的值
    span['data-start'], span['data-end'] = end, start

# 输出调整后的HTML，每个span占一行
output_lines = []
for content in soup.find('p', id='introText').children:
    if content.name == 'span':
        output_lines.append(str(content))

# 以换行符拼接输出
output = '\n'.join(output_lines)
print(output)