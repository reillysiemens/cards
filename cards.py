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

    def create_card(self, setname, color, text, creator):
        """Insert a new card with the given properties into the database.
        
        Args:
          setname (str): Name of set the card will belong to.
          color (str): Color the card will have.
          text (str): Text that will appear on the card.
          creator (str): Creator to attribute the card to.

        Returns:
          None
        """
        card = {
            'set': setname,
            'color': color,
            'text': text,
            'creator': creator,
        }
        self.cards_coll.insert_one(card)
