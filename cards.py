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

    def _constrain_keys(self, dictionary):
        """Constrain a given dictionary to contain only valid keys.

        Args:
            dictionary (dict): A potentially unconstrained dictionary.
        Returns:
            constrained (dict): A new dictionary containing only valid keys.
        """

        constrained = { k: dictionary[k] for k in self._keys if k in dictionary }
        return constrained

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

        self._collection.insert_many([self._constrain_keys(card) for card in cards])

    def delete_cards(self, filterdict):
        """Delete all the cards matching a filter.

        Args:
          filterdict: Dictionary with set, color, text, and/or creator keys.

        Returns:
          None
        """

        self._collection.delete_many(self._constrain_keys(filterdict))

    def update_cards(self, filterdict, values, multiple=True):
        """Update cards matching a filter.

        Args:
          filterdict (dict): Dictionary with set, color, text, and/or creator
                             keys to query collection against.

          values (dict): Dictionary with set, color, text, and/or creator
                         keys with values that should be updated.

          multiple (boolean): Defaults to true. Whether to update all matches
                              or just the first one found.

        Returns:
          None
        """

        self._collection.update(self._constrain_keys(filterdict),
                                {'$set': self._constrain_keys(values)},
                                multi=multiple)
