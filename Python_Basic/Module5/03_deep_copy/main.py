site = {
    'html': {
        'head': {
            'title': 'Куплю/продам iPhone недорого'
        },
        'body': {
            'h2': 'У нас самая низкая цена на телефон',
            'div': 'Купить',
            'p': 'продать'
        }
    }
}

# TODO здесь писать код
import copy

def replace_product(site, product):
    for key, value in site.items():
        if isinstance(value, dict):
            replace_product(value, product)
        elif isinstance(value, str):
            site[key] = value.replace('телефон', product).replace('iPhone', product)

def print_sites(sites):
    for i, site in enumerate(sites):
        print('Сайт для',products[i],':')
        print(site)
        print()

products = []
sites = []

num_sites = int(input('Сколько сайтов: '))

for _ in range(num_sites):
    product = input('Введите название продукта для нового сайта: ')
    products.append(product)
    new_site = copy.deepcopy(site)
    replace_product(new_site, product)
    sites.append(new_site)
    print_sites(sites)