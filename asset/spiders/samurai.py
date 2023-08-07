import scrapy
from itemloaders import ItemLoader

from asset.constants import constants
from asset.items import AssetItem
from asset.urls import urls
from asset.selectors import selectors


def check_is_detail_extraction_complete(text):
    return constants.DETAIL_BREAKING_POINT in text


def check_is_cleaned_text_empty(text):
    text.replace('\n', '').replace('\t', '').replace('\xa0', ' ').strip()
    return text.isspace()


def complete_product_detail_list(detail_content, product):
    is_detail_completed = constants.IS_DETAIL_COMPLETED

    for detail in detail_content:
        detail_text = detail.css(selectors.DETAIL_TEXT).getall()
        if is_detail_completed is True:
            break

        for info in detail_text:

            if check_is_detail_extraction_complete(info):
                is_detail_completed = True
                break

            if check_is_cleaned_text_empty(info):
                continue
            product.add_value('details_list', info)


def add_product_overview_details(product, overview_details):
    overview_fields = ['Prijs', 'Available', 'Bedrooms', 'Bathrooms', 'Furnished', 'Type', 'Size', 'ID']
    product_field_map = ['price_in_euro', 'availability_date', 'bedrooms', 'bathrooms', 'furnished_status', 'type',
                         'size', 'id']

    for field in overview_fields:
        if field in overview_details:
            field_index = overview_details.index(field)
            value_index = field_index + 1
            mapping_index = overview_fields.index(field)
            product.add_value(product_field_map[mapping_index], overview_details[value_index])


def add_product_location_fields(product, location):
    location_to_index_mapping = [
        {'field_name': 'city', 'index': 0},
        {'field_name': 'district', 'index': 1},
        {'field_name': 'local_area', 'index': 2},
    ]

    for location_index_map in location_to_index_mapping:
        product.add_value(location_index_map['field_name'], location[location_index_map['index']])


class AssetSpider(scrapy.Spider):
    name = "samurai"
    start_urls = [urls.ASSET_URL]

    def parse(self, response, **kwargs):

        page_property_data = response.css(selectors.MAIN_CONTENT)

        for rental in page_property_data.css(selectors.PROPERTIES_CONTENT):
            product = ItemLoader(item=AssetItem())

            name = rental.css(selectors.NAME).get()
            product.add_value('title', name)

            badge_status = rental.css(selectors.PROPERTY_BADGE_STATUS).get()
            product.add_value('badge_status', badge_status)

            location = rental.css(selectors.LOCATION).getall()
            add_product_location_fields(product, location)

            rental_detail_link = rental.css(selectors.FURTHER_DETAIL_LINK).get()
            yield scrapy.Request(rental_detail_link, callback=self.detail_parse, meta={"product": product})

        next_page_link = response.css(selectors.NEXT_PAGE).get()
        if next_page_link is not None:
            yield scrapy.Request(next_page_link, callback=self.parse)

    @staticmethod
    def detail_parse(response):
        product = response.meta["product"]

        overview_details = response.css(selectors.OVERVIEW_DETAILS).getall()
        add_product_overview_details(product, overview_details)

        detail_content = response.css(selectors.DETAIL_CONTENT)
        complete_product_detail_list(detail_content, product)

        images_urls_list = response.css(selectors.IMAGES_URLS).getall()
        for image in images_urls_list:
            product.add_value('images_urls_list', image)

        facilities_list = response.css(selectors.FACILITIES).getall()
        for facility in facilities_list:
            product.add_value('facilities_list', facility)

        yield product.load_item()
