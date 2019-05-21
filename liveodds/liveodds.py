#!/usr/bin/env python3

''' Library for live odds and information on UK/IRE horse racing. '''

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
        try:
            self.distance = info["distance"]
        except KeyError:
            self.distance = ''
        try:
            self.going = info["going"]
        except KeyError:
            self.going = ''
        try:
            self.grade = info["grade"]
        except KeyError:
            self.grade = ''
        try:
            self.name = info["name"]
        except KeyError:
            self.name = ''
        try:
            self.prize = info["prize"]
        except KeyError:
            self.prize = ''
        try:
            self.size = info["field_size"]
        except KeyError:
            self.size = ''
        try:
            self.age = info['age']
        except KeyError:    
            self.age = ''
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
            f"Age:{self.age}\n"
            f"Runners: {self.size}\n"
            f"Winner: {self.prize}\n"
        )

    def odds(self):
        pass

    def pretty_odds(self):
        pass


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

    def odds(self):
        return self._odds

    def pretty_odds(self):
        pass


races = {}


def race_links(race=None):
    r = requests.get(
        "https://www.oddschecker.com/horse-racing",
        headers={"User-Agent": "Mozilla/5.0"},
    )

    if r.status_code == 200:
        doc = html.fromstring(r.content)
        try:
            races = doc.xpath('//div[@class="module show-times"]')[0].xpath(
                './/div[@class="racing-time"]/a'
            )
        except IndexError:
            print('IndexError when attempting to retrieve race links, it could be 00:00, try again in a few minutes.')
            return []

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
    except IndexError:
        info["jockey"] = ""
    try:
        info["form"] = runner.xpath('.//span[@class="current-form"]/text()')[0]
    except IndexError:
        info["form"] = ""
    info["odds"] = {}

    return info


def race_info(race):
    info = {}
    info['name'] = race.find('.//div[@class="event"]').text_content()
    content_right = race.find('.//div[@class="content-right"]').xpath('.//li')

    for data in content_right:
        content = data.text_content()

        if 'Starter' in content:
            info['field_size'] = int(data.find('.//span[@class="info info beta-caption4"]').text)
        elif 'Distance' in content:
            info['distance'] = data.find('.//span[@class="info beta-caption4"]').text
        elif 'Class' in content:
            info['grade'] = 'Class:' + data.find('.//span[@class="info beta-caption4"]').text
        elif 'Prize' in content:
            info['prize'] = data.find('.//span[@class="info beta-caption4"]').text
        elif 'Age' in content:
            info['age'] = data.find('.//span[@class="info beta-caption4"]').text
        elif 'Going' in content:
            info['going'] = data.find('.//span[@class="info beta-caption4"]').text

    return info


def load_race(link):
    race = []
    r = requests.get(link, headers={"User-Agent": "Mozilla/5.0"})

    if r.status_code == 200:
        doc = html.fromstring(r.content)
        race_time = link.split("/")[5]
        race_course = link.split("/")[4]
        r_info = race_info(
            doc.xpath('//div[@class="page-description module grid-header-all-sports"]')[0]
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

            bookies = [
                'bet365', 'skybet', 'ladbrokes', 'william_hill', 'betfair', 'betvictor',
                'paddy_power', 'unibet', 'coral', 'betfred', 'betway', 'totesport', 'boylesports'
            ]

            for bookie, price in zip(bookies, prices):
                info['odds'][bookie] = {
                    "price": float(price.attrib["data-odig"]),
                    "time": time,
                    "bookie": bookie.replace('_', ' ').title()
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
        return [link.split("/")[5] for link in links if link.split("/")[4] == course]

    return [link.split("/")[5] for link in links]


def list_courses():
    return list(set([link.split("/")[4] for link in race_links()]))
