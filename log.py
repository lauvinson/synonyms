import os  # 内置模块 用于创建文件
import random

import requests as rs  # 第三方模块 需要 pip install requests 安装  用于请求网页数据
import pandas as pd

list = []
id1 = 0
id2 = 0


def save(hero_title, hero_name, image_url):
    path = f'lol\\{hero_title}\\'
    if not os.path.exists(path):
        os.makedirs(path)
    image_content = rs.get(image_url).content
    with open(path + hero_name + '.jpg', mode='wb') as f:
        f.write(image_content)


def get_hero_url(hero_id):
    global id1
    global id2
    page_url = f'https://game.gtimg.cn/images/lol/act/img/js/hero/{hero_id}.js'
    hero_data = rs.get(page_url).json()

    hero = hero_data['hero']
    hero_alias = hero['alias']
    hero_name = hero['name']
    avatar = f'https://game.gtimg.cn/images/lol/act/img/champion/{hero_alias}.png'
    list.append(
        {'id': id1, 'title': hero_name, 'price': random.randint(0, 100), 'typed': 1, 'status': 1, 'data': avatar,
         'createAt': '2021-08-06 12:00:13', 'updateAt': '2021-08-06 12:00:13'})
    id1 = id1 + 1

    skins = hero_data['skins']
    for index in skins:
        # 皮肤url
        image_url = index['mainImg']
        # 皮肤名字
        hero_name = index['name']
        # 文件夹名字
        hero_title = index['heroTitle']
        if image_url:
            list.append({'id': id2, 'title': hero_name, 'price': random.randint(0, 100), 'typed': 3, 'status': 1,
                         'data': image_url, 'createAt': '2021-08-06 12:00:13', 'updateAt': '2021-08-06 12:00:13'})
            # save(hero_title, hero_name, image_url)
        else:
            image_2_url = index['chromaImg']
            list.append({'id': id2, 'title': hero_name, 'price': random.randint(0, 100), 'typed': 3, 'status': 1,
                         'data': image_2_url, 'createAt': '2021-08-06 12:00:13', 'updateAt': '2021-08-06 12:00:13'})
            # save(hero_title, hero_name, image_2_url)
        id2 = id2 + 1


url = 'https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js'
json_data = rs.get(url).json()['hero']
for i in json_data:
    hero_id = i['heroId']
    get_hero_url(hero_id)

pd.DataFrame(list).to_csv('lol.csv')
