# CS2-Product-Analysis
This project will use steam market data of Counter-Strike 2 skins to predict which skins will sell well and analyze market trends, historical sales data, etc.

## Introduction
I like to refer to Counter-Strike skins as one of the earliest forms of online currency. In August 2013, Counter-Strike released virtual "skins", a pattern that changes the cosmetics of weapons in the game. These skins have real-life monetary value and can be bought and sold on online marketplaces such as the Steam marketplace. Just like cryptocurrency, there is an entire economy based around these virtual items with some items being bought for over $1,000,000. The game currently hosts around 1,000,000 concurrent monthly players leading to millions of dollars worth of transactions every month. It is interesting to note that because these items are virtual and loosely regulated just like cryptocurrencies, the same complications of scamming, market manipulation, and money laundering are present with Counter-Strike skins. The market of skins tends to follow that of cryptocurrencies as many users choose crypto as the method of purchasing skins.

## Research Questions
At the end of my data analysis, I hope to answer the following questions as well as others along the way:

Which products(skins) will be easy to sell in the future?

What are some external factors that affect the price of skins?

What are some of the most popular and sought-after items in the game? And will they increase in value over time i.e. is there a finite amount?

## How the Data was Obtained
Based on prior knowledge, I know that the largest skin marketplace is buff163.com. It is a Chinese website with the most users and the most "accurate" prices. However, when trying to obtain historical price data, just as in many other online marketplaces, the data is limited to recent sales within only the past week. Because of this, I decided to try and get the most data possible which after surfing the internet, can be found through Steam marketplace API endpoints. This is how I am able to obtain as much data as possible.

Process to storing data in MySQL Database:

### Structure of the Data
The endpoints provide data in JSON format with the structure:[DateTime, average price of sold items, number of items sold] for every hour since the skin was released.
