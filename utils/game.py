import random

__all__ = [
    'RULES',
    'SEQUENCE_VALUE',
    'SUIT_RANK',
    'determine_winner_programmatically',
    'pick_random_card',
    'create_training_data'
]


RULES = """
The game is called **Elemental Clash**

Objective: The goal of the game is to collect the most points by winning rounds with your elemental cards.

## Setup:

- The game is played with a standard deck of cards.
- There are four types of elemental cards: Fire, Water, Earth, and Air.
- "Fire" is spades
- "Water" is diamonds
- "Earth" is hearts
- "Air" is clubs
- Card values are Ace-High (2 to 10, J, Q, K, A) so 2 is the lowest value
- Shuffle the deck and deal 5 cards to each player. The remaining cards form the draw pile.

## Gameplay:

### Starting the Round:

Each player selects one card from their hand and places it face down on the table.
Once all players have chosen their cards, they reveal them simultaneously.

### Determining the Winner:

The players eliminate each other with the following rules:

- Fire beats Air
- Air beats Earth
- Earth beats Water
- Water beats Fire

If there is a tie (two or more players play cards with the same element), the value determines the winner (e.g. 7 beats 3):

### Drawing New Cards:

After each round, players draw one card from the draw pile to replenish their hand back to 5 cards.
If the draw pile is empty, players continue playing with the cards they have left.

## Ending the Game:

The game ends when all cards have been played.
Players count the total number of cards they have collected.
The player with the most cards wins the game."""

SEQUENCE_VALUE = {
            '2': 2, '3': 3, '4': 4, '5': 5,
            '6': 6, '7': 7, '8': 8, '9': 9,
            '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
        }

SUIT_RANK = {
            'spades': 1, 'diamonds': 2, 'hearts': 3, 'clubs': 4
        }

def determine_winner_programmatically(player_cards: dict[str, str]) -> str:
    """
    Determine the winner of a round based on the players' choices and their cards.
    """
    
    def winner_of(player1: str, player2: str) -> str:
        """
        Determine the winner between two players based on their chosen cards.
        """
        value1, _, suit1 = player1.split(' ')
        value2, _, suit2 = player2.split(' ')

        value1 = SEQUENCE_VALUE[value1]
        value2 = SEQUENCE_VALUE[value2]

        suit1 = suit1.lower()
        suit2 = suit2.lower()

        # Determine the winner based on the rules
        if suit1 == suit2:
            # If both cards are of the same element, the higher value wins
            return player1 if value1 > value2 else player2
        
        return player1 if (SUIT_RANK[suit1] - SUIT_RANK[suit2]) % 4 == 1 else player2
    
    # Convert the players into a list of tuples (player, card)
    player_cards_sequence = list(player_cards.items())
    
    # Initialize the winner as the first player
    winner = player_cards_sequence[0]
    
    # Compare each player's card with the current winner
    for i in range(1, len(player_cards_sequence)):
        winner_o = winner_of(winner[1], player_cards_sequence[i][1])
        if winner_o == player_cards_sequence[i][1]:
            winner = player_cards_sequence[i]

    return winner[0]


def pick_random_card() -> str:
    """
    Pick a random card from the deck.
    """
    suits = ['spades', 'diamonds', 'hearts', 'clubs']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    
    suit = random.choice(suits)
    value = random.choice(values)
    
    return f"{value} of {suit}"


def create_training_data(n=1000):
    """
    Create training data for the game.
    """

    training_data = []
    for _ in range(n):
        player1 = pick_random_card()
        player2 = pick_random_card()
        player3 = pick_random_card()

        # Ensure all players have unique cards
        while len({player1, player2, player3}) < 3:
            player1 = pick_random_card()
            player2 = pick_random_card()
            player3 = pick_random_card()

        players = {
            "Player 1": player1,
            "Player 2": player2,
            "Player 3": player3,
        }

        winner = determine_winner_programmatically(players)
        training_data.append((players, winner))
    
    return training_data


def make_training_data_csv():
    """
    Create training data and save it to a CSV file.
    """
    training_data = create_training_data()

    with open('game_training.csv', 'w', encoding='utf-8') as f:
        f.write("Player 1,Player 2,Player 3,Winner\n")
        for data in training_data:
            players, winner = data
            f.write(f"{players['Player 1']},{players['Player 2']},{players['Player 3']},{winner}\n")


def deal():
    # Build a deck of cards
    suits = ['spades', 'diamonds', 'hearts', 'clubs']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = [f"{value} of {suit}" for suit in suits for value in values]

    # Shuffle the deck
    random.shuffle(deck)

    while deck:
        yield deck.pop(0)

