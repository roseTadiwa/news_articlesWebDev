import scrapy


class BbcSportSpider(scrapy.Spider):
    name = 'bbc_sport'
    start_urls = ['https://www.bbc.com/sport']

    def parse(self, response):
        articles = response.css('a[class*="PromoLink"]')

        for article in articles:
            title = article.css('p[class*="PromoHeadline"] span[aria-hidden="false"]::text').get()
            description = article.xpath('.//following::p[contains(@class,"Paragraph")][1]/text()').get()
            url = article.attrib.get('href')

            if url:
                url = response.urljoin(url)

            if title and description:
                yield {
                    'title': title.strip(),
                    'description': description.strip(),
                    'url': url,
                    'category': 'Sport'
                }
