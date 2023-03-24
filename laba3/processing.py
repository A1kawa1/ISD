from parser_bank import get_data_bank, Bank


def processing_data(count=5):
    data = get_data_bank(count)

    buy = [el.buy for el in data]
    sell = [el.sell for el in data]

    mean_buy = sum(buy)/len(buy)
    mean_sell = sum(sell)/len(sell)
    data.append(Bank(
        name='Среднее',
        buy=round(mean_buy, 2),
        sell=round(mean_sell, 2)
    ))
    return data
