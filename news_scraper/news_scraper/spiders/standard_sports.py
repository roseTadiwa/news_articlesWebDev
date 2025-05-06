import scrapy


class TheStandardSportSpider(scrapy.Spider):
    name = 'thestandard_sport'
    start_urls = ['https://www.thestandard.co.zw/category/19/sports']

    def parse(self, response):
        articles = response.css('div.card.border-0.mb-3')

        for article in articles:
            # Extract title and URL
            a_tag = article.css('a.text-dark::attr(href)').get()
            title = article.css('div.sub-title::text').get()

            # Extract description
            description = article.css('div.mb-3.pt-2.top-article::text').get()

            if a_tag and title and description:
                yield {
                    'title': title.strip(),
                    'description': description.strip(),
                    'url': response.urljoin(a_tag.strip()),
                    'category': 'Sport'
                }
