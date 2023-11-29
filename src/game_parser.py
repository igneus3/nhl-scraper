import cchardet
from bs4 import BeautifulSoup, Tag
from logging import warn
import lxml
import re

from parsed_play import ParsedPlay

def filter_newlines(array):
    return list(filter(lambda x: x != '\n', array))

class GameParser:
    def __init__(self, content, game_id):
        self.game_id = game_id
        self.soup = BeautifulSoup(content, 'lxml')
        self.game_state = None
        self.plays = []
        
    def get_game_state(self):
        if self.game_state is None:
            game_info = self.soup.find('table', id='GameInfo')
            if game_info is None:
                return None

            self.game_state = self.soup.find('table', id='GameInfo').contents[-2].contents[1].text.upper()

        return self.game_state

    def get_play_data(self):
        if self.plays == []:
            plays_html = filter_newlines(self.soup.find_all('tr', class_='evenColor'))

            for play_html in plays_html:
                children = filter_newlines(play_html.contents)

                if len(children) < 6:
                    continue
                
                play = ParsedPlay()

                play.id = int(children[0].text)
                play.period = int(children[1].text) if children[1].text != '' else None
                play.event = children[2].text.replace('\xa0', '') if type(children[2].text) == str else None
                play.time = children[3].contents[0] if type(children[3].contents[0]) != Tag else None
                play.type = children[4].text
                play.description = children[5].text

                if play.type in ['GOAL', 'FAC', 'PENL', 'SHOT', 'HIT', 'GIVE', 'MISS']:
                    matches = re.search('^[a-zA-Z\.]*', play.description)
                    play.team = matches.group(0)

                # TODO: Figure out player plus/minus
                #if play.type == 'GOAL':

                if self.plays == [] or play.id != self.plays[-1].id:
                    self.plays.append(play)

        return self.plays
