import scrapy

class DailyNewsEntertainmentSpider(scrapy.Spider):
    name = 'dailynews_entertainment'
    start_urls = ['https://dailynews.co.zw/entertainment/']

    def parse(self, response):
        articles = response.css('article')
        for article in articles:
            title = article.css('h3.post-title.entry-title a::text').get()
            url = article.css('h3.post-title.entry-title a::attr(href)').get()
            description = article.css('div.post-excerpt p::text').get()

            yield {
                'title': title,
                'url': url,
                'description': description,
                'category': 'Arts/Culture/Celebrities'
            }

        # Handle pagination if present
        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
