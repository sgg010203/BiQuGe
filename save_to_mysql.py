import mysql.connector

from novel_info import get_novel_info


def basic_info(title, author, description):
    # 添加记录
    cursor.execute(f"""
        INSERT INTO novels (novel_name, author, description)
            VALUES ({title}, {author}, {description});
    """)


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

    # 添加基本小说信息
    basic_info(novel_info['novel_name'], novel_info['author'], novel_info['description'])
