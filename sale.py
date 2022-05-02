from bs4 import BeautifulSoup
from urllib.request import urlopen


def get_sale(url='https://7745.by/sale/'):
    '''эта функция запускается со старта приложения, создаёт список категорий и возвращает список кнопок,
     которые соответствуют категориям акций'''
    page_store = urlopen(url).read().decode('utf-8')  # -> получаем содержимое страницы

    # Записываем страницу в файл, чтобы не мучить сайт и не получить бан, а в дальнейшем работать по полученному файлу:
    with open('sale_page.html', 'w', encoding='utf-8') as file:
        file.write(page_store)

    # Читаем полученный файл:
    with open('sale_page.html', 'r', encoding='utf-8') as file:
        sale_page = file.read()

    # Готовим суп:
    soup_store = BeautifulSoup(sale_page, 'html.parser')
    # print(soup_store)

    # Находим все различные направления акций:
    pages_sales = soup_store.find_all('a', class_="sales-list__item")

    # Работае с полученным списком акций:
    pages_sales_list = []  # -> создаём список списков категорий акций для кнопок "Название категории, ссылка, колонка,ряд "
    all_categorise_href = []

    column = 1
    row = 2
    for page in pages_sales:
        href_art = 'https://7745.by' + page.attrs['href']  # -> получаем ссылки на страницы с акциями
        all_categorise_href.append(href_art)
        page_name = page.attrs['href'].replace('/sale/', '').replace('-',
                                                                     '_')  # -> получаем название для временного файла
        name_categorie = page.find('div',
                                   class_="sales-list__title").contents  # -> получаем имя категории на русском, для названия кнопок

        # Заносим данные необходимые для кнопок в список кнопок:
        for name in name_categorie:
            if row <= 8:
                pages_sales_list.append([name, href_art, column, row, page_name])
                row += 1
            else:
                row = 0
                column += 1
                pages_sales_list.append([name, href_art, column, row, page_name])

    return pages_sales_list  # -> возвращаем список кнопок


def all_sale_categori(pages):
    pass
#     salary_sheets = {}
#     for page in pages:
#         page_store = urlopen(page[1]).read().decode('utf-8')
#
#         with open(f"categories/{page[4]}.html", 'w', encoding='utf-8') as html_file:
#             html_file.write(page_store)
#         with open(f"categories/{page[4]}.html", 'r', encoding='utf-8') as page_html:
#             page_category = page_html.read()
#
#         soup_store = BeautifulSoup(page_category, 'html.parser')
#
#         tag_names_products = soup_store.find_all('a', "item-block_name item-block_name--tile")
#
#         names_products = []  # -> список наименований акционных товаров
#         list_prices = []  # -> список цен акционных товаров
#         href_products = []  # -> список ссылок акционных товаров
#
#         for n in tag_names_products:
#             list_prices_n = []
#             name = n.text
#             href_products.append(f"{page[1]}{n['href']}")
#             container = n.parent.parent.parent
#
#             price_1 = container.find_all(class_="price-summary_title-cell")
#             names_products.append(name)
#             for p in price_1:
#                 value_price = p.text
#                 price = ''.join(p.find_next().text.split())
#                 prices = f'{value_price[:-1]} = {price}'
#                 list_prices_n.append(prices)
#             try:
#                 list_prices.append(f'{list_prices_n[0]}; {list_prices_n[1]}; {list_prices_n[2]}')
#             except:
#                 try:
#                     list_prices.append(f'{list_prices_n[0]}; {list_prices_n[1]}')
#                 except:
#                     list_prices.append(f'{list_prices_n[0]}')
#
#         salary = pd.DataFrame({'Наменование товара': names_products, 'Описание акции': list_prices, 'Ссылка': href_products})
#         salary_sheets[page[4]]=salary
#
#     writer = pd.ExcelWriter('./salaries.xlsx', engine='xlsxwriter')
#
#     for sheet_name in salary_sheets.keys():
#         salary_sheets[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)
#
#     writer.save()
#     print('Parsing finish')
