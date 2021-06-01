import re
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import font
from PIL import ImageTk, Image
from entry_with_placeholder import EntryWithPlaceholder
from tkinter_custom_button import TkinterCustomButton
from constants import *
from dynamic_entry import DynamicEntry
from tkcalendar import DateEntry
from datetime import date, datetime
from dateutil import parser
from connect import conn
from functools import partial

cursor = conn.cursor()

SELECTED_seat = None


class Main:
    def __init__(self, parent, user_id):
        self.parent = parent
        self.user = user_id
        self.frame = tk.Frame(self.parent, bg=BACKGROUND)
        self.frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.83)
        self.label_font = font.Font(family=MAIN_FONT, size=30, weight='bold')
        self.entry_font = font.Font(family=MAIN_FONT, size=13, weight='bold')
        tk.Label(self.parent,
                 text='RAILWAY',
                 font=self.label_font,
                 bg=BACKGROUND,
                 fg=RED,
                 anchor='e').place(relx=0.2, rely=0.03, relwidth=0.45, relheight=0.05)
        tk.Label(self.parent,
                 text='.KZ',
                 font=self.label_font,
                 bg=BACKGROUND,
                 fg=SKY,
                 anchor='w').place(relx=0.65, rely=0.03, relwidth=0.2, relheight=0.05)

        self.booking()
        self.search_img = ImageTk.PhotoImage(Image.open('./icons/loupe.png').resize((26, 26), Image.ANTIALIAS))
        self.btn_search = tk.Button(master=self.parent, image=self.search_img, bd=1, bg=BACKGROUND,
                                    activebackground=SKY, command=self.booking)
        self.btn_search.place(relx=0, rely=0.93, relwidth=0.167, relheight=0.07)

        self.user_img = ImageTk.PhotoImage(Image.open('./icons/user.png').resize((26, 26), Image.ANTIALIAS))
        self.btn_user = tk.Button(master=self.parent, image=self.user_img, bd=1, bg=BACKGROUND, activebackground=SKY,
                                  command=self.profile)
        self.btn_user.place(relx=0.167, rely=0.93, relwidth=0.167, relheight=0.07)

        self.return_img = ImageTk.PhotoImage(Image.open('./icons/return.png').resize((26, 26), Image.ANTIALIAS))
        self.btn_return = tk.Button(master=self.parent, image=self.return_img, bd=1, bg=BACKGROUND,
                                    activebackground=SKY, command=self.return_ticket)
        self.btn_return.place(relx=0.334, rely=0.93, relwidth=0.167, relheight=0.07)

        self.schedule_img = ImageTk.PhotoImage(Image.open('./icons/schedule.png').resize((26, 26), Image.ANTIALIAS))
        self.btn_schedule = tk.Button(master=self.parent, image=self.schedule_img, bd=1, bg=BACKGROUND,
                                      activebackground=SKY, command=self.schedule)
        self.btn_schedule.place(relx=0.501, rely=0.93, relwidth=0.167, relheight=0.07)

        self.info_img = ImageTk.PhotoImage(Image.open('./icons/information.png').resize((26, 26), Image.ANTIALIAS))
        self.btn_info = tk.Button(master=self.parent, image=self.info_img, bd=1, bg=BACKGROUND, activebackground=SKY,
                                  command=self.info)
        self.btn_info.place(relx=0.668, rely=0.93, relwidth=0.167, relheight=0.07)

        self.more_img = ImageTk.PhotoImage(Image.open('./icons/more.png').resize((26, 26), Image.ANTIALIAS))
        self.btn_more = tk.Button(master=self.parent, image=self.more_img, bd=1, bg=BACKGROUND, activebackground=SKY,
                                  command=self.more)
        self.btn_more.place(relx=0.835, rely=0.93, relwidth=0.167, relheight=0.07)
        self.style = ttk.Style()

    def review(self):

        def get_text(user):
            s = text.get(1.0, tk.END)
            review = s

            if star5_btn['fg'] == BLACK:
                starss = 5
            elif star4_btn['fg'] == BLACK:
                starss = 4
            elif star3_btn['fg'] == BLACK:
                starss = 3
            elif star2_btn['fg'] == BLACK:
                starss = 2
            elif star1_btn['fg'] == BLACK:
                starss = 1
            else:
                starss = 0

            cursor.execute("EXEC PROCEDURE9_review '%s', '%i', '%i'" % (review, starss, user))
            cursor.commit()
            tk.messagebox.showinfo('status', 'Спасибо за отзыв!')

        def delete_text():
            text.delete(1.0, tk.END)
            star1_btn['image'] = root.photoimgg22
            star2_btn['image'] = root.photoimgg22
            star3_btn['image'] = root.photoimgg22
            star4_btn['image'] = root.photoimgg22
            star5_btn['image'] = root.photoimgg22

            star1_btn['fg'] = WHITE
            star2_btn['fg'] = WHITE
            star3_btn['fg'] = WHITE
            star4_btn['fg'] = WHITE
            star5_btn['fg'] = WHITE

        def star1():
            star1_btn['image'] = root.photoimgg11
            star2_btn['image'] = root.photoimgg22
            star3_btn['image'] = root.photoimgg22
            star4_btn['image'] = root.photoimgg22
            star5_btn['image'] = root.photoimgg22

            star1_btn['fg'] = BLACK
            star2_btn['fg'] = WHITE
            star3_btn['fg'] = WHITE
            star4_btn['fg'] = WHITE
            star5_btn['fg'] = WHITE

        def star2():
            star1_btn['image'] = root.photoimgg11
            star2_btn['image'] = root.photoimgg11
            star3_btn['image'] = root.photoimgg22
            star4_btn['image'] = root.photoimgg22
            star5_btn['image'] = root.photoimgg22

            star1_btn['fg'] = BLACK
            star2_btn['fg'] = BLACK
            star3_btn['fg'] = WHITE
            star4_btn['fg'] = WHITE
            star5_btn['fg'] = WHITE

        def star3():
            star1_btn['image'] = root.photoimgg11
            star2_btn['image'] = root.photoimgg11
            star3_btn['image'] = root.photoimgg11
            star4_btn['image'] = root.photoimgg22
            star5_btn['image'] = root.photoimgg22

            star1_btn['fg'] = BLACK
            star2_btn['fg'] = BLACK
            star3_btn['fg'] = BLACK
            star4_btn['fg'] = WHITE
            star5_btn['fg'] = WHITE

        def star4():
            star1_btn['image'] = root.photoimgg11
            star2_btn['image'] = root.photoimgg11
            star3_btn['image'] = root.photoimgg11
            star4_btn['image'] = root.photoimgg11
            star5_btn['image'] = root.photoimgg22

            star1_btn['fg'] = BLACK
            star2_btn['fg'] = BLACK
            star3_btn['fg'] = BLACK
            star4_btn['fg'] = BLACK
            star5_btn['fg'] = WHITE

        def star5():
            star1_btn['image'] = root.photoimgg11
            star2_btn['image'] = root.photoimgg11
            star3_btn['image'] = root.photoimgg11
            star4_btn['image'] = root.photoimgg11
            star5_btn['image'] = root.photoimgg11

            star1_btn['fg'] = BLACK
            star2_btn['fg'] = BLACK
            star3_btn['fg'] = BLACK
            star4_btn['fg'] = BLACK
            star5_btn['fg'] = BLACK

        root = tk.Toplevel()
        root.geometry('400x600')
        BACKGROUND = ("#213142")
        BLACK = ("#000000")
        WHITE = '#FFFFFF'
        RED = '#D63A29'
        root.configure(background=BACKGROUND)

        text3 = tk.Label(root, text="", fg=WHITE, background=BACKGROUND)
        text3.pack()
        text4 = tk.Label(root, text="", fg=WHITE, background=BACKGROUND)

        text2 = tk.Label(root, text="Оставьте отзыв", fg=WHITE, background=BACKGROUND)
        text2.config(font=("Courier", 25))
        text2.pack()

        text = tk.Text(root, width=35, height=15)
        text.pack()

        frame = tk.Frame(root)
        frame.pack()

        tk.Button(frame, text="Оставить отзыв",
                  command=partial(get_text, self.user), background=RED).pack(side=tk.LEFT)

        tk.Button(frame, text="Очистить",
                  command=delete_text, background=RED).pack(side=tk.LEFT)

        text4.pack()

        imggg = Image.open("./icons/star1.png")
        imggg = imggg.resize((60, 60), Image.ANTIALIAS)
        root.photoimgg11 = ImageTk.PhotoImage(imggg)

        imggg2 = Image.open("./icons/star2.png")
        imggg2 = imggg2.resize((60, 60), Image.ANTIALIAS)
        root.photoimgg22 = ImageTk.PhotoImage(imggg2)

        star1_btn = tk.Button(root, image=root.photoimgg22, border=0, background=BACKGROUND,
                              command=star1, fg=WHITE)
        star1_btn.place(x=40, y=500)
        star2_btn = tk.Button(root, image=root.photoimgg22, border=0, background=BACKGROUND,
                              command=star2, fg=WHITE)
        star2_btn.place(x=105, y=500)

        star3_btn = tk.Button(root, image=root.photoimgg22, border=0, background=BACKGROUND,
                              command=star3, fg=WHITE)
        star3_btn.place(x=170, y=500)
        star4_btn = tk.Button(root, image=root.photoimgg22, border=0, background=BACKGROUND,
                              command=star4, fg=WHITE)
        star4_btn.place(x=235, y=500)
        star5_btn = tk.Button(root, image=root.photoimgg22, border=0, background=BACKGROUND,
                              command=star5, fg=WHITE)
        star5_btn.place(x=300, y=500)

        text5 = tk.Label(root, text="", fg=WHITE, background=BACKGROUND)
        text5.pack()
        text3 = tk.Label(root, text="Сколько звезд вы бы поставили?", fg=WHITE, background=BACKGROUND)
        text3.config(font=("Courier", 10))
        text3.pack()

        review = []
        starss = []

        root.mainloop()

    def lost_items(self):
        new = tk.Toplevel()
        cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='LOST_ITEMS'")

        style = ttk.Style()

        xscroll = tk.Scrollbar(new, orient=tk.HORIZONTAL)

        yscroll = tk.Scrollbar(new, orient=tk.VERTICAL)

        style.theme_use('clam')

        table = ttk.Treeview(

            new, columns=[i[0] for i in cursor], show='headings', xscrollcommand=xscroll.set, yscrollcommand=yscroll.set

        )

        style.configure('Treeview.Heading', background='#0894A5')

        xscroll['command'] = table.xview

        yscroll['command'] = table.yview

        xscroll.pack(side=tk.BOTTOM, fill=tk.X)

        yscroll.pack(side=tk.RIGHT, fill=tk.Y)

        for i in table['columns']:
            table.heading(i, text=i, anchor=tk.CENTER)

            table.column(i, width=70, anchor=tk.CENTER)

        cursor.execute("SELECT * FROM lost_items ")

        iid = 0

        for i in cursor:
            table.insert(parent='', index='end', iid=iid, values=list(i))

            iid += 1

        table.pack(fill=tk.BOTH, expand=1)

    def delay_trains(self):

        new_frame = tk.Toplevel()

        cursor.execute("""SELECT name FROM sys.dm_exec_describe_first_result_set_for_object

                ( OBJECT_ID('dbo.PROCEDURE5_TRAIN_SCHEDULE'), NULL)"""

                       )

        xscroll = tk.Scrollbar(new_frame, orient=tk.HORIZONTAL)

        yscroll = tk.Scrollbar(new_frame, orient=tk.VERTICAL)

        table = ttk.Treeview(

            new_frame, columns=[i[0] for i in cursor.fetchall()], show='headings',

            xscrollcommand=xscroll.set, yscrollcommand=yscroll.set

        )

        xscroll['command'] = table.xview

        yscroll['command'] = table.yview

        xscroll.pack(side=tk.BOTTOM, fill=tk.X)

        yscroll.pack(side=tk.RIGHT, fill=tk.Y)

        for i in table['columns']:
            table.heading(i, text=i, anchor=tk.CENTER)

            table.column(i, width=70)

        cursor.execute("EXEC PROCEDURE5_train_schedule")

        iid = 0

        for i in cursor.fetchall():
            table.insert(parent='', index='end', iid=iid, values=list(i))

            iid += 1

        table.pack(fill=tk.BOTH, expand=1)

    def more(self):
        dy = 0.15
        self.frame.forget()
        self.frame = tk.Frame(self.parent, bg=BACKGROUND)
        self.frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.83)
        btn_font = font.Font(family=MAIN_FONT, size=13, weight='bold')
        delay_img = ImageTk.PhotoImage(Image.open('./icons/clock.png').resize((26, 26), Image.ANTIALIAS))
        delay_btn = tk.Button(master=self.frame, bd=0, text='Расписание задержок поездов', image=delay_img,
                              compound=tk.LEFT,
                              font=btn_font, command=self.delay_trains)
        delay_btn.image = delay_img
        delay_btn.place(relx=0.05, rely=0 * dy, relwidth=0.9, relheight=0.1)

        lost_img = ImageTk.PhotoImage(Image.open('./icons/lost-items.png').resize((26, 26), Image.ANTIALIAS))
        lost_btn = tk.Button(master=self.frame, bd=0, text='Потерянные предметы', image=lost_img, compound=tk.LEFT,
                             font=btn_font, command=self.lost_items)
        lost_btn.image = lost_img
        lost_btn.place(relx=0.05, rely=1 * dy, relwidth=0.9, relheight=0.1)

        review_img = ImageTk.PhotoImage(Image.open('./icons/feedback.png').resize((26, 26), Image.ANTIALIAS))
        review_btn = tk.Button(master=self.frame, bd=0, text='Оставить отзыв', image=review_img, compound=tk.LEFT,
                               font=btn_font, command=self.review)
        review_btn.image = review_img
        review_btn.place(relx=0.05, rely=2 * dy, relwidth=0.9, relheight=0.1)

    def buy_card(self):
        cursor.execute("INSERT INTO discount(passenger_id) VALUES('%i')" % self.user)
        cursor.commit()
        cursor.execute("UPDATE pas_cash SET cash -= 5000, change='-' WHERE passenger_id='%i'" % self.user)
        cursor.commit()
        tk.messagebox.showinfo('status', 'Поздравляем, вы купили дисконтную карту! ')
        self.profile()

    def final_add_cash(self, entry):
        cash = int(entry.get())
        cursor.execute("UPDATE pas_cash SET cash += '%i', change='-' WHERE passenger_id='%i'" % (cash, self.user))
        cursor.commit()
        self.profile()

    def add_cash(self):
        level = tk.Toplevel(bg=BACKGROUND)
        entry = tk.Entry(level)
        entry.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.2)

        btn = tk.Button(level, text='ok', command=partial(self.final_add_cash, entry), bg=RED, fg=WHITE)
        btn.place(relx=0.35, rely=0.4, relwidth=0.3, relheight=0.2)

    def profile(self):
        self.frame.forget()
        self.frame = tk.Frame(self.parent, bg=BACKGROUND)
        self.frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.83)
        user = cursor.execute("SELECT * FROM passenger WHERE passenger_id='%i'" % self.user).fetchone()
        new_font = font.Font(family=MAIN_FONT, size=14)
        dy = 0.07
        tk.Label(self.frame,
                 text='Имя: ',
                 font=new_font,
                 bg=BACKGROUND,
                 fg=RED,
                 anchor='w').place(relx=0.05, rely=dy * 0, relwidth=0.4, relheight=0.05)
        tk.Label(self.frame,
                 text=user[3],
                 font=new_font,
                 bg=BACKGROUND,
                 fg=WHITE,
                 anchor='w').place(relx=0.45, rely=dy * 0, relwidth=0.5, relheight=0.05)
        tk.Label(self.frame,
                 text='Фамилия: ',
                 font=new_font,
                 bg=BACKGROUND,
                 fg=RED,
                 anchor='w').place(relx=0.05, rely=dy * 1, relwidth=0.4, relheight=0.05)
        tk.Label(self.frame,
                 text=user[4],
                 font=new_font,
                 bg=BACKGROUND,
                 fg=WHITE,
                 anchor='w').place(relx=0.45, rely=dy * 1, relwidth=0.5, relheight=0.05)

        tk.Label(self.frame,
                 text='Идентификация: ',
                 font=new_font,
                 bg=BACKGROUND,
                 fg=RED,
                 anchor='w').place(relx=0.05, rely=dy * 2, relwidth=0.4, relheight=0.05)
        tk.Label(self.frame,
                 text=user[5],
                 font=new_font,
                 bg=BACKGROUND,
                 fg=WHITE,
                 anchor='w').place(relx=0.45, rely=dy * 2, relwidth=0.5, relheight=0.05)

        tk.Label(self.frame,
                 text='Статус: ',
                 font=new_font,
                 bg=BACKGROUND,
                 fg=RED,
                 anchor='w').place(relx=0.05, rely=dy * 3, relwidth=0.4, relheight=0.05)
        if user[6] is None:
            user[6] = '-'
        tk.Label(self.frame,
                 text=user[6],
                 font=new_font,
                 bg=BACKGROUND,
                 fg=WHITE,
                 anchor='w').place(relx=0.45, rely=dy * 3, relwidth=0.5, relheight=0.05)
        response = ''
        valid = True
        cursor.execute("SELECT * FROM discount WHERE passenger_id='%i'" % self.user)

        if cursor.rowcount == 0:
            response += 'У пассажира нет дисконтной карты.'
            valid = False
        else:
            res = cursor.fetchone()
            date = res[3]
            persentage = res[2]
            bd_date = parser.parse(date)
            if datetime.now() > bd_date:
                response += 'К сожалению, срок действия дисконтной карты истек.'
                valid = False
        tk.Label(self.frame,
                 text='Дисконтная карта: ',
                 font=new_font,
                 bg=BACKGROUND,
                 fg=RED,
                 anchor='w').place(relx=0.05, rely=dy * 4, relwidth=0.4, relheight=0.05)

        if valid:
            if persentage == -1:
                persentage = 0
            tk.Label(self.frame,
                     text=str(persentage) + '%',
                     font=new_font,
                     bg=BACKGROUND,
                     fg=WHITE,
                     anchor='w').place(relx=0.45, rely=dy * 4, relwidth=0.5, relheight=0.05)
        else:
            n_font = font.Font(family=MAIN_FONT, size=10)
            tk.Label(self.frame,
                     text=response,
                     font=n_font,
                     bg=BACKGROUND,
                     fg=WHITE,
                     anchor='w').place(relx=0.45, rely=dy * 4, relwidth=0.55, relheight=0.05)

            discount_btn = tk.Button(self.frame, text='Купить дисконтную карту.',
                                     command=partial(self.buy_card),
                                     bg=RED, fg=WHITE)
            discount_btn.place(relx=0.45, rely=dy * 5, relwidth=0.5, relheight=0.05)

        tk.Label(self.frame,
                 text='Штраф: ',
                 font=new_font,
                 bg=BACKGROUND,
                 fg=RED,
                 anchor='w').place(relx=0.05, rely=dy * 6, relwidth=0.4, relheight=0.05)

        penalty = 0

        if cursor.execute("SELECT * FROM penalty WHERE passenger_id='%i'" % self.user).rowcount != 0:
            penalty = \
                cursor.execute("SELECT SUM(penalty_price) FROM penalty WHERE passenger_id='%i'" % self.user).fetchone()[
                    0]

        tk.Label(self.frame,
                 text=str(penalty) + ' тг.',
                 font=new_font,
                 bg=BACKGROUND,
                 fg=WHITE,
                 anchor='w').place(relx=0.45, rely=dy * 6, relwidth=0.5, relheight=0.05)

        tk.Label(self.frame,
                 text='Кошелок: ',
                 font=new_font,
                 bg=BACKGROUND,
                 fg=RED,
                 anchor='w').place(relx=0.05, rely=dy * 7, relwidth=0.4, relheight=0.05)

        cash = cursor.execute("SELECT cash FROM pas_cash WHERE passenger_id='%i'" % self.user).fetchone()[0]

        tk.Label(self.frame,
                 text=str(cash) + ' тг.',
                 font=new_font,
                 bg=BACKGROUND,
                 fg=WHITE,
                 anchor='w').place(relx=0.45, rely=dy * 7, relwidth=0.5, relheight=0.05)
        cash_btn = tk.Button(self.frame, text='Пополнить баланс.',
                             command=self.add_cash,
                             bg=RED, fg=WHITE)
        cash_btn.place(relx=0.45, rely=dy * 8, relwidth=0.5, relheight=0.05)

    def booking(self):
        self.frame.forget()
        self.frame = tk.Frame(self.parent, bg=BACKGROUND)
        self.frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.83)
        img = ImageTk.PhotoImage(Image.open('train.png').resize((401, 185), Image.ANTIALIAS))
        label = tk.Label(self.frame, image=img, bg=BACKGROUND)
        label.image = img
        label.place(relx=0, rely=0, relwidth=1, relheight=0.36)
        new_font = font.Font(family=MAIN_FONT, size=15)
        tk.Label(self.frame,
                 text='Рейс:',
                 font=new_font,
                 bg=BACKGROUND,
                 fg=SKY,
                 anchor='w').place(relx=0.05, rely=0.4, relwidth=1, relheight=0.05)

        choices = [i[0] for i in cursor.execute("SELECT trip_id FROM trip").fetchall()]
        trip = DynamicEntry(self.frame, self.entry_font, *choices)
        trip.place(relx=0.05, rely=0.45, relwidth=0.9, relheight=0.12)
        trip.config(highlightbackground=SKY, highlightcolor=SKY, highlightthickness=2)

        tk.Label(self.frame,
                 text='Дата:',
                 font=new_font,
                 bg=BACKGROUND,
                 fg=SKY,
                 anchor='w').place(relx=0.05, rely=0.58, relwidth=1, relheight=0.05)

        today = date.today()
        cal = DateEntry(self.frame, font=self.entry_font, width=12, background=SKY, foreground=WHITE, borderwidth=2,
                        mindate=today)
        cal.place(relx=0.05, rely=0.65, relwidth=0.9, relheight=0.07)

        search_btn = TkinterCustomButton(master=self.frame, text="Найти билеты", fg_color=RED,
                                         hover_color=RED_LIGHT,
                                         command=partial(self.find_tickets, trip, cal))
        search_btn.place(relx=0.35, rely=0.8)

    def info(self):
        self.frame.destroy()
        self.frame = tk.Frame(self.parent, bg=BACKGROUND)
        self.frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.83)
        style = ttk.Style()
        style.configure("style.Treeview.Heading", font=('Calibri', 13, 'bold'))
        style.configure("style.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11))
        style.layout("style.Treeview", [('style.Treeview.treearea', {'sticky': 'nswe'})])
        cols = ('Trip', 'From', 'To', 'Price')
        listBox = ttk.Treeview(self.frame, columns=cols, show='headings', style='style.Treeview')
        for col in cols:
            listBox.column(col, width=100, anchor='center')
            listBox.heading(col, text=col)
        listBox.place(relx=0, rely=0, relwidth=1, relheight=1)
        trip_list = cursor.execute('SELECT * FROM dbo.get_trip_info()').fetchall()

        s = None
        for i, (trip_id, from_station, to_station, price) in enumerate(trip_list):
            if i % 2 == 0:
                s = 'even'
            else:
                s = 'odd'
            listBox.insert("", "end", values=(trip_id, from_station, to_station, price), tags=(s,))

    def inside_return(self, ticket_id):
        print(ticket_id)
        if tk.messagebox.askquestion(message='Вы точно хотите вернуть билет?') == 'no':
            return
        status = cursor.execute("EXEC ticket_return @ticket_id='%i'" % ticket_id).fetchone()[0]
        print(status)
        if status:
            print(status)
            return_price = float(status.split()[6])
            cursor.execute(
                "UPDATE pas_cash SET cash -= '%f', change='+' WHERE passenger_id='%i'" % (return_price, self.user))
            cursor.commit()
            tk.messagebox.showinfo('status', status)
        Main.return_ticket(self)

    def return_ticket(self):

        self.frame.forget()
        self.frame = tk.Frame(self.parent, bg=BACKGROUND)
        self.frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.83)
        tickets = cursor.execute("EXEC report_of_passenger @passenger_id='%i'" % self.user).fetchall()
        d = {}
        for ticket in tickets:
            d[ticket[7]] = [ticket[4], ticket[5], ticket[6], ticket[8], ticket[9], ticket[10], ticket[11]]
        new_font = font.Font(family=MAIN_FONT, size=12)
        dy = 0
        for k, v in d.items():
            exec(
                f"ticket_frame_{k} = tk.Frame(self.frame, bd=1, highlightbackground=SKY, highlightcolor=SKY, highlightthickness=1)")
            exec(f"ticket_frame_{k}.place(relx=0.1, rely=dy, relwidth=0.8, relheight=0.15)")
            exec(f"order_{k} = 'Билет ' + str(k)")
            exec(
                f"tk.Label(ticket_frame_{k}, text=order_{k}, font=self.entry_font, anchor='w').place(relx=0.05, rely=0.05, relwidth=0.6, relheight = 0.3)")

            exec(
                f"return_img_{k} = ImageTk.PhotoImage(Image.open('./icons/return.png').resize((22, 22), Image.ANTIALIAS))")
            exec(
                f"btn_return_{k} = tk.Button(ticket_frame_{k}, image=return_img_{k}, bd=0, command=partial(self.inside_return, {k}))")
            exec(f"btn_return_{k}.image_{k} = return_img_{k}")
            exec(f"btn_return_{k}.place(relx=0.85, rely=0.05, relwidth=0.1, relheight=0.3)")

            exec(f"img_{k} = ImageTk.PhotoImage(Image.open('./icons/train.png').resize((24, 24), Image.ANTIALIAS))")
            exec(f"img_label_{k} = tk.Label(ticket_frame_{k}, image=img_{k})")
            exec(f"img_label_{k}.image = img_{k}")
            exec(f"img_label_{k}.place(relx=0.05, rely=0.35, relwidth=0.1, relheight=0.3)")

            exec(f"road_{k} = v[1] + '->' + v[2]")
            exec(
                f"tk.Label(ticket_frame_{k}, text=road_{k}, font=new_font, anchor='w').place(relx=0.15, rely=0.35, relwidth=0.8, relheight=0.3)")
            exec(f"date_{k} = v[0]")
            exec(
                f"tk.Label(ticket_frame_{k}, text=date_{k}, font=new_font, anchor='w').place(relx=0.15, rely=0.65, relwidth=0.8, relheight=0.3)")
            dy += 0.2

    def find_tickets(self, trip, cal):

        def seat_choose(user, d, trip, date):
            global SELECTED_seat
            dy = -0.1
            window = tk.Toplevel()
            window.resizable(width=False, height=False)

            labelimage = tk.Label(window)
            labelimage.pack()

            window.title("Welcome")

            window.geometry('1100x400')

            height = 600
            weight = 400

            GREEN = (0, 200, 64)
            LIGHTGREEN = (0, 255, 0)

            img = Image.open("./icons/red_btn.png")
            img = img.resize((30, 30), Image.ANTIALIAS)
            window.photoimgg = ImageTk.PhotoImage(img)

            img2 = Image.open("./icons/empty_btn.png")
            img2 = img2.resize((30, 30), Image.ANTIALIAS)
            window.photoimgg2 = ImageTk.PhotoImage(img2)

            img3 = Image.open("./icons/white_square.png")
            img3 = img3.resize((30, 30), Image.ANTIALIAS)
            window.photoimgg3 = ImageTk.PhotoImage(img3)

            img4 = Image.open("./icons/green_btn.png")
            img4 = img4.resize((30, 30), Image.ANTIALIAS)
            window.photoimgg4 = ImageTk.PhotoImage(img4)

            window.configure(background=BACKGROUND)
            label_font = font.Font(family=MAIN_FONT, size=20, weight='bold')
            coach = str(int(d[0] / 100 % 100))
            tk.Label(window,
                     text=coach + ' вагон',
                     font=label_font,
                     bg=BACKGROUND,
                     fg=WHITE,
                     anchor='w').place(relx=0.05, rely=0.2 + dy, relwidth=1, relheight=0.05)

            imgg = Image.open("./icons/kupe.png")
            resized_img = imgg.resize((1100, 200))
            window.photoimg = ImageTk.PhotoImage(resized_img)
            labelimage.configure(image=window.photoimg)

            labelimage.place(relx=0.5,
                             rely=0.6 + dy,
                             anchor='center')

            Free_seats = d.copy()

            Free_seats2 = d.copy()

            Leng = len(Free_seats)

            num = int(str(Free_seats[1])[:4]) * 100

            def b_tnn(roundedbutton):
                if Check == 1:
                    roundedbutton_test = tk.Button(window, image=window.photoimgg, text=roundedbutton,
                                                   compound="center",
                                                   fg='WHITE', command=lambda i=roundedbutton: on_click(i),
                                                   state=tk.DISABLED)
                    if len(Free_seats) != 0:
                        for i in range(len(Free_seats)):
                            if roundedbutton == 0:
                                roundedbutton_test = tk.Button(window, image=window.photoimgg3,
                                                               command=lambda i=roundedbutton: on_click(i))
                            elif Free_seats[i] % (int(str(Free_seats[i])[:4]) * 100) == roundedbutton:
                                roundedbutton_test = tk.Button(window, image=window.photoimgg2, text=roundedbutton,
                                                               compound="center", fg=BACKGROUND,
                                                               command=lambda i=roundedbutton: on_click(i))

                    roundedbutton_test["border"] = "0"
                    return roundedbutton_test

            # n1 = 0
            # n2 = 0
            # for i in range(len(Free_seats)):
            #     for j in range(len(Free_seats2)):
            #         if Free_seats[i]==Free_seats2[j]:
            #             n += 1

            def on_click(i):
                global SELECTED_seat
                if i != 0:
                    hh = 1
                    for j in range(len(Free_seats2)):
                        jjj = (Free_seats2[j] % (int(str(Free_seats2[j])[:4]) * 100))
                        if roundedbutton[jjj]['fg'] == BLACK:
                            hh = 2
                            gg = jjj
                            ss = j
                            # print("hh", hh)
                            # print("j", jjj)
                            # print("s", ss)

                    if hh == 1:
                        for j in range(len(Free_seats)):
                            if i + num == Free_seats[j]:
                                Free_seats.pop(j)
                                hh = 0
                                roundedbutton[i]['image'] = window.photoimgg4
                                roundedbutton[i]['fg'] = BLACK
                                break
                    if hh == 1:
                        Free_seats.append(i + num)
                        roundedbutton[i]['image'] = window.photoimgg2
                        roundedbutton[i]['fg'] = BACKGROUND
                    if hh == 2:
                        if (i == gg):
                            Free_seats.append(gg + num)
                            roundedbutton[i]['image'] = window.photoimgg2
                            roundedbutton[i]['fg'] = BACKGROUND
                            # print("helooooooooooo2")

                        elif (i != gg):
                            Free_seats.append(gg + num)
                            roundedbutton[gg]['image'] = window.photoimgg2
                            roundedbutton[gg]['fg'] = BACKGROUND
                            for kk in range(len(Free_seats)):
                                if i + num == Free_seats[kk]:
                                    # print(len(Free_seats))
                                    # print("kk",kk)
                                    # print("helooooooooooo")
                                    roundedbutton[i]['image'] = window.photoimgg4
                                    roundedbutton[i]['fg'] = BLACK
                                    Free_seats.pop(kk)
                                    # print("helooooooooooo")
                                    break
                    SELECTED_seat = None
                    for l in range(len(Free_seats2)):
                        lll = (Free_seats2[l] % (int(str(Free_seats2[l])[:4]) * 100))
                        if roundedbutton[lll]['fg'] == BLACK:
                            SELECTED_seat = [Free_seats2[l]][0]
                            # print(Free_seats2[l])

                    print("SELECTED_seat", SELECTED_seat)
                    # print("len", len(Free_seats))
                    # print(Free_seats)

            Check = 1
            roundedbutton = []

            # 28
            roundedbutton0 = 0
            roundedbutton0 = b_tnn(roundedbutton0)
            roundedbutton.append(roundedbutton0)
            roundedbutton[0].place(relx=0.716, rely=0.533 + dy)

            # 1
            roundedbutton1 = 1
            roundedbutton1 = b_tnn(roundedbutton1)
            roundedbutton.append(roundedbutton1)
            roundedbutton[1].place(relx=0.155, rely=0.415 + dy)

            # 2
            roundedbutton2 = 2
            roundedbutton2 = b_tnn(roundedbutton2)
            roundedbutton.append(roundedbutton2)
            roundedbutton[2].place(relx=0.155, rely=0.533 + dy)

            # 3
            roundedbutton3 = 3
            roundedbutton3 = b_tnn(roundedbutton3)
            roundedbutton.append(roundedbutton3)
            roundedbutton[3].place(relx=0.206, rely=0.415 + dy)

            # 4
            roundedbutton4 = 4
            roundedbutton4 = b_tnn(roundedbutton4)
            roundedbutton.append(roundedbutton4)
            roundedbutton[4].place(relx=0.206, rely=0.533 + dy)

            # 5
            roundedbutton5 = 5
            roundedbutton5 = b_tnn(roundedbutton5)
            roundedbutton.append(roundedbutton5)
            roundedbutton[5].place(relx=0.2403, rely=0.415 + dy)

            # 6
            roundedbutton6 = 6
            roundedbutton6 = b_tnn(roundedbutton6)
            roundedbutton.append(roundedbutton6)
            roundedbutton[6].place(relx=0.2403, rely=0.533 + dy)

            # 7
            roundedbutton7 = 7
            roundedbutton7 = b_tnn(roundedbutton7)
            roundedbutton.append(roundedbutton7)
            roundedbutton[7].place(relx=0.291, rely=0.415 + dy)

            # 8
            roundedbutton8 = 8
            roundedbutton8 = b_tnn(roundedbutton8)
            roundedbutton.append(roundedbutton8)
            roundedbutton[8].place(relx=0.291, rely=0.533 + dy)

            # 9
            roundedbutton9 = 9
            roundedbutton9 = b_tnn(roundedbutton9)
            roundedbutton.append(roundedbutton9)
            roundedbutton[9].place(relx=0.325, rely=0.415 + dy)

            # 10
            roundedbutton10 = 10
            roundedbutton10 = b_tnn(roundedbutton10)
            roundedbutton.append(roundedbutton10)
            roundedbutton[10].place(relx=0.325, rely=0.533 + dy)

            # 11
            roundedbutton11 = 11
            roundedbutton11 = b_tnn(roundedbutton11)
            roundedbutton.append(roundedbutton11)
            roundedbutton[11].place(relx=0.375, rely=0.415 + dy)

            # 12
            roundedbutton12 = 12
            roundedbutton12 = b_tnn(roundedbutton12)
            roundedbutton.append(roundedbutton12)
            roundedbutton[12].place(relx=0.375, rely=0.533 + dy)

            # 13
            roundedbutton13 = 13
            roundedbutton13 = b_tnn(roundedbutton13)
            roundedbutton.append(roundedbutton13)
            roundedbutton[13].place(relx=0.41, rely=0.415 + dy)

            # 14
            roundedbutton14 = 14
            roundedbutton14 = b_tnn(roundedbutton14)
            roundedbutton.append(roundedbutton14)
            roundedbutton[14].place(relx=0.41, rely=0.533 + dy)

            # 15
            roundedbutton15 = 15
            roundedbutton15 = b_tnn(roundedbutton15)
            roundedbutton.append(roundedbutton15)
            roundedbutton[15].place(relx=0.4605, rely=0.415 + dy)

            # 16
            roundedbutton16 = 16
            roundedbutton16 = b_tnn(roundedbutton16)
            roundedbutton.append(roundedbutton16)
            roundedbutton[16].place(relx=0.4605, rely=0.533 + dy)

            # 17
            roundedbutton17 = 17
            roundedbutton17 = b_tnn(roundedbutton17)
            roundedbutton.append(roundedbutton17)
            roundedbutton[17].place(relx=0.4945, rely=0.415 + dy)

            # 18
            roundedbutton18 = 18
            roundedbutton18 = b_tnn(roundedbutton18)
            roundedbutton.append(roundedbutton18)
            roundedbutton[18].place(relx=0.4945, rely=0.533 + dy)

            # 19
            roundedbutton19 = 19
            roundedbutton19 = b_tnn(roundedbutton19)
            roundedbutton.append(roundedbutton19)
            roundedbutton[19].place(relx=0.545, rely=0.415 + dy)

            # 20
            roundedbutton20 = 20
            roundedbutton20 = b_tnn(roundedbutton20)
            roundedbutton.append(roundedbutton20)
            roundedbutton[20].place(relx=0.545, rely=0.533 + dy)

            # 21
            roundedbutton21 = 21
            roundedbutton21 = b_tnn(roundedbutton21)
            roundedbutton.append(roundedbutton21)
            roundedbutton[21].place(relx=0.58, rely=0.415 + dy)

            # 22
            roundedbutton22 = 22
            roundedbutton22 = b_tnn(roundedbutton22)
            roundedbutton.append(roundedbutton22)
            roundedbutton[22].place(relx=0.58, rely=0.533 + dy)

            # 23
            roundedbutton23 = 23
            roundedbutton23 = b_tnn(roundedbutton23)
            roundedbutton.append(roundedbutton23)
            roundedbutton[23].place(relx=0.630, rely=0.415 + dy)

            # 24
            roundedbutton24 = 24
            roundedbutton24 = b_tnn(roundedbutton24)
            roundedbutton.append(roundedbutton24)
            roundedbutton[24].place(relx=0.630, rely=0.533 + dy)

            # 25
            roundedbutton25 = 25
            roundedbutton25 = b_tnn(roundedbutton25)
            roundedbutton.append(roundedbutton25)
            roundedbutton[25].place(relx=0.664, rely=0.415 + dy)

            # 26
            roundedbutton0 = 0
            roundedbutton0 = b_tnn(roundedbutton0)
            roundedbutton0.place(relx=0.664, rely=0.533 + dy)

            # 27
            roundedbutton26 = 26
            roundedbutton26 = b_tnn(roundedbutton26)
            roundedbutton.append(roundedbutton26)
            roundedbutton[26].place(relx=0.715, rely=0.415 + dy)

            # 29
            roundedbutton27 = 27
            roundedbutton27 = b_tnn(roundedbutton27)
            roundedbutton.append(roundedbutton27)
            roundedbutton[27].place(relx=0.749, rely=0.415 + dy)

            # 30
            roundedbutton0 = 0
            roundedbutton0 = b_tnn(roundedbutton0)
            roundedbutton0.place(relx=0.749, rely=0.533 + dy)

            # 31
            roundedbutton28 = 28
            roundedbutton28 = b_tnn(roundedbutton28)
            roundedbutton.append(roundedbutton28)
            roundedbutton[28].place(relx=0.800, rely=0.415 + dy)

            # 32
            roundedbutton0 = 0
            roundedbutton0 = b_tnn(roundedbutton0)
            roundedbutton0.place(relx=0.801, rely=0.533 + dy)

            # 33
            roundedbutton29 = 29
            roundedbutton29 = b_tnn(roundedbutton29)
            roundedbutton.append(roundedbutton29)
            roundedbutton[29].place(relx=0.8342, rely=0.415 + dy)

            # 34
            roundedbutton0 = 0
            roundedbutton0 = b_tnn(roundedbutton0)
            roundedbutton0.place(relx=0.8342, rely=0.533 + dy)

            # 35
            roundedbutton30 = 30
            roundedbutton30 = b_tnn(roundedbutton30)
            roundedbutton.append(roundedbutton30)
            roundedbutton[30].place(relx=0.8842, rely=0.415 + dy)

            # 36
            roundedbutton0 = 0
            roundedbutton0 = b_tnn(roundedbutton0)
            roundedbutton0.place(relx=0.8852, rely=0.533 + dy)

            def action(user, trip, date):
                global SELECTED_seat
                seat_id = SELECTED_seat
                window.destroy()
                print(seat_id)
                if seat_id is None:
                    messagebox.showinfo('status', 'Бронирование отменена.')
                    return
                cursor.execute(
                    "EXEC ticket_booking_part_2 @passenger_id='%i', @trip_id='%s', @date='%s', @seat_id='%i'" % (
                        user, trip, date, seat_id))
                ticket_id = cursor.execute("SELECT ticket_id FROM ticket WHERE depature_date='%s' AND seat_id='%i'" % (
                    date, seat_id)).fetchone()[0]
                price = cursor.execute("SELECT price FROM passenger_ticket WHERE ticket_id='%i'" % ticket_id).fetchone()[0]
                if tk.messagebox.askquestion('Страховка', 'Хотите ли вы купить страховку?') == 'yes':
                    cursor.execute("EXEC BUY_INSURANCE @TICKET_ID='%i'" % ticket_id)
                    txt = cursor.execute("SELECT dbo.INSURANCE_RES('%i')" % ticket_id).fetchone()[0]
                    messagebox.showinfo('Страховка', txt)
                    if txt != 'Так как у вас есть лготность, вы получите страховку бесплатно ':
                        price += (price * 0.2)

                price = float(price)

                cursor.execute(
                    "UPDATE pas_cash SET cash -= '%f', change='-' WHERE passenger_id='%i'" % (price, self.user))
                cursor.commit()
                messagebox.showinfo('status', 'Бронирование прошло успешно.')
                self.booking()

            search_btn = tk.Button(master=window, text="Выбрать место",
                                   command=partial(action, user, trip, date), bg=RED, fg=WHITE)
            search_btn.place(relx=0.5, rely=0.8)

            window.mainloop()

        trip = trip.entry.get()
        date = cal.get_date()
        ans = cursor.execute(
            "EXEC railway_new_db.dbo.ticket_booking_part_1 @trip_id='%s', @date='%s'" % (trip, date)).fetchall()
        if not ans:
            messagebox.showinfo("Status", "There are no free tickets.")
            self.booking()
            return
        self.frame.forget()
        self.frame = tk.Frame(self.parent, bg=BACKGROUND)
        self.frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.83)
        d = {}
        for each in ans:
            train_id = (each[0] // 100000) * 100000
            if each[0] not in d:
                d[each[0]] = [each[1]]
            else:
                d[each[0]] = d[each[0]] + [each[1]]
        train_name = cursor.execute("SELECT train_name FROM train WHERE train_id = '%i'" % train_id).fetchone()[0]
        price = cursor.execute("SELECT price FROM trip WHERE trip_id='%s'" % trip).fetchone()[0]
        label_font = font.Font(family=MAIN_FONT, size=30, weight='bold')
        entry_font = font.Font(family=MAIN_FONT, size=13, weight='bold')
        train_name_font = font.Font(family=MAIN_FONT, size=16, weight='bold')

        tk.Label(self.frame,
                 text='Поезд: ' + train_name,
                 font=train_name_font,
                 bg=BACKGROUND,
                 fg=WHITE,
                 anchor='w').place(relx=0.05, rely=0, relwidth=1, relheight=0.05)
        tk.Label(self.frame,
                 text='Цена билета: ' + str(price),
                 font=train_name_font,
                 bg=BACKGROUND,
                 fg=WHITE,
                 anchor='w').place(relx=0.05, rely=0.05, relwidth=1, relheight=0.05)
        y = 0.15
        user = self.user
        for k, v in d.items():
            coach = f'{int(k / 100 % 100)} вагон'
            exec(
                f"btn_{k} = tk.Button(self.frame, text=coach, bd=1, bg=WHITE, font=entry_font, command=partial(seat_choose, user, v, trip, date))")
            exec(f'btn_{k}.place(relx=0.05, rely=y, relwidth=0.9, relheight=0.05)')
            y += 0.05

    def schedule(self):

        self.frame.forget()
        self.frame = tk.Frame(self.parent, bg=BACKGROUND)
        self.frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.83)
        self.frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.83)
        img = ImageTk.PhotoImage(Image.open('train.png').resize((401, 185), Image.ANTIALIAS))
        label = tk.Label(self.frame, image=img, bg=BACKGROUND)
        label.image = img
        label.place(relx=0, rely=0, relwidth=1, relheight=0.36)
        tk.Label(self.frame,
                 text='Откуда:',
                 font=(MAIN_FONT, 15),
                 bg=BACKGROUND,
                 fg=SKY,
                 anchor='w').place(relx=0.05, rely=0.45, relwidth=1, relheight=0.05)

        choices = [i[0] for i in cursor.execute("SELECT station_name FROM station").fetchall()]
        from_entry = ttk.Combobox(self.frame, state='readonly', values=choices, font=(MAIN_FONT, 13, 'bold'),
                                  background=WHITE)
        from_entry.place(relx=0.05, rely=0.5, relwidth=0.9, relheight=0.05)
        tk.Label(self.frame,
                 text='Куда:',
                 font=(MAIN_FONT, 15),
                 bg=BACKGROUND,
                 fg=SKY,
                 anchor='w').place(relx=0.05, rely=0.6, relwidth=1, relheight=0.05)
        to_entry = DynamicEntry(self.frame, (MAIN_FONT, 13, 'bold'), *choices)
        to_entry.place(relx=0.05, rely=0.65, relwidth=0.9, relheight=0.09)
        to_entry.config(highlightbackground=SKY, highlightcolor=SKY, highlightthickness=2)
        button = TkinterCustomButton(master=self.frame, text='Посмотреть', fg_color=RED, hover_color=RED_LIGHT,
                                     command=partial(self.find, from_entry, to_entry)
                                     )
        button.place(relx=0.35, rely=0.775)

    def find(self, from_entry, to_entry):
        stat1 = from_entry.get()
        stat2 = to_entry.entry.get()

        cursor.execute(f"EXEC ROUTE_OF_STATION '{stat1}' ,'{stat2}'")
        path = cursor.execute(f"SELECT DBO.PROCEDURE2_RES('{stat1}','{stat2}')").fetchall()[0][0]

        time = cursor.execute(f"SELECT DBO.TOTAL_TIME('{stat1}','{stat2}')").fetchall()[0][0]
        path = '\n'.join(['\U000027A1'.join(i.split()) for i in path.split(' & ')])
        if path == 'Current route does not exist':
            messagebox.showerror('ERROR', 'Sorry, but the current route does not exist \U00002757')
        else:
            self.show(time, path)

    def show(self, time, path):
        cursor.execute(
            "SELECT TOP 3 COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='STATION_TIME'"
        )
        self.new_frame = tk.Toplevel(self.frame, bg=BACKGROUND)
        self.new_frame.geometry('375x350')
        self.new_frame.resizable(False, False)
        self.new_frame.title('Schedule \U0001F4C5')
        font_size = 500 // len(path) + 2
        tk.Label(self.new_frame, text=path, font=('rockwell', font_size, 'bold'), wraplength=175, bg=SKY, bd=5,
                 relief=tk.RIDGE).place(relx=0.01, rely=0.01, relwidth=0.5, relheight=0.27)
        tk.Label(self.new_frame, text=time, font=('Tw Cen MT Condensed', 30), bg=SKY, bd=7, relief=tk.GROOVE).place(
            relx=0.53, rely=0.01, relwidth=0.45, relheight=0.27)

        self.style.theme_use("clam")
        self.style.configure(
            "Treeview", rowheight=20, font=('Calibri', 13))
        self.style.configure("Treeview.Heading", background=SKY, foreground="black")

        self.scroll = tk.Scrollbar(self.new_frame, orient=tk.VERTICAL)
        self.schedule = ttk.Treeview(
            self.new_frame,
            columns=[i[0] + ' ' + j for i, j in zip(cursor, ['\U0001F3E4', '\U0001F556', '\U0001F557'])],
            show='headings', yscrollcommand=self.scroll.set
        )

        self.scroll.place(relx=0.925, rely=0.30, relheight=0.665, relwidth=0.05)
        self.scroll['command'] = self.schedule.yview
        for i in self.schedule['columns']:
            self.schedule.column(i, width=len(i) * 10, anchor=tk.CENTER)
            self.schedule.heading(i, text=i, anchor=tk.CENTER)
        cursor.execute("SELECT STATION_NAME, TIME_ARR, TIME_DEP FROM STATION_TIME")
        self.schedule.tag_configure('1', background='purple')
        iid = 0
        for i in cursor.fetchall():
            self.schedule.insert(parent="", index='end', iid=iid, values=list(i))
            iid += 1

        self.schedule.place(relx=0.01, rely=0.3)


class Registration:

    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(self.parent, bg=BACKGROUND)
        self.frame.pack(side="top", fill="both", expand=True)
        label_font = font.Font(family=MAIN_FONT, size=20, weight='bold')
        entry_font = font.Font(family=MAIN_FONT, size=12)
        self.label = tk.Label(self.frame,
                              text='Регистрация',
                              font=label_font,
                              bg=BACKGROUND,
                              fg=WHITE).place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.1)
        self.login_entry = EntryWithPlaceholder(self.frame, placeholder='Логин')
        self.login_entry.config(highlightbackground=SKY, highlightcolor=SKY, highlightthickness=2, font=entry_font)
        self.login_entry.place(relx=0.05, rely=0.25, relwidth=0.9, relheight=0.075)
        self.password_entry = EntryWithPlaceholder(self.frame, placeholder='Пароль', password=True)
        self.password_entry.config(highlightbackground=SKY, highlightcolor=SKY, highlightthickness=2, font=entry_font)
        self.password_entry.place(relx=0.05, rely=0.35, relwidth=0.9, relheight=0.075)

        self.name_entry = EntryWithPlaceholder(self.frame, placeholder='Имя')
        self.name_entry.config(highlightbackground=SKY, highlightcolor=SKY, highlightthickness=2, font=entry_font)
        self.name_entry.place(relx=0.05, rely=0.45, relwidth=0.9, relheight=0.075)
        self.surname_entry = EntryWithPlaceholder(self.frame, placeholder='Фамилия')
        self.surname_entry.config(highlightbackground=SKY, highlightcolor=SKY, highlightthickness=2, font=entry_font)
        self.surname_entry.place(relx=0.05, rely=0.55, relwidth=0.9, relheight=0.075)

        self.identification_entry = EntryWithPlaceholder(self.frame, placeholder='Идентификационный номер')
        self.identification_entry.config(highlightbackground=SKY, highlightcolor=SKY, highlightthickness=2,
                                         font=entry_font)
        self.identification_entry.place(relx=0.05, rely=0.65, relwidth=0.9, relheight=0.075)

        self.reg_btn = TkinterCustomButton(master=self.frame, text="Регистрация", fg_color=RED, hover_color=RED_LIGHT,
                                           command=self.register)
        self.reg_btn.place(relx=0.35, rely=0.75)

        self.auth_btn = TkinterCustomButton(master=self.frame, text='или Войти', fg_color=BACKGROUND, height=20,
                                            hover=False, command=self.auth)
        self.auth_btn.place(relx=0.35, rely=0.825)

    def register(self):
        login = self.login_entry.get()
        password = self.password_entry.get()
        identification = self.identification_entry.get()
        valid = True
        response = ''
        if not re.fullmatch(
                r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[.,:;?!*+%-<>@\[\]{}\/\\_$#])[A-Za-z\d.,:;?!*+%-<>@\[\]{}\/\\_$#]{8,14}$",
                password):
            response += 'Пароль недостаточно надежный.\n'
            valid = False

        if cursor.execute("SELECT * FROM passenger WHERE user_name='%s'" % login).rowcount != 0:
            response += 'Пользователь с таким именем уже существует.\n'
            valid = False

        if cursor.execute("SELECT * FROM passenger WHERE identification='%s'" % identification).rowcount != 0 or \
                len(identification) != 9:
            response += 'Неверный идентификационный номер.\n'
            valid = False

        if valid:
            first_name = self.name_entry.get()
            last_name = self.surname_entry.get()
            cursor.execute("""
            INSERT INTO passenger(user_name, password, first_name, last_name, identification) VALUES ('%s', '%s', '%s', '%s', '%s')
            """ % (login, password, first_name, last_name, identification))
            conn.commit()
            messagebox.showinfo("Status", f"{login} успешно зарегистрирован!")
            user_id = cursor.execute("SELECT passenger_id FROM passenger WHERE user_name='%s'" % login).fetchone()[0]
            self.frame.forget()
            Main(self.parent, user_id)
        else:
            messagebox.showerror("Status", response)

    def auth(self):
        self.frame.forget()
        Authorization(self.parent)


class Authorization:

    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        self.frame = tk.Frame(self.parent, bg=BACKGROUND)
        self.frame.pack(side="top", fill="both", expand=True)
        label_font = font.Font(family=MAIN_FONT, size=20, weight='bold')
        entry_font = font.Font(family=MAIN_FONT, size=12)
        self.label = tk.Label(self.frame,
                              text='Авторизация',
                              font=label_font,
                              bg=BACKGROUND,
                              fg=WHITE).place(relx=0.25, rely=0.2, relwidth=0.5, relheight=0.1)
        self.login_entry = EntryWithPlaceholder(self.frame, placeholder='Логин')
        self.login_entry.config(highlightbackground=SKY, highlightcolor=SKY, highlightthickness=2, font=entry_font)
        self.login_entry.place(relx=0.05, rely=0.35, relwidth=0.9, relheight=0.075)
        self.password_entry = EntryWithPlaceholder(self.frame, placeholder='Пароль', password=True)
        self.password_entry.config(highlightbackground=SKY, highlightcolor=SKY, highlightthickness=2, font=entry_font)
        self.password_entry.place(relx=0.05, rely=0.45, relwidth=0.9, relheight=0.075)
        self.auth_btn = TkinterCustomButton(master=self.frame, text="Войти", fg_color=RED, hover_color=RED_LIGHT,
                                            command=self.auth)
        self.auth_btn.place(relx=0.35, rely=0.625)
        self.reg_btn = TkinterCustomButton(master=self.frame, text='или Зарегистрироваться', fg_color=BACKGROUND,
                                           height=20, width=200,
                                           hover=False, command=self.register)
        self.reg_btn.place(relx=0.25, rely=0.7)

    def register(self):
        self.frame.forget()
        Registration(self.parent)

    def auth(self):
        login = self.login_entry.get()
        password = self.password_entry.get()
        response = ''
        valid = True
        if cursor.execute("SELECT * FROM passenger WHERE user_name='%s'" % login).rowcount != 0:
            if cursor.execute(
                    """SELECT password FROM passenger WHERE user_name='%s'"""
                    % login).fetchone()[0].strip() != password.strip():
                response += 'Не правильный пароль.\n'
                valid = False
        else:
            response += 'Пользователь с этим логином не существует.\n'
            valid = False

        if valid:
            self.frame.forget()
            user_id, is_admin = cursor.execute(
                "SELECT passenger_id, is_admin FROM passenger WHERE user_name='%s'" % login).fetchone()
            Main(self.parent, user_id)
        else:
            messagebox.showinfo("Status", response)
            return False
