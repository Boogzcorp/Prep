import datetime
import json
import pandas as pd
import os
import openpyxl


# Create a program to catalogue items for storage.

# Each dictionary represents a tub number, each key will be an item for storage, the value pair will be a list of
# remaining attributes, Volume, Quantity, Expiration and any other possible information needed.

# A list of all containers, containers are dictionaries that hold stockpiled items and their associated attributes
stockOnHand = []
currentdate = datetime.date.today()
oneMonth = datetime.timedelta(days=30)
oneWeek = datetime.timedelta(days=7)

def addNewItem(inventory, itemDescription):
    entry = ["ITEM", "Volume", "Quantity", "Expiration", "Container"]
    # search the loaded current inventory to match for Item, volume and container, and to check if Expiration date
    # is among a list of dates as some items may have multiple expiration dates within their quantity.
    itemDescription = checkIfInStock(inventory, itemDescription)
    itemDescription[2] = int(itemDescription[2])
    inventory.setdefault(itemDescription[4], [])
    inventory[itemDescription[4]].append(
        {itemDescription[0]: {key: val for key, val in zip(entry[1:4], itemDescription[1:4])}})
    return inventory


def checkOutOfDate(data):
    expired = []
    urgent = []
    for container in data:
        for item in data[container]:
            for i in item:
                for j in item[i]["Expiration"]:
                    if j == "N/A":
                        pass
                    else:
                        expDate = datetime.datetime.strptime(j, '%d-%m-%y').date()
                        if currentdate + oneWeek >= expDate:
                            urgent.append("{}: {}, In container {} Expires soon! ({})".format(i, item[i]["Volume"],
                                                                                              container, j))
                        if currentdate + oneMonth >= expDate:
                            expired.append("{}: {}, In container {} Expires soon! ({})".format(i, item[i]["Volume"],
                                                                                               container, j))
    return [expired, urgent]


def checkIfInStock(current_inventory, itemDescription):
    for container in current_inventory:
        for item in current_inventory[container]:
            for i in item:
                if i in itemDescription and item[i]["Volume"] in itemDescription and container == itemDescription[4]:
                    if itemDescription[3] in item[i]["Expiration"]:
                        itemDescription[2] = int(itemDescription[2]) + int(item[i]["Quantity"])
                        itemDescription[3] = item[i]["Expiration"]
                        del item[i]
                        return itemDescription
                    else:
                        # If expiration date (itemDescription[3]) is not in list of known dates (item[i]["Expiration"])
                        # add date to list and add Item to assigned container.
                        a = [item[i]["Expiration"]]
                        if type(item[i]["Expiration"]) == list:
                            # If There are already multiple expiration dates, append new date
                            item[i]["Expiration"].append(itemDescription[3])
                            itemDescription[3] = item[i]["Expiration"]
                            itemDescription[2] = int(itemDescription[2]) + int(item[i]["Quantity"])
                            del item[i]
                            return itemDescription
                        else:
                            # Otherwise set the expiration dates to be a list and append new date.
                            a.append(itemDescription[3])
                            itemDescription[3] = a
                            itemDescription[2] = int(itemDescription[2]) + int(item[i]["Quantity"])
                            del item[i]
                            return itemDescription
    a = [itemDescription[3]]
    itemDescription[3] = a
    return itemDescription


def removeStock(inventory, item, expiry_state):
    # REDUCE QUANTITY AND ASK IF EXPIRY DATES ARE GONE.
    b = "-" + item[2]
    item[2] = b
    expiry = item[3]
    inventory = addNewItem(inventory, item)
    if expiry_state:
        # Now we need to remove the date from the list in Inventory
        for each in inventory[item[4]]:
            if item[0] in each and len(each[item[0]]["Expiration"]) > 1:
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
        inventory = addNewItem(inventory, item)
        inventoryWriter(inventory)
    elif x0 == "R":
        # Removes items from from inventory as they're used.
        item = x[1]
        inventory = removeStock(inventory, item, x[2])
        inventoryWriter(inventory)
    elif x0 == "D":
        # Will delete mistyped entries or any other entry that needs to be removed
        item = x[1]
        for i in inventory:
            count = 0
            if i == item[4]:
                for j in inventory[i]:
                    count += 1
                    for k in j:
                        if k in item and j[k]["Volume"] in item:
                            del inventory[i][count-1]
        if not inventory[i]:
            del inventory[i]

        inventoryWriter(inventory)
        # Now to get it to Delete empty containers and re-save

    elif x == "C":
        # Checks expiry dates of items returning those with less than 1 month before expiry
        # and flags urgent those that have less than 1 week
        return checkOutOfDate(inventory)

    elif x == "L":
        # Will output Inventory to an Excel spreadsheet
        with pd.ExcelWriter('output.xlsx') as writer:
            cols = ["ITEM", "Volume", "Quantity", "Expiration", "Container"]
            for each in inventory:
                basedf = pd.DataFrame(columns=cols)
                while {} in inventory[each]:
                    inventory[each].remove({})
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
                    column_length = max(basedf[column].astype(str).map(len).max()+2, len(column))
                    col_idx = basedf.columns.get_loc(column)
                    writer.sheets[each].set_column(col_idx, col_idx, column_length)
        try:
            os.startfile('output.xlsx')
        except:
            pass


def inventoryWriter(inventory):
    with open("inventory.txt", "a+") as contents:
        for each in inventory:
            while {} in inventory[each]:
                inventory[each].remove({})
        contents.truncate(0)
        contents.write(json.dumps(inventory))