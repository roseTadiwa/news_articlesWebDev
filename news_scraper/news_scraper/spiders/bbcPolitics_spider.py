import scrapy

class BbcPoliticsSpider(scrapy.Spider):
    name = 'bbc_politics'
    start_urls = ['https://www.bbc.com/news/politics']

    def parse(self, response):
        articles = response.css('a[data-testid="internal-link"]')

        for article in articles:
            title = article.css('h2[data-testid="card-headline"]::text').get()
            description = article.css('p[data-testid="card-description"]::text').get()
            url = article.attrib.get('href')

            if url:
                url = response.urljoin(url)

            if title and description:
                yield {
                    'title': title.strip(),
                    'description': description.strip(),
                    'url': url,
                    'category': 'Politics'
                }
