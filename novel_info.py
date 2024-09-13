import time

import requests
from bs4 import BeautifulSoup


def get_novel_info(base_url):
    # 获取小说基本信息
    response = requests.get(base_url)
    if response.status_code != 200:
        print(f"请求失败，状态码：{response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # with open('output.html', 'w', encoding='utf-8') as file:
    #     file.write(soup.prettify())

    # 获取小说标题
    name_tag = soup.find('meta', {'property': 'og:title'})
    novel_name = name_tag['content'] if name_tag else '未知标题'

    # 获取小说作者
    author_tag = soup.find('meta', {'property': 'og:novel:author'})
    author = author_tag['content'] if author_tag else '未知作者'

    # 获取小说简介
    # 查找所有的 <dd> 元素
    dd_elements = soup.find_all('dd')

    # 获取 <dd> 元素内的所有文本，包括 <span> 元素内的文本
    description = dd_elements[0].get_text(strip=True)[:-14]  # strip=True 去除空白字符，后14字符为 无意义的乱码和“展开全部”

    # 获取章节列表
    chapters_url = base_url.replace('.html', '/')
    response = requests.get(chapters_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    chapters = []
    for chapter_tag in soup.find_all('dd'):
        a_tag = chapter_tag.find('a')
        if a_tag:
            chapter_title = a_tag.text
            chapter_url = a_tag['href']
            chapters.append({'title': chapter_title, 'url': chapter_url})

    return {
        'novel_name': novel_name,
        'author': author,
        'description': description,
        'chapters': chapters
    }


def get_chapter_content(chapter_url):
    response = requests.get(chapter_url)
    if response.status_code != 200:
        print(f"请求失败，状态码：{response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    content_tag = soup.find('div', {'id': 'chaptercontent'})
    content = content_tag.get_text(separator='\n').strip() if content_tag else '无内容'
    print(content)
    return content


if __name__ == '__main__':
    # 小说页面网址
    novel_url = 'https://www.bqgda.cc/books/5238/'
    novel_info = get_novel_info(novel_url)

    if novel_info:
        print("小说标题:", novel_info['title'])
        print("作者:", novel_info['author'])
        print("简介:", novel_info['description'])
        print("\n章节列表:")
        for i, chapter in enumerate(novel_info['chapters'], 1):
            print(f"{chapter['title']}")

            # 获取章节正文内容
            chapter_url = 'https://www.bqgda.cc' + chapter['url']
            content = get_chapter_content(chapter_url)
            print("章节内容:", content)
            print("-" * 40)
            time.sleep(1)
