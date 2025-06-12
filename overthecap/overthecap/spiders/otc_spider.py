import scrapy
import re


class OverthecapSpider(scrapy.Spider):
    name = "overthecap"
    allowed_domains = ["overthecap.com"]
    start_urls = [
        "https://overthecap.com/career-earnings/quarterback",
        "https://overthecap.com/career-earnings/running-back",
        "https://overthecap.com/career-earnings/wide-receiver",
        "https://overthecap.com/career-earnings/tight-end",
        "https://overthecap.com/career-earnings/left-tackle",
        "https://overthecap.com/career-earnings/left-guard",
        "https://overthecap.com/career-earnings/center",
        "https://overthecap.com/career-earnings/right-guard",
        "https://overthecap.com/career-earnings/right-tackle",
        "https://overthecap.com/career-earnings/interior-defensive-line",
        "https://overthecap.com/career-earnings/edge-rusher",
        "https://overthecap.com/career-earnings/linebacker",
        "https://overthecap.com/career-earnings/cornerback",
        "https://overthecap.com/career-earnings/safety",
        "https://overthecap.com/career-earnings/kicker",
        "https://overthecap.com/career-earnings/punter",
        "https://overthecap.com/career-earnings/long-snapper",
    ]

    def parse(self, response):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse_contracts)

    def parse_contract_details(self, response):
        print(
            f"Parsing contract details for {response.meta.get('player_name', 'Unknown')}")

        pay_table = response.xpath(
            '//div[@class="contract-container"]//table[@class="contract salary-cap-history player-new"]')
        if not pay_table:
            print("No pay table found in the response.")
            return

        headers = pay_table.xpath('.//tr[1]/th').getall()
        if not headers:
            print("No headers found in the pay table.")
            return

        # XPath to select <tr> elements where a <td> has text exactly '2024'
        target_row = pay_table.xpath(
            './/tr[td[normalize-space(text())="2024"]]')
        if not target_row:
            print("No target row found for the year 2024.")
            return

        target_row_cells = target_row.xpath('.//td').getall()
        if not target_row_cells:
            print("No cells found in the target row.")
            return

        result = {}

        for header, cell in zip(headers, target_row_cells):
            header_text = re.sub(
                '<[^<]+?>',
                '',
                header).strip().lower().replace(
                ' ',
                '_').replace(
                '%',
                'percent')
            cell_text = re.sub(
                '<[^<]+?>',
                '',
                cell).strip().replace(
                '$',
                '').replace(
                ',',
                '')
            result[header_text] = cell_text

        yield {
            'player_name': response.meta.get('player_name', 'Unknown'),
            **result
        }

    def parse_active_2024(self, years_active_string):
        # Extract the years active from the string
        if not years_active_string:
            return None

        # Replace em dash with regular hyphen and split
        years_active_arr = years_active_string.replace('‑', '-').split('-')
        print("ARRAY:", years_active_arr)

        if len(years_active_arr) == 1:
            year_active_since = int(years_active_arr[0].strip())
            if year_active_since <= 2024:
                return True
            else:
                return False
        elif len(years_active_arr) == 2:
            start_year = int(years_active_arr[0].strip())
            # Handle empty end_year (ongoing career)
            end_year = int(years_active_arr[1].strip(
            )) if years_active_arr[1].strip() else 2024
            if start_year <= 2024 and end_year >= 2024:
                return True
            else:
                return False
        else:
            print(f"Unexpected format for years active: {years_active_string}")
            return None

    def parse_contracts(self, response):
        earnings_table = response.xpath(
            '//table[@class="career-earnings-position position-table sortable"]')
        if not earnings_table:
            print("No earnings table found in the response.")
            return
        # Extract column names from the table header

        rows = earnings_table.xpath('.//tbody/tr')
        if not rows:
            print("No rows found in the earnings table.")
            return

        for row in rows:
            # Skip the header row
            if row.xpath('.//th'):
                continue

            link = row.xpath('.//td[1]//a/@href').get()
            if link:
                # Construct the full URL for the contract details
                full_url = response.urljoin(link) + '#contract-history'
                player_name = row.xpath(
                    './/td[1]//a/text()').get().strip().replace(',', '')

                if not player_name:
                    print("Player name not found in the row.")
                    continue

                years_active_string = row.xpath('.//td[2]/text()').get()
                if not years_active_string:
                    print(f"No years active found for player: {player_name}")
                    continue

                is_active_2024 = self.parse_active_2024(years_active_string)

                if is_active_2024:
                    yield scrapy.Request(full_url, callback=self.parse_contract_details, meta={'player_name': player_name})
                else:
                    print(
                        f"Player {player_name} is not active in 2024, skipping contract details.")
                    continue
            else:
                continue
