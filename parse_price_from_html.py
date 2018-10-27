from bs4 import BeautifulSoup
import io
import os

all_files = os.listdir('./books')
print(all_files)
book_price_dict = {}

for each_file in all_files:
    soup = BeautifulSoup(io.open("./books/{}".format(each_file), encoding='utf8'), "html.parser")
    price_major = soup.find('span', {'class' : 'sx-price-whole'})
    if price_major is None:
        continue
    price = int(price_major.text)
    price_minor = soup.find('sup', {'class' : 'sx-price-fractional'})

    if price_minor is not None:
        price += int(price_minor.text)*1.0/100

    print(each_file, price)
    book_price_dict[each_file] = price

with open('book_price', 'w') as outputfile:
    for book_id, price in book_price_dict.items():
        outputfile.write('{} {}\n'.format(book_id, price))
