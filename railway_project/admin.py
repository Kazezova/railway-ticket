import re
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import font
from turtle import color, setpos, width, write
from PIL import ImageTk, Image
from entry_with_placeholder import EntryWithPlaceholder
from tkinter_custom_button import TkinterCustomButton
from constants import *
from dynamic_entry import DynamicEntry
from tkcalendar import DateEntry
from datetime import date
from connect import conn
from tkinter import ttk
import pandas as pd

cursor = conn.cursor()


class Admin():
    def __init__(self, parent):
        self.parent = parent
        self.master = Frame(self.parent, bg=BACKGROUND)
        self.master.pack(fill=BOTH, side=TOP, expand=True)
        Label(self.master, text='Welcome,', bg=BACKGROUND, fg=SKY, font=(MAIN_FONT, 23, 'bold')).place(relx=0.2,
                                                                                                       rely=0.15)
        Label(self.master, text='Admin', bg=BACKGROUND, fg=RED, font=(MAIN_FONT, 23, 'bold')).place(rely=0.15,
                                                                                                    relx=0.54)
        self.status_button = TkinterCustomButton(
            master=self.master, text="Статус пользователя", fg_color=RED, hover_color=RED_LIGHT,
            width=200, command=self.procedure3
        )
        self.procedure_button = TkinterCustomButton(
            master=self.master, text="Просмотр задержку", fg_color=RED, hover_color=RED_LIGHT,
            width=200, command=self.procedure5
        )
        self.penalty_button = TkinterCustomButton(
            master=self.master, text="Штраф", fg_color=RED, hover_color=RED_LIGHT,
            width=200, command=self.procedure7
        )
        self.items_button = TkinterCustomButton(
            master=self.master, text="lost item", fg_color=RED, hover_color=RED_LIGHT,
            width=200, command=self.procedure8
        )
        self.status_button.place(relx=0.25, rely=0.5)
        self.procedure_button.place(relx=0.25, rely=0.6)
        self.penalty_button.place(relx=0.25, rely=0.7)
        self.items_button.place(relx=0.25, rely=0.8)

    def procedure5(self):
        self.master.forget()
        self.frame = Frame(self.parent, bg=BACKGROUND)
        self.frame.pack(fill=BOTH, expand=1, side=TOP)
        self.pro5_back = TkinterCustomButton(master=self.frame, text='\U000021AA', hover_color=SKY, fg_color=BACKGROUND,
                                             width=70, command=self.back_from_pro5, text_font=(MAIN_FONT, 25),
                                             text_color=WHITE)
        self.pro5_back.place(relx=0.005, rely=0.005)
        Label(self.frame, text='Для просмотра задержок необходимо\nввести ниже перечисленные данные', bg=BACKGROUND,
              fg=RED, font=('Consolas', 14, 'bold')).place(relx=0.07, rely=0.1)

        self.from_entry = ttk.Combobox(self.frame, values=list(range(1, 25)), font=(MAIN_FONT, 13))
        self.to_entry = ttk.Combobox(self.frame, values=list(range(1, 25)), font=(MAIN_FONT, 13))
        Label(self.frame, text='Station-1:', bg=BACKGROUND, fg=SKY, font=(MAIN_FONT, 13, 'bold')).place(relx=0.15,
                                                                                                        rely=0.2)
        Label(self.frame, text='Station-2:', bg=BACKGROUND, fg=SKY, font=(MAIN_FONT, 13, 'bold')).place(relx=0.55,
                                                                                                        rely=0.2)
        self.from_entry.place(relx=0.15, rely=0.25, relwidth=0.3);
        self.to_entry.place(relx=0.55, rely=0.25, relwidth=0.3)

        Label(self.frame, text='Train:', bg=BACKGROUND, fg=SKY, font=(MAIN_FONT, 13, 'bold')).place(relx=0.25,
                                                                                                    rely=0.35)
        self.train_entry = ttk.Combobox(self.frame, values=list(range(100000, 600001, 100000)), font=(MAIN_FONT, 13))
        self.train_entry.place(relx=0.25, rely=0.4)

        self.delay_time_entry = EntryWithPlaceholder(self.frame, placeholder='Delay time', color=BACKGROUND)
        self.delay_time_entry.config(highlightbackground=SKY, highlightcolor=SKY, highlightthickness=1,
                                     font=('rockwell', 13, 'italic'))
        self.delay_time_entry.place(relx=0.25, rely=0.5, relwidth=0.5)

        self.yes_no = ''
        self.int_var = IntVar()
        Label(self.frame, text="Is it train company's fault?", bg=BACKGROUND, fg=SKY,
              font=(MAIN_FONT, 14, 'bold')).place(relx=0.25, rely=0.57)
        self.no_button = Radiobutton(self.frame, variable=self.int_var, text='NO', command=self.no_value, value=1,
                                     bg=BACKGROUND, fg=SKY, activebackground=BACKGROUND, activeforeground=SKY,
                                     font=(MAIN_FONT, 13, 'bold italic'))
        self.yes_button = Radiobutton(self.frame, variable=self.int_var, text='YES', command=self.yes_value, value=2,
                                      bg=BACKGROUND, fg=SKY, activebackground=BACKGROUND, activeforeground=SKY,
                                      font=(MAIN_FONT, 13, 'bold italic'))
        self.yes_button.place(relx=0.3, rely=0.62);
        self.no_button.place(rely=0.62, relx=0.5)

        self.direction_entry = EntryWithPlaceholder(self.frame, placeholder='Direction', color=BACKGROUND)
        self.direction_entry.config(highlightbackground=SKY, highlightcolor=SKY, font=('rockwell', 13, 'italic'),
                                    highlightthickness=1)
        self.direction_entry.place(relx=0.3, rely=0.68)

        self.reason_entry = EntryWithPlaceholder(self.frame, placeholder='Reason', color=BACKGROUND)
        self.reason_entry.config(highlightbackground=SKY, highlightcolor=SKY, font=('rockwell', 13, 'italic'),
                                 highlightthickness=1)
        self.reason_entry.place(relx=0.15, rely=0.75, relwidth=0.7)

        self.button = TkinterCustomButton(
            master=self.frame, text='Execute', fg_color=RED, hover_color=RED_LIGHT, corner_radius=5,
            command=self.execute
        )
        self.button.place(relx=0.35, rely=0.85)

    def no_value(self):
        self.yes_no = 'NO'

    def yes_value(self):
        self.yes_no = 'YES'

    def execute(self):
        cursor.execute(f"""
        EXEC PROCEDURE5_train_delay 
        {self.from_entry.get()},{self.to_entry.get()},{self.train_entry.get()},'{self.delay_time_entry.get()}',
        '{self.yes_no}','{self.direction_entry.get()}', '{self.reason_entry.get()}'
        """)
        self.new_frame = Toplevel(self.frame)
        cursor.execute("""SELECT name FROM sys.dm_exec_describe_first_result_set_for_object
        ( OBJECT_ID('dbo.PROCEDURE5_TRAIN_SCHEDULE'), NULL)"""
                       )
        self.xscroll = Scrollbar(self.new_frame, orient=HORIZONTAL)
        self.yscroll = Scrollbar(self.new_frame, orient=VERTICAL)
        self.table = ttk.Treeview(
            self.new_frame, columns=[i[0] for i in cursor.fetchall()], show='headings',
            xscrollcommand=self.xscroll.set, yscrollcommand=self.yscroll.set
        )
        self.xscroll['command'] = self.table.xview
        self.yscroll['command'] = self.table.yview
        self.xscroll.pack(side=BOTTOM, fill=X)
        self.yscroll.pack(side=RIGHT, fill=Y)

        for i in self.table['columns']:
            self.table.heading(i, text=i, anchor=CENTER)
            self.table.column(i, width=70)
        cursor.execute("EXEC PROCEDURE5_train_schedule")
        iid = 0
        for i in cursor.fetchall():
            self.table.insert(parent='', index='end', iid=iid, values=list(i))
            iid += 1
        self.table.pack(fill=BOTH, expand=1)

    def procedure3(self):
        self.master.forget()
        self.frm = Frame(self.parent, bg=BACKGROUND)
        self.frm.pack(fill=BOTH, expand=1, side=TOP)
        self.pro3_back = TkinterCustomButton(master=self.frm, text='\U000021AA', hover_color=SKY, fg_color=BACKGROUND,
                                             width=70, command=self.back_from_pro3, text_font=(MAIN_FONT, 25),
                                             text_color=WHITE)
        self.pro3_back.place(relx=0.05, rely=0.05)
        Label(self.frm, text='Введите\n номер пользователя\n и статус', bg=BACKGROUND, fg=RED,
              font=(MAIN_FONT, 22, 'italic')).place(relx=0.15, rely=0.2)
        self.user_ent = EntryWithPlaceholder(master=self.frm, placeholder='Passenger', color=BACKGROUND)
        self.status_ent = EntryWithPlaceholder(master=self.frm, placeholder='Status', color=BACKGROUND)
        self.user_ent.config(highlightbackground=SKY, highlightcolor=SKY, font=(MAIN_FONT, 15))
        self.status_ent.config(highlightbackground=SKY, highlightcolor=SKY, font=(MAIN_FONT, 15, 'bold italic'))
        self.user_ent.place(relx=0.35, rely=0.4, relwidth=0.3)
        self.status_ent.place(relx=0.25, rely=0.6)
        self.change_but = TkinterCustomButton(
            master=self.frm, text='Изменить', hover_color=RED_LIGHT, fg_color=RED, corner_radius=7,
            width=150, command=self.change_status
        )
        self.change_but.place(relx=0.3, rely=0.8)

    def change_status(self):
        self.user = self.user_ent.get()
        self.status = self.status_ent.get()
        cursor.execute(
            F"EXEC PROCEDURE3_50_percent_discount {self.user},'{self.status}'"
        )
        messagebox.showinfo('Статус', f"Статус и цены пользователя №{self.user} \nуспешно изменены")

    def back_from_pro3(self):
        self.frm.forget()
        Admin(self.parent)

    def back_from_pro5(self):
        self.frame.forget()
        Admin(self.parent)

    def procedure7(self):
        self.master.forget()
        self.penalty_frame = Frame(self.parent, bg=BACKGROUND)
        self.penalty_frame.pack(fill=BOTH, expand=1, side=TOP)
        self.main_back = TkinterCustomButton(
            master=self.penalty_frame, text='\U000021AA', hover_color=SKY, fg_color=BACKGROUND,
            width=70, command=self.back_from_pro7, text_font=(MAIN_FONT, 25), text_color=WHITE)
        self.main_back.place(relx=0.1, rely=0.05)
        self.add_pen = TkinterCustomButton(
            master=self.penalty_frame, text='Добавить штраф', hover_color=RED_LIGHT, fg_color=RED, width=180,
            command=self.adding_pen
        )
        self.change_pen = TkinterCustomButton(
            master=self.penalty_frame, text='Изменить штраф', hover_color=RED_LIGHT, fg_color=RED, width=180,
            command=self.changing_pen
        )
        self.show_pen = TkinterCustomButton(
            master=self.penalty_frame, text='Посмотреть штрафы', hover_color=RED_LIGHT, fg_color=RED, width=180,
            command=self.showing
        )
        self.add_pen.place(relx=0.3, rely=0.3)
        self.change_pen.place(relx=0.3, rely=0.5)
        self.show_pen.place(relx=0.3, rely=0.7)

    def back_from_pro7(self):
        self.penalty_frame.forget()
        Admin(self.parent)

    def adding_pen(self):
        self.penalty_frame.forget()
        self.adding_frame = Frame(self.parent, bg=BACKGROUND)
        self.current = 'add'
        self.adding_frame.pack(fill=BOTH, expand=1, side=TOP)
        self.to_back = TkinterCustomButton(
            master=self.adding_frame, text='\U000021AA', hover_color=SKY, fg_color=BACKGROUND,
            width=70, command=self.back_pen_frame, text_font=(MAIN_FONT, 25), text_color=WHITE)
        self.to_back.place(relx=0.1, rely=0.05)
        d = {
            'Passenger_id': 100,
            'Penalty_price': 100,
            'Penalty_status': 200
        }
        a = 0
        for i in d.keys():
            exec(
                f"self.{i} = EntryWithPlaceholder(self.adding_frame,placeholder='{i}',color = BACKGROUND);"
                f"self.{i}.config(highlightbackground=SKY,highlightcolor=SKY,font=(MAIN_FONT,15,'bold italic'),justify=CENTER);"
                f"self.{i}.place(relx=0.3,rely=0.2+a)"
            )
            a += 0.1
        self.description = ttk.Combobox(self.adding_frame,
                                        values=["Smoked in the wrong place",
                                                "Fight on the train with other passengers",
                                                "Got drunk on the train", "else"], font=(MAIN_FONT, 13))
        self.description.place(relx=0.3, rely=0.6)
        self.adding_button = TkinterCustomButton(master=self.adding_frame,
                                                 text='Add', hover_color=SKY, fg_color=BACKGROUND, command=self.adding)
        self.adding_button.place(relx=0.3, rely=0.7)

    def changing_pen(self):
        self.penalty_frame.forget()
        self.changing_frame = Frame(self.parent, bg=BACKGROUND)
        self.current = 'change'
        self.changing_frame.pack(fill=BOTH, expand=1, side=TOP)
        self.to_back = TkinterCustomButton(
            master=self.changing_frame, text='\U000021AA', hover_color=SKY, fg_color=BACKGROUND,
            width=70, command=self.back_pen_frame, text_font=(MAIN_FONT, 25), text_color=WHITE)
        self.to_back.place(relx=0.1, rely=0.05)

        self.penalty_id = EntryWithPlaceholder(
            master=self.changing_frame, placeholder='Penalty_Id', color=BACKGROUND
        )
        self.penalty_id.config(highlightbackground=SKY, highlightcolor=SKY, font=(MAIN_FONT, 15, 'bold italic'),
                               justify=CENTER)
        self.penalty_id.place(relx=0.2, rely=0.3)
        self.penalty_status = EntryWithPlaceholder(
            master=self.changing_frame, placeholder='Penalty_status', color=BACKGROUND
        )
        self.penalty_status.config(highlightbackground=SKY, highlightcolor=SKY, font=(MAIN_FONT, 15, 'bold italic'),
                                   justify=CENTER)
        self.penalty_status.place(relx=0.2, rely=0.5)
        self.changing_button = TkinterCustomButton(master=self.changing_frame,
                                                   text='Change', hover_color=SKY, fg_color=BACKGROUND,
                                                   command=self.changing)
        self.changing_button.place(relx=0.3, rely=0.7)

    def adding(self):
        cursor.execute(
            f"EXEC PROCEDURE7_penalty {self.Passenger_id.get()},'{self.descpiption.get()}',{self.Penalty_price.get()},'{self.Penalty_status.get()}'")
        messagebox.showinfo("Штраф", "Штраф зачислен!")

    def changing(self):
        cursor.execute(
            f"EXEC PROCEDURE7_penalty_paid {self.penalty_id.get()},'{self.penalty_status.get()}'"
        )
        messagebox.showinfo("Штраф", "Данные штрафа изменены!")

    def showing(self):
        df = pd.read_sql_query("SELECT * FROM penalty", conn)
        with pd.io.excel.ExcelWriter('results.xlsx') as writer:
            df.to_excel(writer)

    def back_pen_frame(self):
        if self.current == 'add':
            self.adding_frame.forget()
            self.procedure7()
        else:
            self.changing_frame.forget()
            self.procedure7()

    def procedure8(self):
        self.master.forget()
        self.frame_8 = Frame(self.parent, bg=BACKGROUND)
        self.frame_8.pack(fill=BOTH, expand=1, side=TOP)
        self.go_back = TkinterCustomButton(
            master=self.frame_8, text='\U000021AA', hover_color=SKY, fg_color=BACKGROUND,
            width=70, command=self.back_from_pro8, text_font=(MAIN_FONT, 25), text_color=WHITE
        )
        self.go_back.place(relx=0.1, rely=0.1)
        self.adding_8 = TkinterCustomButton(
            master=self.frame_8, text='Добавить', hover_color=RED_LIGHT, fg_color=RED, width=150,
            command=self.add_8
        )
        self.changing_8 = TkinterCustomButton(
            master=self.frame_8, text='Изменить', hover_color=RED_LIGHT, fg_color=RED, width=150,
            command=self.change_8
        )
        self.showing_8 = TkinterCustomButton(
            master=self.frame_8, text='Просмотреть', hover_color=RED_LIGHT, fg_color=RED, width=150,
            command=self.show_8
        )
        self.adding_8.place(relx=0.3, rely=0.3)
        self.changing_8.place(relx=0.3, rely=0.5)
        self.showing_8.place(relx=0.3, rely=0.7)

    def back_from_pro8(self):
        self.frame_8.forget()
        Admin(self.parent)

    def add_8(self):
        self.frame_8.forget()
        self.add_frame_8 = Frame(self.parent, bg=BACKGROUND)
        self.add_frame_8.pack(fill=BOTH, expand=1, side=TOP)
        self.current = 'add'
        self.pro8_back = TkinterCustomButton(
            master=self.add_frame_8, text='\U000021AA', hover_color=SKY, fg_color=BACKGROUND,
            width=70, command=self.back_pro8, text_font=(MAIN_FONT, 25), text_color=WHITE
        )
        self.pro8_back.place(relx=0.1, rely=0.05)
        d = {
            'Item_name', 'Item_description', 'Item_status', 'Item_weight', 'Item_repaiment'
        }
        a = 0
        for i in d:
            exec(
                f"self.{i} = EntryWithPlaceholder(self.add_frame_8,placeholder='{i}',color = BACKGROUND);"
                f"self.{i}.config(highlightbackground=SKY,highlightcolor=SKY,font=(MAIN_FONT,15,'bold italic'),justify=CENTER);"
                f"self.{i}.place(relx=0.25,rely=0.15+a)"
            )
            a += 0.1
        self.adding_button = TkinterCustomButton(master=self.add_frame_8,
                                                 text='Add', hover_color=RED_LIGHT, fg_color=RED, command=self.add_item)
        self.adding_button.place(relx=0.25, rely=0.7)

    def change_8(self):
        self.frame_8.forget()
        self.change_frame_8 = Frame(self.parent, bg=BACKGROUND)
        self.change_frame_8.pack(fill=BOTH, expand=1, side=TOP)
        self.current = 'change'
        self.pro8_back = TkinterCustomButton(
            master=self.change_frame_8, text='\U000021AA', hover_color=SKY, fg_color=BACKGROUND,
            width=70, command=self.back_pro8, text_font=(MAIN_FONT, 25), text_color=WHITE
        )
        self.pro8_back.place(relx=0.1, rely=0.05)
        self.item_id = EntryWithPlaceholder(
            master=self.change_frame_8, placeholder='Item Id', color=BACKGROUND
        )
        self.item_id.config(highlightbackground=SKY, highlightcolor=SKY, font=(MAIN_FONT, 14, 'bold italic'))
        self.item_status = EntryWithPlaceholder(
            master=self.change_frame_8, placeholder='Item status', color=BACKGROUND
        )
        self.item_status.config(highlightbackground=SKY, highlightcolor=SKY, font=(MAIN_FONT, 14, 'bold italic'),
                                justify=CENTER)
        self.item_id.place(relx=0.05, rely=0.4, relwidth=0.3);
        self.item_status.place(relx=0.45, rely=0.4)
        self.changing_button = TkinterCustomButton(master=self.change_frame_8,
                                                   text='Change', hover_color=RED_LIGHT, fg_color=RED,
                                                   command=self.change_item)
        self.changing_button.place(relx=0.3, rely=0.7)

    def show_8(self):
        df = pd.read_sql_query("SELECT * FROM lost_items", conn)
        with pd.io.excel.ExcelWriter('results.xlsx') as writer:
            df.to_excel(writer)

    def back_pro8(self):
        if self.current == 'add':
            self.add_frame_8.forget()
            self.procedure8()
        else:
            self.change_frame_8.forget()
            self.procedure8()

    def add_item(self):
        cursor.execute(
            f"exec PROCEDURE8_lost_items '{self.Item_name.get()}','{self.Item_description.get()}','{self.Item_status.get()}',{self.Item_weight.get()},{self.Item_repaiment.get()}"
        )
        messagebox.showinfo('Предметы', "Данные о потеренном предмете успешно записан!")

    def change_item(self):
        cursor.execute(
            f"EXEC PROCEDURE8_lost_items_status {self.item_id.get()},'{self.item_status.get()}'"
        )
        messagebox.showinfo('Предметы', 'Предмет успешно найден!')


root = tk.Tk()
root.geometry(SCREEN_SIZE)
root.configure(background=BACKGROUND)
root.resizable(width=False, height=False)

Admin(root)
root.mainloop()