class BetStoreBatchCmd:
    def __init__(self, bets):
        self.bets = bets

    def apply(self, bs):
        return bs.store_bets(self.bets)


class BetWinnersCmd:
    def __init__(self, agency_id):
        self.agency_id = agency_id
    
    def apply(self, bs):
        return bs.winners(self.agency_id)


class BetEofCmd:
    def __init__(self, agency_id):
        self.agency_id = agency_id

    def apply(self, bs):
        return bs.eof(self.agency_id)

