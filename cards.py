from pymongo import MongoClient

class Cards:
    def __init__(self, dbname='cards'):
        """Instantiate this class.

           Set up a connection to the given Mongo database.
           Get to the collection we'll store cards in.
        
        Args:
          dbname (str): Database name.
        """
        self.client = MongoClient()
        self.db = self.client[dbname]
        self.cards_coll = self.db['cards']

    @property
    def sets(self):
        """Return a list of all the card sets in the database.
        
        Args:
          None

        Returns:
          list: List of all card sets in the database.
        """
        return self.cards_coll.distinct('set')

    def retrieve_set(self, setname):
        """Return a list of all the cards in the given set.
        
        Args:
          setname (str): Name of set.

        Returns:
          list: List of all cards in the the given set.
        """
        return list(self.cards_coll.find({'set': setname}))

    def create_cards(self, cards):
        """Insert a new card with the given properties into the database.
        
        Args:
          cards: List of dictionaries with set, color, text, and creator keys.

        Returns:
          None
        """

        keys = ['set', 'color', 'text', 'creator']
        filtered = [ { k: card[k] for k in keys if k in card} for card in cards]
        self.cards_coll.insert_many(filtered)

    def delete_cards(self, filterdict):
        """Delete all the cards matching a filter.

        Args:
          filterdict: Dictionary with set, color, text, and/or creator keys.

        Returns:
          None
        """

        keys = ['set', 'color', 'text', 'creator']
        filterdict = { k: filterdict[k] for k in keys if k in filterdict }
        self.cards_coll.delete_many(filterdict)
