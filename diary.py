#! /usr/bin/env python3

from collections import OrderedDict
import datetime
import os
import sys

from peewee import *


db = SqliteDatabase('diary.db')


class Entry(Model):
    """ This is the entry for a diary record """

    content = TextField() # use this field since no max length is needed
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

# have a function that initalizes everything for us
def initialize():
    """create the database and the table if they don't exist"""
    
    db.connect()
    #the "create_table" function has an underscore always
    db.create_tables([Entry], safe=True)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def menu_loop():
    """ show the menu """

    choice = None

    while choice != 'q':
        clear()
        print ("Enter 'q' to quit.")
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('Action: ').lower().strip()

        if choice in menu:
            clear()
            menu[choice]()
def add_entry():
    """Add an entry"""
    
    print("Enter your entry. Press ctrl+d when finished.")
    data = sys.stdin.read().strip()

    if data:
        if input('Save entry? [Y/n] ').lower() != 'n':
            Entry.create(content=data)
            print("Entry Saved Successfully!")

def view_entries(search_query=None):
    """View previous entries"""
    
    entries = Entry.select().order_by(Entry.timestamp.desc())
    if search_query:
        entries = entries.where(Entry.content.contains(search_query))

    for entry in entries:
        #show timestamp of entries for viewers
        timestamp = entry.timestamp.strftime('%A %B %d, %Y %I:%M%p')
        clear()
        print(timestamp)
        print('='*len(timestamp))
        print(entry.content)
        print('\n\n'+'='*len(timestamp))
        print('n) next entry')
        print('d) delete_entry')
        print('q) return to main menu')

        next_action = input('Action: [N/d/q] ').lower().strip()
        if next_action == 'q':
            break
        elif next_action == 'd':
            delete_entry(entry)

def search_entries():
    """search entries for a phrase/word"""
    
    view_entries(input('Search query: '))

def delete_entry(entry):
    """Delete an entry"""
    
    if input('Are you sure? [y/N] ').lower().strip() == 'y':
        entry.delete_instance()
        print('Deleted Successfully!')

menu = OrderedDict([
    ('a', add_entry),
    ('v', view_entries),
    ('s', search_entries),
])
#run the initialize() function whenever the script is run, not when the script is just imported
if __name__ == '__main__':
    initialize()
    menu_loop()
