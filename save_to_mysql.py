import mysql.connector

from novel_info import get_novel_info, get_chapter_content


# 向 novels表中 添加小说基本信息
def basic_info(title, author, description):
    cursor.execute(f"""
        INSERT INTO novels (novel_name, author, description)
            VALUES ('{title}', '{author}', '{description}');
    """)

    # 提交更改
    db.commit()


# 向 chapters表中 添加小说章节内容
def catalogue_content(chapters):
    for chapter in chapters:
        title = chapter["title"]
        url = chapter["url"]
        chapter_url = 'https://www.bqgda.cc' + url
        content = get_chapter_content(chapter_url)

        sql = f"""
            INSERT INTO chapters (chapter_name, novel_id, content)
                VALUES (%s, 1, %s);
        """
        param = (title, content)
        cursor.execute(sql, param)

        # 提交更改
        db.commit()


if __name__ == '__main__':
    # 创建数据库连接
    db = mysql.connector.connect(
        host="localhost",  # MySQL服务器地址
        user="root",  # 用户名
        password="030609",  # 密码
        database="biquge_novel"  # 数据库名称
    )

    # 创建游标对象，用于执行SQL查询
    cursor = db.cursor()

    # # 创建一个名为 "BiQuGe_novel" 的数据库,存放小说信息
    # cursor.execute("CREATE DATABASE BiQuGe_novel")

    # # 创建小说基本信息表（书名，作者，简介）
    # cursor.execute("""
    #     CREATE TABLE novels (
    #         id INT AUTO_INCREMENT PRIMARY KEY,
    #         novel_name VARCHAR(255) NOT NULL,
    #         author VARCHAR(255) NOT NULL,
    #         description TEXT);"""
    #                )

    # 小说页面网址
    novel_url = 'https://www.bqgda.cc/books/5238/'
    novel_info = get_novel_info(novel_url)

    # # 添加基本小说信息
    # basic_info(novel_info['novel_name'], novel_info['author'], novel_info['description'])

    # # 创建小说章节内容表（章节号，小说号，章节名称，章节内容）
    # cursor.execute("""
    #     CREATE TABLE chapters (
    #         chapter_id INT AUTO_INCREMENT PRIMARY KEY,
    #         novel_id INT,
    #         chapter_name VARCHAR(255) NOT NULL,
    #         content TEXT);
    #         """
    #                )

    catalogue_content(novel_info['chapters'])

    cursor.close()
    db.close()
