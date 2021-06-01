import tkinter as tk


class DynamicEntry(tk.Frame):
    def __init__(self, parent, font, *args):
        tk.Frame.__init__(self, parent)

        self.choices = args

        self.entryVar = tk.StringVar()
        self.entry = tk.Entry(self, textvariable=self.entryVar, font=font)
        self.listbox = tk.Listbox(self)
        self.listbox.insert("end", *self.choices)

        self.entry.pack(side="top", fill="x")
        self.listbox.pack(side="top", fill="both", expand=True)

        self.entryVar.trace("w", self.show_choices)
        self.listbox.bind("<<ListboxSelect>>", self.on_listbox_select)

    def on_listbox_select(self, event):
        """Set the value based on the item that was clicked"""
        index = self.listbox.curselection()[0]
        data = self.listbox.get(index)
        self.entryVar.set(data)

    def show_choices(self, name1, name2, op):
        """Filter choices based on what was typed in the entry"""
        pattern = self.entryVar.get()
        choices = [x for x in self.choices if x.startswith(pattern)]
        self.listbox.delete(0, "end")
        self.listbox.insert("end", *choices)


if __name__ == "__main__":
    root = tk.Tk()
    choices = ("one", "two", "three", "four", "five",
                        "six", "seven", "eight", "nine", "ten",
                        "eleven", "twelve", "thirteen", "fourteen",
                        "fifteen", "sixteen", "seventeen", "eighteen",
                        "nineteen", "twenty")
    DynamicEntry(root, *choices).place(relx=0, rely=0, relwidth=1, relheight=0.2)
    root.mainloop()
