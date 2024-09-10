from typing import Generator

import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse, Response
from webdriver_manager.chrome import ChromeDriverManager


class DouSpider(scrapy.Spider):
    name = "dou"
    start_urls = [
        "https://jobs.dou.ua/vacancies/?category=Python&exp=0-1",
        "https://jobs.dou.ua/vacancies/?category=Python&exp=1-3",
        "https://jobs.dou.ua/vacancies/?category=Python&exp=3-5",
        "https://jobs.dou.ua/vacancies/?category=Python&exp=5plus",
    ]
    keywords = [
        "Python", "Django", "Flask", "Git", "SQL", "REST", "API",
        "Docker", "AWS", "Linux", "PostgreSQL", "AI", "Artificial Intelligence",
        "JavaScript", "JS", "React", "OOP", "NoSQL", "Networking",
        "Fullstack", "Microservice", "MongoDB", "HTML", "CSS", "DRF",
        "Asyncio", "GraphQL", "Machine Learning", "Deep Learning",
        "Kubernetes", "Terraform", "CI/CD", "Jenkins", "Ansible", "Bootstrap",
        "Tailwind", "Vue", "Angular", "TypeScript", "Pandas", "NumPy", "TensorFlow",
        "PyTorch", "Data Science", "Data Analysis", "Big Data", "ETL"
    ]

    def __init__(self, *args, **kwargs):
        super(DouSpider, self).__init__(*args, **kwargs)
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(
            service=service,
            options=chrome_options)

    def parse(
            self,
            response: Response, **kwargs
    ) -> Generator[scrapy.Request, None, None]:
        self.driver.get(response.url)
        exp_param = response.url.split("exp=")[1]
        while True:
            try:
                more_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "div.more-btn a"))
                )
                more_button.click()

            except Exception as e:
                self.logger.info(f"The button is absent or error: {e}")
                break

        page_source = self.driver.page_source
        scrapy_response = HtmlResponse(
            url=self.driver.current_url,
            body=page_source,
            encoding="utf-8"
        )

        for job in scrapy_response.css("li.l-vacancy"):
            title = job.css("div.title a::text").get()
            link = job.css("div.title a::attr(href)").get()
            company = job.css("strong a.company::text").get()
            salary = job.css("span.salary::text").get()
            cities = job.css("span.cities::text").get()
            if title and link:
                yield scrapy.Request(
                    url=link,
                    callback=self.parse_vacancy_details,
                    meta={
                        "title": title,
                        "link": link,
                        "exp": exp_param,
                        "company": company,
                        "salary": salary,
                        "cities": cities,
                    }
                )

    def parse_vacancy_details(
            self,
            response: Response
    ) -> Generator[dict, None, None]:

        title = response.meta["title"]
        link = response.meta["link"]
        exp = response.meta["exp"]
        company = response.meta["company"]
        salary = response.meta["salary"]
        cities = response.meta["cities"]

        content = response.css("div.b-typo.vacancy-section *::text").getall()
        content_text = " ".join([text.strip() for text in content if text.strip()])
        content_text = content_text.replace(u"\xa0", u" ")
        # pdb.set_trace()

        tags = [keyword for keyword in self.keywords if keyword.lower() in content_text.lower()]

        yield {
            "title": title,
            "link": link,
            "exp": exp,
            "company": company,
            "salary": salary,
            "cities": cities,
            "tags": tags,
        }

    def close(self, reason):
        if self.driver:
            self.driver.quit()
        super().close(reason)
