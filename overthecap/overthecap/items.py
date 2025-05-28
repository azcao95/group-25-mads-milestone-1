# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class OverthecapItem(scrapy.Item):
    # Define all the fields we expect in the contract data
    player = scrapy.Field()
    position = scrapy.Field()
    team = scrapy.Field()
    total_value = scrapy.Field()
    apy = scrapy.Field()  # Average Per Year
    total_guaranteed = scrapy.Field()
    fully_guaranteed = scrapy.Field()
    free_agency = scrapy.Field()
    avg_guaranteed_per_year = scrapy.Field()
    percent_guaranteed = scrapy.Field()
    age = scrapy.Field()
    scrape_date = scrapy.Field()
