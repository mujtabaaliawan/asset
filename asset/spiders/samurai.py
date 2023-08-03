import scrapy
from itemloaders import ItemLoader
from asset.items import AssetItem
from asset.urls import urls
from asset.selectors import selectors


class AssetSpider(scrapy.Spider):
    name = "samurai"
    start_urls = [urls.ASSET_URL]

    def parse(self, response, **kwargs):

        location_to_index_mapping = [
            {'field_name': 'city', 'index': 0},
            {'field_name': 'district', 'index': 1},
            {'field_name': 'local_area', 'index': 2},
        ]

        meta_data_to_index_mapping = [
            {'field_name': 'price_in_pounds', 'index': 0},
            {'field_name': 'number_of_bedrooms', 'index': 1},
            {'field_name': 'size', 'index': 2},
            {'field_name': 'availability_date', 'index': 3},
        ]

        page_property_data = response.css(selectors.MAIN_CONTENT)

        for rental in page_property_data.css(selectors.PROPERTIES_CONTENT):

            name = rental.css(selectors.NAME).get()
            image_url = rental.css(selectors.IMAGE_URL).get()
            location = rental.css(selectors.LOCATION).getall()
            description = rental.css(selectors.DESCRIPTION).get()
            meta_data = rental.css(selectors.META_DATA_PRICE_BEDROOM_SIZE_DATE).getall()
            badge_status = rental.css(selectors.PROPERTY_BADGE_STATUS).get()

            product = ItemLoader(item=AssetItem())
            product.add_value('title', name)
            product.add_value('image_url', image_url)
            product.add_value('badge_status', badge_status)
            product.add_value('description', description)

            for location_index_map in location_to_index_mapping:
                product.add_value(location_index_map['field_name'], location[location_index_map['index']])

            for meta_data_index_map in meta_data_to_index_mapping:
                product.add_value(meta_data_index_map['field_name'], meta_data[meta_data_index_map['index']])

            yield product.load_item()

        next_page_link = response.css(selectors.NEXT_PAGE).get()
        if next_page_link is not None:
            yield scrapy.Request(next_page_link, callback=self.parse)

