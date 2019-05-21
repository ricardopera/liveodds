#!/usr/bin/env python3

import liveodds


def main():

    # get list of todays meetings
    meetings = liveodds.list_courses()

    print(meetings, '\n')

    
    # list race times for each course
    for meet in meetings:
        print(meet)
        for race in liveodds.list_races(meet):
            print(race)
        print()

    
    # get Race objects for all races at Nottingham
    races = liveodds.course('nottingham')


    # liveodds.course() func return a dictionary
    print(type(races))


    # each key is a race time
    # each value is the corresponding Race object
    for key, val in races.items():
        print('Key:', key, ' Value:', val)

    print()

    
    # accessing the Race objects
    for race in races.values():
        print(race.info())

        print('Runners:')

        for horse in race.runners():
            print(f'{horse.number}. {horse.name} ({horse.jockey}) {horse.form}')

        print('\n')


    # accessing the odds
    race_time = liveodds.list_races()[0]

    race = liveodds.race(race_time)

    print(type(race))
    print(race)






if __name__ == '__main__':
    main()
