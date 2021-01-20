import datetime
import json
import pandas as pd
import openpyxl



# Create a program to catalogue items for storage.

# Each dictionary represents a tub number, each key will be an item for storage, the value pair will be a list of
# remaining attributes, Volume, Quantity, Expiration and any other possible information needed.

# A list of all containers, containers are dictionaries that hold stockpiled items and their associated attributes
stockOnHand = []
currentdate = datetime.date.today()
oneWeek = datetime.timedelta(days=7)


def addNewItem(main_dict, itemDescription):
    entry = ["ITEM", "Volume", "Quantity", "Expiration", "Container"]
    # search the loaded current inventory to match for Item, volume and container, and to check if Expiration date
    # is among a list of dates as some items may have multiple expiration dates within their quantity.
    itemDescription = checkIfInStock(inventory, itemDescription)

    # THE ISSUE IS THAT THE DELETED ENTRIES ARE LEAVING EMPTY DICTIONARIES INSTEAD OF BEING COMPLETELY REMOVED
    # MAY USE FILTER AND COMPILE NEW LIST.
    itemDescription[2] = int(itemDescription[2])
    main_dict.setdefault(itemDescription[4], [])
    main_dict[itemDescription[4]].append(
        {itemDescription[0]: {key: val for key, val in zip(entry[1:4], itemDescription[1:4])}})
    return main_dict


def checkOutOfDate(data):
    for container in data:
        for item in data[container]:
            for i in item:
                for j in item[i]["Expiration"]:
                    expDate = datetime.datetime.strptime(j, '%d-%m-%y').date()
                    if currentdate + oneWeek >= expDate:
                        print("{}: {}, In container {} Expires soon! ({})".format(i, item[i]["Volume"],
                                                                                   container, j))


def checkIfInStock(current_inventory, itemDescription):
    # print(current_inventory)
    for container in current_inventory:
        # print("CONTAINER: ", container, "CURRENT INVENTORY: ", current_inventory)
        for item in current_inventory[container]:
            # print("ITEM: ", item, "CURRENT INVENTORY FOR CONTAINER: ", current_inventory[container])
            for i in item:
                # print(i, "52")
                # Compare values in itemDescription(LIST) to see if item already in stock.
                if i in itemDescription and item[i]["Volume"] in itemDescription and container == itemDescription[4]:
                    # If new item by volume is already in the assigned container.
                    # print("ITEM IS ALREADY STORED 55")
                    # print("3    ", itemDescription[3], "***", item[i]["Expiration"])
                    if itemDescription[3] in item[i]["Expiration"]:
                        # print("EXPIRY DATE IS ALREADY LISTED! 58")
                        # Check if expiration date is already in list of known expiration dates
                        # And add item to the assigned container
                        itemDescription[2] = int(itemDescription[2]) + int(item[i]["Quantity"])
                        itemDescription[3] = item[i]["Expiration"]
                        del item[i]
                        # print("4    ", "64", itemDescription)
                        return itemDescription
                    else:
                        # print("THIS IS A NEW EXPIRY DATE! 62")
                        # If expiration date (itemDescription[3]) is not in list of known dates (item[i]["Expiration"])
                        # add date to list and add Item to assigned container.
                        a = [item[i]["Expiration"]]
                        if type(item[i]["Expiration"]) == list:
                            #  print("THE ITEM ALREADY HAS MULTIPLE EXPIRY DATES, THIS IS A NEW ONE! 71")
                            # If There are already multiple expiration dates, append new date
                            item[i]["Expiration"].append(itemDescription[3])
                            # print(item[i]["Expiration"], "Line 75")  # list shows date and list with date
                            itemDescription[3] = item[i]["Expiration"]
                            itemDescription[2] = int(itemDescription[2]) + int(item[i]["Quantity"])
                            del item[i]
                            # print("79", itemDescription)
                            return itemDescription
                        else:
                            # print("THIS IS THE FIRST DATE FOR THIS ITEM! 82")
                            # Otherwise set the expiration dates to be a list and append new date.
                            a.append(itemDescription[3])
                            itemDescription[3] = a
                            itemDescription[2] = int(itemDescription[2]) + int(item[i]["Quantity"])
                            del item[i]
                            # print("88", itemDescription)
                            return itemDescription
                # else:
                # if container == itemDescription[4]:
                # print("THIS IS A NEW ITEM BUT NOT THE FIRST ENTRY! 84")

                # THIS IS WHERE IT GOES WRONG! GETS SORTED AND APPLIED HERE BEFORE GOING TO LOOP THROUGH
                # ADDITIONAL CONTAINERS. NEED TO APPEND TO LIST
                # Otherwise, add it to the assigned container
                # return itemDescription
    # print("THIS IS THE FIRST TIME THIS ITEM IS ENTERED! 90")
    a = [itemDescription[3]]
    itemDescription[3] = a
    # print("101", itemDescription)
    return itemDescription


def removeStock(inventory, item):
    # print("1    ", inventory)
    # NOW REDUCE QUANTITY AND ASK IF EXPIRY DATES ARE GONE.
    b = "-" + item[2]
    item[2] = b
    expiry = item[3]
    # print("2    ", item)
    addNewItem(inventory, item)
    # print("5    ", inventory)
    x = ""
    while x != "Y" and x != "N":
        x = input("Have all items for the expiry date been removed?")
        x = x[0].upper()
        if x == "Y":
            # Now we need to remove the date from the list in Inventory
            for each in inventory[item[4]]:
                if item[0] in each:  # Item
                    test = each[item[0]]["Expiration"]
                    test.remove(expiry)
                    contents.truncate(0)
                    contents.write(json.dumps(inventory))


def itemCall():
    # Item and it's related attributes
    itemDescription = []
    # List of attributes for items
    entry = ["ITEM", "Volume", "Quantity", "Expiration", "Container"]
    # Loop through to add new Items and their attributes to the list
    for each in entry:
        g = input(f"{each}: ")
        if g.upper() != "END":
            itemDescription.append(g)

        else:
            # CHECK TO MAKE SURE EVERY THING IS SAVED!
            contents.truncate(0)
            contents.write(json.dumps(inventory))
            exit()
    return itemDescription

def baseSelection():
    # Set up for selecting user options.
    x = ""
    while x != "A" and x != "R" and x != "D" and x != "C" and x != "L":
        x = input("Would you like to Add, Remove, Delete or Check expiry date?")
        x = x[0].upper()
    if x == "A":
        # Creates the new item then adds that item to the inventory.
        while True:
            print()
            print()
            print()
            print("Expiry dates to use dd-mm-yy format".center(100))
            item = itemCall()
            addNewItem(inventory, item)
    elif x == "R":
        print()
        print()
        print()
        print("Enter Item to be removed from stock: ".center(100))
        item = itemCall()
        removeStock(inventory, item)

    elif x == "C":
        checkOutOfDate(inventory)

    elif x == "L":
        # Create Excel output
        with pd.ExcelWriter('output.xlsx') as writer:
            cols = ["ITEM", "Volume", "Quantity", "Expiration", "Container"]
            for each in inventory:
                basedf = pd.DataFrame(columns=cols)
                while {} in inventory[each]:
                    inventory[each].remove({})
                # [Errno 13] Permission denied: 'output.xlsx' occurs when EXCEL is left open and I try to run it
                for i in range(len(inventory[each])):
                    entry = []
                    for key in inventory[each][i]:
                        entry.append(key)
                        for k in inventory[each][i][key]:
                            if k in cols:
                                entry.append(inventory[each][i][key][k])
                    entry.append(each)
                    basedf.loc[len(basedf)] = entry
                basedf.to_excel(writer, sheet_name=each, index=False)  # index false
                for column in basedf:
                    column_length = max(basedf[column].astype(str).map(len).max(), len(column))
                    # input()
                    col_idx = basedf.columns.get_loc(column)
                    writer.sheets[each].set_column(col_idx, col_idx, column_length)


with open("inventory.txt", "a+") as contents:
    # Create file or open then set marker to start to read previous content
    contents.seek(0)
    text = contents.read()
    if text == "":
        # If empty set up a dictionary to store items
        inventory = {}
    else:
        # RELOAD THE CONTENTS OF TEXT INTO THE INVENTORY VARIABLE AGAIN!
        inventory = json.loads(text)

    baseSelection()
    contents.truncate(0)
    contents.write(json.dumps(inventory))