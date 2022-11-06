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


if __name__ == '__main__':
    # 连接Neo4j
    # @Hakii
    uri = "bolt://localhost:7687"  # 127.0.0.1:7687.
    driver = GraphDatabase.driver(uri, auth=("neo4j", "040811"))

    get_all()  # 获取全部信息
    get_album_name_by_song('Mojito')
    get_album_include('叶惠美')
    get_album_releasedBy('周杰伦')
