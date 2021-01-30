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


def addNewItem(inventory, itemDescription):
    entry = ["ITEM", "Volume", "Quantity", "Expiration", "Container"]
    # search the loaded current inventory to match for Item, volume and container, and to check if Expiration date
    # is among a list of dates as some items may have multiple expiration dates within their quantity.
    itemDescription = checkIfInStock(inventory, itemDescription)

    # THE ISSUE IS THAT THE DELETED ENTRIES ARE LEAVING EMPTY DICTIONARIES INSTEAD OF BEING COMPLETELY REMOVED
    # MAY USE FILTER AND COMPILE NEW LIST.
    itemDescription[2] = int(itemDescription[2])
    inventory.setdefault(itemDescription[4], [])
    inventory[itemDescription[4]].append(
        {itemDescription[0]: {key: val for key, val in zip(entry[1:4], itemDescription[1:4])}})
    # (inventory)
    return inventory


def checkOutOfDate(data):
    expired = []
    for container in data:
        for item in data[container]:
            for i in item:
                for j in item[i]["Expiration"]:
                    expDate = datetime.datetime.strptime(j, '%d-%m-%y').date()
                    if currentdate + oneWeek >= expDate:
                        expired.append("{}: {}, In container {} Expires soon! ({})".format(i, item[i]["Volume"],
                                                                                   container, j))
                        # So I'm thinking that if I place the return statement HERE it'll check one item then exit.
                        # Confirm, then consider adding to a list and have the GUI print them to the Frame read as
                        # Elements from the list.
    return expired

def checkIfInStock(current_inventory, itemDescription):
    # (current_inventory, itemDescription)
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
    # ("112", itemDescription)
    return itemDescription


def removeStock(inventory, item, expiry_state):
    # NOW REDUCE QUANTITY AND ASK IF EXPIRY DATES ARE GONE.
    b = "-" + item[2]
    item[2] = b
    expiry = item[3]
    inventory = addNewItem(inventory, item)
    # SOME KIND OF TOGGLE OR CHECKBOX IN PrepGui REMOVE FOR WHETHER OR NOT ALL ITEMS FOR EXPIRY HAVE BEEN REMOVED
    if expiry_state:
        # Now we need to remove the date from the list in Inventory
        for each in inventory[item[4]]:
            if item[0] in each and len(each[item[0]]["Expiration"]) > 1:  # Item
                test = each[item[0]]["Expiration"]
                test.remove(expiry)
                inventoryWriter(inventory)
            else:
                print("Only one date left")  # Work on writing to removeFrame.
    else:
        inventoryWriter(inventory)
    return inventory

def baseSelection(inventory, x):
    # Set up for selecting user options.
    x0 = x[0].upper()
    if x0 == "A":
        # Creates the new item then adds that item to the inventory.
        item = x[1]
        print(item, "A ITEM")
        inventory = addNewItem(inventory, item)  # Line 20
        inventoryWriter(inventory)
        # THINK I MIGHT HAVE TO PASS inventory BACK TO PrepGui to get it to write.
    elif x0 == "R":
        item = x[1]
        print(item, "R ITEM")
        inventory = removeStock(inventory, item, x[2])
        inventoryWriter(inventory)
    elif x0 == "D":
        item = x[1]
        print(item)
        for i in inventory:
            if i == item[4]:
                for j in inventory[i]:
                    print(j, "WHERE IS THIS?")
                    for k in j:
                        if k in item and j[k]["Volume"] in item:
                            print("Delete this!")
                            print(type(inventory))
                            del inventory[i][k]
                            inventoryWriter(inventory)
                            # Now to get it to Delete and re-save

    elif x == "C":
        print("DOES IT RUN?")
        return checkOutOfDate(inventory)

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


def inventoryWriter(inventory):
    # GET THIS TO WRITE INVENTORY?
    with open("inventory.txt", "a+") as contents:
        for each in inventory:
            while {} in inventory[each]:
                inventory[each].remove({})
        contents.truncate(0)
        contents.write(json.dumps(inventory))
