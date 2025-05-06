import scrapy

class DailyNewsBusinessSpider(scrapy.Spider):
    name = 'dailynews_business'
    allowed_domains = ['dailynews.co.zw']
    start_urls = ['https://dailynews.co.zw/business/']

    def parse(self, response):
        # Each article block is under a <h3 class="post-title entry-title">
        articles = response.css('h3.post-title.entry-title')

        for article in articles:
            # Extract title and URL from <a> tag inside <h3>
            a_tag = article.css('a')
            title = a_tag.css('::text').get()
            url = a_tag.css('::attr(href)').get()
            
            # Navigate to the full article page to extract the description
            if url:
                yield response.follow(url, callback=self.parse_article, meta={
                    'title': title.strip() if title else '',
                    'url': response.urljoin(url)
                })

    def parse_article(self, response):
        # Extract the description from the article content
        # First paragraph is typically in <div class="post-excerpt"><p>...</p>
        description = response.css('div.post-excerpt > p::text').get()

        # Fall back: try to grab first <p> from content if not in excerpt
        if not description:
            description = response.css('div.entry-content p::text').get()

        yield {
            'title': response.meta['title'],
            'url': response.meta['url'],
            'description': description.strip() if description else '',
            'category': 'Business'
        }
