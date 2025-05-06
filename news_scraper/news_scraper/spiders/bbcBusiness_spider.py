import scrapy

class BbcBusinessSpider(scrapy.Spider):
    name = 'bbc_business'
    start_urls = ['https://www.bbc.com/news/business']

    def parse(self, response):
        # Extract all article links on the business page
        articles = response.css('a[data-testid="internal-link"]')

        for article in articles:
            title = article.css('h2[data-testid="card-headline"]::text').get()
            description = article.css('p[data-testid="card-description"]::text').get()
            url = article.attrib.get('href')

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
