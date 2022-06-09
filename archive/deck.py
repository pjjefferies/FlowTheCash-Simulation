class Deck(object):
    def __init__(self, deckType):
        self.deckType = deckType
        self.cards = []
    def getDeckType(self):
        return self.deckType
    def getCards(self):
        return self.Cards
    def getNoCards(self):
        return len(self.cards)
    def addCard(self, card):
        self.cards.append(card)
        return self.getNoCards()
    def takeRandomCard(self):
        import random
        try:
            return self.cards.pop(int(random.random()*self.getNoCards()))
        except IndexError:
            return None
    def takeTopCard(self):
        try:
            return self.cards.pop()
        except IndexError:
            return None
    def shuffle(self):
        import random
        random.shuffle(self.cards)
    def __str__(self):
        cardString = ""
        for card in self.cards:
            cardString = cardString + str(card) + "\n"
        return cardString[:-1]
