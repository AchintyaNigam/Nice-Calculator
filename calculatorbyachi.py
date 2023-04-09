from tkinter import Entry
from tkinter import Canvas
from tkinter import Tk
from tkinter import Button
from tkinter import END

from tkinter import messagebox
import re

class backend:
    def __init__(self, data):
        self.data = data

    def data_gather(self):

        global nums_vals, operators_keys, infix;
        self.data = self.data.replace(' ', '')

        operators_keys = []
        nums_vals = []
        infix = []


        """
            GETTING DATA:
            My idea is to arrange the entered data into operators and numbers separately, 
            I initially wanted to use dictionaries but they don't support duplicates.
            So I have made separate lists for keys and values as If I was using dictionaries.
            For operators, the keys are the operators and the values are the index positions in the string input.
            For numbers it is opposite: the keys are index positions of the end of the numbers and the values are the numbers.
            I have used regular expressions for searching the operators. I have also used a 'counter' for finding the index
            within the for loop.
            
            7th april 2023
            11:11AM:
            I have integrated the backend into the main program and removed unnecessary variables.
            12:30pm:
            UI has been updated. bodmas mode is yet to be made but calculator displays 'coming soon'.
            8th april 2023
            12:53pm:
            added power and brackets and delt with errors for data gathering system involving brackets.
            started building boadmas mode. for now we have made an infix expression list. plan to convert this into postfix,
            and then we can evaluate the postix expression. stack will used which simply list in python.
            5:30pm
            bodmas mode has beem created.
        """

        if len(self.data) > 1:
            counter = 0
            temp_num = ''

            ops1 = r"^[\+\-\*\/\^]"
            ops2 = r"[\+\-\*\/\^]$"
            ops3 = r"[\+\-\*\/\^/(/)]"
            ops4 = r"^[/(][\+\-\*\/\^]"

            if re.search(ops1, self.data) or re.search(ops2, self.data) or re.search(ops4, self.data) or not (re.search(ops3, self.data) or (re.search('[/)]', self.data) and not re.search('[/)]'))):
                return 1 #invalid input
            elif mode == 1 and (re.search('[/(]', self.data)):
                return 3 #brackets are not allowed in sequential mode
            else:
                for i in self.data:
                    if re.search(ops3, i):
                        if i == ')' or i == '(':
                            infix.append(temp_num)
                            operators_keys.append(i)
                            infix.append(i)
                            if temp_num != '':
                                nums_vals.append(temp_num)

                                temp_num = ''
                        else:
                            nums_vals.append(temp_num)
                            infix.append(temp_num)
                            operators_keys.append(i)
                            infix.append(i)
                            temp_num = ''
                    else:
                        if counter == (len(self.data) - 1):
                            temp_num += i
                            nums_vals.append(temp_num)
                            infix.append(temp_num)
                            temp_num = ''
                        else:
                            temp_num += i
                    counter += 1
                return 0
        elif len(e.get()) == 0:
            return 2 #nothing has been entered.

    # sequential calculation without BODMAS
    def sequential_mode(self):
        res = 0
        for i in range(len(nums_vals)):
            if i == 0:
                res += float(nums_vals[i])
            elif (i - 1) != len(operators_keys):
                if operators_keys[i - 1] == '+':
                    res += float(nums_vals[i])
                elif operators_keys[i - 1] == '-':
                    res -= float(nums_vals[i])
                elif operators_keys[i - 1] == '*':
                    res *= float(nums_vals[i])
                elif operators_keys[i - 1] == '/':
                    res /= float(nums_vals[i])
                elif operators_keys[i - 1] == '^':
                    res **= float(nums_vals[i])

        return res

    def bodmas_mode(self):
        global infix
        while '' in nums_vals:
            nums_vals.remove('')
        stack = []
        operators = ['+', '-', '*', '/', '(', ')', '^']
        priority = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
        postfix = []

        for i in infix:
            if i != '':
                if i not in operators:
                    postfix.append(i)
                elif i == '(':
                    stack.append(i)
                elif i == ')':
                    while stack and stack[-1] != '(':
                        postfix.append(stack.pop())
                elif i != '(' and i!= ')':
                    while stack and stack[-1] != '(' and priority[i] <= priority[stack[-1]]:
                        postfix.append(stack.pop())
                    stack.append(i)
        while stack:
            postfix.append(stack.pop())
        while '(' in postfix:
            postfix.remove('(')
        while ')' in postfix:
            postfix.remove(')')
        stack.clear()
        for i in postfix:
            if i not in operators:
                stack.append(i)
            else:
                op1 = stack.pop()
                op2 = stack.pop()
                if i == '+':
                    stack.append(str(float(op2)+float(op1)))
                elif i == '-':
                    stack.append(str(float(op2)-float(op1)))
                elif i == '/':
                    stack.append(str(float(op2)/float(op1)))
                elif i == '*':
                    stack.append(str(float(op2)*float(op1)))
                elif i == '^':
                    stack.append(str(float(op2)**float(op1)))
        res = stack[-1]
        return res

#-----------------------------------------------F R O N T E N D--------------------------------------------------------#

root = Tk()
root.title("Nice Calculator | By Achintya Nigam")
root.config(bg='black')
mode = 2 #mode1 is for sequential and mode2 is for bodmas
#main entry
canvas= Canvas(root, bd=0, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=6, padx=0, pady=0)
e = Entry(canvas, width=70, bg = 'silver', fg='black')
e.config(highlightbackground = "silver", highlightcolor= "silver")
e.grid(row=0, column=0, columnspan=6, padx=15, pady=15)

#function defintions

def button_click(operator):
    global mode
    if mode == 1 and (operator == ' ( ' or operator == ' ) ' ):
        error(3)
    else:
        current = e.get()
        e.delete(0, END)
        e.insert(0, str(current) + str(operator))

def clear():
    e.delete(0, END)

def setmode():
    global mode, button_mode
    if button_mode["text"]=="SQE":
        mode = 2
        button_mode.configure(text="NSQ")
        clear()
    else:
        mode = 1
        button_mode.configure(text="SQE")
        clear()
def backspace():
    current = e.get()
    len_current = len(current)
    if current:
        if current[len_current-1] == ' ':
            current = current[:(len_current-2)]

        else:
            current = current[:(len_current-1)]
    
    len_current = len(current)

    if current:
        if current[len_current-1] == ' ':
            current = current[:(len_current-1)]

    e.delete(0, END)
    e.insert(0, current)
def error(code):
    global b
    if code == 1:
        e.delete(0, END)
        e.insert(0, "Invalid Input!")
    elif code == 2:
        e.delete(0, END)
        e.insert(0, "Not enough information!")
        b.data_gather()
    elif code == 3:
        current = e.get()
        e.delete(0, END)
        messagebox.showwarning("warning", "Brackets are not allowed in sequential mode as they defeat the purpose of this mode.")
        e.delete(0, END)
        e.insert(0, str(current))

def equal():
    global b, mode
    temp = e.get()
    b = backend(temp)
    error_code = b.data_gather()
    if error_code != 0:
        error(error_code)
    else:
        if mode == 1:
            result = b.sequential_mode()

        else:
            result = b.bodmas_mode()

        e.delete(0, END)
        e.insert(0, str(result))

#define butons
button_1 = Button(root, text="1", padx=40, pady=20, fg = 'white', bg='black', activebackground='silver', activeforeground='cyan', command=lambda: button_click(1))
button_2 = Button(root, text="2", padx=40, pady=20, fg = 'white', bg='black', activebackground='silver', activeforeground='cyan', command=lambda: button_click(2))
button_3 = Button(root, text="3", padx=40, pady=20, fg = 'white', bg='black', activebackground='silver', activeforeground='cyan', command=lambda: button_click(3))
button_4 = Button(root, text="4", padx=40, pady=20, fg = 'white', bg='black', activebackground='silver', activeforeground='cyan', command=lambda: button_click(4))
button_5 = Button(root, text="5", padx=40, pady=20, fg = 'white', bg='black', activebackground='silver', activeforeground='cyan', command=lambda: button_click(5))
button_6 = Button(root, text="6", padx=40, pady=20, fg = 'white', bg='black', activebackground='silver', activeforeground='cyan', command=lambda: button_click(6))
button_7 = Button(root, text="7", padx=40, pady=20, fg = 'white', bg='black', activebackground='silver', activeforeground='cyan', command=lambda: button_click(7))
button_8 = Button(root, text="8", padx=40, pady=20, fg = 'white', bg='black', activebackground='silver', activeforeground='cyan', command=lambda: button_click(8))
button_9 = Button(root, text="9", padx=40, pady=20, fg = 'white', bg='black', activebackground='silver', activeforeground='cyan', command=lambda: button_click(9))
button_0 = Button(root, text="0", padx=40, pady=20, fg = 'white', bg='black', activebackground='silver', activeforeground='cyan', command=lambda: button_click(0))
button_point = Button(root, text=" . ", padx=40, pady=20, fg = 'white', bg='black', activebackground='silver', activeforeground='cyan', command=lambda: button_click('.'))
button_mode = Button(root, text="NSQ", padx=30, pady=20, fg = 'red', bg='black', activebackground='silver', activeforeground='cyan', command=setmode)
button_add = Button(root, text=" + ", padx=40, pady=20, fg = 'white', bg='black', activebackground='silver', activeforeground='cyan', command=lambda: button_click(' + '))
button_sub = Button(root, text=" - ", padx=40, pady=20, fg = 'white', bg='black', activebackground='silver', activeforeground='cyan', command=lambda: button_click(' - '))
button_mul = Button(root, text=" * ", padx=40, pady=20, fg = 'white', bg='black', activebackground='silver', activeforeground='cyan', command=lambda: button_click(' * '))
button_div = Button(root, text=" / ", padx=40, pady=20, fg = 'white', bg='black', activebackground='silver', activeforeground='cyan', command=lambda: button_click(' / '))
button_power = Button(root, text=" ^ ", padx=40, pady=20, fg = 'white', bg='black', activebackground='silver', activeforeground='cyan', command=lambda: button_click(' ^ '))
button_backspace = Button(root, text=" <- ", padx=37, pady=20, fg = 'white', bg='black', activebackground='silver', activeforeground='cyan', command=backspace)
button_open_bracket = Button(root, text=" ( ", padx=41, pady=20, fg = 'white', bg='black', activebackground='silver', activeforeground='cyan', command=lambda: button_click(' ( '))
button_close_bracket = Button(root, text=" ) ", padx=41, pady=20, fg = 'white', bg='black', activebackground='silver', activeforeground='cyan', command=lambda: button_click(' ) '))
button_equal = Button(root, text=" = ", padx=90, pady=20, fg = 'white', bg='black', activebackground='silver', activeforeground='cyan', command=equal)
button_clear = Button(root, text="Clear", padx=83, pady=20, fg = 'white', bg='black', activebackground='silver', activeforeground='cyan', command=clear)


# buttons on screen
button_1.grid(row=3, column=0)
button_2.grid(row=3, column=1)
button_3.grid(row=3, column=2)

button_4.grid(row=2, column=0)
button_5.grid(row=2, column=1)
button_6.grid(row=2, column=2)

button_7.grid(row=1, column=0)
button_8.grid(row=1, column=1)
button_9.grid(row=1, column=2)

button_0.grid(row=4, column=1)
button_point.grid(row=4, column=2)
button_mode.grid(row=4, column=0)

button_clear.grid(row=1, column=3, columnspan=2)
button_backspace.grid(row=1, column=5)
button_add.grid(row=2, column=3)
button_sub.grid(row=2, column=4)
button_mul.grid(row=3, column=3)
button_div.grid(row=3, column=4)
button_open_bracket.grid(row=2, column=5)
button_close_bracket.grid(row=3, column=5)
button_power.grid(row=4, column=5)
button_equal.grid(row=4, column=3, columnspan=2)

root.mainloop()