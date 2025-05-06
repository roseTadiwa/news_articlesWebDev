import scrapy

class DailyNewsSportSpider(scrapy.Spider):
    name = 'dailynews_sport'
    start_urls = ['https://dailynews.co.zw/sport/']

    def parse(self, response):
        # Extracting article URLs, titles, and descriptions
        articles = response.css('article')  # Use article tags to find each article
        for article in articles:
            title = article.css('h3.post-title.entry-title a::text').get()
            url = article.css('h3.post-title.entry-title a::attr(href)').get()
            description = article.css('div.post-excerpt p::text').get()

            # Storing the extracted data
            yield {
                'title': title,
                'url': url,
                'description': description,
                'category': 'Sport'
            }

        # Follow pagination links if available (for next pages)
        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
