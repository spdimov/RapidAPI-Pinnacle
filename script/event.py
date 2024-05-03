from datetime import datetime


# Holds converted response from rapid pinnacle API
class Event:
    event_id: int
    home_team: str
    away_team: str
    league_id: int
    league_name: str
    starts: datetime
    home: float
    draw: float
    away: float
    event_type: str

    def __init__(self,
                 event_id: int,
                 home_team: str,
                 away_team: str,
                 league_id: int,
                 league_name: str,
                 starts: datetime,
                 home: float,
                 draw: float,
                 away: float,
                 event_type: str, ) -> None:
        self.event_id = event_id
        self.home_team = home_team
        self.away_team = away_team
        self.league_id = league_id
        self.league_name = league_name
        self.starts = starts
        self.home = home
        self.away = away
        self.event_type = event_type
        self.draw = draw
