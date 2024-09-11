
# Steam Marketplace Scraper 🤖

Scraper to Fetch data points from https://steamcommunity.com/market (Steam Community Marketplace), store that into `mysql` database, & generate data report in `excel` format.





## Environment Variables 🚩

.env file contains the most sensitive information. It contains the `Database` credentials

`DB_HOST`

`DB_NAME`

`DB_USERNAME`

`DB_PASSWORD`


## Requirements⚡

To Install script dependencies, run the following command:

```python
  pip install -r requirements.txt
```



## Database Setup 📅

Import schema on mysql using GUI tools like workbench, dbeaver, xampp. or run following command on CLI

```bash
  mysql -p -u [user] [database] < DB/schema.sql
```
    
## Scraper Execution 🚀

To execute scraper run

```python
  python main.py
```
following data points get dump into database
| Column        | Type      | Description                |
| :--------     | :-------  | :------------------------- |
| `id`          | `int`     | Auto Increment (**PK**) |
| `game`        | `varchar` | Game Name (UN) |
| `item`        | `varchar` | Item Name (UN) |
| `type`        | `varchar` | Item Type |
| `listings`    | `varchar` | Total Listings |
| `price`       | `varchar` | Sell Price |
| `description` | `text`    | Item Description |
| `icon`        | `text`    | Icon URL |
| `url`         | `text`    | Product URL |
| `inserted_at` | `datetime`| Default: Current timestamp |
| `updated_at`  | `datetime`| Update timestamp |

**NOTE:** there is an composite key on `game` & `item` to avoid duplicate entries.

## Report Generator 📄

To generate report, run the following command

```python
  python reports.py
```


## Techologies Used 💻

**Language:** Python

**Libraries Use:** scrapy, pandas, rotating-proxies

**Database:** MYSQL

## Author👦

- [@Mhassanniazi](https://github.com/Mhassanniazi)

