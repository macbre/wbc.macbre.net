index:
	zcat ../wbc/106644.xml.gz | docker-compose exec -T sphinx indexer -c /opt/sphinx/conf/sphinx.conf --rotate wbc
	# zcat kronika_gazeta_wielkiego_ksiestwa.xml.gz | docker-compose run sphinx indexer -c /opt/sphinx/conf/sphinx.conf --rotate wbc

stopwords:
	zcat ../wbc/106644.xml.gz | docker-compose run sphinx indexer wbc -c /opt/sphinx.conf --buildfreqs --buildstops /dev/stdout 250000 > stopwords.txt
	cat stopwords.txt | docker-compose run app stopwords

sitemap:
	docker-compose run app sitemap
	curl 'http://google.com/ping?sitemap=http://wbc.macbre.net/sitemap.xml' -svo /dev/null

start:
	GIT_HASH=`git rev-parse HEAD` \
	HOST=`hostname` \
	docker-compose up -d

stop:
	docker-compose stop

console:
	mysql -h127.0.0.1 -P 36307 --default-character-set=utf8

search:
	# @see http://sphinxsearch.com/docs/current.html#extended-syntax
	mysql -h127.0.0.1 -P 36307 --default-character-set=utf8 -e "select id, SNIPPET(title, '$(q)', 'limit=75') as name, chapter, SNIPPET(content, '$(q)', 'limit=500') as snippet, published_year, publication_id, document_id  from wbc where match('$(q)') order by published_year ASC limit 150" --vertical | less
