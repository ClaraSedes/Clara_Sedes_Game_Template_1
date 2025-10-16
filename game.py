# !/usr/bin/python3
# -- coding: utf-8 --

# 11/10/25

__author__ = 'Clara Sedes'

from map import g_rooms
import string


def remove_punct(p_text):
    """This function is used to remove all punctuation
    marks from a string. Spaces do not count as punctuation and should
    not be removed. The funcion takes a string and returns a new string
    which does not contain any puctuation. For example:

    >>> remove_punct("Hello, World!")
    'Hello World'
    >>> remove_punct("-- ...Hey! -- Yes?!...")
    ' Hey  Yes'
    >>> remove_punct(",go!So.?uTh")
    'goSouTh'
    """
    l_no_punct = ''.join([ch for ch in p_text if ch not in string.punctuation])
    return l_no_punct
    

def remove_spaces(p_text):
    """This function is used to remove leading and trailing spaces from a string.
    It takes a string and returns a new string with does not have leading and
    trailing spaces. For example:

    >>> remove_spaces("  Hello!  ")
    'Hello!'
    >>> remove_spaces("  Python  is  easy!   ")
    'Python  is  easy!'
    >>> remove_spaces("Python is easy!")
    'Python is easy!'
    >>> remove_spaces("")
    ''
    >>> remove_spaces("   ")
    ''
    """
    l_no_spaces = p_text.strip()
    return l_no_spaces


def normalise_input(p_user_input):
    """This function removes all punctuation, leading and trailing
    spaces from a string, and converts the string to lower case.
    For example:

    >>> normalise_input("  Go south! ")
    'go south'
    >>> normalise_input("!!! tAkE,. LAmp!?! ")
    'take lamp'
    >>> normalise_input("HELP!!!!!!!")
    'help'
    """
    l_check_1 = remove_punct(p_user_input)
    l_check_2 = remove_spaces(l_check_1)

    return l_check_2.lower()

    
def display_room(p_room):
    """This function takes a room as an input and nicely displays its name
    and description. The room argument is a dictionary with entries "name",
    "description" etc. (see map.py for the definition). The name of the room
    is printed in all capitals and framed by blank lines. Then follows the
    description of the room and a blank line again. For example:

    >>> display_room(g_rooms["Office"])
    <BLANKLINE>
    THE GENERAL OFFICE
    <BLANKLINE>
    You are standing next to the cashier's till at
    30-36 Newport Road. The cashier looks at you with hope
    in their eyes. If you go west you can return to the
    Queen's Buildings.
    <BLANKLINE>

    Note: <BLANKLINE> here means that doctest should expect a blank line.
    """
    print()
    print(p_room["name"].upper())
    print()
    print(p_room["description"])
    print()

    
def exit_leads_to(p_exits, p_direction):
    """This function takes a dictionary of exits and a direction (a particular
    exit taken from this dictionary). It returns the name of the room into which
    this exit leads. For example:

    >>> exit_leads_to(g_rooms["Reception"]["exits"], "south")
    "MJ and Simon's room"
    >>> exit_leads_to(g_rooms["Reception"]["exits"], "east")
    "your personal tutor's office"
    >>> exit_leads_to(g_rooms["Tutor"]["exits"], "west")
    'Reception'
    """
    l_identifier = p_exits[p_direction]
    return g_rooms[l_identifier]["name"]
    

def print_menu_line(p_direction, p_leads_to):
    """This function prints a line of a menu of exits. It takes two strings: a
    direction (the name of an exit) and the name of the room into which it
    leads (leads_to), and should print a menu line in the following format:

    Go <EXIT NAME UPPERCASE> to <where it leads>.

    For example:
    >>> print_menu_line("east", "you personal tutor's office")
    Go EAST to you personal tutor's office.
    >>> print_menu_line("south", "MJ and Simon's room")
    Go SOUTH to MJ and Simon's room.
    """
    # return f'Go {p_direction.upper()} to {p_leads_to}'
    print('Go', p_direction.upper(), 'to', p_leads_to + '.')


def print_menu(p_exits):
    """This function displays the menu of available exits to the player. The
    argument p_exits is a dictionary of exits as exemplified in map.py. The
    menu should, for each exit, call the function print_menu_line() to print
    the information about each exit in the appropriate format. The room into
    which an exit leads is obtained using the function exit_leads_to().

    For example, the menu of exits from Reception may look like this:

    You can:
    Go EAST to your personal tutor's office.
    Go WEST to the parking lot.
    Go SOUTH to MJ and Simon's room.
    Where do you want to go?
    """
    print("You can:")

    for l_exit in p_exits.keys():
        print_menu_line(l_exit, exit_leads_to(p_exits, l_exit))

    print("Where do you want to go?")


def is_valid_exit(p_exits, p_user_input):
    """This function checks, given a dictionary "exits" (see map.py) and
    a players's choice "user_input" whether the player has chosen a valid exit.
    It returns True if the exit is valid, and False otherwise. Assume that
    the name of the exit has been normalised by the function normalise_input().
    For example:

    >>> is_valid_exit(g_rooms["Reception"]["exits"], "south")
    True
    >>> is_valid_exit(g_rooms["Reception"]["exits"], "up")
    False
    >>> is_valid_exit(g_rooms["Parking"]["exits"], "west")
    False
    >>> is_valid_exit(g_rooms["Parking"]["exits"], "east")
    True
    """
    return p_user_input in p_exits


def menu(p_exits):
    """This function, given a dictionary of possible exits from a room, prints the
    menu of exits using print_menu() function. It then prompts the player to type
    a name of an exit where she wants to go. The players's input is normalised
    using the normalise_input() function before further checks are done.  The
    function then checks whether this exit is a valid one, using the function
    is_valid_exit(). If the exit is valid then the function returns the name
    of the chosen exit. Otherwise the menu is displayed again and the player
    prompted, repeatedly, until a correct choice is entered."""

    # Repeat until the player enter a valid choice
    while True:
        # Display menu
        print_menu(p_exits)
        # Read player's input
        l_answer = input("Please type your answer here (only type the direction) ")

        # Normalise the input
        l_checked_answer = normalise_input(l_answer)

        # Check if the input makes sense (is valid exit)
        if is_valid_exit(p_exits, l_checked_answer):
            return l_checked_answer
        print("\nPlease enter a valid exit as instructed.")


def move(p_exits, p_direction):
    """This function returns the room into which the player will move if, from a
    dictionary "exits" of avaiable exits, they choose to move towards the exit
    with the name given by "direction". For example:

    >>> move(g_rooms["Reception"]["exits"], "south") == g_rooms["Admins"]
    True
    >>> move(g_rooms["Reception"]["exits"], "east") == g_rooms["Tutor"]
    True
    >>> move(g_rooms["Reception"]["exits"], "west") == g_rooms["Office"]
    False
    """
    l_identifier = p_exits[p_direction]
    l_current_room = g_rooms[l_identifier]
    return l_current_room


# This is the entry point of our program
def main():
    # Start game at the reception
    l_current_room = g_rooms["Reception"]

    # Main game loop
    while True:
        # Display game status (room description etc.)
        display_room(l_current_room)

        # What are the possible exits from the current room?
        l_exits = l_current_room["exits"]

        # Show the menu with exits and ask the player
        l_direction = menu(l_exits)

        # Move the protagonist, i.e. update the current room
        l_current_room = move(l_exits, l_direction)


# Are we being run as a script? If so, run main().
# '__main__' is the name of the scope in which top-level code executes.
# See https://docs.python.org/3.4/library/__main__.html for explanation
if __name__ == "__main__":
    main()
