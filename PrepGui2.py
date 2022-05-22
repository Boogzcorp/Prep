from tkinter import *
from tkinter import messagebox
import PrepStore2
import json
import sys


root = Tk()
root.title("Prep inventory")
root.iconbitmap('fire.ico')
width = int(root.winfo_screenwidth()/2)
height = int(root.winfo_screenheight()/2)
root.geometry(f'{width}x{height}')


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
    root.update()
    def __init__(self, root):  # What kind of Attributes?
        self.inventory = inventorySetup()
    def multi(self, var):
        # Multiple functions set to run successively from single button click in addFrame Submit button LINE 94 and
        # removeFrame Submit button LINE 152
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

    def destroy_menu(self):
        for child in root.winfo_children():
            child.destroy()
        root.update()
        # Once everything in current frame is destroyed leaving only root, Runs menu and status_bar
        self.menu()
        self.status_bar(root, status="")  # Find out why this runs but only shows misplaced in fullscreen

    def menu(self):
        menu = Menu(root)
        root.config(menu=menu)
        file_menu = Menu(menu)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Add Items", command=lambda: [self.destroy_menu(), self.add_frame()])
        file_menu.add_command(label="Remove Items", command=lambda: [self.destroy_menu(), self.remove_frame()])
        file_menu.add_command(label="Delete Entries", command=lambda: [self.destroy_menu(), self.delete_frame()])
        file_menu.add_command(label="Check for Items soon to Expire",
                              command=lambda: [self.destroy_menu(), self.check_Expiry()])
        file_menu.add_command(label="Output Inventory to Excel",
                              command=lambda: [self.destroy_menu(), self.output_Cycle()])
        file_menu.add_command(label="Exit", command=sys.exit)

    def status_bar(self, frame, status):
        # Creates a status bar at the bottom that gives "Tooltips" about the function or purpose of a Widget
        stat_bar = Label(frame, text=status, bd=1, relief=SUNKEN, anchor=W)
        stat_bar.place(x=0, y=(height-20), width=width)


    def on_enter(self, event):
        # When cursor enters area of a widget, identifies widget by text or name and sets status to information found
        # in phrasedict before sending to status bar for updating.
        phrasedict = {"Add Items": "Add Items to the inventory", "Remove Items": "For when an Item is used up",
                      "Delete Entries": "For when an entry has been made in error and needs to be removed",
                      "Check for Items soon to Expire": "Gives one months notice on items due to expire and a WARNING "
                                                        "when there is only one week left",
                      "Output Inventory to Excel": "Produce Excel spreadsheet of Inventory",
                      "item": "Name of Item to be stored, removed or deleted",
                      "volume": "Measured units, Grams, Kilograms, Litres etc",
                      "quantity": "How many of that Item at that Volume? Store different volumes as different entries",
                      "expiration Date": "Use format DD-MM-YY or N/A if not Applicable",
                      "container": "Name or ID number of where Item stored",
                      "SUBMIT": "Commit all details to the Inventory", "HOME": "Return to the Main Page",
                      "Retrieve": "Retrieve information on all items in Listbox", "search": "Search for Items by name.",
                      "listbox": "List of potential item matches."}
        try:
            status = phrasedict[event.widget['text']]  # status = event.widget["text"] in phrasedict Key:Value
        except (KeyError, TclError):
            status = phrasedict[repr(str(event.widget))[repr(str(event.widget)).rfind(".")+1:-1]]
        frame = root  # event.widget.master
        self.status_bar(frame, status)

    def on_leave(self, event):
        # Clears status bar when cursor leaves widget area
        status = ""
        frame = root
        self.status_bar(frame, status)

    def home_frame(self):
        # Setup for Home including all buttons.
        self.homeframe = Frame(root)
        self.homeframe.pack()
        self.menu()
        self.status_bar(root, status="")  # Runs with incorrect sizing
        self.Add = Button(self.homeframe, text="Add Items", command=self.add_frame)
        self.Add.grid(row=0, column=0, pady=100)
        self.Add.bind("<Enter>", self.on_enter)
        self.Add.bind("<Leave>", self.on_leave)
        self.Remove = Button(self.homeframe, text="Remove Items", command=self.remove_frame)
        self.Remove.grid(row=0, column=1)
        self.Remove.bind("<Enter>", self.on_enter)
        self.Remove.bind("<Leave>", self.on_leave)
        self.Delete = Button(self.homeframe, text="Delete Entries", command=self.delete_frame)
        self.Delete.grid(row=0, column=2)
        self.Delete.bind("<Enter>", self.on_enter)
        self.Delete.bind("<Leave>", self.on_leave)
        self.Check = Button(self.homeframe, text="Check for Items soon to Expire", command=self.check_Expiry)
        self.Check.grid(row=1, column=0)
        self.Check.bind("<Enter>", self.on_enter)
        self.Check.bind("<Leave>", self.on_leave)
        self.Output = Button(self.homeframe, text="Output Inventory to Excel", command=self.output_Cycle)
        self.Output.grid(row=1, column=2, pady=10)
        self.Output.bind("<Enter>", self.on_enter)
        self.Output.bind("<Leave>", self.on_leave)
        self.search = Label(self.homeframe, text="Item Search", font=("Ariel", 10))
        self.search.grid(row=2, column=0, pady=30)
        self.Search = Entry(self.homeframe, font=("Ariel", 10), name="search")
        self.Search.grid(row=2, column=1, pady=30)
        self.Search.bind("<KeyRelease>", self.Searchf)
        self.Search.bind("<Enter>", self.on_enter)
        self.Search.bind("<Leave>", self.on_leave)
        self.listbox = Listbox(self.homeframe, font=("Ariel", 10), height=5, width=50, name="listbox")
        self.listbox.grid(row=3, column=1)
        self.listbox.bind("<Enter>", self.on_enter)
        self.listbox.bind("<Leave>", self.on_leave)
        self.retrieve = Button(self.homeframe, text="Retrieve", command=self.retrieve_cycle)
        self.retrieve.grid(row=4, column=1)
        self.retrieve.bind("<Enter>", self.on_enter)
        self.retrieve.bind("<Leave>", self.on_leave)

    def add_frame(self):
        # Setup for Adding items to inventory including all buttons and entry boxes
        self.homeframe.destroy()
        self.addframe = Frame(root)
        self.addframe.pack()
        self.itemlabel = Label(self.addframe, text="Item")
        self.itemlabel.grid(row=0, column=0, pady=40)
        ivar = StringVar()
        self.item = Entry(self.addframe, textvariable=ivar, name="item")
        self.item.grid(row=0, column=1, pady=40)
        self.item.bind("<Enter>", self.on_enter)
        self.item.bind("<Leave>", self.on_leave)
        self.volumelabel = Label(self.addframe, text="Volume")
        self.volumelabel.grid(row=0, column=3, pady=40)
        vvar = StringVar()
        self.volume = Entry(self.addframe, textvariable=vvar, name="volume")
        self.volume.grid(row=0, column=4, pady=40)
        self.volume.bind("<Enter>", self.on_enter)
        self.volume.bind("<Leave>", self.on_leave)
        self.quantitylabel = Label(self.addframe, text="Quantity")
        self.quantitylabel.grid(row=0, column=5, pady=40)
        qvar = StringVar()
        self.quantity = Entry(self.addframe, textvariable=qvar, name="quantity")
        self.quantity.grid(row=0, column=6, pady=40)
        self.quantity.bind("<Enter>", self.on_enter)
        self.quantity.bind("<Leave>", self.on_leave)
        self.expirylabel = Label(self.addframe, text="Expiration Date")
        self.expirylabel.grid(row=1, column=0, pady=40)
        evar = StringVar()
        self.expiry = Entry(self.addframe, textvariable=evar, name="expiration Date")
        self.expiry.grid(row=1, column=1, pady=40)
        self.expiry.bind("<Enter>", self.on_enter)
        self.expiry.bind("<Leave>", self.on_leave)
        self.containerlabel = Label(self.addframe, text="Container")
        self.containerlabel.grid(row=1, column=3, pady=40)
        cvar = StringVar()
        self.container = Entry(self.addframe, textvariable=cvar, name="container")
        self.container.grid(row=1, column=4, pady=40)
        self.container.bind("<Enter>", self.on_enter)
        self.container.bind("<Leave>", self.on_leave)
        self.Submit = Button(self.addframe, text="SUBMIT", command=lambda: [self.multi(var=''), self.addCycle()])
        self.Submit.grid(row=3, column=0, pady=40)
        self.Submit.bind("<Enter>", self.on_enter)
        self.Submit.bind("<Leave>", self.on_leave)
        self.Return = Button(self.addframe, text="HOME", command=lambda: [self.home_frame(), self.addframe.destroy()])
        self.Return.grid(row=3, column=1, pady=40)
        self.Return.bind("<Enter>", self.on_enter)
        self.Return.bind("<Leave>", self.on_leave)

    def addCycle(self):
        # Runs the PrepStore code for Adding an Item to the store.
        regex_expression = re.compile(r"\d{2}-\d{2}-\d{2}|N/A")
        matches = regex_expression.finditer(self.getExpiry)
        for match in matches:
            if self.getExpiry == match.group(0):
                try:
                    int(self.getQuantity)
                except:
                    pass
                else:
                    PrepStore2.baseSelection(self.inventory,
                                        ["A", [self.getItem, self.getVolume, self.getQuantity, self.getExpiry,
                                               self.getContainer]])
            else:
                pass

    def remove_frame(self):
        # Setup for Removing items from inventory including all buttons and entry boxes
        self.homeframe.destroy()
        self.removeframe = Frame(root)
        self.removeframe.pack()
        self.itemlabel = Label(self.removeframe, text="Item")
        self.itemlabel.grid(row=0, column=0, pady=40)
        ivar = StringVar()
        self.item = Entry(self.removeframe, textvariable=ivar, name="item")
        self.item.grid(row=0, column=1, pady=40)
        self.item.bind("<Enter>", self.on_enter)
        self.item.bind("<Leave>", self.on_leave)
        self.volumelabel = Label(self.removeframe, text="Volume")
        self.volumelabel.grid(row=0, column=3, pady=40)
        vvar = StringVar()
        self.volume = Entry(self.removeframe, textvariable=vvar, name="volume")
        self.volume.grid(row=0, column=4, pady=40)
        self.volume.bind("<Enter>", self.on_enter)
        self.volume.bind("<Leave>", self.on_leave)
        self.quantitylabel = Label(self.removeframe, text="Quantity")
        self.quantitylabel.grid(row=0, column=5, pady=40)
        qvar = StringVar()
        self.quantity = Entry(self.removeframe, textvariable=qvar, name="quantity")
        self.quantity.grid(row=0, column=6, pady=40)
        self.quantity.bind("<Enter>", self.on_enter)
        self.quantity.bind("<Leave>", self.on_leave)
        self.expirylabel = Label(self.removeframe, text="Expiration Date")
        self.expirylabel.grid(row=1, column=0, pady=40)
        evar = StringVar()
        self.expiry = Entry(self.removeframe, textvariable=evar, name="expiration Date")
        self.expiry.grid(row=1, column=1, pady=40)
        self.expiry.bind("<Enter>", self.on_enter)
        self.expiry.bind("<Leave>", self.on_leave)
        self.containerlabel = Label(self.removeframe, text="Container")
        self.containerlabel.grid(row=1, column=3, pady=40)
        cvar = StringVar()
        self.container = Entry(self.removeframe, textvariable=cvar, name="container")
        self.container.grid(row=1, column=4, pady=40)
        self.container.bind("<Enter>", self.on_enter)
        self.container.bind("<Leave>", self.on_leave)
        var = BooleanVar()
        self.checkbox = Checkbutton(self.removeframe, text="Have all items for the expiry date been removed?",
                                    variable=var)
        self.checkbox.deselect()
        self.checkbox.grid(row=2, column=4, pady=40)
        self.Submit = Button(self.removeframe, text="SUBMIT", command=lambda: [self.multi(var), self.removeCycle()])
        self.Submit.grid(row=3, column=0, pady=40)
        self.Submit.bind("<Enter>", self.on_enter)
        self.Submit.bind("<Leave>", self.on_leave)
        self.Return = Button(self.removeframe, text="HOME",
                             command=lambda: [self.home_frame(), self.removeframe.destroy()])
        self.Return.grid(row=3, column=1, pady=40)
        self.Return.bind("<Enter>", self.on_enter)
        self.Return.bind("<Leave>", self.on_leave)


    def removeCycle(self):
        # Runs the PrepStore code for removing an Item from the store.
        regex_expression = re.compile(r"\d{2}-\d{2}-\d{2}|N/A")
        matches = regex_expression.finditer(self.getExpiry)
        for match in matches:
            if self.getExpiry == match.group(0):
                try:
                    int(self.getQuantity)
                except:
                    pass
                else:
                    PrepStore2.baseSelection(self.inventory, ["R", [self.getItem, self.getVolume, self.getQuantity,
                                                                   self.getExpiry, self.getContainer], self.getcheck])
            else:
                pass


    def delete_frame(self):
        # Setup for deleting bad entries in inventory including all buttons and entry boxes
        self.homeframe.destroy()
        self.deleteframe = Frame(root)
        self.deleteframe.pack()
        self.itemlabel = Label(self.deleteframe, text="Item")
        self.itemlabel.grid(row=0, column=0, pady=40)
        ivar = StringVar()
        self.item = Entry(self.deleteframe, textvariable=ivar, name="item")
        self.item.grid(row=0, column=1, pady=40)
        self.item.bind("<Enter>", self.on_enter)
        self.item.bind("<Leave>", self.on_leave)
        self.volumelabel = Label(self.deleteframe, text="Volume")
        self.volumelabel.grid(row=0, column=3, pady=40)
        vvar = StringVar()
        self.volume = Entry(self.deleteframe, textvariable=vvar, name="volume")
        self.volume.grid(row=0, column=4, pady=40)
        self.volume.bind("<Enter>", self.on_enter)
        self.volume.bind("<Leave>", self.on_leave)
        qvar = StringVar("")
        self.quantity = qvar
        evar = StringVar()
        self.expiry = evar
        self.containerlabel = Label(self.deleteframe, text="Container")
        self.containerlabel.grid(row=1, column=3, pady=40)
        cvar = StringVar()
        self.container = Entry(self.deleteframe, textvariable=cvar, name="container")
        self.container.grid(row=1, column=4, pady=40)
        self.container.bind("<Enter>", self.on_enter)
        self.container.bind("<Leave>", self.on_leave)
        self.Submit = Button(self.deleteframe, text="SUBMIT", command=lambda: [self.multi(var=''), self.deletecycle()])
        self.Submit.grid(row=3, column=0, pady=40)
        self.Submit.bind("<Enter>", self.on_enter)
        self.Submit.bind("<Leave>", self.on_leave)
        self.Return = Button(self.deleteframe, text="HOME",
                             command=lambda: [self.home_frame(), self.deleteframe.destroy()])
        self.Return.grid(row=3, column=1, pady=40)
        self.Return.bind("<Enter>", self.on_enter)
        self.Return.bind("<Leave>", self.on_leave)

    def deletecycle(self):
        # Runs the PrepStore code for deleting a bad entry from the store.
        PrepStore2.baseSelection(self.inventory, ["D", [self.getItem, self.getVolume, self.getQuantity,
                                                       self.getExpiry, self.getContainer]])

    def check_Expiry(self):
        # Checks to see which items are going to expire within a month
        self.homeframe.destroy()
        self.checkframe = Frame(root)
        self.checkframe.pack()
        out_of_date = PrepStore2.baseSelection(self.inventory, "C")
        if len(out_of_date[1]) >= 1:
            for each in out_of_date[1]:
                messagebox.showinfo(title="URGENT", message=each)
        # Create warning popup
        for each in out_of_date[0]:
            Label(self.checkframe, text=each).pack()
        self.Return = Button(self.checkframe, text="HOME",
                             command=lambda: [self.home_frame(), self.checkframe.destroy()])
        self.Return.pack()
        self.Return.bind("<Enter>", self.on_enter)
        self.Return.bind("<Leave>", self.on_leave)

    def output_Cycle(self):
        # Outputs the inventory to Excel for easy reading.
        PrepStore2.baseSelection(self.inventory, "L")


    def retrieve_cycle(self):
        g = self.listbox.get(0, END)
        self.homeframe.destroy()
        self.retrieveframe = Frame(root)
        self.retrieveframe.pack()
        # Now to post them on the frame as "There are X units of ITEM in CONTAINER"
        for each in g:
            for container in self.inventory:
                for item in self.inventory[container]:
                    for i in item:
                        if each in i:
                            Label(self.retrieveframe, text="There are " + str(item[i]["Quantity"]) + " " + each +
                                                           " in " + container + " Container").pack()
        self.Return = Button(self.retrieveframe, text="HOME",
                             command=lambda: [self.home_frame(), self.retrieveframe.destroy()])
        self.Return.pack()
        self.Return.bind("<Enter>", self.on_enter)
        self.Return.bind("<Leave>", self.on_leave)

    def update(self, data):
        # Clear the listbox
        self.listbox.delete(0, END)
        # Add items to listbox
        for each in data:
            self.listbox.insert(END, each)



    def Searchf(self, e):
        # Searches inventory for items
        typed = self.Search.get()
        if typed == "":
            data = ""
        else:
            data = PrepStore2.Search(self.inventory, typed)

        self.update(data)

        # Now to get the listbox to update
        # https://www.youtube.com/watch?v=0CXQ3bbBLVk&list=PLCC34OHNcOtoC6GglhF3ncJ5rLwQrLGnV&index=162
Prep = Prep(root)
Prep.home_frame()
mainloop()