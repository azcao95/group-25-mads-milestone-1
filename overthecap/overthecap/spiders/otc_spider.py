from datetime import datetime, date, time
import scrapy
import re

class OverthecapSpider(scrapy.Spider):
    name = "overthecap"
    allowed_domains = ["overthecap.com"]
    start_urls = [
        "https://overthecap.com/contracts",
    ]

    def parse(self, response):
        # Extract the current date and time
        current_datetime = datetime.now()
        print(f"Current date and time: {current_datetime}")

        return scrapy.Request(self.start_urls[0], callback=self.parse_contracts)

    def parse_contracts(self, response):
        contract_table = response.xpath('//div[@class="contracts-container"]//table')

        rows = contract_table.xpath('.//tr')
        # Extract column names from the table header
        header = contract_table.xpath('.//thead//tr[1]//th')
        column_names = [th.xpath('string()').get().strip() for th in header]

        for row in rows:
            # Skip the header row
            if row.xpath('.//th'):
                continue
            cells = row.xpath('.//td')
            cell_values = [cell.xpath('string()').get().strip().replace('$', '').replace(',', '') for cell in cells]
            # print(cell_values)
            yield dict(zip(column_names, cell_values))