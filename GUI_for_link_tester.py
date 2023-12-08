# from tkinter import *
#
# # todo: maximaze text, buttons and inputs in 2 times
# class MyWindow:
#     def __init__(self, win):
#         self.labelForLink = Label(win, text='Link strony do testowania', font=('Arial', 12))
#         self.labelForTxt = Label(win, text='Nazwa dla pliku txt z uwagami', font=('Arial', 12))
#
#         # створення об'єкта типу StringVar, який буде використовуватися для збереження текстового значення.
#         self.entry_var = StringVar()
#         # bd - розмір рамки текстового поля; за замовчуванням 2 пікселі
#         self.entryForLink = Entry(win, bd=4, textvariable=self.entry_var, font=('Arial', 10))
#         self.entryForTxt = Entry(win, bd=4, textvariable=self.entry_var, font=('Arial', 10))
#
#         # entry.pack - ?
#         self.entryForLink.pack()
#         self.entryForTxt.pack()
#         # self.entry = Entry(bd=4)
#         self.buttonStart = Button(win, text='Start test', command=self.start_test, font=('Arial', 14))
#         self.buttonGetTxtFile = Button(win, text='See txt file', command=self.getTxtFile, font=('Arial', 14))
#
#         self.label.place(x=340, y=50)
#         self.entry.place(x=340, y=75)
#         self.buttonStart.place(x=320, y=125)
#         self.buttonGetTxtFile.place(x=415, y=125)
#
#     def start_test(self):
#         pass
#
#     def getTxtFile(self):
#         pass
#
#
# # ініціалізує Tk і створює вікно
# window=Tk()
# mywin=MyWindow(window)
# window.title('Link tester')
# window.geometry("800x600+10+10")
# window.mainloop()



#####################################LAST VERSION
# from tkinter import *
#
# # todo: maximaze text, buttons and inputs in 2 times
# class MyWindow:
#     def __init__(self, win):
#         self.labelForLink = Label(win, text='Link strony do testowania', font=('Arial', 12))
#         self.labelForTxt = Label(win, text='Nazwa dla pliku txt z uwagami', font=('Arial', 12))
#
#         # створення об'єкта типу StringVar, який буде використовуватися для збереження текстового значення.
#         self.entry_var = StringVar()
#         # bd - розмір рамки текстового поля; за замовчуванням 2 пікселі
#         self.entryForLink = Entry(win, bd=4, textvariable=self.entry_var, font=('Arial', 10))
#         self.entryForTxt = Entry(win, bd=4, textvariable=self.entry_var, font=('Arial', 10))
#
#         # entry.pack - ?
#         self.entryForLink.pack()
#         self.entryForTxt.pack()
#         # self.entry = Entry(bd=4)
#         self.buttonStart = Button(win, text='Start test', command=self.start_test, font=('Arial', 14))
#         self.buttonGetTxtFile = Button(win, text='See txt file', command=self.getTxtFile, font=('Arial', 14))
#
#         self.label.place(x=340, y=50)
#         self.entry.place(x=340, y=75)
#         self.buttonStart.place(x=320, y=125)
#         self.buttonGetTxtFile.place(x=415, y=125)
#
#     def start_test(self):
#         pass
#
#     def getTxtFile(self):
#         pass
#
#
# # ініціалізує Tk і створює вікно
# window=Tk()
# mywin=MyWindow(window)
# window.title('Link tester')
# window.geometry("800x600+10+10")
# window.mainloop()



# from tkinter import *
# from tkinter import ttk
#
# #  ініціалізує клас Tk і створює пов’язаний з ним інтерпретатор
# root = Tk()
# #  створює кореневе вікно програми
# frm = ttk.Frame(root, padding=10)
# # створює віджет який міститиме інші(елементи) віджети в собі (мітку та кнопку)
# # створення таблиці для розміти
# frm.grid()
#
# ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
# # command виконається при натисканні
# ttk.Button(frm, text="Quit",command=root.destroy).grid(column=3, row=3)
# btn = ttk.Button(frm, text="btn")
# fblack = Button(frm, text="red btn", style="red",command=root.destroy).grid(column=1, row=3)
# print(dir(btn))
# root.mainloop()



import tkinter as tk

class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()

        self.entrythingy = tk.Entry()
        self.entrythingy.pack()

        # Create the application variable.
        self.contents = tk.StringVar()
        # Set it to some value.
        self.contents.set("this is a variable")
        # Tell the entry widget to watch this variable.
        self.entrythingy["textvariable"] = self.contents

        # Define a callback for when the user hits return.
        # It prints the current value of the variable.
        self.entrythingy.bind('<Key-Return>',
                             self.print_contents)

    def print_contents(self, event):
        print("Hi. The current entry content is:",
              self.contents.get())

root = tk.Tk()
myapp = App(root)
myapp.mainloop()