# Python Technologies Statistics

This project combines web scraping and data analysis to help you
understand the most demanded technologies in the current tech job market.
The goal is to gather data on technology mentions from job listings and 
analyze which technologies are most in demand for Python developers.

## Project Overview

The project is split into two parts:
1. **Web Scraping**: Using Scrapy to scrape job listings from
[dou.ua](https://dou.ua/), extracting relevant technology mentions.
The results are saved to `data/output.csv`.
2. **Data Analysis**: Using Jupyter Notebook to analyze the scraped 
data and generate insights. Various charts are saved in the `data/charts/` directory.

## Getting Started

### Prerequisites

To run this project, you'll need:

- Python 3.x
- Scrapy
- Pandas
- Matplotlib
- Seaborn
- Jupyter Notebook (for analysis)

### Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/SrMusienko/portfolio_scrapy.git
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```


### Running the Scraper

To scrape job listings and save the results:

```bash
cd parce_teh
scrapy crawl dou -o output.csv 
```
The output will be saved in data/output.csv
To perform data analysis, follow these steps:

#### Running Jupyter Notebook:

```bash
# 1. Open the Jupyter Notebook by running the following command:
jupyter notebook 

# 2. Navigate to the `analysis` directory and open the `main.ipynb` file.

# 3. Execute the notebook cells to analyze the data.
# The generated charts will be saved in the `data/charts/` directory.
# For example, a chart showing the most common technologies will be saved as:
plt.savefig("../data/charts/top_tech.png")