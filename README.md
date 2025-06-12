# group-25-mads-milestone-1

This repo contains a scraper that needs to be run to produce the csv that the notebook needs to function.

## To run scraper

First, make sure scrapy is installed. If it isn't, you can run

```
pip install scrapy
```

cd into `overthecap` then run the following command:

`scrapy crawl overthecap -O overthecap-earnings.csv`

This process may take ~45 minutes. There are over 2500 active contracts, which means over 2500 pages the scraper has to visit!

Scrapy should create the file `overthecap-earnings.csv` in the `overthecap` folder

Now you're ready to run the notebook!