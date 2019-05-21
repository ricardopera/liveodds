# liveodds
A small library for live UK/IRE racing odds and runner information.

## Requirements

[Python3](https://www.python.org/downloads/) is needed with [lxml](https://lxml.de/) and [requsts](https://2.python-requests.org/en/master/) modules.

```
$ pip install lxml requests
```

## Installation

```
$ pip install liveodds
```

```
$ git clone https://github.com/4A47/liveodds.git
```
or download [here](https://github.com/4A47/liveodds/archive/master.zip)


# Main functions

## liveodds.list_courses()
Returns list of courses for the days meetings.
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


## liveodds.list_races(optional_course)
Returns list of all race times, or all from a given course.

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


## liveodds.all()
Returns dict of all races where, the key is the race time e.g '13:50', and the value is a Race object for that race.
```python
import liveodds

races = liveodds.all()

for race in races.values():
	# do stuff

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


## liveodds.race(race)
Returns Race object for given race time.
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


## liveodds.course(course)
Returns dict of all races at given course, where the key is the race time e.g '13:50', and the value is a Race object for that race.
```python
races = liveodds.course('redcar')

for race in races.values():
    # do stuff
```

# Types 

## Race
Returned by liveodds.race() function. Contains information about the race and a list of Horse objects for all runners in race. 

### Data

#### Race.time
(Type: String) The off time of the race in 24 hour format e.g '14:35'.

#### Race.course
(Type: String) The name of the racecourse.

#### Race.name
(Type: String) The name of the race.

#### Race.distance
(Type: String) The distance of the race. e.g '5f'

#### Race.grade
(Type: String) The grade of the race in class. e.g 'Class 4'

#### Race.going
(Type: String) The ground conditions of the course. e.g 'Soft'

#### Race.prize
(Type: String) The prizemoney to the winner.

#### Race.age
(Type: String) The age group elligible to run in the race if info is available.

#### Race.size
(Type: Int) The number of runners in the race.

### Methods

#### Race.info()
Returns a formatted string with all available race info.
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

#### Race.runners()
Return a list of Horse objects for every horse in a race.
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


#### Race.json()
Returns JSON for a given race.
```python
import liveodds

race = liveodds.race('19:15')

print(race.json())
```

![Race JSON](https://i.postimg.cc/VL0W8D6p/Screenshot-2019-05-20-JSON-Editor-Online-view-edit-and-format.png)


#### Race.odds()
Returns all odds from race
```python
import liveodds

race = liveodds.race(liveodds.list_races()[0])

for bookie in race.odds():
	

```

#### Race.odds_table()
Returns formatted odds table for printing
```python
import liveodds

race_time = liveodds.list_races()[0]

race = liveodds.race(race_time)

table = race.odds_table()

print(table)

```
Output:
	╒══════════════════╤══════════╤══════════╤═════════════╤════════════════╤═══════════╤ 
	│                  │   Bet365 │   Skybet │   Ladbrokes │   William Hill │   Betfair │  
	╞══════════════════╪══════════╪══════════╪═════════════╪════════════════╪═══════════╪ 
	│ Alkaraama        │      1.3 │     1.29 │        1.25 │           1.25 │      1.25 │ 
	├──────────────────┼──────────┼──────────┼─────────────┼────────────────┼───────────┼ 
	│ Journey Of Life  │       19 │       17 │          17 │             17 │        17 │   
	├──────────────────┼──────────┼──────────┼─────────────┼────────────────┼───────────┼ 
	│ Victory Rose     │       67 │       67 │          67 │             67 │        67 │ 
	├──────────────────┼──────────┼──────────┼─────────────┼────────────────┼───────────┼ 
	│ Chil Chil        │        6 │        6 │           6 │              6 │         6 │ 
	├──────────────────┼──────────┼──────────┼─────────────┼────────────────┼───────────┼ 
	│ Alliseeisnibras  │       26 │       26 │          26 │             26 │        26 │
	├──────────────────┼──────────┼──────────┼─────────────┼────────────────┼───────────┼ 
	│ Alabama Dreaming │       21 │       19 │          21 │             21 │        21 │
	├──────────────────┼──────────┼──────────┼─────────────┼────────────────┼───────────┼ 

	...


## Horse

### Data

#### Horse.number
(Type: Int) The number of the horse.

#### Horse.name
(Type: String) The name of the horse.

#### Horse.draw
(Type: Int) The draw of the horse.

#### Horse.jockey
(Type: String) The name of the jockey.

#### Horse.form
(Type: String) The horses recent form figures.

#### Horse.best_odds
(Type: Dict) Dictionary containing the best price, the bookie offering it, and the time of the request. Where multiple bookies are joint top price, one is chosen at random.

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



## Methods

#### Horse.info()
Returns formatted string containing information about the horse.

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



#### Horse.odds()
Returns a dict of the horses current odds(decimal), where the key is the name of the bookie, and the value is a dict containing the name of the bookie, the current odds and the time of the request.

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


#### Horse.json()
Returns JSON for a horse.

```python
import liveodds

race = liveodds.race('20:15')
horse = race.runners()[0]

print(horse.json())

```

![Horse JSON](https://i.postimg.cc/zBN1Z8hB/Screenshot-2019-05-20-JSON-Editor-Online-view-edit-and-format.png) 


#### Horse.odds_table()
Returns table of horse odds for printing

```python
import liveodds

horse = liveodds.race(liveodds.list_races()[0]).runners()[0]

print(horse.odds_table())

```

Output:
	╒══════════════╤═════════════╕
	│              │   Alkaraama │
	╞══════════════╪═════════════╡
	│ Bet365       │         1.3 │
	├──────────────┼─────────────┤
	│ Skybet       │        1.29 │
	├──────────────┼─────────────┤
	│ Ladbrokes    │        1.25 │
	├──────────────┼─────────────┤
	│ William Hill │        1.25 │
	├──────────────┼─────────────┤
	│ Betfair      │        1.25 │
	├──────────────┼─────────────┤
	│ Betvictor    │        1.25 │
	├──────────────┼─────────────┤
	│ Paddy Power  │        1.25 │
	├──────────────┼─────────────┤
	│ Unibet       │        1.25 │
	├──────────────┼─────────────┤
	│ Coral        │        1.25 │
	├──────────────┼─────────────┤
	│ Betfred      │        1.25 │
	├──────────────┼─────────────┤
	│ Betway       │        1.25 │
	├──────────────┼─────────────┤
	│ Totesport    │        1.25 │
	├──────────────┼─────────────┤
	│ Boylesports  │        1.25 │
	╘══════════════╧═════════════╛

