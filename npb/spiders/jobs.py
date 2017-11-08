# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy import Request

from scrapy.selector import Selector

import re
from datetime import datetime

from npb.spiders import Player


class JobsSpider(Spider):
    name = 'jobs'
    allowed_domains = ['2689web.com']
    start_urls = ['http://2689web.com/ind/ind.html']
    OVER_10_YEAR = 10
    BATTER_PITCHER = "batter/pitcher"

    def parse(self, response):
        jobs = response.xpath(
            "//table[@class='aiueo2'][4]//td[contains(@class, 'indbig')]")
        for job in jobs:
            if self.is_old_times(job):
                continue
            relative_url = job.xpath("a/@href").extract_first()
            absolute_url = response.urljoin(relative_url)
            yield Request(absolute_url, callback=self.parse_player_in_year)

    def is_old_times(self, job):
        if job.xpath("a/text()").extract_first() in ["1930年代", "1940年代"]:
            return True
        return False

    def parse_player_in_year(self, response):
        jobs = response.xpath(
            "//table[@class='list']//td[contains(@class, 'name11')]/"
            "parent::tr")
        for job in jobs:
            if self.is_less_than_10_year(job):
                continue
            absolute_url = re.sub(
                r"[0-9]{4}.html", job.xpath(
                    "td[@class='name11']/a/@href"
                    ).extract_first(), response.url)
            yield Request(absolute_url, callback=self.parse_player)

    def is_less_than_10_year(self, job):
        whole_years = job.xpath("td[@class='name12']/text()").extract_first()
        start_year = int(whole_years[0:4])
        if whole_years[-1] == "-":
            end_year = int(datetime.now().strftime("%Y"))
        else:
            end_year = int(whole_years[-4:])
        if end_year - start_year < self.OVER_10_YEAR:
            return True
        else:
            return False

    def parse_player(self, response):
        stat = []
        player = Player()
        name = response.xpath("//table[@class='ind2']/tr[2]/td[@class='name']/text()").extract_first()
        category, stat = player.create_player(response, name)
        if category is not None:
            yield {
                "name": name,
                "category": category,
                "stat": stat}
