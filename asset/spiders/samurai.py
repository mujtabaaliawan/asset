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
            {'field_name': 'price_in_euro', 'index': 0},
            {'field_name': 'number_of_bedrooms', 'index': 1},
            {'field_name': 'size', 'index': 2},
            {'field_name': 'availability_date', 'index': 3},
        ]

        page_property_data = response.css(selectors.MAIN_CONTENT)

        for rental in page_property_data.css(selectors.PROPERTIES_CONTENT):

            name = rental.css(selectors.NAME).get()
            location = rental.css(selectors.LOCATION).getall()
            meta_data = rental.css(selectors.META_DATA_PRICE_BEDROOM_SIZE_DATE).getall()
            badge_status = rental.css(selectors.PROPERTY_BADGE_STATUS).get()
            rental_detail_link = rental.css(selectors.FURTHER_DETAIL_LINK).get()

            product = ItemLoader(item=AssetItem())
            product.add_value('title', name)
            product.add_value('badge_status', badge_status)

            for location_index_map in location_to_index_mapping:
                product.add_value(location_index_map['field_name'], location[location_index_map['index']])

            for meta_data_index_map in meta_data_to_index_mapping:
                product.add_value(meta_data_index_map['field_name'], meta_data[meta_data_index_map['index']])

            yield scrapy.Request(rental_detail_link, callback=self.detail_parse, meta={"product": product,
                                                                                       "badge_status": badge_status})

        next_page_link = response.css(selectors.NEXT_PAGE).get()
        if next_page_link is not None:
            yield scrapy.Request(next_page_link, callback=self.parse)

    @staticmethod
    def detail_parse(response):
        product = response.meta["product"]
        badge_status = response.meta["badge_status"]

        overview_to_index_mapping = [
            {'field_name': 'number_of_bathrooms', 'index': 3},
            {'field_name': 'furnished_status', 'index': 4},
            {'field_name': 'type', 'index': 5},
            {'field_name': 'id', 'index': 7},
        ]

        overview = response.css(selectors.OVERVIEW_DETAILS).getall()
        images_urls_list = response.css(selectors.IMAGES_URLS).getall()
        facilities_list = response.css(selectors.FACILITIES).getall()

        detail_content = response.css(selectors.DETAIL_CONTENT)
        details_list = detail_content.css(selectors.DETAIL).getall()

        if badge_status is not None:
            overview_to_index_mapping[3]['index'] = 8

        for image in images_urls_list:
            product.add_value('images_urls_list', image)

        for paragraph in details_list:
            if paragraph == "Locatie : ":
                break
            product.add_value('details_list', paragraph)

        for facility in facilities_list:
            product.add_value('facilities_list', facility)

        for overview_index_map in overview_to_index_mapping:
            product.add_value(overview_index_map['field_name'], overview[overview_index_map['index']])

        yield product.load_item()

