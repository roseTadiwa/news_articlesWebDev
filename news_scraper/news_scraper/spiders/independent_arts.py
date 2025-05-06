import scrapy

class ZimIndependentArtsSpider(scrapy.Spider):
    name = 'zim_independent_arts'
    start_urls = ['https://www.theindependent.co.zw/category/66885/lifestyle-and-arts']

    def parse(self, response):
        # Select each article block
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
                    'category': 'Arts'
                }

        # Optional: handle pagination if available
        next_page = response.css('li.page-item a.page-link::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
