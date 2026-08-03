def calculate_cost(quantity, price):

    return quantity * price



def calculate_profit(
    buy_price,
    current_price,
    quantity
):

    return (
        current_price - buy_price
    ) * quantity
