import scrapy

class TheStandardPoliticsSpider(scrapy.Spider):
    name = 'thestandard_politics'
    start_urls = ['https://www.thestandard.co.zw/category/196/politics']

    def parse(self, response):
        articles = response.css('div.card.border-0.mb-3')

        for article in articles:
            title = article.css('div.sub-title.mt-3::text').get()
            description = article.css('div.top-article p::text').get()
            url = article.css('a.text-dark::attr(href)').get()

            if title and description and url:
                yield {
                    'title': title.strip(),
                    'description': description.strip(),
                    'url': response.urljoin(url),
                    'category': 'Politics'
                }

        # Optional: follow pagination if available
        next_page = response.css('li.page-item a.page-link::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
