# KG_Final_Project

## 2022-10-26

@Hakii

共计9张专辑，66首单曲

周杰伦限定珍藏DEMO空间

$\downarrow$

2011最新创作



@outis

共计10张专辑，66首单曲

最伟大的作品

$\downarrow$

跨时代



*约定：*

1. *新建一个专辑*
2. *专辑添加属性released_by、album_name、album_introduction、album_release_date*
3. *新建若干首单曲*
4. *单曲添加属性song_name、include_by*
5. *返回专辑，添加单曲include*
5. 返回歌手周杰伦，添加release专辑

---

## 2022-11-02

@Hakii

1. 测试有没有switch 到main



@yy

1. 通过`rdf2rdf-1.0.1-2.3.1.jar`将`song.owl`文件转为`song.turtle`,再导入`neo4j`

neo4j related version info:

1. `java version 1.8.0`
2. `neo4j version 3.5.35`
3. `neosemantics-3.5.0.4.jar`



## 2022-11-4

@yy

[数据来源]：(https://mojim.com/cnh100951.htm)

[思路]：用`protage`从头建立`owl`，安装`neo4j` 一路到将`owl`转为`turtle`再导入`neo4j`(遇到了诸如版本问题，插件问题、结点显示问题)，手动调整导入`neo4j`的数据结点，完成知识图谱的建立，使用`cypher`进行简单查询，作为展示

[前戏]：

```cypher
match (n) detach delete n //删除数据库
CALL semantics.importRDF('file:///E:/All_University_File/Junior/Knowledge_graph/experiment/KG_Final_Project/song.turtle', 'RDF/XML',{handleVocabUris: "IGNORE"}) //导入数据
```

[查询]:

1. 查询歌手、专辑、歌曲(作为最开始的展示)

   ```cypher
   //@Hakii：约定n、m、o分别表示歌曲、专辑、歌手
   match(n:`歌曲`) return n	// 查询有哪些歌曲
   match(m:`专辑`) return m	// 查询有哪些专辑
   match(o:`歌手`) return o	// 查询有哪些歌手，其实只有Jay
   ```

2. 查询某一年份之前发布的专辑名字

   ```cypher
   match(m:`专辑`)
   where m.album_release_date < '2019-11'	// '2019'也可以
   return m;
   ```

3. 查询含有某个歌曲的专辑名字

   ```cypher
   match (n) --(m:`专辑`)
   where n.song_name = 'Mojito'
   return m;
                   
   //通过`include_by`的关系查
   //@Hakii：已实现 
   match(n:`歌曲`) - [r:include_by] -> (m:`专辑`) 
   where n.song_name='Mojito' 
   return m
                                           
   //通过`include`的关系查
   match(m:`专辑`)-[r:include]->(n:`歌曲`) 
   where n.song_name='Mojito' 
   return m                               
   ```

4. 查询某个专辑包含哪些歌曲

   ```cypher
   match(n:`歌曲`)--(m:`专辑`) 
   where m.album_name='叶惠美' 
   return n
   
   match(n:`歌曲`) - [r:include_by] ->(m:`专辑`) 
   where m.album_name='叶惠美'
   return n 
   
   match(m:`专辑`)-[r:include]->(n:`歌曲`) 
   where m.album_name='叶惠美' 
   return n
   ```

5. 查询某个歌手发行了哪些专辑（反之，类似。由于这里只有一个歌手周杰伦，不做演示）

   ```cypher
   match(m:`专辑`)--(o:`歌手`)
   where o.singer_name='周杰伦'
   return m
   
   match(m:`专辑`)-[r:released_by]->(o:`歌手`)
   where o.singer_name='周杰伦'
   return m
                                      
   match(o:`歌手`)-[r:release]->(m:`专辑`)
   where o.singer_name='周杰伦'
   return m
   ```

6. 

7. 

8. 



## 2022-11-06

@Hakii

解决yy未解决问题

实现python+cypher+neo4j简单Demo







