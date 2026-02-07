# Mobile Home Park Scraper

A Python web scraper that collects publicly listed mobile home park information
from a directory-style website for educational and data analysis purposes.

## Overview
This project scrapes publicly accessible listings of mobile home parks and
extracts structured information such as park name, address, space count,
and phone number. The scraper iterates through state-level directory pages
and follows individual listings to retrieve contact details.

The goal of this project is to demonstrate web scraping, HTML parsing,
and basic data extraction techniques using Python.

## Data Collected
For each mobile home park listing, the scraper attempts to collect:

- Park name  
- Address  
- Space (lot) count (if available)  
- Phone number  

The output is written to a CSV file for easy inspection and analysis.

## Requirements
- Python 3.8+
- requests
- beautifulsoup4
- pandas

## Example Output
```csv
Park Name,Address,Space Count,Phone Number
Pineview/Cloverleaf Mobile Home Park,"3309 Main Street, Adamsville, AL, 35005, US",,205-674-0222
Daisy City Mobile Home Park,"Adamsville, AL, 35005-0147, US",,205-674-6130
