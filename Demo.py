#!/usr/bin/env python
# coding: utf-8

from neo4j import GraphDatabase
import warnings

warnings.filterwarnings('ignore')  # 忽略Warning

# 定义全局变量
all_songs = []  # 所有的歌曲
all_albums = []  # 所有的专辑
all_singers = []  # 所有的歌手


# 功能函数

# 1.查询歌曲、专辑、歌手
def init(tx):
    songs = []
    albums = []
    singers = []
    result1 = tx.run("match (n:`歌曲`) return n as item")
    result2 = tx.run("match (n:`专辑`) return n as item")
    result3 = tx.run("match (n:`歌手`) return n as item")
    for record in result1:
        songs.append(record["item"])
    for record in result2:
        albums.append(record["item"])
    for record in result3:
        singers.append(record["item"])
    return songs, albums, singers


# 2.1. 查询指定日期前发行的专辑

def albums_by_date_back(tx, date):
    albums = []
    result = tx.run("match(m:`专辑`) where m.album_release_date <= $DATE return m as album", DATE=date)
    for record in result:
        albums.append(record["album"])
    return albums


# 2.2. 查询指定日期后发行的专辑
def albums_by_date_forward(tx, date):
    albums = []
    result = tx.run("match(m:`专辑`) where m.album_release_date >= $DATE return m as album", DATE=date)
    for record in result:
        albums.append(record["album"])
    return albums


# 3. 歌曲的专辑名
def album_name_by_song(tx, song):
    names = []
    result = tx.run("match (n) --(m:`专辑`) where n.song_name = $name return m as album", name=song)
    for record in result:
        names.append(record["album"])
    return names


# 4. 专辑包含哪些歌曲
def album_include(tx, album):
    songs = []
    result = tx.run("match(m:`专辑`)-[r:include]->(n:`歌曲`) where m.album_name=$name return n as song", name=album)
    for record in result:
        songs.append(record["song"])
    return songs


# 5. 歌手发行了哪些专辑
def album_releasedBy(tx, singer):
    albums = []
    result = tx.run("match(m:`专辑`)-[r:released_by]->(o:`歌手`) where o.singer_name=$name return m as album",
                    name=singer)
    for record in result:
        albums.append(record["album"])
    return albums


# 1-1. 获取全部信息
def get_all():
    with driver.session() as session:
        [cns1, cns2, cns3] = session.read_transaction(init)
        for tmp in cns1:
            all_songs.append(tmp['song_name'])
        for tmp in cns2:
            all_albums.append(tmp['album_name'])
        for tmp in cns3:
            all_singers.append(tmp['singer_name'])


# 3-3. 歌曲的专辑名
def get_album_name_by_song(song):
    ans = []
    with driver.session() as session:
        albums = session.read_transaction(album_name_by_song, song)
        albums = list(set(albums))  # 去重，不知为什么有重复
        for album in albums:
            # print(album['album_name'])
            ans.append(album['album_name'])
    return ans


# 4-4. 专辑包含哪些歌曲
def get_album_include(album):
    ans = []
    with driver.session() as session:
        songs = session.read_transaction(album_include, album)
        for song in songs:
            # print(song['song_name'])
            ans.append(song['song_name'])
    return ans


# 5-5. 歌手发行了哪些专辑
def get_album_releasedBy(singer):
    ans = []
    with driver.session() as session:
        albums = session.read_transaction(album_releasedBy, '周杰伦')
        for album in albums:
            # print(album['album_name'])
            ans.append(album['album_name'])
    return ans


# 功能1
def func1():
    print('输入格式[op](op=1, 2, 3 分别表示歌曲、专辑、歌手)')
    op = int(input())
    if op == 1:
        print(all_songs)
    elif op == 2:
        print(all_albums)
    elif op == 3:
        print(all_singers)
    else:
        print('请重新输入')


# 功能2
def func2():
    print('输入格式[start,end](start和end表示起止时间，格式为Y/M，可以不同时输入)')
    cns = input()
    [start, end] = cns.split(',')

    album_start = []
    with driver.session() as session:
        songs = session.read_transaction(albums_by_date_forward, start)
        for song in songs:
            # print(song['song_name'])
            album_start.append(song['album_name'])
    album_end = []
    with driver.session() as session:
        songs = session.read_transaction(albums_by_date_back, end)
        for song in songs:
            # print(song['song_name'])
            album_end.append(song['album_name'])
    ans = [i for i in album_start if i in album_end]
    if start == '':
        if len(album_end) == 0:
            print('无')
        else:
            print(album_end)
    elif end == '':
        if len(album_start) == 0:
            print('无')
        else:
            print(album_start)
    else:
        if len(ans) == 0:
            print('无')
        else:
            print(ans)
    return ans


# 交互
def homepage():
    print('0. Exit\n'
          '1. 查询所有歌曲、专辑、歌手\n'
          '2. 查询时间区间内的发行的专辑\n'
          '3. 查询歌曲在什么专辑里\n'
          '4. 查询专辑有哪些歌曲\n'
          '5. 查询歌手有哪些专辑\n')
    op = int(input())
    if op == 0:
        return 0
    elif op == 1:
        func1()
    elif op == 2:
        func2()
    elif op == 3:
        print('请输入需要查询的歌曲：')
        q_song = input()
        q_albums = get_album_name_by_song(q_song)
        print(q_albums)
    elif op == 4:
        print('请输入需要查询的专辑：')
        q_album = input()
        q_songs = get_album_include(q_album)
        print(q_songs)
    elif op == 5:
        print('请输入需要查询的歌手：')
        q_singer = input()
        q_albums = get_album_releasedBy(q_singer)
        print(q_albums)
    else:
        print('请重新输入')  # 本来想写一个异常抛出

    return 1


if __name__ == '__main__':
    # 连接Neo4j
    # @Hakii
    uri = "bolt://localhost:7687"  # 127.0.0.1:7687.
    driver = GraphDatabase.driver(uri, auth=("neo4j", "040811"))

    get_all()  # 获取全部信息
    while homepage():
        pass
