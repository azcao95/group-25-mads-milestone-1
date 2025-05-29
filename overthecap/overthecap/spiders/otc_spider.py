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
        return scrapy.Request(self.start_urls[0], callback=self.parse_contracts)
    
    def parse_contract_details(self, response):
        pay_table = response.xpath('//div[@class="contract-container"]//table[@class="contract salary-cap-history player-new"]')
        if not pay_table:
            print("No pay table found in the response.")
            return
        
        headers = pay_table.xpath('.//tr[1]/th').getall()
        if not headers:
            print("No headers found in the pay table.")
            return

        # XPath to select <tr> elements where a <td> has text exactly '2024'
        target_row = pay_table.xpath('.//tr[td[normalize-space(text())="2024"]]')
        if not target_row:
            print("No target row found for the year 2024.")
            return

        target_row_cells = target_row.xpath('.//td').getall()
        if not target_row_cells:
            print("No cells found in the target row.")
            return
        
        result = {}

        for header, cell in zip(headers, target_row_cells):
            header_text = re.sub('<[^<]+?>', '', header).strip().lower().replace(' ', '_').replace('%', 'percent')
            cell_text = re.sub('<[^<]+?>', '', cell).strip().replace('$', '').replace(',', '')
            result[header_text] = cell_text

        yield {
            'player_name': response.meta.get('player_name', 'Unknown'),
            **result
        }

    def parse_contracts(self, response):
        contract_table = response.xpath('//div[@class="contracts-container"]//table')
        rows = contract_table.xpath('.//tr')
        # Extract column names from the table header

        for row in rows:
            # Skip the header row
            if row.xpath('.//th'):
                continue

            link = row.xpath('.//td[1]//a/@href').get()
            if link:
                # Construct the full URL for the contract details
                full_url = response.urljoin(link)+'#contract-history'
                player_name = row.xpath('.//td[1]//a/text()').get().strip()
                if not player_name:
                    print("Player name not found in the row.")
                    continue
                yield scrapy.Request(full_url, callback=self.parse_contract_details, meta={'player_name': player_name})

            else:
                continue
