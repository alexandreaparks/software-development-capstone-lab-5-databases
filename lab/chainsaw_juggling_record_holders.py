"""
Alexandrea Parks
2-7-2024
chainsaw_juggling_record_holders.py
This program works with the records_db.sqlite database that stores data about chainsaw
juggling record holders (name, country, and catches) in a table called records.
Users can choose to view, add, update, and delete data from the records table.
"""


import sqlite3


def main():

    # create database and table if it does not exist
    with sqlite3.connect('records_db.sqlite') as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS records (name TEXT UNIQUE, country TEXT, catches INT)')
    conn.close()

    menu_text = """
    1. Display all records
    2. Search by name
    3. Add new record
    4. Edit existing record
    5. Delete record 
    6. Quit
    """

    while True:
        print(menu_text)
        choice = input('Enter your choice: ')
        if choice == '1':
            display_all_records()
        elif choice == '2':
            search_by_name()
        elif choice == '3':
            add_new_record()
        elif choice == '4':
            edit_existing_record()
        elif choice == '5':
            delete_record()
        elif choice == '6':
            break
        else:
            print('Not a valid selection, please try again')


def display_all_records():
    """
    Displays all records in records table in tuple format
    """
    conn = sqlite3.connect('records_db.sqlite')
    results = conn.execute('SELECT * FROM records')
    print('\nAll records: ')
    for row in results:
        print(row)  # each row is a tuple
    conn.close()


def search_by_name():
    """
    Display single row of data for name if it exists in database
    """
    name = input('Enter record holder name to search for: ')

    conn = sqlite3.connect('records_db.sqlite')
    results = conn.execute('SELECT * FROM records WHERE name like ?', (name,))

    first_row = results.fetchone()  # fetchone() returns None if no rows found

    if first_row:
        print(first_row)
    else:  # prints if None is returned from fetchone()
        print('\nName not found')
    conn.close()


def add_new_record():
    """
    Add new record to records table if it does not already exist
    """
    name = input('Enter new record holder name: ')
    country = input('Enter country: ')
    catches = int(input('Enter number of catches: '))

    try:
        with sqlite3.connect('records_db.sqlite') as conn:
            conn.execute('INSERT INTO records (name, country, catches) VALUES (?, ?, ?)',
                         (name, country, catches))
    except sqlite3.IntegrityError as e:  # catch exception if trying to add duplicate name which is a unique column
        print('\n' + name + ' already exists in the database')
    finally: # this always runs even if there's an error
        conn.close()


def edit_existing_record():
    """
    Update number of catches for name if it exists in database
    """
    name = input('Enter name of record holder to update their number of catches: ')
    update_catches = input('What is ' + name + '\'s new catch record? ')

    with sqlite3.connect('records_db.sqlite') as conn:
        updated = conn.execute('UPDATE records SET catches = ? WHERE UPPER(name) = UPPER(?)',
                               (update_catches, name))
        rows_modified = updated.rowcount
    conn.close()

    if rows_modified == 0:
        print('\nThe name ' + name + ' was not found')
    else:
        print(name + ' was updated to ' + update_catches + ' catches')


def delete_record():
    """
    Delete row from table if name exists in database
    """
    name = input('Enter name of record holder to delete: ')

    with sqlite3.connect('records_db.sqlite') as conn:
        deleted = conn.execute('DELETE FROM records WHERE UPPER(name) = UPPER(?)', (name, ))
        deleted_count = deleted.rowcount  # rowcount returns number of rows affected
    conn.close()

    if deleted_count == 0:  # if no rows were affected, then nothing was deleted
        print('\nThe name ' + name + ' was not found')
    else:
        print(name + ' was deleted')


if __name__ == '__main__':
    main()
