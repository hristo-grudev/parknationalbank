import scrapy

from scrapy.loader import ItemLoader

from ..items import ParknationalbankItem
from itemloaders.processors import TakeFirst


class ParknationalbankSpider(scrapy.Spider):
	name = 'parknationalbank'
	start_urls = ['https://parknationalbank.com/about/news/']

	def parse(self, response):
		post_links = response.xpath('//div[@class="columns"]')
		for post in post_links:
			url = post.xpath('.//a[@class="more"]/@href').get()
			date = post.xpath('.//time/text()').get()
			yield response.follow(url, self.parse_post, cb_kwargs={'date': date})

	def parse_post(self, response, date):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//article[@class="main_content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()

		item = ItemLoader(item=ParknationalbankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
