'''
    Black Jack Simulator

    Author: Steve (Seonghoon Cho)

    This program siumlates Black Jack

    purpose: finding the best strategy of Black Jack

    Created: Nov 3, 2021,
    updated: Nov 29, 2021
'''

import random
import pandas as pd
import os
from collections import deque
import copy

shapes_tpl = ('spade', 'clover', 'diamond', 'heart')
numbers_tpl = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')

class Card:
    """
    Card class represents single card
    
    ...

    Attributes
    ----------
    shape_str : str
        shape of the card ('spade', 'clover', 'diamond', 'heart')
    number_str : str
        number of card (2, 3, ... 10, J, Q, K, A)
    is_exposed_bool : boolean
        true if the card is exposed to players

    Methods
    -------
    value()
        return the integer value of the card
        'A' has value 1
    is_ace()
        return true if the card is ace

    # Getters
    get_is_exposed()
    get_number_str()
    get_shape_str()

    # Setters
    set_is_exposed()

    """
    def __init__(self, shape, number, is_exposed=False):
        ''' initialize a card with shape, number '''
        self.__shape_str = shape
        self.__number_str = number
        self.__is_exposed_bool = is_exposed
    
    def __str__(self):
        ''' return string representation of Card object '''
        return self.get_number_str() + ' ' + self.get_shape_str()

    def value(self):
        ''' calculate the value of a card. A is assigned as 1 '''
        values_tpl = (2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 1)
        search_in_dic = dict(zip(numbers_tpl, values_tpl))
        return int(search_in_dic[self.get_number_str()])

    def is_ace(self):
        ''' return true if this card is ace '''
        is_ace = False
        if self.get_number_str() == 'A':
            is_ace = True
        return is_ace

    # getter methods 
    def get_is_exposed(self):
        return self.__is_exposed_bool

    def get_number_str(self):
        return self.__number_str
    
    def get_shape_str(self):
        return self.__shape_str

    # setter methods
    def set_is_exposed(self, is_exposed):
        self.__is_exposed_bool = is_exposed


class Deck:
    """
    A class used to represent a deck

    ...

    Attributes
    ----------
    __cards_deq : deque
        a card deck consists of n decks of cards
    __num_decks : int
        number of card decks in this Deck
    __num_cards : int
        number of cards in this Deck

    Methods
    -------
    shuffle()
        shuffle the deck
    draw()
        return a Card object drawn from a Deck object
    
    # Getters
    get_num_decks()
    get_num_cards

    """
    def __init__(self, count_int):
        ''' initialize the deck with count_int decks of card '''
        self.__cards_deq = deque()     # cards attribute
        self.__num_decks = count_int
        # fill Deck with cards of __num_decks amount
        for i in range(count_int):
            for shape in shapes_tpl:
                for number in numbers_tpl:
                    card = Card(shape, number)
                    self.__cards_deq.append(card)
        # count num of cards after assignment
        self.__num_cards = len(self.__cards_deq)

    def __str__(self):
        ''' string representation of deck object '''
        return str(self.__cards_deq)
    
    def shuffle(self):
        ''' shuffle this deck '''
        print("........Shuffle deck")
        random.shuffle(self.__cards_deq)

    def draw(self, is_exposed=False):
        ''' draw a card from Deck. return Card object '''
        drawed_card = self.__cards_deq.popleft()
        drawed_card.set_is_exposed(is_exposed)
        self.__num_cards -= 1
        return drawed_card
    
    # getter methods
    def get_num_decks(self):
        return self.__num_decks
    
    def get_num_cards(self):
        return self.__num_cards


class Hands:
    """
    A class used to represent a Hands collection    

    ...

    Attributes
    ----------
    __hands : list
        collection of Hhand objects
    __player : Player 
        Player object, owner of this Hands 

    Methods
    -------
    __iter__()
        iterator method
    add_hand()
        add Hand object to this Hands collection
     
    # Getters
    get_player()

    """
    def __init__(self, player):
        ''' initialize the Hands by adding one hand default '''
        self.__hands = list()
        self.__player = player
        self.add_hand()
        self.__is_splited = False   # check
        self.__splited_hands = 1    # number of hand within hands (one player)

    def __iter__(self):
        ''' iterator method '''
        return HandsIterator(self.__hands)
    
    def add_hand(self):
        ''' add a Hand object to the Hands collection'''
        new_hand = Hand(player = self.get_player(), hands = self)
        self.__hands.append(new_hand)
        return new_hand
    
    # getter methods
    def get_player(self):
        return self.__player


class HandsIterator:
    """
    A class used to implement iterator of Hands collection

    ...

    Attributes
    ----------
    __hands : Hands object
        Hands object to iterate
    __index : int
        index of current iteration

    Methods
    -------
    __next__()
        return the next Hand
    
    """

    def __init__(self, hands):
        ''' initialize iterator '''
        self.__hands = hands
        self.__index = 0

    def __next__(self):
        ''' return the next Hand, otherwise raise StopIteration '''
        if self.__index < len(self.__hands):
            result = self.__hands[self.__index]
            self.__index += 1
            return result
        else:
            raise StopIteration


class Hand:
    """
    Hand class represents one hand of the player
    
    ...

    Attributes
    ----------
    __cards_lst : list
        list of cards in hand
    __hands : Hand object
        Hands collection that this Hand belongs to
    __is_soft : bool
        true if a hand is soft, having ace
    __is_pair : bool
        true if a hand is pair, two cards with same number
    __is_break : bool
        true if a hand is over 21
    __no_more_card : bool
        true if no more card is necessary, otherwise false

    Methods
    -------
    __str__()
        return string of __cards_lst (ex: 7 spade)
    add()
        add a card to the hand
    update_status()
        checking soft, pair, and break
    value()
        return the total value of a hand
        if a hand is soft add 10
    face_value()
        return the total of exposed cards
    check_soft()
        if current status is not soft and added card is ace
        then status is changed to soft
    check_pair()
        return true if Hand has only two cards and they are same numbers
    check_break()
        return true if the value of a hand is over 21
    show_hand()
        return cards string in current hand
    decide(player, dealer, strategy_tuple)
        decide strategy based on strategy_tuple
    cards_value_except_one_a()
        return value except one ace. If a hand holds two ace
        only one ace will be counted.
    cards_split()
        returns card string. for example 'A, A', 'T, T'
        this is used for conversion for pair_splitting
    cards_soft()
        returns card string. for example 'A, 9', 'A, 8'
        this is used for conversion for soft_hand
    split_hand()
        split two cards into two hands

    # Getters
    get_card_lst()
    is_soft()
    is_pair()
    is_break()
    get_hands()
    no_more_card()
    get_player()
    get_last_decision()

    # setters
    __set_is_soft()
    set_is_pair()
    set_no_more_card()
    set_last_decision()

    """
    def __init__(self, player, hands):
        self.__player = player
        self.__cards_lst = list()
        self.__hands = hands
        self.__is_soft= False
        self.__is_pair = False
        self.__is_break = False
        self.__no_more_card = False
        self.__last_decision = None

    # return string representation of Hdnd object
    def __str__(self):
        ''' eturn string of __cards_lst (ex: 7 spade) '''
        # output_str = ''
        output_str = list()
        for card in self.get_card_lst():
            # output_str += str(card) + "\n"
            output_str.append(str(card))
        output_str = "\n".join(output_str) + "\n"
        return output_str

    def add(self, card):
        ''' add a card to the hand '''
        self.get_card_lst().append(card)
        self.update_status(card)
    
    def update_status(self, card):
        ''' checking soft, pair, and break '''
        self.check_soft(card)
        self.check_pair()
        self.check_break()

    def value(self):
        ''' return the total value of a hand 
        if a hand is soft add 10 '''
        value_total = 0
        for card in self.get_card_lst():
            value_total += card.value()
        
        if self.is_soft():
            if value_total + 10 <= 21:
                value_total += 10
            
        return value_total

    def face_value(self):
        ''' return the total of exposed cards '''
        value_total = 0
        for card in self.get_card_lst():
            # count only exposed cards
            if card.get_is_exposed():
                if card.is_ace():
                    value_total += 11
                else:
                    value_total += card.value()
        
        return value_total    

    def check_soft(self, card):
        ''' if current status is not soft and added card is ace
        then status is changed to soft '''
        if (not self.is_soft() and card.is_ace()):
            self.__set_is_soft(True)

    def check_pair(self):
        ''' return true if Hand has only two cards and they are same numbers '''
        is_pair = False
        card_lst = self.get_card_lst()
        if len(card_lst) == 2:
            if card_lst[0].get_number_str() == card_lst[1].get_number_str():
                is_pair = True
        
        self.set_is_pair(is_pair)
    
    def check_break(self):
        '''return true if the value of a hand is over 21'''
        if self.value() > 21:
            self.__is_break = True
        
    def show_hand(self, player):
        '''return cards string in current hand'''
        return f"{player.get_name_str()}'s hand: {self.value()} \n" + str(self) + "\n"

    def decide(self, player, dealer, strategy_tuple):
        ''' decide strategy based on strategy_tuple '''
        game = player.get_game()
        file_output_str = game.get_output_log_str()
        file_output_str.append(self.show_hand(player))
        decision = ""
        if (not self.is_soft() and self.value() in [15, 16]):    # if not soft check whether to surrender or not
            try:
                decision = strategy_tuple['surrender'].loc[self.value(), dealer.get_hand().face_value()]    
            except KeyError:
                decision = 'NOSUR'
        else:
            decision = 'NOSUR'
        
        if decision == 'NOSUR':     # if not surrender, check it is pair or soft
            # check split is necessary
            if (self.is_pair()):
                file_output_str.append("player " + player.get_name_str() + "'s value: " + str(self.cards_split()) + "\n")
                file_output_str.append("dealer face_value(): " + str(dealer.get_hand().face_value()) + "\n")
                decision = strategy_tuple['pair_splitting'].loc[self.cards_split(), dealer.get_hand().face_value()] 
                if decision in ['Y', 'Y/N']:
                    decision = 'SPLIT'
                self.set_is_pair(False)

            # if the decision is not split keep decide
            if decision != 'SPLIT':
                if (self.is_soft() and self.cards_value_except_one_a() < 10): # check is_soft
                    file_output_str.append("player " + player.get_name_str() + "'s value: " + str(self.cards_soft()) + "\n")
                    file_output_str.append("dealer face_value(): " + str(dealer.get_hand().face_value()) + "\n")
                    # decide from hard_totals
                    decision = strategy_tuple['soft_totals'].loc[self.cards_soft(), dealer.get_hand().face_value()]
                    decision_map = ['S', 'Ds', 'H', 'D']
                    if (len(self.get_card_lst()) == 2): # if only two cards we can bet on double
                        decision_str = ['STAND', 'DOUBLE', 'HIT', 'DOUBLE']
                    else:       # else we can only bet on hit and stand
                        decision_str = ['STAND', 'HIT', 'HIT', 'HIT']

                    decision = decision_str[decision_map.index(decision)]
                else: # else the hand is hard
                    file_output_str.append("player " + player.get_name_str() + "'s value: " + str(self.value()) + "\n")
                    file_output_str.append("dealer face_value(): " + str(dealer.get_hand().face_value()) + "\n")
                    # decide from hard_totals
                    decision = strategy_tuple['hard_totals'].loc[self.value(), dealer.get_hand().face_value()]
                    decision_map = ['S', 'H', 'D']
                    if (len(self.get_card_lst()) == 2): # if only two cards we can bet on doubl
                        decision_str = ['STAND', 'HIT', 'DOUBLE']
                    else:
                        decision_str = ['STAND', 'HIT', 'HIT']

                    decision = decision_str[decision_map.index(decision)]
        
        return decision
    
    def cards_value_except_one_a(self):
        ''' return value except one ace. If a hand holds two ace
        only one ace will be counted. '''
        str_list = list()
        cards = copy.deepcopy(self.get_card_lst())  # deep copy for preserving 
        for card in cards:
            if card.get_number_str() == 'A': 
                cards.remove(card)   # remove one A
                break

        for card in cards:
            curr_val = card.value()
            str_list.append(curr_val)

        cards_value_output = sum(str_list)

        return cards_value_output

    def cards_split(self):
        ''' returns card string. for example 'A, A', 'T, T'. 
        This is used for conversion for pair_splitting '''
        str_list = list()
        cards = copy.deepcopy(self.get_card_lst())  # deep copy for preserving
        for i in range(len(cards)):
            curr_val = cards[i].value()
            if curr_val == 10:
                curr_val = 'T'
            if curr_val == 1:
                curr_val = 'A'
            str_list.append(str(curr_val))

        str_output = ", ".join(str_list)

        return str_output

    def cards_soft(self):
        ''' returns card string. for example 'A, 9', 'A, 8'
        this is used for conversion for soft_hand '''
        cards = copy.deepcopy(self.get_card_lst())  # deep copy for preserving
        for card in cards:
            if card.get_number_str() == 'A': 
                cards.remove(card)   # remove one A
                break
        
        sum_of_not_a = 0
        for card in cards:
            sum_of_not_a += card.value()

        str_output = "A, " + str(sum_of_not_a)

        return str_output

    def split_hand(self):
        ''' split two cards into two hands '''
        first_card = self.get_card_lst()[0]
        second_card = self.get_card_lst()[1] 

        player = self.get_player()
        game = player.get_game()
        file_output_str = game.get_output_log_str()
        file_output_str.append(f"splitting the first card: {str(first_card)}\n") 
        self.__cards_lst = [first_card]
        # file_output_str.append(f"print __cards_lst: {str(self.__cards_lst)}\n")
        self.update_status(first_card)

        file_output_str.append(f"splitting the second card: {str(second_card)}\n")

        new_hand = self.get_hands().add_hand()
        new_hand.add(second_card)

    # getter method
    def get_card_lst(self):
        return self.__cards_lst

    def is_soft(self):
        return self.__is_soft
    
    def is_pair(self):
        return self.__is_pair
    
    def is_break(self):
        return self.__is_break
    
    def get_hands(self):
        return self.__hands
    
    def no_more_card(self):
        return self.__no_more_card
    
    def get_player(self):
        return self.__player
    
    def get_last_decision(self):
        return self.__last_decision
    
    # setter method
    def __set_is_soft(self, is_soft):
        self.__is_soft = is_soft

    def set_is_pair(self, is_pair = False):
        self.__is_pair = is_pair
    
    def set_no_more_card(self, no_more_card):
        self.__no_more_card = no_more_card
    
    def set_last_decision(self, decision):
        self.__last_decision = decision


class Player:
    """
    Player class represents the player
    
    ...

    Attributes
    ----------
    __game : Game
        represents Game object that this play is play in
    __name_str : str
        name of the player
    __count_of_win : float
        count of win
    __count_of_tie : float
        count of tie
    __count_of_lose : float
        count of lose, if SURRENDER count -0.5 win count id decreased
    __hands : Hands
        hands object of the player
    __strategy : tuple
        strategy data of this player, read from file

    Methods
    -------
    add_win_count()
        add +1 when player win
    add_tie_count()
        add +1 when player tied with dealer
    add_lose_count()
        add -1 when player lose, -0.5 when player SURRENDER
    load_strategy()
        read strategy data from file and store it in tuple
    reset_hands()
        reset hands of the player

    # getters
    get_win_count()
    get_tie_count()
    get_lose_count()
    get_name_str()
    get_strategy()
    get_game()

    """
    def __init__(self, game, name='Player'):
        self.__game = game
        self.__name_str = name
        self.__count_of_win = float(0.0)
        self.__count_of_tie = float(0.0)
        self.__count_of_lose = float(0.0)
        self.__hands = Hands(self)
        self.__strategy = None

    def add_win_count(self, count = 1.0):
        '''add +1 when player win'''
        self.__count_of_win += count

    def add_tie_count(self, count = 1.0):
        '''add +1 when player tied with dealer'''
        self.__count_of_tie += count

    def add_lose_count(self, count = 1.0):
        '''add -1 when player lose, -0.5 when player SURRENDER'''
        self.__count_of_lose += count

    def load_strategy(self):
        '''read strategy data from file and store it in tuple'''
        curr_dicrectory = os.getcwd()
        try:
            hard_totals = pd.read_excel(curr_dicrectory + os.sep + self.get_name_str() + os.sep + 'hard_totals.xlsx', \
                                        skiprows=0, index_col=0, header=1)
            hard_totals = hard_totals.rename(columns={'A': 11}) # ace is valued as 11
            
            soft_totals = pd.read_excel(curr_dicrectory + os.sep + self.get_name_str() + os.sep + 'soft_totals.xlsx', \
                                        skiprows=0, index_col=0, header=1)        
            soft_totals = soft_totals.rename(columns={'A': 11}) # ace is valued as 11

            surrender = pd.read_excel(curr_dicrectory + os.sep + self.get_name_str() + os.sep + 'surrender.xlsx', \
                                        skiprows=0, index_col=0, header=1)
            surrender = surrender.fillna(value='NOSUR')     # fill empty cell with 'NOSUR
            surrender = surrender.rename(columns={'A': 11}) # ace is valued as 11

            pair_splitting = pd.read_excel(curr_dicrectory + os.sep + self.get_name_str() + os.sep + 'pair_splitting.xlsx', \
                                        skiprows=0, index_col=0, header=1)
            pair_splitting = pair_splitting.rename(columns={'A': 11})   # ace is valued as 11
        except FileNotFoundError:
            raise FileNotFoundError()
        
        strategy_tuple = dict(zip(['hard_totals', 'soft_totals', 'surrender', 'pair_splitting'], [hard_totals, soft_totals, surrender, pair_splitting]))
        self.__strategy = strategy_tuple

    def reset_hands(self):
        '''reset hands of the player'''
        self.__hands = Hands(self)

    # getter methods
    def get_win_count(self):
        return self.__count_of_win

    def get_tie_count(self):
        return self.__count_of_tie
    
    def get_lose_count(self):
        return self.__count_of_lose 

    def get_hands(self):
        return self.__hands
    
    def get_name_str(self):
        return self.__name_str
    
    def get_strategy(self):
        return self.__strategy
    
    def get_game(self):
        return self.__game


class Dealer:
    """
    Dealer class represents the dealer
    
    ...

    Attributes
    ----------
    __game : Game
        represents Game object that this play is play in
    __name_str : str
        name of the player
    __count_of_win : float
        count of win
    __count_of_tie : float
        count of tie
    __count_of_lose : float
        count of lose, if SURRENDER count -0.5 win count id decreased
    __hand : Hand
        hand object of the player, dealer always has one hand 
        so not implemented Hands of dealer
    __default_deck : int
        number of deck of cards used for one shoe
    __deck : Deck
        deck of cards that dealer uses

    Methods
    -------
    add_win_count()
        add +1 when dealer win
    add_tie_count()
        add +1 when dealer tied with dealer
    add_lose_count()
        add -1 when dealer lose
    value()
        return value of dealer's hand
    dist_to_hand()
        distribute one Card to hand
    dist_to_player()
        distribute card to one player
    dist_to_players()
        distribute cards (one card per player's hand, 
        if player has two hands one for each)   
    dist_to_dealer()
        distribute card to dealer's hand
    play()
        dealer plays his card
    reset_hand()
        reset dealer's hand
    shuffle_deck()
        shuffle cards in shoe
    dist_default()
        draw card and distribute it to players and dealer two times

    # getters
    get_deck()
    get_name_str()
    get_hand()
    get_win_count()
    get_tie_count()
    get_lose_count()
    get_game()

    """
    def __init__(self, game, name='Dealer'):
        self.__game = game
        self.__name_str = name      # name of dealer
        self.__count_of_win = 0
        self.__count_of_tie = 0
        self.__count_of_lose = 0
        self.__hand = Hand(player = self, hands = None)
        # dealer handles deck
        self.__default_deck = 8
        self.__deck = Deck(self.__default_deck)     # this game use 8 decks of card for game
        self.__deck.shuffle()

    def add_win_count(self, count = 1.0):
        '''add +1 when dealer win'''
        self.__count_of_win += count

    def add_tie_count(self, count = 1.0):
        '''add +1 when dealer tied with dealer'''
        self.__count_of_tie += count

    def add_lose_count(self, count = 1.0):
        '''add -1 when dealer lose'''
        self.__count_of_lose += count

    def value(self):
        '''return value of dealer's hand'''
        return self.__hand.value()
    
    def dist_to_hand(self, hand):
        '''distribute a card to hand'''
        if not hand.no_more_card():
            drawed_card = self.__deck.draw(is_exposed=True)
            hand.add(drawed_card)

    def dist_to_player(self, player):
        '''distribute card to one player'''
        for hand in player.get_hands():      
            self.dist_to_hand(hand)  

    def dist_to_players(self, players):
        '''distribute cards (one card per player's hand, 
        if player has two hands one for each)'''
        for player in players:
            self.dist_to_player(player)
    
    def dist_to_dealer(self, is_exposed=False):
        '''distribute card to dealer's hand'''
        drawed_card = self.get_deck().draw(is_exposed=is_exposed)
        self.__hand.add(drawed_card)
    
    def play(self):
        '''dealer plays his card'''
        file_output_str = self.get_game().get_output_log_str()
        # expose all dealer card
        for card in self.get_hand().get_card_lst():
            if not card.get_is_exposed():
                card.set_is_exposed(True)
        file_output_str.append("dealer's current value: " + str(self.get_hand().value()) + "\n" + str(self.get_hand()) + "\n")

        isBreak = self.get_hand().is_break()
        if isBreak:
            file_output_str.append("DEALER BREAK!\n")
        
        while (self.get_hand().value() < 17 and not self.get_hand().is_soft()) or \
               (self.get_hand().value() <= 17 and self.get_hand().is_soft()):
            file_output_str.append(self.get_name_str() + "'s DECISION: HIT\n")
            self.dist_to_dealer(is_exposed = True)
            file_output_str.append(str(self.get_hand()) + "\n")
            file_output_str.append("dealer's current value: " + str(self.get_hand().value()) + "\n")
            isBreak = self.get_hand().is_break()
            if isBreak:
                file_output_str.append("DEALER BREAK!\n")
        
    def reset_hand(self):
        '''reset dealer's hand'''
        self.__hand = Hand(player = self, hands = None)
    
    def shuffle_deck(self):
        '''shuffle cards in shoe'''
        self.__deck = Deck(self.__default_deck)     # this game use 8 decks of card for game
        self.__deck.shuffle()

    # utility methods
    def dist_default(self, players):
        '''draw card and distribute it to players and dealer two times'''
        for i in range(2):
            self.dist_to_players(players)
            if i == 0:
                self.dist_to_dealer(is_exposed=False)
            else:
                self.dist_to_dealer(is_exposed=True)

    # getter method
    def get_deck(self):
        return self.__deck

    def get_name_str(self):
        return self.__name_str
    
    def get_hand(self):
        return self.__hand

    def get_win_count(self):
        return self.__count_of_win

    def get_tie_count(self):
        return self.__count_of_tie
    
    def get_lose_count(self):
        return self.__count_of_lose
    
    def get_game(self):
        return self.__game


# this class represents a game
class Game:
    """
    Game class represents the game
    
    ...

    Attributes
    ----------
    __output_log_str : list
        stores string to print out to file
    __round : int
        round of game
    __players : Player
        players of the game
    __dealer : Dealer
        dealer of the game

    Methods
    -------
    add_player()
        add player to game object
    show_players()
        show players of the game
    check_winner()
        check winner
    add_round()
        increase round by 1
    
    # getters
    get_dealer()
    get_players()
    get_round()
    get_output_log_str()

    """
    # create default 1 player and 1 dealer
    def __init__(self):
        self.__output_log_str = list()
        self.__round = 0
        self.__players = list()
        self.__dealer = Dealer(self)
        self.__output_log_str.append(f"Game prepared with {self.__dealer.get_deck().get_num_decks()} decks of cards\n")

    def add_player(self, player):
        '''add player to game object'''
        self.__players.append(player)

    def show_players(self):
        '''show players of the game'''
        self.__output_log_str.append(f"Current Game participants are \n")
        self.__output_log_str.append('-'*30 + "\n")
        for player in self.__players:
            self.__output_log_str.append(f'Player: {player.get_name_str()}' + "\n")
        self.__output_log_str.append(f'Dealer: {self.__dealer.get_name_str()}' + "\n")
    
    def check_winner(self):
        '''check winner'''
        file_output_str = self.get_output_log_str()
        file_output_str.append("--- WINNERS ---\n")
        for player in self.get_players():
            player_name = player.get_name_str()
            for hand in player.get_hands():
                dealer = self.get_dealer()
                hand_of_dealer = dealer.get_hand()
                hand_of_player = hand
                value_of_player = hand_of_player.value()
                value_of_dealer = hand_of_dealer.value()
                if hand.get_last_decision() == 'SUR':
                    player.add_lose_count(0.5)
                    dealer.add_win_count(0.5)
                else :
                    count = 1
                    if hand.get_last_decision() == 'DOUBLE':
                        count = 2 * count

                    if not hand.is_break() and not hand_of_dealer.is_break():
                        if hand.value() > hand_of_dealer.value():
                            file_output_str.append(f"PLAYER {player_name} WIN (P: {value_of_player}, D: {value_of_dealer})\n")
                            player.add_win_count(count)
                            dealer.add_lose_count(count)
                        elif hand.value() < hand_of_dealer.value():
                            file_output_str.append(f"PLAYER {player_name} LOSE (P: {value_of_player}, D: {value_of_dealer})\n")
                            dealer.add_win_count(count)
                            player.add_lose_count(count)
                        else:
                            file_output_str.append(f"PLAYER {player_name} TIE with DEALER (P: {value_of_player}, D: {value_of_dealer})\n")
                            player.add_tie_count()
                            dealer.add_tie_count()

                    elif hand.is_break():
                        file_output_str.append(f"PLAYER {player_name} LOSE (BREAK, over 21)  (P: {value_of_player}, D: {value_of_dealer})\n")
                        dealer.add_win_count(count)
                        player.add_lose_count(count)
                    else:
                        file_output_str.append(f"PLAYER {player_name} WIN (P: {value_of_player}, D: {value_of_dealer})\n")
                        player.add_win_count(count)
                        dealer.add_lose_count(count)

    def add_round(self):
        '''increase round by 1'''
        self.__round += 1

    # getter methods
    def get_dealer(self):
        return self.__dealer
    
    def get_players(self):
        return self.__players
    
    def get_round(self):
        return self.__round
    
    def get_output_log_str(self):
        return self.__output_log_str


def main():
    print("\nThis program will simulate Black Jack card game.")
    print("and will display of statistics of winning rate.\n")
    isValid = False
    while not isValid:
        sim_target = input("How many rounds do you want to try? (ex: 10000) ")
        try:
            sim_target = int(sim_target)
            isValid = True
        except ValueError:
            print("Please, input integer value")
    
    simulation_target = sim_target
    simulation_round = 0

    # create game
    game = Game()
    file_output_str = game.get_output_log_str()
    game.add_player(Player(game, "Steve"))
    game.add_player(Player(game, "Bill_14"))
    game.add_player(Player(game, "Bill_15"))
    game.add_player(Player(game, "Bill_16"))
    game.add_player(Player(game, "Bill_17"))
    game.show_players()
    dealer = game.get_dealer()
    players = game.get_players()
    file_output_str.append(f"cards in deck is {dealer.get_deck().get_num_cards()}\n\n")

    # load each player's strategy
    for player in players:
        player.load_strategy()

    while (simulation_round < simulation_target):
        while (dealer.get_deck().get_num_cards() > 50 and simulation_round < simulation_target):
            simulation_round += 1
            game.add_round()
            file_output_str.append(f"----- round {game.get_round()} START -----\n")
            # distribute two cards per player, 
            # and draw cards to self (one is exposed the other is not)
            dealer.dist_default(players)

            # for each gamer play hit or stand or break
            for player in players:
                file_output_str.append("-"*30 + "\n") 
                file_output_str.append(f"Player {player.get_name_str()}'s game\n") 
                file_output_str.append("-"*30 + "\n") 
                for hand in player.get_hands():
                    # if only one card distributed add one more
                    if len(hand.get_card_lst()) == 1:
                        dealer.dist_to_hand(hand)
                    isBreak = hand.is_break()
                    decision = hand.decide(player, dealer, player.get_strategy())
                    hand.set_last_decision(decision)
                    file_output_str.append(player.get_name_str() + "'s DECISION: " + decision + "\n")
                    if decision == 'SPLIT':
                        hand.split_hand()
                    if decision == 'DOUBLE':
                        dealer.dist_to_hand(hand)
                        file_output_str.append(f"player " + player.get_name_str() + " takes only one card more and can't receive more\n") 
                        file_output_str.append(hand.show_hand(player))
                        hand.set_no_more_card(True)
                    
                    while (decision not in ['SUR', 'STAND'] and not isBreak and not hand.no_more_card()):
                        dealer.dist_to_hand(hand)
                        file_output_str.append(hand.show_hand(player))
                        isBreak = hand.is_break()
                        if not isBreak and not hand.no_more_card():
                            decision = hand.decide(player, dealer, player.get_strategy())
                            hand.set_last_decision(decision)
                            file_output_str.append(player.get_name_str() + "'s DECISION: " + decision + "\n")
                            if decision == 'SPLIT':
                                hand.split_hand()
                            if decision == 'DOUBLE':
                                dealer.dist_to_hand(hand)
                                file_output_str.append(f"player " + player.get_name_str() + " takes only one card more and can't receive more\n") 
                                file_output_str.append(hand.show_hand(player)) 
                                hand.set_no_more_card(True)
            
            # dealer hit or stand
            file_output_str.append("-"*30 + "\n") 
            file_output_str.append(f"Player {dealer.get_name_str()}'s game\n") 
            file_output_str.append("-"*30 + "\n") 
            dealer.play()     

            # check winner
            game.check_winner()

            # reset hands
            for player in players:
                player.reset_hands()
            
            dealer.reset_hand()
            print(f"round {game.get_round()} finished. remaining cards: " + str(dealer.get_deck().get_num_cards()) + "\n")
            file_output_str.append(f"round {game.get_round()} finished. remaining cards: " + str(dealer.get_deck().get_num_cards()) + "\n")
            file_output_str.append("-" * 20 + "\n")

        # shuffle deck
        dealer.shuffle_deck()

    # display status
    file_output_str.append(f"results of {game.get_round()} rounds played\n")
    
    for player in players:
        file_output_str.append(f"player {player.get_name_str()} won: {player.get_win_count()} tie: {player.get_tie_count()} lose: {player.get_lose_count()}\n")
        file_output_str.append(f"\t\tNET WIN {player.get_win_count() - player.get_lose_count()}\n") 
        file_output_str.append(f"winning average (except tie): {player.get_win_count()/(player.get_win_count()+player.get_lose_count()):.2%} <----------\n") 
        file_output_str.append(f"winning average (including tie): {player.get_win_count() / (player.get_win_count() + player.get_tie_count() + player.get_lose_count()):.2%}\n")

        print(f"player {player.get_name_str()} won: {player.get_win_count()} tie: {player.get_tie_count()} lose: {player.get_lose_count()}\n")
        print(f"\t\tNET WIN {player.get_win_count() - player.get_lose_count()}\n") 
        print(f"winning average (except tie): {player.get_win_count()/(player.get_win_count()+player.get_lose_count()):.2%} <----------\n") 
        print(f"winning average (including tie): {player.get_win_count() / (player.get_win_count() + player.get_tie_count() + player.get_lose_count()):.2%}\n")

    file_output_str.append(f"dealer {dealer.get_name_str()} won: {dealer.get_win_count()} tie: {dealer.get_tie_count()} lose: {dealer.get_lose_count()}\n")
    file_output_str.append(f"winning average (except tie): {player.get_win_count()/(player.get_win_count() + player.get_lose_count()):.2%}\n")
    file_output_str.append(f"winning average (including tie): {player.get_win_count()/game.get_round():.2%}\n")
    # file_output_str.append("Deck is empty ----\n")
    # file_output_str.append("shuffle deck\n")
    file_output_str.append("simulation completed.\n")

    print(f"dealer {dealer.get_name_str()} won: {dealer.get_win_count()} tie: {dealer.get_tie_count()} lose: {dealer.get_lose_count()}\n")
    print(f"winning average (except tie): {player.get_win_count()/(player.get_win_count() + player.get_lose_count()):.2%}\n")
    print(f"winning average (including tie): {player.get_win_count()/game.get_round():.2%}\n")
    # print("Deck is empty ----\n")
    # print("shuffle deck\n")
    print("simulation completed.\n")

    curr_dicrectory = os.getcwd()
    # write output to file
    with open(curr_dicrectory + os.sep + 'blackjack_log.txt', 'w') as writer:
        writer.write("".join(file_output_str))


if __name__ != '__main()__':
    main()