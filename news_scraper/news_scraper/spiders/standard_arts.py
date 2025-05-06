import scrapy

class NewsDayArtsSpider(scrapy.Spider):
    name = 'standard_arts'
    start_urls = ['https://www.newsday.co.zw/category/8/lifestyle-and-arts']

    def parse(self, response):
        articles = response.css('div.card.border-0.mb-3')

        for article in articles:
            title = article.css('div.sub-title::text').get()
            description = article.css('div.top-article::text').get()
            url = article.css('a.text-dark::attr(href)').get()

            if url:
                url = response.urljoin(url)

            if title and description:
                yield {
                    'title': title.strip(),
                    'description': description.strip(),
                    'url': url,
                    'category': 'Arts'
                }
