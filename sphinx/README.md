## Stats

### 106644.xml.gz

```sql
mysql> show index wbc status;
+-------------------+-----------+
| Variable_name     | Value     |
+-------------------+-----------+
| index_type        | disk      |
| indexed_documents | 6968      |
| indexed_bytes     | 122697908 |
| ram_bytes         | 132069840 |
| disk_bytes        | 194896793 |
+-------------------+-----------+
5 rows in set (0.00 sec)

mysql> desc wbc;
+----------------+--------+
| Field          | Type   |
+----------------+--------+
| id             | bigint |
| title          | field  |
| chapter        | field  |
| content        | field  |
| title          | string |
| chapter        | string |
| content        | string |
| published_year | uint   |
| publication_id | uint   |
| document_id    | uint   |
+----------------+--------+
10 rows in set (0.00 sec)
```

```sql
            id: 6563
          name: Kronika Miasta Poznania 2001 Nr3 ; Rataje i Żegrze
       chapter: Z ROMANEM MISIEM PRZECHADZKA PO STARYM ZEGRZU
       snippet:  ... . Obszar zamyka linia ulic: Inflanckiej, <b>Kurlandzkiej</b> i Bobrzańskiej. - Przed powstaniem ...  osiedli Inflanckiej tu nie byłol.
<b>Kurlandzka</b> nazywała się po wojnie Obodrzycka ...  żegierskie pola.
2 Fragment ul. <b>Kurlandzkiej</b> między obecnymi ulicami Zegrze i ... 
published_year: 2001
publication_id: 106644
   document_id: 168145
```
