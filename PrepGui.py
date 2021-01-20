from tkinter import *
import PrepStore
import json
import openpyxl
# from PIL import ImageTk,Image

root = Tk()
root.title("Prep inventory")
# root.iconbitmap("icon")
root.geometry("750x750")


def inventorySetup():
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
        contents.truncate(0)
        contents.write(json.dumps(inventory))
    return inventory


class Prep:

    def __init__(self, root):# What kind of Atributes?
        pass

    def multi(self):
        # Multiple functions set to run successively from single button click in addFrame Submit button LINE 94
        self.getItem = self.item.get()
        self.item.delete(0, END)
        self.getVolume = self.volume.get()
        self.volume.delete(0, END)
        self.getQuantity = self.quantity.get()
        self.quantity.delete(0, END)
        self.getExpiry = self.expiry.get()
        self.expiry.delete(0, END)
        self.getContainer = self.container.get()
        self.container.delete(0, END)

    def homeframe(self):
        self.homeframe = Frame(root)
        self.homeframe.pack()
        #menu(homeframe)
        #statusbar(homeframe)
        self.Add = Button(self.homeframe, text="Add Items", command=self.addframe)
        self.Add.grid(row=0, column=0)
        self.Remove = Button(self.homeframe, text="Remove Items", command=self.removeframe)
        self.Remove.grid(row=0, column=1)
        self.Delete = Button(self.homeframe, text="Delete Entries", command = self.deleteframe)
        self.Delete.grid(row=0, column=3)
        self.Check = Button(self.homeframe, text="Check for Items soon to Expire", command=self.checkExpiry)
        self.Check.grid(row=1, column=0)
        self.Output = Button(self.homeframe, text="Output Inventory to Excel", command=self.outputCycle)
        self.Output.grid(row=1, column=1)


    def addframe(self):
        self.homeframe.destroy()
        self.addframe = Frame(root, width=500, height=500)
        self.addframe.pack()
        # menu(addframe)
        # statusbar(addframe)
        self.itemlabel = Label(self.addframe, text="Item")
        self.itemlabel.grid(row=0, column=0, pady=40)
        ivar = StringVar()
        self.item = Entry(self.addframe, textvariable=ivar)
        self.item.grid(row=0, column=1, pady=40)
        self.volumelabel = Label(self.addframe, text="Volume")
        self.volumelabel.grid(row=0, column=3, pady=40)
        vvar = StringVar()
        self.volume = Entry(self.addframe, textvariable=vvar)
        self.volume.grid(row=0, column=4, pady=40)
        self.quantitylabel = Label(self.addframe, text="Quantity")
        self.quantitylabel.grid(row=0, column=5, pady=40)
        qvar = StringVar()
        self.quantity = Entry(self.addframe, textvariable=qvar)
        self.quantity.grid(row=0, column=6, pady=40)
        self.expirylabel = Label(self.addframe, text="Expiration Date")
        self.expirylabel.grid(row=1, column=0, pady=40)
        evar = StringVar()
        self.expiry = Entry(self.addframe, textvariable=evar)
        self.expiry.grid(row=1, column=1, pady=40)
        self.containerlabel = Label(self.addframe, text="Container")
        self.containerlabel.grid(row=1, column=3, pady=40)
        cvar = StringVar()
        self.container = Entry(self.addframe, textvariable=cvar)
        self.container.grid(row=1, column=4, pady=40)
        self.Submit = Button(self.addframe, text="SUBMIT", command=lambda : [self.multi(), self.addCycle()])
        self.Submit.grid(row=3, column=0, pady=40)
        self.Return = Button(self.addframe, text="HOME", command=lambda : [self.homeframe, self.addframe.Destroy])
        self.Return.grid(row=3, column=1, pady=40)

    def addCycle(self):
        # Runs the PrepStore code for Adding an Item to the store.
        PrepStore.baseSelection(
            ["A", [self.getItem, self.getVolume, self.getQuantity, self.getExpiry, self.getContainer]], inventory)

    def removeframe(self):
        # Runs the PrepStore code for removing an Item to the store.
        PrepStore.baseSelection(
            ["A", [self.getItem, self.getVolume, self.getQuantity, self.getExpiry, self.getContainer]])

    def deleteframe(self):
        # WILL NEED TO WRITE ADDITIONAL CODE FOR THIS IN PrepStore
        print("It works")

    def checkExpiry(self):
        self.homeframe.destroy()
        self.checkframe = Frame(root, width=500, height=500)
        self.checkframe.pack()
        PrepStore.baseSelection("C")
        print("It works")

    def outputCycle(self):
        print("It works")


Prep = Prep(root)
Prep.homeframe()
mainloop()
