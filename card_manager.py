#!/usr/bin/env python

"""
Command line client for interfacing with the cards MongoDB API
"""

from clint.textui import puts, colored, prompt, validators
import cards

def unknown(cards):
    """Returns instructions when an unknown action is entered

    Args:
        cards (Cards): Cards object to interface with MongoDB
    Returns:
        None
    """
    puts(colored.yellow('Unknown action, ? for list of actions'))    

def list_actions(cards):
    """Prints all possible actions

    Args:
        cards (Cards): Cards object to interface with MongoDB
    Returns:
        None
    """
    for item in sorted(actions):
        print("{}: {}".format(item, actions[item][1]))
    print()

def list_sets(cards):
    """Prints all card sets in the database

    Args:
        cards (Cards): Cards object to interface with MongoDB
    Returns:
        None
    """
    for s in cards.sets:
        print(s)

def list_cards(cards):
    """Lists all cards in the database, from all sets

    Args:
        cards (Cards): Cards object to interface with MongoDB
    Returns:
        None
    """
    print("{:10} {:10} {:10} {}".format('Set', 'Color', 'Creator',
                                            'Text'))
    for s in cards.sets:
        for card in cards.retrieve_set(s):
            print("{:10} {:10} {:10} {}".format(card['set'], card['color'],
                                                card['creator'], card['text']))

def add_card(cards):
    """Adds card to the database based on user input

    Args:
        cards (Cards): Cards object to interface with MongoDB
    Returns:
        None
    """
    card_set = prompt.query('Enter card set: ', default='None')
    card_color = prompt.query('Enter card color: ')
    card_text = prompt.query('Enter card text: ')
    card_creator = prompt.query('Enter card creator: ', default='None')
    cards.create_cards([{'set': card_set, 'color': card_color,
                        'text': card_text, 'creator': card_creator}])

actions = {'exit': (exit, "Exit the program"),
            'help': (list_actions, "List all actions"),
            '?': (list_actions, "List all actions"),
            'list sets': (list_sets, "List all card sets in database"),
            'list cards': (list_cards, "List all cards in database"),
            'add': (add_card, "Add card to database")}

def get_action(cmd):
    """Returns appropriate function pointer from actions dictionary

    Args:
        cmd (str): Action the user has entered
    Returns:
        Function Pointer
    """

    try:
        return actions[cmd][0]
    except KeyError:
        return unknown

if __name__ == '__main__':
    dbname = prompt.query('Enter DB Name >', default='cards')
    cards = cards.Cards()

    while(1):
        action = get_action(prompt.query('Enter Action >'))
        if action == exit:
            action()
        else:
            action(cards)
