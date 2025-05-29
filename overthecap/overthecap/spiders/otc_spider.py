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
    
    def parse_contract_details(self, response):
        print("Parsing contract details...")

        pay_table = response.xpath('//div[@class="contract-container"]//table')
        if not pay_table:
            print("No pay table found in the response.")
            return
        
        headers = pay_table.xpath('.//tr[1]/th/text()').getall()
        if not headers:
            print("No headers found in the pay table.")
            return

        # XPath to select <tr> elements where a <td> has text exactly '2024'
        target_row = pay_table.xpath('.//tr[td[normalize-space(text())="2024"]]')
        if not target_row:
            print("No target row found for the year 2024.")
            return

        target_row_cells = target_row.xpath('.//td/text()').getall()
        if not target_row_cells:
            print("No cells found in the target row.")
            return
        
        result = {}
        for header, cell in zip(headers, target_row_cells):
            header = header.strip()
            cell = cell.strip()
            if header and cell:
                result[header] = cell
        print("Parsed result:", result)

        yield {
            'player_name': response.meta.get('player_name', 'Unknown'),
            **result
        }

    def parse_contracts(self, response):
        contract_table = response.xpath('//div[@class="contracts-container"]//table')
        headers = ['team', 'base_salary', 'guaranteed_salary', 'cap_number', 'cap_percent', 'cash_paid']

        rows = contract_table.xpath('.//tr')
        # Extract column names from the table header

        for row in rows[1:10]:
            # Skip the header row
            if row.xpath('.//th'):
                continue

            link = row.xpath('.//td[1]//a/@href').get()
            if link:
                # Construct the full URL for the contract details
                full_url = response.urljoin(link)
                player_name = row.xpath('.//td[1]//a/text()').get().strip()
                print("Player Name: ", player_name)
                if not player_name:
                    print("Player name not found in the row.")
                    continue
                yield scrapy.Request(full_url, callback=self.parse_contract_details, meta={'player_name': player_name})

            else:
                continue
