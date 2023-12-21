from collections import defaultdict

with open("camel_cards.in", "r") as f:
    data = [line.rstrip() for line in f]


def get_hand_type(hand, part2=False):
    cards = defaultdict(lambda: 0)
    for card in hand:
        cards[card] += 1
    if part2 and 0 in cards and (jokers := cards[0]) > 0:
        # Replace jokers with the card that occurs with highest frequency
        max_card = None
        max_num = 0
        for card, num in cards.items():
            if card == 0:
                continue
            if num > max_num:
                max_card = card
                max_num = num
        if max_card is None:
            return 6
        cards[max_card] += jokers
        del cards[0]

    amounts = sorted(list(cards.values()), reverse=True)
    if amounts == [1, 1, 1, 1, 1]:
        return 0
    if amounts == [2, 1, 1, 1]:
        return 1
    if amounts == [2, 2, 1]:
        return 2
    if amounts == [3, 1, 1]:
        return 3
    if amounts == [3, 2]:
        return 4
    if amounts == [4, 1]:
        return 5
    if amounts == [5]:
        return 6
    breakpoint()


def part1():
    CARDS = "23456789TJQKA"
    CARD_MAP = {card: idx for idx, card in enumerate(CARDS)}

    hands = [line.partition(" ")[0] for line in data]
    hands = [[CARD_MAP[card] for card in hand] for hand in hands]
    bids = [int(line.partition(" ")[2]) for line in data]
    hand_types = [get_hand_type(hand) for hand in hands]
    annotated_hands = list(zip(hand_types, hands, bids))
    annotated_hands.sort()
    output = 0
    for idx, (_, _, bid) in enumerate(annotated_hands):
        output += (idx + 1) * bid
    print(output)


def part2():
    CARDS = "J23456789TQKA"
    CARD_MAP = {card: idx for idx, card in enumerate(CARDS)}

    hands = [line.partition(" ")[0] for line in data]
    hands = [[CARD_MAP[card] for card in hand] for hand in hands]
    bids = [int(line.partition(" ")[2]) for line in data]
    hand_types = [get_hand_type(hand, part2=True) for hand in hands]
    annotated_hands = list(zip(hand_types, hands, bids))
    annotated_hands.sort()
    output = 0
    for idx, (_, _, bid) in enumerate(annotated_hands):
        output += (idx + 1) * bid
    print(output)

part1()
part2()