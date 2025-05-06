import scrapy

class ZimIndependentBusinessSpider(scrapy.Spider):
    name = 'zim_independent_business'
    start_urls = ['https://www.theindependent.co.zw/category/83/business-digest']

    def parse(self, response):
        # Extract all article links in the business digest
        articles = response.css('div.card-body')

        for article in articles:
            title = article.css('div.sub-title::text').get()
            description = article.css('div.top-article::text').get()
            url = article.css('a::attr(href)').get()

            # Ensure the URL is fully qualified
            if url:
                url = response.urljoin(url)

            # Only yield if title and description are available
            if title and description:
                yield {
                    'title': title.strip(),
                    'description': description.strip(),
                    'url': url,
                    'category': 'Business'  # Add a category field for identification
                }

        # Follow pagination links if available (if there are multiple pages)
        next_page = response.css('a.page-link::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
