BestDeal Project
=======================

Easily compare your most wanted products among your favorite vendors to buy cheapest.

Currently it implements a comparator of NVidia graphic cards among multiple hardware vendors.

<img src='https://github.com/RichardDally/BestDeal/blob/master/screenshots/GTX2080_20181202.png' style='width:334px; height:306px; float: right;'>

BestDeal provides you a visualization tool to anticipate best timing to buy.

Requirements
-------------

[Python 3.6+](https://www.python.org/downloads/)

[External modules (requirements)](requirements.txt)

[How to install requirements with pip ?](https://stackoverflow.com/a/39537053/5037799)

Usage
-------------
1. Run nvidia_fetcher.py to feed price database (powered by [MongoDB](https://docs.mongodb.com)).
2. Run frontend.py to run a local web server displaying prices graph.
3. Analyze and profit !

Backend
-------------
Backend is composed of two main modules : deals scrappers and price database.

[Deals scrappers](https://github.com/RichardDally/BestDeal/blob/master/dealscrappers.py) will navigate on vendors page (e.g. Amazon) and scraps product name, type and price to store it in [price database](https://github.com/RichardDally/BestDeal/blob/master/pricedatabase.py) !

MongoDB basics
-------------

List all databases:

    > show dbs


Switch to `PriceHistorization` database:

    > use PriceHistorization

Show some statistics:

    > db.stats()

Display every documents:

    > db.NVidiaGPU.find()

Filtering on timestamp:

    > db.NVidiaGPU.find({"product_brand": "GIGABYTE", "timestamp": /20191130_181011/})


Frontend
-------------
[Frontend](https://github.com/RichardDally/BestDeal/blob/master/frontend.py) uses [Dash](https://plot.ly/products/dash/) to display beautiful and customizable graphs.
