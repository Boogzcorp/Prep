from tkinter import *
import PrepStore
import json
import openpyxl
# from PIL import ImageTk,Image

root = Tk()
root.title("Prep inventory")
# root.iconbitmap("icon")
root.geometry("500x500")


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

    def __init__(self, root):  # What kind of Attributes?
        self.inventory = inventorySetup()
    def multi(self, var):
        # Multiple functions set to run successively from single button click in addFrame Submit button LINE 94 and
        # removeFrame Submit button 152
        try:
            self.getcheck = var.get()
        except AttributeError:
            pass

        finally:
            self.getItem = self.item.get()
            self.item.delete(0, END)
            self.getVolume = self.volume.get()
            self.volume.delete(0, END)
            self.getQuantity = self.quantity.get()
            self.getExpiry = self.expiry.get()
            try:
                self.quantity.delete(0, END)
                self.expiry.delete(0, END)
            except AttributeError:
                pass
            finally:
                self.getContainer = self.container.get()
                self.container.delete(0, END)

    # def status_change(self, event):
    #     change = "FUCK!"
    #     self.statusbar(event, change)
    #
    # def statusbar(self, frame, change):
    #     print("You work?")
    #     status = Label(frame, text=change, bd=1, relief=SUNKEN, anchor=W)
    #     return status

    def home_frame(self):
        self.homeframe = Frame(root)
        self.homeframe.pack()
        #menu(homeframe)
        # self.status = self.statusbar(self.homeframe, change="")
        # self.status.grid(row=4, column=0, columnspan=6, sticky=W+E)
        self.Add = Button(self.homeframe, text="Add Items", command=self.addframe)
        self.Add.grid(row=0, column=0, pady=100)
        # self.Add.bind("<Enter>", self.status_change(self.homeframe))  #don't bind to button press, bind to button area
        # maybe Label?
        # Leave here
        self.Remove = Button(self.homeframe, text="Remove Items", command=self.removeframe)
        self.Remove.grid(row=0, column=1)
        self.Delete = Button(self.homeframe, text="Delete Entries", command = self.deleteframe)
        self.Delete.grid(row=0, column=2)
        self.Check = Button(self.homeframe, text="Check for Items soon to Expire", command=self.checkExpiry)
        self.Check.grid(row=1, column=0)
        self.Output = Button(self.homeframe, text="Output Inventory to Excel", command=self.outputCycle)
        self.Output.grid(row=1, column=2)


    def addframe(self):
        self.homeframe.destroy()
        self.addframe = Frame(root)
        self.addframe.pack()
        # menu(addframe)
        # self.status = self.statusbar(self.addframe)
        # self.status.grid(row=4, column=0, columnspan=6, sticky=W+E)
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
        self.Submit = Button(self.addframe, text="SUBMIT", command=lambda: [self.multi(var=''), self.addCycle()])
        self.Submit.grid(row=3, column=0, pady=40)
        self.Return = Button(self.addframe, text="HOME", command=lambda: [self.home_frame(), self.addframe.destroy()])
        self.Return.grid(row=3, column=1, pady=40)

    def addCycle(self):
        # Runs the PrepStore code for Adding an Item to the store.
        PrepStore.baseSelection(self.inventory, ["A", [self.getItem, self.getVolume, self.getQuantity, self.getExpiry,
                                                       self.getContainer]])

    def removeframe(self):
        self.homeframe.destroy()
        self.removeframe = Frame(root, width=500, height=500)
        self.removeframe.pack()
        # menu(removeframe)
        # self.status = self.statusbar(self.removeframe)
        # self.status.grid(row=4, column=0, columnspan=4, sticky=W + E)
        self.itemlabel = Label(self.removeframe, text="Item")
        self.itemlabel.grid(row=0, column=0, pady=40)
        ivar = StringVar()
        self.item = Entry(self.removeframe, textvariable=ivar)
        self.item.grid(row=0, column=1, pady=40)
        self.volumelabel = Label(self.removeframe, text="Volume")
        self.volumelabel.grid(row=0, column=3, pady=40)
        vvar = StringVar()
        self.volume = Entry(self.removeframe, textvariable=vvar)
        self.volume.grid(row=0, column=4, pady=40)
        self.quantitylabel = Label(self.removeframe, text="Quantity")
        self.quantitylabel.grid(row=0, column=5, pady=40)
        qvar = StringVar()
        self.quantity = Entry(self.removeframe, textvariable=qvar)
        self.quantity.grid(row=0, column=6, pady=40)
        self.expirylabel = Label(self.removeframe, text="Expiration Date")
        self.expirylabel.grid(row=1, column=0, pady=40)
        evar = StringVar()
        self.expiry = Entry(self.removeframe, textvariable=evar)
        self.expiry.grid(row=1, column=1, pady=40)
        self.containerlabel = Label(self.removeframe, text="Container")
        self.containerlabel.grid(row=1, column=3, pady=40)
        cvar = StringVar()
        self.container = Entry(self.removeframe, textvariable=cvar)
        self.container.grid(row=1, column=4, pady=40)
        var = BooleanVar()
        self.checkbox = Checkbutton(self.removeframe, text="Have all items for the expiry date been removed?",
                                    variable=var)
        self.checkbox.deselect()
        self.checkbox.grid(row=2, column=4, pady=40)
        self.Submit = Button(self.removeframe, text="SUBMIT", command=lambda: [self.multi(var), self.removeCycle()])
        self.Submit.grid(row=3, column=0, pady=40)
        self.Return = Button(self.removeframe, text="HOME",
                             command=lambda: [self.home_frame(), self.removeframe.destroy()])
        self.Return.grid(row=3, column=1, pady=40)


    def removeCycle(self):
        # Runs the PrepStore code for removing an Item from the store.
        PrepStore.baseSelection(self.inventory, ["R", [self.getItem, self.getVolume, self.getQuantity,
                                                       self.getExpiry, self.getContainer], self.getcheck])

    def deleteframe(self):
        self.homeframe.destroy()
        self.deleteframe = Frame(root, width=500, height=500)
        self.deleteframe.pack()
        # menu(deleteframe)
        # self.status = self.statusbar(self.deleteframe)
        # self.status.grid(row=4, column=0, columnspan=4, sticky=W + E)
        self.itemlabel = Label(self.deleteframe, text="Item")
        self.itemlabel.grid(row=0, column=0, pady=40)
        ivar = StringVar()
        self.item = Entry(self.deleteframe, textvariable=ivar)
        self.item.grid(row=0, column=1, pady=40)
        self.volumelabel = Label(self.deleteframe, text="Volume")
        self.volumelabel.grid(row=0, column=3, pady=40)
        vvar = StringVar()
        self.volume = Entry(self.deleteframe, textvariable=vvar)
        self.volume.grid(row=0, column=4, pady=40)
        qvar = StringVar("")
        self.quantity = qvar
        evar = StringVar()
        self.expiry = evar
        self.containerlabel = Label(self.deleteframe, text="Container")
        self.containerlabel.grid(row=1, column=3, pady=40)
        cvar = StringVar()
        self.container = Entry(self.deleteframe, textvariable=cvar)
        self.container.grid(row=1, column=4, pady=40)
        self.Submit = Button(self.deleteframe, text="SUBMIT", command=lambda: [self.multi(var=''), self.deletecycle()])
        self.Submit.grid(row=3, column=0, pady=40)
        self.Return = Button(self.deleteframe, text="HOME",
                             command=lambda: [self.home_frame(), self.deleteframe.destroy()])
        self.Return.grid(row=3, column=1, pady=40)

    def deletecycle(self):
        PrepStore.baseSelection(self.inventory, ["D", [self.getItem, self.getVolume, self.getQuantity,
                                                       self.getExpiry, self.getContainer]])

    def checkExpiry(self):
        self.homeframe.destroy()
        self.checkframe = Frame(root, width=500, height=500)
        self.checkframe.pack()
        out_of_date = PrepStore.baseSelection(self.inventory, "C")
        if len(out_of_date[1] >= 1:
               pass
               # Create warning popup
        for each in out_of_date[0]:
            Label(self.checkframe, text=each).pack()
        self.Return = Button(self.checkframe, text="HOME",
                             command=lambda: [self.home_frame(), self.checkframe.destroy()])
        self.Return.pack()
        # self.status = self.statusbar(self.checkframe)
        # self.status.pack(anchor=S)

    def outputCycle(self):
        PrepStore.baseSelection(self.inventory, "L")



Prep = Prep(root)
Prep.home_frame()
mainloop()
