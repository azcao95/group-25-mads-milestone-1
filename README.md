# group-25-mads-milestone-1

This repo contains a scraper that needs to be run to produce the csv that the notebook needs to function.

# Scraper setup + notebook setup

This scraper will go into overthecap.com's career earnings page for each position. In each page, there is a table that lists all players who have played that position. The scraper then checks the table if they have played during 2024. If they have, then it navigates to the player's contract history page and extracts their pay data from 2024. After doing all that, it outputs the results into a csv.

First, make sure scrapy is installed. If it isn't, you can run the following to get all packages necessary to run the scraper and the notebook

```
pip install -r requirements.txt
```

cd into `overthecap` then run the following command:

`scrapy crawl overthecap - O overthecap - earnings.csv`

This process may take around an hour to complete. There are over 2500 active contracts, which means over 2500 pages the scraper has to visit and parse!

If for whatever reason, you need another copy of the csv but don't want to run the scraper, you can find the csv here at this link and paste it in the `overthecap` directory:

```
https://drive.google.com/file/d/1DNqsFW24Ylb0oVDyJtyrqA8ICl5PgviN/view?usp=sharing
```

Scrapy should create the file `overthecap - earnings.csv` in the `overthecap` folder.

Now you're ready to run the notebook!
