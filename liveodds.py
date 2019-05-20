#!/usr/bin/env python3

import json
from lxml import html
from random import shuffle
import requests
from time import ctime


class Race:
    def __init__(self, runners, course, time, info):
        self._json = info
        self.time = time
        self.course = course
        self.distance = info["distance"]
        self.going = info["going"]
        self.grade = info["grade"]
        self.name = info["name"]
        self.prize = info["prize"]
        self.size = info["field_size"]
        self._runners = runners

    def __repr__(self):
        return f"{__class__.__name__}({self.course.title()} {self.time})"

    def json(self):
        runners = []
        for runner in self.runners():
            runners.append({runner.name: runner._odds})

        self._json["runners"] = runners

        return json.dumps(self._json)

    def runners(self):
        return self._runners

    def info(self):
        return (
            f"{self.time} {self.course.title()}\n"
            f"{self.name}\n"
            f"{self.distance}   {self.grade}\n"
            f"Going: {self.going}\n"
            f"Runners: {self.size}\n"
            f"Winner: {self.prize}\n"
        )


class Horse:
    def __init__(self, info):
        self._json = info
        self.number = info["number"]
        self.name = info["name"]
        self.draw = info["draw"]
        self.jockey = info["jockey"]
        self.form = info["form"]
        self._odds = info["odds"]
        self.best_odds = info["best_odds"]

    def __repr__(self):
        return f"{__class__.__name__}({self.name})"

    def json(self):
        return json.dumps(self._json)

    def odds(self):
        return self._odds

    def info(self):
        if self.draw:
            draw = f"({self.draw})"
        else:
            draw = ""
        return (
            f"{self.number}. {self.name} {draw}\n"
            f"({self.jockey}) {self.form}\n"
            f'Best Odds:  {self.best_odds["price"]} ({self.best_odds["bookie"]})\n'
        )


races = {}


def race_links(race=None):
    r = requests.get(
        "https://www.oddschecker.com/horse-racing",
        headers={"User-Agent": "Mozilla/5.0"},
    )

    if r.status_code == 200:
        doc = html.fromstring(r.content)
        races = doc.xpath('//div[@class="module show-times"]')[0].xpath(
            './/div[@class="racing-time"]/a'
        )

        return ["https://www.oddschecker.com" + race.attrib["href"] for race in races]
    else:
        return []


def runner_info(runner):
    info = {}
    info["name"] = runner.attrib["data-bname"]
    info["draw"] = runner.attrib["data-stall"]
    info["number"] = runner.xpath('.//td[@class="cardnum"]/text()')[0]
    try:
        info["jockey"] = runner.xpath('.//div[@class="bottom-row jockey"]/text()')[0]
    except:
        info["jockey"] = ""
    try:
        info["form"] = runner.xpath('.//span[@class="current-form"]/text()')[0]
    except:
        info["form"] = ""
    info["odds"] = {}

    return info


def race_info(race):
    info = {}
    left_info = race.find(
        './/ul[@class="race-headline-info race-headline-info-left"]'
    ).findall(".//li")
    right_info = race.find('.//ul[@class="race-headline-info"]').findall(".//li")

    info["name"] = race.find(
        './/p[@class="map-title beta-footnote betam-caption2"]'
    ).text
    info["field_size"] = int(
        left_info[0].find('.//span[@class="info info beta-caption4"]').text
    )
    info["distance"] = left_info[1].find('.//span[@class="info beta-caption4"]').text
    info["grade"] = (
        "Class:" + left_info[2].find('.//span[@class="info beta-caption4"]').text
    )

    if len(right_info) > 2:
        right_info.pop(0)

    info["prize"] = right_info[0].find('.//span[@class="info beta-caption4"]').text
    info["going"] = right_info[1].find('.//span[@class="info beta-caption4"]').text

    return info


def load_race(link):
    race = []
    r = requests.get(link, headers={"User-Agent": "Mozilla/5.0"})

    if r.status_code == 200:
        doc = html.fromstring(r.content)
        race_time = link.split("/")[5]
        race_course = link.split("/")[4]
        r_info = race_info(
            doc.xpath('//div[@class="page-description module grid-header-all-sports"]')[
                0
            ]
        )

        runners = doc.xpath('//tbody[@id="t1"]')[0].xpath(".//tr")

        for runner in runners:
            info = runner_info(runner)
            prices = runner.xpath(".//td[@data-odig]")

            try:
                prices = [
                    prices[i] for i in [0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 15]
                ]
            except IndexError:
                return []

            time = ctime().split()[3]

            info["odds"]["bet365"] = {
                "bookie": "Bet365",
                "time": time,
                "price": float(prices[0].attrib["data-odig"]),
            }
            info["odds"]["skybet"] = {
                "bookie": "Skybet",
                "time": time,
                "price": float(prices[1].attrib["data-odig"]),
            }
            info["odds"]["ladbrokes"] = {
                "bookie": "Ladbrokes",
                "time": time,
                "price": float(prices[2].attrib["data-odig"]),
            }
            info["odds"]["williamhill"] = {
                "bookie": "William Hill",
                "time": time,
                "price": float(prices[3].attrib["data-odig"]),
            }
            info["odds"]["betfair"] = {
                "bookie": "Betfair",
                "time": time,
                "price": float(prices[4].attrib["data-odig"]),
            }
            info["odds"]["betvictor"] = {
                "bookie": "BetVictor",
                "time": time,
                "price": float(prices[5].attrib["data-odig"]),
            }
            info["odds"]["paddypower"] = {
                "bookie": "Paddy Power",
                "time": time,
                "price": float(prices[6].attrib["data-odig"]),
            }
            info["odds"]["unibet"] = {
                "bookie": "Unibet",
                "time": time,
                "price": float(prices[7].attrib["data-odig"]),
            }
            info["odds"]["coral"] = {
                "bookie": "Coral",
                "time": time,
                "price": float(prices[8].attrib["data-odig"]),
            }
            info["odds"]["betfred"] = {
                "bookie": "BetFred",
                "time": time,
                "price": float(prices[9].attrib["data-odig"]),
            }
            info["odds"]["betway"] = {
                "bookie": "Betway",
                "time": time,
                "price": float(prices[10].attrib["data-odig"]),
            }
            info["odds"]["totesport"] = {
                "bookie": "Totesport",
                "time": time,
                "price": float(prices[11].attrib["data-odig"]),
            }
            info["odds"]["boylesports"] = {
                "bookie": "Boylesports",
                "time": time,
                "price": float(prices[12].attrib["data-odig"]),
            }

            _odds = [info["odds"][bookie] for bookie in info["odds"]]
            shuffle(_odds)
            info["best_odds"] = max(_odds, key=lambda k: k["price"])

            race.append(Horse(info))

    return Race(race, race_course, race_time, r_info)


def all():
    races.clear()
    links = race_links()

    for link in links:
        races[link.split("/")[5]] = load_race(link)

    return races


def race(race):
    if race in list_races():
        races.clear()

        if race:
            links = race_links()

            for link in links:
                if link.split("/")[5] == race:
                    return load_race(link)

    return {}


def course(course):
    if course in list_courses():
        races.clear()

        links = race_links()

        for link in links:
            if link.split("/")[4] == course:
                races[link.split("/")[5]] = load_race(link)

        return races

    return {}


def list_races(course=None):
    links = race_links()

    if course in list_courses():
        return [link.split("/")[5] for link in links if link.split("/")[4] == meeting]

    return [link.split("/")[5] for link in links]


def list_courses():
    links = race_links()
    return list(set([link.split("/")[4] for link in links]))
