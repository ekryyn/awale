import random


class RandomAI(object):
    def process_message(self, mtype, mval):
        available_plays = {
            0: "ABCDEF",
            1: "abcdef",
        }
        if mtype == 'player_id':
            # get my id (0 or 1)
            self.myid = mval
        if mtype == 'game_state':
            # it's my turn ?
            if mval['to_play'] == self.myid:
                # yes, then play:
                # choose a random valid play
                play = random.choice(
                    available_plays[self.myid]
                )
                return play
        return None
