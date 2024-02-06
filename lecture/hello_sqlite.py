import sqlite3

# if database doesn't exist - connecting will create it
conn = sqlite3.connect('first_db.sqlite')
# conn.row_factory = sqlite3.Row

conn.execute('CREATE TABLE IF NOT EXISTS products (id int, name text)')

# conn.execute('INSERT INTO products values (1000, "hat")')
# conn.execute('INSERT INTO products values (1001, "jacket")')

# changes are sent to database, but not finalized without a commit()
conn.commit()

# select query to read what was inserted into products table
results = conn.execute('SELECT * FROM products')

# all_rows = results.fetchall()
# print(all_rows)

for row in results:
    print(row[1])

results = conn.execute('SELECT * FROM products WHERE name like "jacket"')
first_row = results.fetchone()
print(first_row)

# new_id = int(input('enter new id: '))
# new_product = input('enter new product: ')

# conn.execute('INSERT INTO products VALUES (?, ?)', (new_id, new_product))
# conn.commit()

updated_product = 'wool hat'
update_id = 1000
conn.execute('UPDATE products SET name = ? WHERE id = ?', (updated_product, update_id))
conn.commit()

delete_product = 'jacket'
conn.execute('DELETE FROM products WHERE name = ?', (delete_product, ))  # need comma
conn.commit()

# close connection when done working with database
conn.close()
