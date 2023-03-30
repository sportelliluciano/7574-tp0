from common.utils import has_won, load_bets, store_bets


class BetServer:
    def __init__(self):
        self.open_agencies = {i for i in range(1, 6)}
        self.winners_id = None

    def store_bets(self, bets):
        return store_bets(bets)

    def winners(self):
        if self.winners_id is not None:
            return self.winners_id

        if len(self.open_agencies) > 0:
            return None

        bets = load_bets()
        winners = [bet.document for bet in filter(has_won, bets)]
        self.winners_id = winners
        return self.winners_id

    def eof(self, agency_id):
        self.open_agencies.discard(agency_id)
