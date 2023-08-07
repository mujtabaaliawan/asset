DOCUMENT_TITLE = "div.document-title h1::text"
DOCUMENT_TITLE_DETAIL = "div.document-title p::text"
TOTAL_PROPERTIES = "div.total-property::text"

'''MAIN PAGE SELECTORS'''
MAIN_CONTENT = "div.content"
PROPERTIES_CONTENT = "article.property-row"
IMAGE_URL = "a.property-row-image img::attr(src)"
PROPERTY_BADGE_STATUS = "span.property-badge::text"
PROPERTY_DATA = "div.property-row-main"
NAME = "h2.property-row-title a::text"
FURTHER_DETAIL_LINK = "h2.property-row-title a::attr(href)"
LOCATION = "div.property-row-location a::text"
NEXT_PAGE = "a.next::attr(href)"

'''DETAIL PAGE SELECTORS'''

OVERVIEW_DETAILS = "div.property-overview dt::text, dd::text"
IMAGES_URLS = "div.property-gallery a::attr(href)"
FACILITIES = "div.property-amenities li::text"
DETAIL_CONTENT = "div.entry-content"
DETAIL_TEXT = "*::text"
