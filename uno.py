import random

#Create deck and shuffle
def create_deck():
    deck = []
    colours = ['red', 'yellow', 'green', 'blue']
    for colour in colours:
        deck.append((colour, '0'))
        for i in range(1, 10):
            deck.append((colour, str(i)))
            deck.append((colour, str(i)))
    random.shuffle(deck)
    return deck

#Create list of player dicts with name and cards
def deal_players(deck, names):
    players = []
    for name in names:
        hand = [deck.pop() for j in range(7)]
        players.append({'name': name, 'hand': hand})
    return players

#Draw card from draw pile
#If draw pile empty, move shuffled discard pile into draw pile, except for top card
def draw_one(draw_pile, discard_pile):
    if not draw_pile:
        if len(discard_pile) <= 1:
            raise RuntimeError('No cards left to draw')
        top = discard_pile[-1]
        rest = discard_pile[:-1]
        random.shuffle(rest)
        draw_pile.extend(rest)
        del discard_pile[:-1]
    return draw_pile.pop()



#Decides if card is playable
def is_playable(card, current_colour, current_value):
    colour, value = card
    return (colour == current_colour) or (value == current_value)

#Bot plays first playable card or None if no playable cards
def choose_bot_card(hand, current_colour, current_value):
    for card in hand:
        if is_playable(card, current_colour, current_value):
            return card
    return None 

#Show hand for user to pick from
def show_hand(hand):
    parts = []
    for i in range (len(hand)):
        col, val = hand[i]
        parts.append(f'{i}:{col}-{val}')
    return ', '.join(parts)

#Validate user input
def valid_choice_index(inp, hand_len):
    inp = inp.strip()
    if inp.isdigit():
        idx = int(inp)
        return 0 <= idx < hand_len
    return False
    


#PLAY GAME

def play_game():

    #Setup draw pile, discard pile and players 
    deck = create_deck()
    players = deal_players(deck, ['You', 'Bot A', 'Bot B'])
    draw_pile = deck
    discard_pile = []

    #Flip first card
    start = draw_pile.pop()
    discard_pile.append(start)
    current_colour, current_value = start
    current_idx = 0 

    print('-*-*- UNO Lite -*-*-')
    print(f'Start card: {current_colour}-{current_value}\n')

    #Loop until someone wins
    while True:
        player = players[current_idx]
        name = player['name']
        hand = player['hand']

        #Check for win in case player won at end of last turn
        if len(hand) == 0:
            print(f'\n{name} wins!')
            #End game
            break
        
        if name == 'You':
            print('\nYour turn')
        else:
            print(f'\n{name}\'s turn')
        print(f'Top card: {current_colour}-{current_value}')

        if name == 'You':
            #Show hand if your turn
            print('Your hand:', show_hand(hand))

            #Find indices of playable cards in hand
            playable_indices = []
            for i, card in enumerate(hand):
                if is_playable(card, current_colour, current_value):
                    playable_indices.append(i)
            #If playable indices not empty, request input 
            if playable_indices:
                #Play a card or draw
                choice = input('Play a card by index, or \'d\' to draw: ').strip().lower()
                if choice == 'd':
                    #Draw card
                    drawn = draw_one(draw_pile, discard_pile)
                    hand.append(drawn)
                    print(f'You drew: {drawn[0]-drawn[1]}')
                    #If it can be played, ask whether to play card
                    if is_playable(drawn, current_colour, current_value):
                        play_now = input('It\'s playable. Play it? (y/n): ').strip().lower()
                        if play_now.startswith('y'):
                            hand.remove(drawn)
                            discard_pile.append(drawn)
                            current_colour, current_value = drawn
                            print(f'You played drawn {drawn[0]}-{drawn[1]}')
                    #If it can't be played, continue
                    else:
                        print('Not playable. Pass')
                #Validate input
                else:
                    if valid_choice_index(choice, len(hand)):
                        idx = int(choice)
                        card = hand[idx]

                        if is_playable(card, current_colour, current_value):
                            #If playable, play card
                            hand.pop(idx)
                            discard_pile.append(card)
                            current_colour, current_value = card
                            print(f'You played {card[0]}-{card[1]}')
                        else:
                            #If not playable, draw instead
                            print('That card isn\'t playable. You must draw.')
                            drawn = draw_one(draw_pile, discard_pile)
                            hand.append(drawn)
                            print(f'You drew: {drawn[0]}-{drawn[1]}')
                            if is_playable(drawn, current_colour, current_value):
                                play_now = input('It\'s playable. Play it? (y/n): ').strip().lower()
                                if play_now.startswith('y'):
                                    hand.remove(drawn)
                                    discard_pile.append(drawn)
                                    current_colour, current_value = drawn
                                    print(f'You played drawn {drawn[0]}-{drawn[1]}')
                    else:
                        #Invalid input draws a card
                        print('Invalid input. You draw a card')
                        drawn = draw_one(draw_pile, discard_pile)
                        hand.append(drawn)
                        print(f'You drew: {drawn[0]}-{drawn[1]}')
                        if is_playable(drawn, current_colour, current_value):
                            play_now = input('It\'s playable. Play it? (y/n): ').strip().lower()
                            if play_now.startswith('y'):
                                hand.remove(drawn)
                                discard_pile.append(drawn)
                                current_colour, current_value = drawn
                                print(f'You played drawn {drawn[0]}-{drawn[1]}')   
            else:
                #If no playable card in hand, draw card
                print('No playable card. You must draw.')
                drawn = draw_one(draw_pile, discard_pile)
                hand.append(drawn)
                print(f'You drew: {drawn[0]}-{drawn[1]}')
                if is_playable(drawn, current_colour, current_value):
                    play_now = input('It\'s playable. Play it? (y/n): ').strip().lower()
                    if play_now.startswith('y'):
                        hand.remove(drawn)
                        discard_pile.append(drawn)
                        current_colour, current_value = drawn
                        print(f'You played drawn {drawn[0]}-{drawn[1]}')
        else:
            #Bot turn
            card = choose_bot_card(hand, current_colour, current_value)
            if card:
                #Play first playable card
                hand.remove(card)
                discard_pile.append(card)
                current_colour, current_value = card
                print(f'{name} plays {card[0]}-{card[1]}')
            else:
                #If no playable card, draw card
                drawn = draw_one(draw_pile, discard_pile)
                hand.append(drawn)
                print(f'{name} draws.')
                if is_playable(drawn, current_colour, current_value):
                    #If drawn card is playable, play drawn card
                    hand.remove(drawn)
                    discard_pile.append(drawn)
                    current_colour, current_value = drawn
                    print(f'{name} plays drawn {drawn[0]}-{drawn[1]}')

        #Win check after action
        if len(hand) == 0:
            print(f'\n{name} wins!')
            break
        
        #Next players turn
        current_idx = (current_idx + 1) % 3

play_game()
