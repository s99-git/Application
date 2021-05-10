# Using: https://pypi.org/project/py-trello/
# https://github.com/sarumont/py-trello
# PDF documentation: https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwji5eCS7OXvAhX-M1kFHeVGADMQFjAAegQIBxAD&url=https%3A%2F%2Freadthedocs.org%2Fprojects%2Fpy-trello-dev%2Fdownloads%2Fpdf%2Flatest%2F&usg=AOvVaw1-vlt-k1FXhBt1uslG60E7
from trello import TrelloClient
import json
import os.path
from os import path

# store our applications API key/secret
os.environ["TRELLO_API_KEY"] = '2e0161c01eca7ad03bda843f811dac8b'
os.environ["TRELLO_API_SECRET"] = 'd4446e39644f0992f6db9859c77441754f0085ad5725d86699780d1ba86dfeea'

class Trello():
    def __init__(self):
        self.client = None
        self.trello_id = None

    # returns dictionary storing
    def dict_generate(self):
        dict_board = {}
        dict_card = {}
        all_boards = self.ping_boards()

        # iterate through all possible boards
        for i in range(len(all_boards)):
            print("BOARD NAME: ", all_boards[i].name)
            all_lists = all_boards[i].get_lists(list_filter="open")
            # reset the dict list for a new board
            dict_list = {}
            # iterate through all of this boards lists
            for j in range(len(all_lists)):
                print("LIST NAME: ", all_lists[j].name)
                all_cards = all_lists[j].list_cards()
                # reset the cards list
                cards = []
                # iterate through all of this lists cards
                for k in range(len(all_cards)):
                    print("CARD NAME: ", all_cards[k].name)
                    # make a collection of all cards for this list
                    cards.append(all_cards[k].name)
                # assign said collection of cards to this list
                dict_list[all_lists[j].name] = cards

            dict_board[all_boards[i].name] = dict_list

        # print(dict_board)
        return dict_board


    # returns all boards for this user
    def ping_boards(self):
        #print("ping_boards")
        return self.client.list_boards()


    # returns all lists under a board
    def ping_lists(self, board_name):
        #print("ping_lists")
        # store the index for the specified board
        i = self.board_index(board_name)

        all_boards = self.ping_boards()
        # return all lists for a board
        return all_boards[i].get_lists(list_filter="open")


    # returns all cards under a list
    def ping_cards(self, board_name, list_name):
        #print("ping_cards")
        # store all boards for this client
        all_boards = self.ping_boards()

        # store the index for the specified board
        i = self.board_index(board_name)
        # store the index for the specified list
        j = self.list_index(board_name, list_name, i)

        # store all lists under a board
        board_lists = all_boards[i].get_lists(list_filter="open")
        # return all cards under a list
        return board_lists[j].list_cards()


    # returns the index of the desired board
    def board_index(self, board_name):
        # store all boards for this client
        all_boards = self.ping_boards()
        # locate the proper board
        for i in range(len(all_boards)):
            # if we have located the board
            if board_name == all_boards[i].name:
                return i
        return None


    # returns the index of the desired list
    def list_index(self, board_name, list_name, i):
        # store all boards for this client
        all_boards = self.ping_boards()
        # store all lists for this board
        board_lists = all_boards[i].get_lists(list_filter="open")

        # locate the proper list
        for j in range(len(board_lists)):
            # if we have located the list
            if list_name == board_lists[j].name:
                return j
        return None


    # returns the index of the desired card
    def card_index(self, board_name, list_name, card_name, i, j):
        print("card_index")
        # store all boards for this client
        all_boards = self.ping_boards()

        # store all lists for this board
        board_lists = all_boards[i].get_lists(list_filter="open")
        # store all the cards for this list
        card_list = board_lists[j].list_cards()
        # locate the proper card
        for k in range(len(card_list)):
            if card_name == card_list[k].name:
                return k
        return None


    # create a task card
    def ping_card_create(self, board_name, list_name, card_name, card_description):
        # store the boards index
        i = self.board_index(board_name)
        if i == None:
            return False
        # store the lists index
        j = self.list_index(board_name, list_name, i)
        if j == None:
            return False

        # store all lists for a board
        board_lists = self.ping_lists(board_name)
        # add card to the desired list
        board_lists[j].add_card(card_name, desc=card_description)
        print(board_lists[j])
        print("Creation Successful")
        return True


    def ping_card_get(self, board_name, list_name, card_name):
        # store the boards index
        i = self.board_index(board_name)
        if i == None:
            return None
        # store the lists index
        j = self.list_index(board_name, list_name, i)
        if j == None:
            return None
        # store the cards index
        k = self.card_index(board_name, list_name, card_name, i, j)
        if k == None:
            return None

        # store all lists for this board
        board_lists = self.ping_lists(board_name)
        # store all cards for this list
        card_list = board_lists[j].list_cards()

        return card_list[k]


    # delete a task card
    # returns True if the task card has been deleted
    # returns False if the task card cannot be deleted
    def ping_card_delete(self, board_name, list_name, card_name):
        print("Delete")
        # get this specific card
        card = self.ping_card_get(board_name, list_name, card_name)
        # if this card does not exist, cannot delete it
        if card is None:
            return False
        # delete the card
        card.delete()
        return True


    # modify a task card's description
    def ping_card_modify(self, board_name, list_name, card_name, new_description):
        # get this specific card
        card = self.ping_card_get(board_name, list_name, card_name)
        # if this card does not exist, cannot delete it
        if card is None:
            return False
        # set this cards description
        card.set_description(new_description)
        return True


    # create a list
    def ping_list_create(self, board_name, list_name):
        # locate this boards index
        i = self.board_index(board_name)
        # store all boards for this client
        all_boards = self.ping_boards()
        # add the new list for this board
        all_boards[i].add_list(list_name)
        return True

    def ping_list_delete(self, board_name, list_name):
        # store the boards index
        i = self.board_index(board_name)
        if i == None:
            return None
        # store the lists index
        j = self.list_index(board_name, list_name, i)
        if j == None:
            return None
        # store all lists for this board
        board_lists = self.ping_lists(board_name)
        # delete the board
        board_lists[j].close()
        return True

    # create a board
    def ping_board_create(self, board_name):
        # make a board with the provided name
        self.client.add_board(board_name)
        return True


    # move a task card to a specified list
    def ping_card_move(self, board_name, list_name, card_name, new_list_name):
        # store the boards index
        i = self.board_index(board_name)
        if i == None:
            return False
        # store the lists index
        j = self.list_index(board_name, list_name, i)
        if j == None:
            return False
        # store the new lists index
        new_list_index = self.list_index(board_name, new_list_name, i)
        if new_list_index == None:
            return False
        # store the cards index
        k = self.card_index(board_name, list_name, card_name, i, j)
        if k == None:
            return False

            # store all lists for this board
        board_lists = self.ping_lists(board_name)
        # store all cards for this list
        card_list = board_lists[j].list_cards()
        # change the list this card is under
        card_list[k].change_list(board_lists[new_list_index].id)
        print("Card Movement Successful")
        return True



    def action_setup2(self, email):
        # if the config file already exists, use the existing tokens
        if path.exists("pinguin.json"):
            file = open("pinguin.json", "r")
            accounts = json.load(file)
            print(accounts.keys())

            # if this email already has a configuration, use it
            if email in accounts.keys():
                client = TrelloClient(
                    api_key='2e0161c01eca7ad03bda843f811dac8b',
                    api_secret='d4446e39644f0992f6db9859c77441754f0085ad5725d86699780d1ba86dfeea',
                    # token = '3e1c54bc5ae2f18fe2e449c102c49b40400de0b39e2aca401dfc7a028c1ed33e',
                    # token_secret = '298b5e59c4c09cff9666ba32fd381c5f'
                    token=accounts[email]["token"],
                    token_secret=accounts[email]["token_secret"]
                )
                self.client = client
            else:
                print("no email in pinguin.json or pinguin.json doesnt exist")

    def add_members(self, board, users):
        for user in users:
            board.add_member(user)

"""
t = Trello()
t.action_setup('s99@umbc.edu')
"""