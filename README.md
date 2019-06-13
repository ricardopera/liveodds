# liveodds
A small library for live UK/IRE racing odds and runner information.

## Requirements

[Python3](https://www.python.org/downloads/) is needed with [lxml](https://lxml.de/), [requsts](https://2.python-requests.org/en/master/) and [tabulate](https://pypi.org/project/tabulate/) modules.

```
$ pip install lxml requests tabulate
```

## Installation

```
$ pip install --upgrade liveodds
```
or

```
$ git clone https://github.com/4A47/liveodds.git
```
or download [here](https://github.com/4A47/liveodds/archive/master.zip)


# Main functions

### liveodds.list_courses()
Returns list of courses for the days meetings.

<details>
    <summary>Usage</summary>
    <br>

```python
import liveodds

courses = liveodds.list_courses()

for course in courses:
    print(course)
```
Output:

    redcar
    carlisle
    windsor
    leicester
    ludlow

</details>
<br>

### liveodds.list_races(optional_course)
Returns list of all race times, or all from a given course.

<details>
    <summary>Usage</summary>
    <br>

```python
import liveodds

race_times = liveodds.list_races('redcar')

print(race_times)

for time in race_times:
    race = liveodds.race(time)
    print(race)
```
Output:

    ['14:00', '14:35', '15:05', '15:35', '16:05', '16:35', '17:05', '17:35']
    Race(Redcar 14:00)
    Race(Redcar 14:35)
    Race(Redcar 15:05)
    Race(Redcar 15:35)
    Race(Redcar 16:05)
    Race(Redcar 16:35)
    Race(Redcar 17:05)
    Race(Redcar 17:35)
</details>
<br>

### liveodds.all()
Returns dict of all races where, the key is the race time e.g '13:50', and the value is a Race object for that race.

<details>
    <summary>Usage</summary>
    <br>

```python
import liveodds

races = liveodds.all()

race_1730 = races['17:30']

print(race_1730.info())
```
Output:

    17:30 Windsor
    Follow At The Races On Twitter Handicap
    1m 3f 99y   Class: 5
    Going: Good (Good to Firm in places)
    Runners: 10
    Winner: £3752
</details>
<br>

### liveodds.race(race)
Returns Race object for given race time.

<details>
    <summary>Usage</summary>
    <br>

```python
import liveodds

race = liveodds.race('17:30')

for horse in race.runners():
    print(horse.info())

```
Output:

    2. Vexed
    (J P Spencer) 73-4
    Best Odds: 4.0 (Bet365)

    5. Mr Zoom Zoom
    (R Havlin) 76-352
    Best Odds: 5.0 (Paddy Power)

    6. Sky Cross
    (S De Sousa) 01-5
    Best Odds: 8.0 (Totesport)

    7. Gold Fleece
    (James Doyle) 6-52
    Best Odds: 8.0 (Unibet)

    ...

</details>
<br>

### liveodds.course(course)
Returns dict of all races at given course, where the key is the race time e.g '13:50', and the value is a Race object for that race.

<details>
    <summary>Usage</summary>
    <br>

```python
races = liveodds.course('newbury')

for race in races.items():
    print(race)
```
Output:

    ('14:00', Race(Newbury 14:00))
    ('14:30', Race(Newbury 14:30))
    ('15:00', Race(Newbury 15:00))
    ('15:35', Race(Newbury 15:35))
    ('16:10', Race(Newbury 16:10))
    ('16:40', Race(Newbury 16:40))
    ('17:15', Race(Newbury 17:15))

</details>
<br>

# Types 

## Race
Returned by liveodds.race() function. Contains information about the race and a list of Horse objects for all runners in race.

### Data

#### Race.time
(Type: String) The off time of the race in 24 hour format e.g '14:35'.
<br>

#### Race.course
(Type: String) The name of the racecourse.
<br>

#### Race.name
(Type: String) The name of the race.
<br>

#### Race.distance
(Type: String) The distance of the race. e.g '5f'
<br>

#### Race.grade
(Type: String) The grade of the race in class. e.g 'Class 4'
<br>

#### Race.going
(Type: String) The ground conditions of the course. e.g 'Soft'
<br>

#### Race.prize
(Type: String) The prizemoney to the winner.
<br>

#### Race.age
(Type: String) The age group elligible to run in the race if info is available.
<br>

#### Race.size
(Type: Int) The number of runners in the race.
<br>

### Methods

#### Race.info()
Returns a formatted string with all available race info.

<details>
    <summary>Usage</summary>
    <br>

```python
import liveodds

race = liveodds.race('19:15')

print(race.info())
```
Output:

    19:15 Leicester
    J.F. Herring Handicap
    1m 2f   Class: 4
    Going: Good to Firm (Good in Places)
    Runners: 4
    Winner: £5531

</details>
<br>

#### Race.runners()
Return a list of Horse objects for every horse in a race.

<details>
    <summary>Usage</summary>
    <br>

```python
import liveodds

race = liveodds.race('19:15')

for horse in race.runners():
    print(type(horse), horse)
```
Output:

    <class 'liveodds.Horse'> Horse(Casement)
    <class 'liveodds.Horse'> Horse(Geetanjali)
    <class 'liveodds.Horse'> Horse(Meaghers Flag)
    <class 'liveodds.Horse'> Horse(Billy Roberts)

</details>
<br>

#### Race.json()
Returns JSON for a given race.

<details>
    <summary>Usage</summary>
    <br>

```python
import liveodds

race = liveodds.race('19:15')

print(race.json())
```

![Race JSON](https://i.postimg.cc/VL0W8D6p/Screenshot-2019-05-20-JSON-Editor-Online-view-edit-and-format.png)

</details>
<br>

#### Race.odds()
Returns all odds from race

<details>
    <summary>Usage</summary>
    <br>


```python
import liveodds

race = liveodds.race(liveodds.list_races()[0])

for horse in race.odds().values():
    for bookie in horse.values():
        print(bookie['bookie'], bookie['price'])
    
```

Output:

    Bet365 1.3
    Skybet 1.29
    Ladbrokes 1.25
    William Hill 1.25
    Betfair 1.25
    Betvictor 1.25
    Paddy Power 1.25
    Unibet 1.25
    Coral 1.25

    ...

</details>
<br>

#### Race.odds_table()
Returns formatted odds table for printing

<details>
    <summary>Usage</summary>
    <br>


```python
import liveodds

race_time = liveodds.list_races()[0]

race = liveodds.race(race_time)

table = race.odds_table()

print(table)

```
Output:

![odds table](https://i.postimg.cc/Qt60NvzT/odds-table.png)

</details>

## Horse

Returned by liveodds.race().runners() function. Contains information about the horse including name, jockey, draw, form and odds.

### Data

#### Horse.number
(Type: Int) The number of the horse.
<br>

#### Horse.name
(Type: String) The name of the horse.
<br>

#### Horse.draw
(Type: Int) The draw of the horse.
<br>

#### Horse.jockey
(Type: String) The name of the jockey.
<br>

#### Horse.form
(Type: String) The horses recent form figures.
<br>

#### Horse.best_odds
(Type: Dict) Dictionary containing the best price, the bookie offering it, and the time of the request. Where multiple bookies are joint top price, one is chosen at random.

<details>
    <summary>Usage</summary>
    <br>

```python
import liveodds

race = liveodds.race('19:15')
best_odds = race.runners()[0].best_odds

print(best_odds)
print(best_odds['price'])
print(best_odds['bookie'])
print(best_odds['time'])

```
Output:

    {'bookie': 'Skybet', 'time': '19:40:00', 'price': 3.75}
    3.75
    Skybet
    19:40:00

</details>
<br>

### Methods

#### Horse.info()
Returns formatted string containing information about the horse.

<details>
    <summary>Usage</summary>
    <br>

```python
import liveodds

race = liveodds.race('20:15')
horse = race.runners()[0]

print(horse.info())
```

Output:

    5. Beryl The Petal (1)
    (C J McGovern) 4-2335
    Best Odds:  5.5 (Unibet)

</details>
<br>

#### Horse.odds()
Returns a dict of the horses current odds(decimal), where the key is the name of the bookie, and the value is a dict containing the name of the bookie, the current odds and the time of the request.

<details>
    <summary>Usage</summary>
    <br>

```python
import liveodds

race = liveodds.race('20:15')
horse = race.runners()[0]

odds = horse.odds()

for bookie in odds:
    print(odds[bookie])

```

Output:

    {'bookie': 'Bet365', 'time': '19:51:42', 'price': 5.0}
    {'bookie': 'Skybet', 'time': '19:51:42', 'price': 5.0}
    {'bookie': 'Ladbrokes', 'time': '19:51:42', 'price': 5.5}
    {'bookie': 'William Hill', 'time': '19:51:42', 'price': 5.0}
    {'bookie': 'Betfair', 'time': '19:51:42', 'price': 5.0}
    {'bookie': 'BetVictor', 'time': '19:51:42', 'price': 5.0}

    ...


```python
import liveodds

race = liveodds.race('20:15')
horse = race.runners()[0]

odds = horse.odds()

for bookie in odds:
    bookmaker = odds[bookie]['bookie']
    price = odds[bookie]['price']
    time = odds[bookie]['time']
    
    print(f'{horse.name} is {price} with {bookmaker} at {time}')
```

Output:
    
    Beryl The Petal is 5.0 with Bet365 at 19:58:48
    Beryl The Petal is 5.0 with Skybet at 19:58:48
    Beryl The Petal is 5.0 with Ladbrokes at 19:58:48
    Beryl The Petal is 4.5 with William Hill at 19:58:48
    Beryl The Petal is 4.5 with Betfair at 19:58:48
    Beryl The Petal is 5.0 with BetVictor at 19:58:48
    
    ...
</details>
<br>

#### Horse.json()
Returns JSON for a horse.

<details>
    <summary>Usage</summary>
    <br>

```python
import liveodds

race = liveodds.race('20:15')
horse = race.runners()[0]

print(horse.json())

```

![Horse JSON](https://i.postimg.cc/zBN1Z8hB/Screenshot-2019-05-20-JSON-Editor-Online-view-edit-and-format.png) 

</details>
<br>

#### Horse.odds_table()
Returns table of horse odds for printing

<details>
    <summary>Usage</summary>
    <br>

```python
import liveodds

horse = liveodds.race(liveodds.list_races()[0]).runners()[0]

print(horse.odds_table())

```

Output:

![odds table](https://i.postimg.cc/KjRQ1JXs/odds-table1.png)

</details>
