import scrapy

class ZimIndependentSportsSpider(scrapy.Spider):
    name = 'zim_independent_sports'
    start_urls = ['https://www.theindependent.co.zw/category/84/sport']

    def parse(self, response):
        articles = response.css('div.card-body.pad-o.mt-3')

        for article in articles:
            title = article.css('div.sub-title.mt-3::text').get()
            description = article.css('div.top-article::text').get()
            url = article.css('a.text-dark::attr(href)').get()

            # Ensure the URL is fully qualified
            if url:
                url = response.urljoin(url)

            if title and description:
                yield {
                    'title': title.strip(),
                    'description': description.strip(),
                    'url': url,
                    'category': 'Sports'  # Indicate the article category
                }

        # Follow pagination if available
        next_page = response.css('a.page-link::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
