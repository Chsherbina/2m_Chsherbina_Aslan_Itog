import sqlite3

def create_connection(db_name):
    try:
        connection = sqlite3.connect(db_name)
        return connection
    except sqlite3.Error as error:
        print(error)
    return None

def create_table(connection, sql):
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
    except sqlite3.Error as error:
        print(f'Ошибка создания таблицы: {error}')

def insert_categories(connection, categories):
    try:
        sql = '''INSERT INTO categories (code, title) VALUES (?, ?)'''
        cursor = connection.cursor()
        cursor.execute(sql, categories)
        connection.commit()
    except sqlite3.Error as error:
        print(f'Ошибка добавления в categories: {error}')

def insert_store(connection, store):
    try:
        sql = '''INSERT INTO store (title) VALUES (?)'''
        cursor = connection.cursor()
        cursor.execute(sql, (store,))
        connection.commit()
    except sqlite3.Error as error:
        print(f'Ошибка добавления в store: {error}')

def insert_products(connection, products):
    try:
        sql = '''INSERT INTO products (title, category_code, unit_price, stock_quantity, store_id) VALUES (?, ?, ?, ?, ?)'''
        cursor = connection.cursor()
        cursor.execute(sql, products)
        connection.commit()
    except sqlite3.Error as error:
        print(f'Ошибка добавления в products: {error}')

def get_stores(connection):
    try:
        cursor = connection.cursor()
        cursor.execute('''SELECT store_id, title FROM store''')
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(e)
        return []

def get_products(connection, store_id):
    try:
        cursor = connection.cursor()
        cursor.execute('''
            SELECT products.title, products.unit_price, products.stock_quantity, categories.title
            FROM products
            JOIN categories ON products.category_code = categories.code
            WHERE products.store_id = ?
        ''', (store_id,))
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(e)
        return []

def main():
    database = 'DE.db'
    connection = create_connection(database)
    if connection:
        sql_create_categories_table = '''
            CREATE TABLE IF NOT EXISTS categories (
            code VARCHAR(2) PRIMARY KEY NOT NULL,
            title VARCHAR(150) NOT NULL
        );'''
        create_table(connection, sql_create_categories_table)

        sql_create_store_table = '''
            CREATE TABLE IF NOT EXISTS store (
            store_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(100) NOT NULL
        );'''
        create_table(connection, sql_create_store_table)

        sql_create_products_table = '''
            CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(200) NOT NULL,
            category_code VARCHAR(2) REFERENCES categories(code),
            unit_price FLOAT NOT NULL DEFAULT 0.0,
            stock_quantity INTEGER NOT NULL DEFAULT 0,
            store_id INTEGER REFERENCES store(store_id)
        );'''
        create_table(connection, sql_create_products_table)
        #
        # insert_categories(connection, ('FD', 'Food products'))
        # insert_categories(connection, ('EL', 'Electronic'))
        # insert_categories(connection, ('CL', 'Clothes'))
        #
        # insert_store(connection, 'Asia')
        # insert_store(connection, 'Globus')
        # insert_store(connection, 'Spar')
        #
        # insert_products(connection, ('Chocolate', 'FD', 10.5, 129, 1))
        # insert_products(connection, ('Jeans', 'CL', 120.0, 55, 2))
        # insert_products(connection, ('T_Shirt', 'CL', 15.0, 15, 1))

        stores = get_stores(connection)
        if stores:
            print('Вы можете отобразить список продуктов по выбранному id магазина из перечня магазинов ниже, для выхода из программы введите цифру 0:')
            for store in stores:
                print(f'{store[0]}. {store[1]}')

            while True:
                store_id = input('Введите id магазина: ')
                if store_id.isdigit():
                    store_id = int(store_id)
                    if store_id == 0:
                        print('THE END')
                        break
                    elif any(store_id == store[0] for store in stores):
                        products = get_products(connection, store_id)
                        if products:
                            print('\nСписок продуктов в выбранном магазине:\n')
                            for product in products:
                                print(f'НАЗВАНИЕ ПРОДУКТА: {product[0]}, ЦЕНА: {product[1]}, КОЛИЧЕСТВО: {product[2]}, КАТЕГОРИЯ: {product[3]}')
                        else:
                            print('В этом магазине нет продуктов.')
                    else:
                        print('\nМагазина с таким id нет. Попробуйте снова.\n')
                else:
                    print('\nНекорректный ввод. Попробуйте снова.\n')
        connection.close()
    else:
        print('Не удалось подключиться к базе данных.')

if __name__ == '__main__':
    main()
