import scrapy
from itemloaders.processors import TakeFirst, MapCompose


def clean_text(value):
    return value.strip().replace('\n', '').replace('\t', '')


def extract_price(value):
    return value.replace('€', '').replace(',', '').strip()


class AssetItem(scrapy.Item):

    title = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst()
    )
    main_image_url = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst()
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
    description = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst()
    )
    price_in_pounds = scrapy.Field(
        input_processor=MapCompose(extract_price),
        output_processor=TakeFirst()
    )
    number_of_bedrooms = scrapy.Field(
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

