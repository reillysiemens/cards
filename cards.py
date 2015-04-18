from pymongo import MongoClient

class Cards:
    def __init__(self, dbname='cards'):
        """Instantiate this class.

           Set up a connection to the given Mongo database.
           Get to the collection we'll store cards in.
        
        Args:
          dbname (str): Database name.
        """
        self._client = MongoClient()
        self._db = self._client[dbname]
        self._collection = self._db[dbname]
        self._keys = ['set', 'color', 'text', 'creator']

    @property
    def sets(self):
        """Return a list of all the card sets in the database.
        
        Args:
          None

        Returns:
          list: List of all card sets in the database.
        """
        return self._collection.distinct('set')

    def retrieve_set(self, setname):
        """Return a list of all the cards in the given set.
        
        Args:
          setname (str): Name of set.

        Returns:
          list: List of all cards in the the given set.
        """
        return list(self._collection.find({'set': setname}))

    def create_cards(self, cards):
        """Insert a new card with the given properties into the database.
        
        Args:
          cards: List of dictionaries with set, color, text, and creator keys.

        Returns:
          None
        """

        filtered = [ { k: card[k] for k in self._keys if k in card} for card in cards]
        self._collection.insert_many(filtered)

    def delete_cards(self, filterdict):
        """Delete all the cards matching a filter.

        Args:
          filterdict: Dictionary with set, color, text, and/or creator keys.

        Returns:
          None
        """

        filterdict = { k: filterdict[k] for k in self._keys if k in filterdict }
        self._collection.delete_many(filterdict)
