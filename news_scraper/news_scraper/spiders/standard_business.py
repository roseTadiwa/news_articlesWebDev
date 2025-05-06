import scrapy

class TheStandardBusinessSpider(scrapy.Spider):
    name = 'thestandard_business'
    start_urls = ['https://www.thestandard.co.zw/category/18/business']

    def parse(self, response):
        articles = response.css('div.card.border-0.mb-3')

        for article in articles:
            title = article.css('div.sub-title.mt-3::text').get()
            description = article.css('div.top-article::text').get()
            url = article.css('a.text-dark::attr(href)').get()

            if title and description and url:
                yield {
                    'title': title.strip(),
                    'description': description.strip(),
                    'url': response.urljoin(url),
                    'category': 'Business'
                }

        # Pagination (if any)
        next_page = response.css('li.page-item a.page-link::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
