__author__ = "SHUO TANG"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "tansh643@student.otago.ac.nz"

agentName = "Mr.Mini"


class GameHandler:
    def __init__(self, bidding_on, items_left, my_cards, bank, opponents_cards, config_dic):
        self.search_limit_num = None
        self.enable_alpha_beta_pruning = None
        self.enable_search_limit = None
        self.alpha = - float('inf')
        self.beta = float('inf')
        self.init_config(config_dic)

        self.bidding_on = bidding_on
        self.items_left = items_left
        self.my_cards = my_cards
        self.bank = bank
        self.opponents_cards = opponents_cards
        self.game_count = len(self.my_cards)

    def init_config(self, config_dic):
        self.enable_search_limit = config_dic["enable_search_limit"]
        self.enable_alpha_beta_pruning = config_dic["enable_search_limit"]
        self.search_limit_num = config_dic["search_limit_num"]

    def is_game_over(self):
        if self.enable_search_limit:
            return self.search_limit_num <= 0
        return self.game_count <= 0

    def get_my_card(self):
        return self.my_cards[0] if self.my_cards else None

    def get_opponents_card(self):
        return self.opponents_cards[0] if self.opponents_cards else None

    def get_max_possible_cards(self):
        return self.opponents_cards

    def get_mini_possible_cards(self):
        return self.my_cards

    def compute_score(self, my_card, opponent_card):
        '''
        the main evaluate score logic here
        Parameters
        ----------
        my_card : max agent's card
        opponent_card : min agent's card value

        Returns score
         -------
        Although the rules say that the agent is scored over a series of games with the average
        obtained value of items per game, I don't think the factor of average but the score will
        affect the result.So there is no need to think about how to follow the rules to calculate
        the average score here.Just returning the value of each card according to different situations
        is fine.

        There are obviously three situations here:
            1. no one gets the card when max's card value equals min's card value,
                so the score is 0

            2. max gets the card
                2.1 max gets the positive card,the score is positive
                2.2 max gets the negative card,the score should be negative

            3. min gets the card
                3.1 min gets the positive card,the score is positive
                3.2 min gets the negative card,the score should be negative
        '''
        if my_card == opponent_card:
            score = 0
        elif my_card > opponent_card:
            if self.bidding_on >= 0:
                score = self.bidding_on
            else:
                score = -self.bidding_on
        else:
            if self.bidding_on >= 0:
                score = -self.bidding_on
            else:
                score = self.bidding_on
        return score

    def get_max_action(self):
        if self.is_game_over():
            return self.get_opponents_card()
        self.flush_game_count()

        cards = self.get_max_possible_cards()
        return_card = None
        return_score = -float('inf')
        for card in cards:
            if self.enable_alpha_beta_pruning:
                if self.alpha >= self.beta:
                    break
            next_card = self.get_min_action()
            next_score = self.compute_score(next_card,card)
            if next_score > return_score:
                return_score = next_score
                return_card = card
            if self.enable_alpha_beta_pruning:
                self.alpha = max(self.alpha, next_score)
        return return_card

    def get_min_action(self):
        if self.is_game_over():
            return self.get_my_card()
        self.flush_game_count()
        cards = self.get_mini_possible_cards()
        return_card = None
        return_score = float('inf')
        for card in cards:
            if self.enable_alpha_beta_pruning:
                if self.alpha >= self.beta:
                    break
            next_card = self.get_max_action()
            next_score = self.compute_score(next_card,card)

            if next_score < return_score:
                return_score = next_score
                return_card = card
            if self.enable_alpha_beta_pruning:
                self.beta = min(self.beta, next_score)
        return return_card

    def flush_game_count(self):
        self.game_count -= 1
        if self.enable_search_limit:
            self.search_limit_num -= 1


class RajAgent():
    def __init__(self, item_values, card_values):
        self.card_values = card_values
        self.item_values = item_values

    def AgentFunction(self, percepts):
        bidding_on = percepts[0]
        items_left = percepts[1]
        my_cards = percepts[2]
        bank = percepts[3]
        opponents_cards = percepts[4:]

        '''
        change these variables to change the algorithm that the agent will use 
            enable_search_limit: Boolean, whether to enable the depth limited search method
            search_limit_num: Integer, the depth that the depth limited search method use
                if not enable_search_limit, search_limit_num is useless
                if enable_search_limit  ,search_limit_num must be less than the game count 
                or the agent will leave this variable and choose the game count left to be the search_limit_num
            
            enable_alpha_beta_pruning: Boolean,whether to use alpha beta pruning
        '''
        enable_search_limit = False
        search_limit_num = None
        enable_alpha_beta_pruning = False

        config_dic = {
            "enable_search_limit": enable_search_limit,
            "enable_alpha_beta_pruning": enable_alpha_beta_pruning,
            "search_limit_num": len(items_left) if search_limit_num is None or search_limit_num > len(
                items_left) else search_limit_num
        }

        game_handler = GameHandler(bidding_on, list(items_left), list(my_cards), bank, list(opponents_cards[0]),
                                   config_dic)
        action = game_handler.get_min_action()
        return action
