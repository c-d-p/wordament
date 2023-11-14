import tkinter as tk
import pyautogui
from pynput import mouse
import random
from english_words import english_words_lower_set
from threading import Timer


### https://wordament.wordpress.com/how-to-play-wordament/ SCORES AND SHIT

class MainWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.prev_widget = None

        for i in range(1, 17):
            cmd = "self.b"+str(i) + " = tk.Button(text='"+str(i)+"', width=10, height=5, bg='orange', font=('Courier', 22))"
            exec(cmd)

        #self.window.bind("<B1-Motion>", lambda event: self.on_drag(event))

        self.score_label = tk.Label(text='Score: 0', width=10, height=2, font=('Courier', 22))
        self.score_label.grid(row=0, column=0)

        self.b1.grid(row=1, column=0)
        self.b2.grid(row=1, column=1)
        self.b3.grid(row=1, column=2)
        self.b4.grid(row=1, column=3)
        self.b5.grid(row=2, column=0)
        self.b6.grid(row=2, column=1)
        self.b7.grid(row=2, column=2)
        self.b8.grid(row=2, column=3)
        self.b9.grid(row=3, column=0)
        self.b10.grid(row=3, column=1)
        self.b11.grid(row=3, column=2)
        self.b12.grid(row=3, column=3)
        self.b13.grid(row=4, column=0)
        self.b14.grid(row=4, column=1)
        self.b15.grid(row=4, column=2)
        self.b16.grid(row=4, column=3)

    def get_widget(self, x,y):
        self.widget = self.window.winfo_containing(x, y)
        return self.widget
        """
        if not self.prev_widget:
            self.prev_widget = self.widget
            return
        if self.prev_widget == self.widget:
            self.prev_widget = self.widget
            return

        if self.widget != self.prev_widget:
            print('widget trigger')
            self.widget.configure(bg = 'white')

        self.prev_widget = self.widget
        """

    def setWidgetsColour(self, colour):
        for i in range(1, 17):
            eval("self.b"+str(i)+".configure(bg='"+colour+"')")

class main():
    def __init__(self, MainWindow):
        self.MainWindow = MainWindow
        self.score = 0
        self.letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z', 'A','B','C','D','E','F','G','H','I','K','L','M','N','O','P','R','S','T','U','W','Y']
        self.current_letters = {}
        self.current_letters_inv = {}
        self.vowels = ['A','E','I','O','U']
        self.conditions = False
        self.letter_scores = {'A': 2,'B': 5,'C': 3,'D': 3,'E': 1,'F': 5,'G': 4,'H': 4,'I': 2,'J': 0,'K': 6,'L': 3,'M': 4,'N': 2,'O': 2,'P': 4,'Q': 0,'R': 2,'S': 2,'T': 2,'U': 4,'V': 0,'W': 6,'X': 0,'Y': 5,'Z':0}
        vowel_count = 0
        for i in range(1, 17):
            rand_letter = random.choice(self.letters)
            self.current_letters["self.MainWindow.b"+str(i)] = rand_letter
            self.current_letters_inv[rand_letter] = "self.MainWindow.b"+str(i)

            if rand_letter in self.vowels:
                vowel_count += 1
            eval("self.MainWindow.b"+str(i)+".configure(text='"+rand_letter+"')")

        while self.conditions <= 2:
            if vowel_count <= 3:
                num = random.randint(1, 16)
                rand_vowel = random.choice(self.vowels)
                eval("self.MainWindow.b"+str(num)+".configure(text='"+rand_vowel+"')")
                vowel_count += 1
                self.conditions += 1

            for letter in self.letters:
                if list(self.current_letters.values()).count(letter) > 2:
                    tmp = self.letters
                    tmp.remove(letter)
                    new_letter = random.choice(tmp)
                    eval(self.current_letters_inv[letter]).configure(text=new_letter)
            self.conditions += 1

    def check_word(self, letters, widgets):
        word = ''.join(letters).lower()
        if word in english_words_lower_set and len(word) > 2:
            print('WORD!',word)
            for widget in widgets:
                self.set_button_colour(widget, 'green')
                t = Timer(1.0, self.set_button_colour, [widget, "orange"])
                t.start()
            self.score_word(letters)
        else:
            print('no',word)
            for widget in widgets:
                self.set_button_colour(widget, 'red')
                t = Timer(1.0, self.set_button_colour, [widget, "orange"])
                t.start()
        self.listener.current_letters = []

    def set_button_colour(self, btn, colour):
        btn.configure(bg=colour)

    def score_word(self, letters):
        for letter in letters:
            self.score += self.letter_scores[letter]
        self.MainWindow.score_label["text"] = "Score: " + str(self.score)

    def set_listener(self, listener):
        self.listener = listener

class Listener():
    def __init__(self, main, window):
        self.main = main
        self.window = window
        self.pressed = False
        self.current_letters = []
        self.last_widget = None
        self.current_widgets = []
        self.last_widget_amnt = 0

        listener = mouse.Listener(on_move=self.on_move, on_click=self.on_click)
        listener.start()

    def on_click(self, x, y, button, pressed):
        if button == mouse.Button.left and pressed == True:
            self.pressed = pressed
            #print('x:',x,'y:',y,'button:',button,'pressed:',pressed)
        elif button == mouse.Button.left and pressed == False:
            self.pressed = pressed
            self.widget = self.window.get_widget(x,y)
            self.main.check_word(self.current_letters, self.current_widgets)
            self.current_widgets = []

    def on_move(self, x, y):
        if self.pressed:
            self.widget = self.window.get_widget(x,y)
            if self.widget == None:
                return
            elif self.widget["background"] == 'white':
                return
            else:
                if self.last_widget == self.widget and self.pressed:
                    self.last_widget_amnt += 1
                else:
                    self.last_widget = self.widget
                if self.last_widget_amnt > 30:
                    self.current_letters.append(self.widget["text"])
                    self.current_widgets.append(self.widget)
                    self.widget.configure(bg='white')
                    self.last_widget_amnt = 0
                    self.last_widget = self.widget

if __name__ == '__main__':
    MainWindow = MainWindow()
    main = main(MainWindow)
    listener = Listener(main, MainWindow)
    main.set_listener(listener)
    MainWindow.window.mainloop()
