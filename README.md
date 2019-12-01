BestDeal Project
=======================

Easily compare your most wanted products among your favorite vendors to buy cheapest.

Currently it implements a comparator of NVidia graphic cards among multiple french hardware vendors.

<img src='https://github.com/RichardDally/BestDeal/blob/master/screenshots/GTX2080_20181202.png' style='width:334px; height:306px; float: right;'>

BestDeal provides you a visualization tool to anticipate best timing to buy.


Continuous quality integration
-------------

[![Build Status](https://travis-ci.org/RichardDally/BestDeal.svg?branch=master)](https://travis-ci.org/RichardDally/BestDeal)

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/09178071e8a8453fa2acc6d47a4937aa)](https://www.codacy.com/manual/RichardDally/BestDeal?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=RichardDally/BestDeal&amp;utm_campaign=Badge_Grade)

Requirements
-------------

[Python 3](https://www.python.org/downloads/)

[External modules (requirements)](requirements.txt)

[How to install requirements with pip ?](https://stackoverflow.com/a/39537053/5037799)

Usage
-------------
1. Run bestdeal.py to feed price database.
2. Run frontend.py to run a local web server displaying prices graph.
3. Analyze and profit !

Backend
-------------
Backend is composed of two main modules : deals scrappers and price database.

[Deals scrappers](https://github.com/RichardDally/BestDeal/blob/master/dealscrappers.py) will navigate on vendors page (e.g. Amazon) and scraps product name, type and price to store it in [price database](https://github.com/RichardDally/BestDeal/blob/master/pricedatabase.py) !


Frontend
-------------
[Frontend](https://github.com/RichardDally/BestDeal/blob/master/frontend.py) uses [Dash](https://plot.ly/products/dash/) to display beautiful and customizable graphs.
