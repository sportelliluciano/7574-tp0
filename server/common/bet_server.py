from common.utils import has_won, load_bets, store_bets


class BetServer:
    def __init__(self):
        self.open_agencies = {i for i in range(1, 6)}
        self.winners_id = None

    def store_bets(self, bets):
        return store_bets(bets)

    def winners(self, agency_id):
        if self.winners_id is not None:
            return self.winners_id.get(agency_id, [])

        if len(self.open_agencies) > 0:
            return None

        bets = load_bets()
        self.winners_id = {}
        for bet in filter(has_won, bets):
            winners = self.winners_id.get(bet.agency, [])
            winners.append(bet.document)
            self.winners_id[bet.agency] = winners
        
        return self.winners_id.get(agency_id, [])

    def eof(self, agency_id):
        self.open_agencies.discard(agency_id)
