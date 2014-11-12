import random
import core

def available_plays(game, player_id):
    plays = "ABCDEFfedcba"
    return [
        letter for i, letter in enumerate(list(plays))
        if core.can_play(game, player_id, i)
    ]


class RandomAI(object):
    def process_message(self, mtype, mval):
        if mtype == 'player_id':
            # get my id (0 or 1)
            self.myid = mval
        if mtype == 'game_state':
            # it's my turn ?
            if mval['to_play'] == self.myid:
                # yes, then play:
                # choose a random valid play
                play = random.choice(
                    available_plays(mval['game'], self.myid)
                )
                return play
        return None
