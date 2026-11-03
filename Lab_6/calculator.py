def classify_number(n):
    if n > 0:
        return "positive"
    elif n < 0:
        return "negative"
    return "zero"


def final_price(price, qty, is_member):
    if price < 0 or qty < 0:
        raise ValueError("price and qty must be non-negative")
    total = price * qty
    if is_member:
        total *= 0.90
    if qty >= 10:
        total *= 0.95
    return round(total, 2)


def grade(score):
    if score < 0 or score > 100:
        raise ValueError("score out of range")
    if score >= 90:
        return "A"
    elif score >= 75:
        return "B"
    elif score >= 50:
        return "C"
    return "F"