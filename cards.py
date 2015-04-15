from pymongo import MongoClient

class Cards:
    def __init__(self, dbname='cards'):
        """Instantiate this class.
           Set up a connection to the given Mongo database.
           Get to the collection we'll store cards in."""
        self.client = MongoClient()
        self.db = self.client[dbname]
        self.cards_coll = self.db['cards']

    def list_sets(self):
        """Return a list of all the card sets in the database."""
        return self.cards_coll.distinct('set')

    def cards_in_set(self, setname):
        """Return a list of all the cards in the given set."""
        return list(self.cards_coll.find({'set': setname}))

    def create_card(self, setname, color, text, creator):
        """Insert a new card with the given properties into the database."""
        card = {
            'set': setname,
            'color': color,
            'text': text,
            'creator': creator,
        }
        self.cards_coll.insert_one(card)
