import scrapy
import re


class Jvcspider(scrapy.Spider):
    name = 'jvc_cz'
    start_urls = ['https://www.jvcaudio.cz/']

    def parse(self, response, **kwargs):
        products_list = response.css('.product-box a::attr(href)').getall()
        yield from response.follow_all(products_list, callback=self.extract_products_fields)

    def extract_products_fields(self, response):

        model = response.css('.page-title::text').get()
        model = re.findall(r'[A-Z]{2}-\w{4,5}', model)
        model = ''.join(model)

        lang = response.url
        lang = re.findall(r'o.([a-z]{2})', lang)
        lang = ''.join(lang)

        brand = response.css('.sr-only::text').get()
        brand = re.findall(r'JVC', brand)

        product = response.css('.page-title::text').get()
        product = re.findall(r'^\w+', product)
        product = ''.join(product)

        type = response.xpath('//ul[@class="download-list"]/li/a/i/following-sibling::text()').get()
        type = re.findall(r'(.+)\sCZ', type)
        type = ''.join(type)

        yield {
            'model': model,
            'model_2': '',
            'parent_product': '',
            'brand': brand[0],
            'product': product.strip(),
            'thumb': response.css('.product-gallery-main img::attr(src)').get(),
            'product_lang': lang,
            'type': type.strip(),
            'url': response.url
        }


class Jvcspiderhu(Jvcspider):
    name = 'jvc_hu'
    start_urls = ['https://www.jvcaudio.hu/']


class Jvcspiderpl(Jvcspider):
    name = 'jvc_pl'
    start_urls = ['https://jvcaudio.pl/']
