import tkinter as tk
from PIL import ImageTk, Image
from tkinter import font
from constants import BACKGROUND, BLACK, MAIN_FONT, WHITE, RED, RED_LIGHT
from functools import partial


def get_selected_seat(d):
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

    SELECTED_seat = []

    def on_click(i):
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
            SELECTED_seat = []
            for l in range(len(Free_seats2)):
                lll = (Free_seats2[l] % (int(str(Free_seats2[l])[:4]) * 100))
                if roundedbutton[lll]['fg'] == BLACK:
                    SELECTED_seat = [Free_seats2[l]]
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

    def action():
        window.destroy()

    seat = ''
    if SELECTED_seat:
        seat = '№' + str(SELECTED_seat[0])
    search_btn = tk.Button(master=window, text="Выбрать место " + seat, command=action)
    search_btn.place(relx=0.4, rely=0.8)

    window.mainloop()

    if tk.Toplevel.winfo_exists(window) == 0:
        return SELECTED_seat[0]
