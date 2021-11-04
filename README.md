# search-engine

I developed a vertical search engine similar to Google Scholar that only retrieves papers/books published by a member of Coventry University. In which one of the co-authors must at least be from CU. To that end, I crawled Google Scholar profiles of academic staff at CU and index their papers in their profiles. The seed page for the crawler was the first  Google Scholar page for Coventry University. 


I crawled 5 pages from the Coventry University Scholar profile page and each page had 10 staff profiles. So, approximately I crawled 50 staff google scholar profile. I also retrieved the “authors”, “title of the articles/papers”, “the URL of the articles/papers” and the unique “id” from the articles which was used to for the Elasticsearch indexing.

Elasticsearch and Elasticsearch DSL were implemented.
