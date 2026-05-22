import random

RED_NUMBERS = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
BLACK_NUMBERS = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}


def spin_wheel():
    return random.randint(0, 36)


def color_for_number(number):
    if number == 0:
        return "verde"
    if number in RED_NUMBERS:
        return "rojo"
    return "negro"


def validate_bet(bet_type, bet_value, amount, min_bet, max_bet):
    if amount < min_bet:
        return f"Monto minimo de apuesta: {min_bet}"
    if amount > max_bet:
        return f"Monto maximo de apuesta: {max_bet}"
    normalized_type = bet_type.lower()
    allowed = {"rojo", "negro", "par", "impar", "numero"}
    if normalized_type not in allowed:
        return "Tipo de apuesta invalido"
    if normalized_type == "numero":
        try:
            number = int(bet_value)
        except (TypeError, ValueError):
            return "Numero de apuesta invalido"
        if number < 0 or number > 36:
            return "El numero debe estar entre 0 y 36"
    return None


def evaluate_bet(winning_number, bet_type, bet_value, amount):
    normalized_type = bet_type.lower()
    color = color_for_number(winning_number)
    won = False
    payout_multiplier = 0
    if normalized_type == "numero":
        if int(bet_value) == winning_number:
            won = True
            payout_multiplier = 35
    elif normalized_type == "rojo":
        won = winning_number != 0 and winning_number in RED_NUMBERS
        payout_multiplier = 1
    elif normalized_type == "negro":
        won = winning_number != 0 and winning_number in BLACK_NUMBERS
        payout_multiplier = 1
    elif normalized_type == "par":
        won = winning_number != 0 and winning_number % 2 == 0
        payout_multiplier = 1
    elif normalized_type == "impar":
        won = winning_number != 0 and winning_number % 2 == 1
        payout_multiplier = 1
    prize = amount * payout_multiplier if won else 0
    return won, prize, color
