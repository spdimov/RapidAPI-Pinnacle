import logging
from datetime import datetime, timedelta
from decimal import Decimal

import requests
import winsound

from Database import Database
from Sport import Sport
from event import Event


class PinnacleAPI:
    MARKETS_URL = "https://pinnacle-odds.p.rapidapi.com/kit/v1/markets"
    STATIC_SETTINGS = {"sport_id": "1", "is_have_odds": "true", "event_type": "prematch"}
    HEADERS = {
        "X-RapidAPI-Key": "<hardcoded-api-key>",
        "X-RapidAPI-Host": "pinnacle-odds.p.rapidapi.com"
    }
    LOGGING = logging.basicConfig()
    odds_finder = Database()
    HOURS_IN_SECONDS = 60 * 60
    TIME_BETWEEN_CALLS = 24
    MINUTES_TO_CHECK_BACK = 8

    @classmethod
    def get_events(cls):
        matchups = []
        for sport in Sport:
            cls.STATIC_SETTINGS["sport_id"] = sport.value
            # cls.STATIC_SETTINGS["since"] = str(floor(time.time()) - cls.TIME_BETWEEN_CALLS)
            response = requests.get(cls.MARKETS_URL, headers=cls.HEADERS, params=cls.STATIC_SETTINGS)
            for event in response.json()["events"]:
                try:
                    if datetime.strptime(event["starts"], "%Y-%m-%dT%H:%M:%S") + timedelta(hours=2) > datetime.now():
                        matchup = Event(
                            event["event_id"],
                            event["home"],
                            event["away"],
                            event["league_id"],
                            event["league_name"],
                            datetime.strptime(event["starts"], "%Y-%m-%dT%H:%M:%S") + timedelta(hours=2),
                            event["periods"]["num_0"]["money_line"]["home"],
                            event["periods"]["num_0"]["money_line"]["draw"],
                            event["periods"]["num_0"]["money_line"]["away"],
                            event["event_type"],
                        )
                        matchups.append(matchup)
                except Exception as e:
                    logging.debug(
                        "Could not create matchup object for {event['home']} - {event['away']} due to possible missing fields: {e}")
                    continue
        return matchups

    def update_database(self):

        for event in self.get_events():
            if (event.starts - datetime.now()).total_seconds() < 3 * self.HOURS_IN_SECONDS:
                self.update_leagues(event)
                self.update_matchups(event)
                latest_odds = self.get_latest_odds(event.event_id, 15)

                if self.has_odds_moved(latest_odds, event):
                    self.update_odds(event)
                else:
                    continue

                if len(latest_odds) == 0:
                    continue

                if self.is_change_significant_from_last_time(latest_odds, event):
                    print("\n")
                    print("Odds havent dropped in a while and now have dropped")
                    print(latest_odds[0][0], latest_odds[0][1], latest_odds[0][2])
                    print(event.home, event.draw, event.away)
                    print((latest_odds[0][0] - event.home) / event.home)
                    print((latest_odds[0][2] - event.away) / event.away)
                    print((event.starts - datetime.now()).total_seconds() / 60)
                    print(event.event_id)
                    print(event.home_team, event.away_team)
                    print(event.league_name)
                    print("\n")
                    self.make_noise()
                    continue

                for odds in latest_odds:
                    if self.is_change_significant_in_last_minutes(odds, event, self.MINUTES_TO_CHECK_BACK):
                        print("\n")
                        print("Odds dropped in last 10 min")
                        print(odds[0], odds[1], odds[2])
                        print(event.home, event.draw, event.away)
                        print((odds[0] - event.home) / event.home)
                        print((odds[2] - event.away) / event.away)
                        print((event.starts - datetime.now()).total_seconds() / 60)
                        print(event.event_id)
                        print(event.home_team, event.away_team)
                        print(event.league_name)
                        print("\n")
                        self.make_noise()
                        break

    @staticmethod
    def has_odds_moved(last_odds, event):
        return not last_odds or \
               last_odds[0][0] != event.home or \
               last_odds[0][1] != event.draw or \
               last_odds[0][2] != event.away

    @staticmethod
    def is_change_significant_from_last_time(latest_odds, event):
        return Decimal((latest_odds[0][0] - event.home) / (event.home * event.home)) > 0.07 or Decimal(
            (latest_odds[0][2] - event.away) / (event.away * event.away)) > 0.07

    @staticmethod
    def is_change_significant_in_last_minutes(odds, event, minutes):
        return ((datetime.now() - odds[3]).total_seconds() < minutes * 60) and (
                Decimal((odds[0] - event.home) / (event.home * event.home)) > 0.105 or
                Decimal((odds[2] - event.away) / (event.away * event.away)) > 0.105)

    @classmethod
    def update_leagues(self, event):
        leagues_update = "INSERT INTO leagues (league_id, league_name) " \
                         "VALUES (%s, %s) " \
                         "ON DUPLICATE KEY UPDATE league_id=league_id"
        values = (event.league_id, event.league_name)
        self.odds_finder.execute_query(leagues_update, values)

    @classmethod
    def update_matchups(self, event):
        matchups_update = "INSERT INTO matchups (matchup_id, league, home_team, away_team, start_time) " \
                          "VALUES (%s, %s, %s, %s, %s) " \
                          "ON DUPLICATE KEY UPDATE matchup_id=matchup_id"
        matchups_update_values = (event.event_id, event.league_id, event.home_team, event.away_team, event.starts)
        self.odds_finder.execute_query(matchups_update, matchups_update_values)

    @classmethod
    def get_latest_odds(self, matchup_id, size):
        get_odds = "SELECT home,draw,away, time_updated " \
                   "FROM odds " \
                   "WHERE matchup_id = %s " \
                   "ORDER BY time_updated DESC " \
                   "LIMIT %s"
        get_odds_value = (matchup_id, size)
        return self.odds_finder.execute_query(get_odds, get_odds_value)

    @classmethod
    def add_to_changed_matchups(self, event, latest_odds):
        matchups_update = "INSERT INTO changed_odds_matchups " \
                          "(matchup_id, home_odds_last, home_odds_new, " \
                          "draw_odds_last, draw_odds_new, " \
                          "away_odds_last, away_odds_new) " \
                          "VALUES (%s, %s, %s, %s, %s, %s, %s) as values_alias " \
                          "ON DUPLICATE KEY UPDATE " \
                          "home_odds_last=values_alias.home_odds_new, " \
                          "draw_odds_last=values_alias.draw_odds_new, " \
                          "away_odds_last=values_alias.away_odds_new"
        changed_matchups_update_values = (event.event_id, event.home, latest_odds[0], event.draw, latest_odds[1], event.away, latest_odds[2])
        self.odds_finder.execute_query(matchups_update, changed_matchups_update_values)

    @classmethod
    def update_odds(self, event):
        odds_update = "INSERT INTO odds (matchup_id, home, draw, away) " \
                      "VALUES (%s, %s, %s, %s)"
        odds_update_values = (event.event_id, event.home, event.draw, event.away)
        self.odds_finder.execute_query(odds_update, odds_update_values)

    @staticmethod
    def make_noise():
        frequency = 800
        duration = 500
        winsound.Beep(frequency, duration)
