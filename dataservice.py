import pickledb
import os

db_path = 'shopping_list.db'
users_key = "users"
password_key = "password"
global_db = None

def load_db():
    global global_db
    db_file_already_exists = os.path.exists(db_path)
    global_db = pickledb.PickleDB(db_path)
    if not db_file_already_exists:
        global_db.set("milk", { "got": False })
        global_db.set("eggs", { "got": False })
        global_db.set("bread", { "got": False })
        global_db.set("sugar", { "got": False })
        global_db.save()

def get_db():
    global global_db
    if global_db is None:
        load_db()
    return global_db


def get_shopping_list():
    db = get_db()
    all_items = db.all()
    shopping_list_items = {}
    for x in all_items:
        shopping_list_items[x] = db.get(x)

    return shopping_list_items

def add_item_to_list(item):
    db = get_db()
    if db.get(item) is None:
        # prevent duplicates
        db.set(item, {"got": False})
    db.save()
    return get_shopping_list()



def add_item_with_image(item, filepath):
    db = get_db()
    if db.get(item) is None:
        # prevent duplicates
        data = {"got": False, "image_path": filepath}
        print(data)
        db.set(item, data)
    db.save()
    return get_shopping_list()

def move_item_between_lists(item):
    db = get_db()
    db_item = db.get(item)
    if db_item is None:
        return get_shopping_list()
    db_item["got"] = not db_item["got"]
    db.set(item, db_item)
    db.save()
    return get_shopping_list()


def remove_item(item):
    db = get_db()
    db.remove(item)
    db.save()
    return get_shopping_list()

