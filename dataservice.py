import pickledb #TODO import 
import os

db_path = 'pet_list.db'
global_db = None

def load_db():
    global global_db
    db_file_already_exists = os.path.exists(db_path)
    global_db = pickledb.PickleDB(db_path)
    if not db_file_already_exists:
        baseStats = {
            "totalAdoptions" : 0,
            "bySpecies": {"cat":0, "dog":0, "bird":0, "bunny":0},
            "byAge": {"0-3":0, "3-5":0, "5-10": 0, "10+":0},
            "byTrait": {"calm": 0, "energetic": 0, "aggressive": 0, "friendly":0},
            "recentAdopts": []
        }
        global_db.set("stats", baseStats) 
    
    global_db.save()

def get_db():
    global global_db
    if global_db is None:
        load_db()
    return global_db


def get_profile_list():
    db = get_db()
    all_pets = db.all()
    animal_list = {}
    for x in all_pets:
        animal_list[x] = db.get(x)

    return animal_list

#TODO finish fixing this
def add_animal(profile, filepath):
    db = get_db()
    if db.get(profile) is None:
        # prevent duplicates
        data = {"got": False, "image_path": filepath} #TODO change to reflect profile data
        print(data)
        db.set(profile, data)
    db.save()
    return get_profile_list()

#TODO finish fixing this
def update_profile_data(profile):
    db = get_db()
    db_item = db.get(profile)
    if db_item is None:
        return get_profile_list()
    #TODO \/ replace with updating profile data
    db_item["got"] = not db_item["got"]
    db.set(profile, db_item)
    db.save()
    return get_profile_list()

def remove_profile(profile):
    db = get_db()
    db.remove(profile)
    db.save()
    return get_profile_list()


def add_user(username, password):
    db = get_db()

    #prevent duplicates
    #if #username in use
    #    return False
    
    user_data = {
        "password": password,
        "position": "user",
        "preferences": {
            "species": "",
            "age_range": "",
            "personality": ""
        }
    }
    db.set(username, user_data)
    db.save()
    return True

