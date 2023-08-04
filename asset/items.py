import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Join


def clean_text(value):
    return value.strip().replace('\n', '').replace('\xa0', ' ')


def extract_price(value):
    return value.replace('€', '').replace(',', '').strip()


class AssetItem(scrapy.Item):

    title = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst()
    )
    images_urls_list = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=Join(separator=',')
    )
    city = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst()
    )
    district = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst()
    )
    local_area = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst()
    )
    details_list = scrapy.Field(
        input_processor=MapCompose(clean_text),
        output_processor=Join()
    )
    facilities_list = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=Join(separator=',')
    )
    price_in_euro = scrapy.Field(
        input_processor=MapCompose(extract_price),
        output_processor=TakeFirst()
    )
    number_of_bedrooms = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst()
    )
    number_of_bathrooms = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst()
    )
    furnished_status = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst()
    )
    type = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst()
    )
    id = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst()
    )
    size = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst()
    )
    availability_date = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst()
    )
    badge_status = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst()
    )

