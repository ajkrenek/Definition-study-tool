from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter.messagebox as box
import json, random, sqlite3

BACKGROUND_COLOR = "#B1DDC6"
window = Tk()
window.title('Flash Card Memorizer')
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

frame = Frame(window)
flash_card_set_list = Listbox(frame)

correct_words = Listbox(frame)
words_to_study_box = Listbox(frame)
connection = sqlite3.connect("flash_cards.db")
cursor = connection.cursor()
#cursor.execute("""CREATE TABLE IF NOT EXISTS flash_cards(title TEXT PRIMARY KEY NOT NULL, flash_dict VARIANT NOT NULL, flash_compare_list VARIANT NOT NULL, flash_study_list VARIANT NOT NULL);""")

flash_card_titles = cursor.execute('SELECT title FROM flash_cards').fetchall()
for flash_titles in flash_card_titles:
    flash_card_set_list.insert('end', flash_titles[0])

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~  - GLOBAL VARIABLES  -  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
show = False                                                        #hides correct answer
word_study = False
temp_list = []                                                      #temp list to store random word and definition
compare_list = []                                                   #list to compare correct words to remaining words
words_to_study = []
sel_list_name = ""                                                  #current flash card set name
selected_dic = {}                                                   #selected dictionary
selected_dic_val_list = []                                          #values of selected dictionary
selected_dic_key_list = []                                          #keys of selected dictionary

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~  - MAIN FUNCTIONS -  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
def list_select():
    global selected_dic, sel_list_name, compare_list
    if flash_card_set_list.curselection() != ():
        displayed_word.configure(state='normal')
        displayed_word.delete("1.0", "end")
        word_list = flash_card_set_list.get(flash_card_set_list.curselection())           #file select based on user click
        correct_words.delete(0, END)                                                      #clears correctly answered words list
        compare_list.clear()
        #db stuff
        rows = cursor.execute('SELECT title, flash_dict, flash_compare_list, flash_study_list FROM flash_cards WHERE title = ?', (word_list,)).fetchall()
        sel_list_name = ""
        selected_dic.clear()
        sel_list_name = sel_list_name + str(rows[0][0])
        db_dict_as_dict = json.loads(rows[0][1])
        comp_list = rows[0][2]
        study_list = rows[0][3]
        db_dict_vals = list(db_dict_as_dict.values())
        db_dict_keys = list(db_dict_as_dict.keys())
        if comp_list != '[]':
            compare_list = json.loads(comp_list)
            for item in compare_list:
                insert_list = db_dict_as_dict[item]
                correct_words.insert('end', insert_list)        #new_comp_list = db_dict_as_dict[db_dict_as_dict.index(comp_list)]
        if study_list != '[]':
            words_to_study = json.loads(study_list)
            for item in words_to_study:
                study_insert_list = db_dict_as_dict[item]
                words_to_study_box.insert('end', study_insert_list)


        selected_dic.update(db_dict_as_dict)


def create_dict():
    global selected_dic, selected_dic_val_list, selected_dic_key_list
    selected_dic_key_list.clear()
    selected_dic_val_list.clear()
    for values in list(selected_dic.values()):
        selected_dic_val_list.append(values)
    for keys in list(selected_dic.keys()):
        selected_dic_key_list.append(keys)


def generate_random_word():
    global temp_list, compare_list, selected_dic, selected_dic_key_list, selected_dic_val_list, words_to_study
    definiton_list = list(selected_dic)                                                      #turns the dictionary into a list
    word = random.choice(selected_dic_val_list)                                              #picks random word from the dictionary

    real_definition = selected_dic_key_list[selected_dic_val_list.index(word)]               #returns the real definition of the chosen word


    if len(compare_list) == len(definiton_list):                    #prompts the user to restart or quit
        restart_window()

    elif real_definition in compare_list:                           #recursively generates a new word that has not been answered correctly
            generate_random_word()

    else:                                                           #adds items to a global list
        temp_list.clear()
        temp_list.append(word)
        temp_list.append(real_definition)


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~  - END OF MAIN FUNCTIONS -  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~  - SECONDARY FUNCTIONS -  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
def show_word():
    generate_random_word()                                          #generates a new word
    word = temp_list[0]
    displayed_word.configure(state='normal')

    displayed_word.delete("1.0", "end")                             #displays word on screen
    displayed_word.insert(INSERT, word)                             #displays word on screen
    displayed_word.configure(state='disabled')


def show_definition(widget):
    global compare_list, word_study, words_to_study
    input_definition.bind('<Return>', lambda event:[clear(), hide_definition(correct_definition)])
    answer_button.configure(state='disabled')
    widget.pack()                                                   #unhides the correct definition text box widget
    real_definition = temp_list[1]
    answer = input_definition.get("1.0", "end").strip().lower()     #strips user input to get raw input
    the_answer = f"The correct answer is: {real_definition}"
    input_definition.configure(state='disabled')

    if  answer == real_definition.lower():
        correct_words.insert('end', temp_list[0])                   #adds correctly answered words into a list for user to see progress
        compare_list.append(answer)                                 #adds list to internal counter
        correct_definition.insert(INSERT, 'Correct!')               #display 'correct!' to user
        correct_definition.configure(state='disabled')
        if word_study == True:
            words_to_study.remove(real_definition)
            words_to_study_box.delete('end', temp_list[0])
    else:
        if real_definition in words_to_study:
            pass
        else:
            words_to_study_box.insert('end', temp_list[0])
            words_to_study.append(real_definition)
            correct_definition.insert(INSERT, the_answer)               #displays the correct answer to the user
            correct_definition.configure(state='disabled')


def hide_definition(widget):                                        #hides the display when generating the next word
    global show
    answer_button.configure(state='normal')
    input_definition.bind('<Return>', lambda event:[show_definition(correct_definition)])
    show = False
    widget.pack_forget()


def clear():                                                        #resets all text boxes
    input_definition.configure(state='normal')
    correct_definition.configure(state='normal')
    displayed_word.configure(state='normal')

    displayed_word.delete("1.0", "end")
    correct_definition.delete("1.0", "end")
    input_definition.delete("1.0", "end")

    show_word()


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~  - DELETING A SET -  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
def confirm_delete():
    delete = Toplevel(window)
    delete.title("Delete?")
    delete.config(bg=BACKGROUND_COLOR)

    delete_label = Label(delete, text=f"Are you sure you want to delete {sel_list_name}?")
    delete_label.config(bg=BACKGROUND_COLOR)
    delete_label.grid(row=1, column=5)
    yes_button = tk.Button(delete, height = 2,width = 20,text ="Yes", command=lambda: [delete_list(sel_list_name), quit(delete)])
    yes_button.grid(row=4, column=5, pady=5)
    no_button = tk.Button(delete, height = 2,width = 20,text ="No", command=lambda: quit(delete))
    no_button.grid(row=5, column=5, pady=5)


def delete_list(sel_list_name):
    cursor.execute("DELETE FROM flash_cards WHERE title = ?",(sel_list_name,))
    connection.commit()
    flash_card_set_list.delete(tk.ANCHOR)


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~  - RESTARTING -  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
def restart_window():                                               #new top level window asking to restart
    top = Toplevel(window)
    top.config(bg=BACKGROUND_COLOR)
    top.title("Restart?")
    next_word.configure(state='disabled')
    answer_button.configure(state='disabled')
    restart_label = Label(top, text="Congrats! You got everything right! Would you like to restart or study words to learn?")
    restart_label.grid(row=1, column=5)
    restart_label.config(bg=BACKGROUND_COLOR)
    restart_button = tk.Button(top, height = 2, width = 20, text ="Restart", command=lambda: restart(top))
    restart_button.grid(row=5, column=5, pady=5)
    if len(words_to_study) != 0:
        study_words_button = tk.Button(top, height = 2, width = 20, text ="Study Words", command=lambda: words_to_learn_restart(top))
        study_words_button.grid(row=6, column=5, pady=5)

    close_button = Button(top, height = 2,width = 20,text ="Close", command=lambda: quit(window))
    close_button.grid(row=7, column=5, pady=5)

def quit(self):
    self.destroy()

def words_to_learn_restart(self):
    global selected_dic_key_list, selected_dic_val_list, selected_dic, compare_list, words_to_study, word_study
    next_word.configure(state='normal')
    answer_button.configure(state='normal')
    new_compare_list = list(set(compare_list).symmetric_difference(words_to_study))
    compare_list.clear()
    correct_words.delete(0, END)
    for item in new_compare_list:
        new_words_list = selected_dic[item]
        correct_words.insert('end', new_words_list)
        compare_list.append(item)
    self.destroy()
    word_study = True
    show_word()

def restart(self):                                                  #closes window and restarts flash deck
    global word_study
    next_word.configure(state='normal')
    answer_button.configure(state='normal')
    correct_words.delete(0, END)                                    #clears correctly answered words list
    compare_list.clear()                                            #clears internal counter
    words_to_study_box.delete(0,END)
    words_to_study.clear()
    self.destroy()
    word_study = False
    show_word()                                                     #generates new word
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~  - END OF SECONDARY FUNCTIONS -  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~  - TOP LEVEL FUNCTIONS -  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
def create_card():
    flash = {}
#                              *  *  *  *  *  *  *  *  - CREATING CREATE WINDOW -  *  *  *  *  *  *  *  *
    create = Toplevel(window)
    create.title("Flash Card Creator")
    create.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

    create_ui = top_level_ui(create, flash)
    create_ui.create_functions(create)


def edit_list():
#                              *  *  *  *  *  *  *  *  - SELECTING FILE -  *  *  *  *  *  *  *  *
    global sel_list_name, selected_dic_key_list, selected_dic_val_list
#                              *  *  *  *  *  *  *  *  - CREATING EDIT WINDOW -  *  *  *  *  *  *  *  *
    edit = Toplevel(window)
    edit.title("Flash Card Editor")
    edit.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
#                              *  *  *  *  *  *  *  *  - INITIALIZING DICTIONARY -  *  *  *  *  *  *  *  *
    #definitions_as_dicts = create_dict()
    edit_ui = top_level_ui(edit, selected_dic)
    edit_ui.edit_functions(edit, sel_list_name, selected_dic_val_list, selected_dic_key_list)
    print(selected_dic_key_list)
    print(selected_dic_val_list)

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~  - END OF TOP LEVEL FUNCTIONS -  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~  - TOP LEVEL INTERFACE -  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
class top_level_ui():
    def __init__(self, window_name, dictionary):
        self.window_name = window_name                              #top level window name
        self.dictionary = dictionary                                #empty dictionary or exisiting dictionary being edited


#                              *  *  *  *  *  *  *  *  - CURRENT WORDS ADDED -  *  *  *  *  *  *  *  *
        self.current_words = Label(window_name, text="Current Words")
        self.current_words.config(bg=BACKGROUND_COLOR)
        self.current_words.grid(row=6, column=1)

        self.current_words = Listbox(window_name)
        self.current_words.grid(row=7, column=1)


#                              *  *  *  *  *  *  *  *  - CURRENT DEFINITIONS ADDED -  *  *  *  *  *  *  *  *
        self.current_definitions = Label(window_name, text="Current Definitions")
        self.current_definitions.config(bg=BACKGROUND_COLOR)
        self.current_definitions.grid(row=6, column=2)

        self.current_definitions = Listbox(window_name)
        self.current_definitions.grid(row=7, column=2)


#                              *  *  *  *  *  *  *  *  - ADD NEW Title -  *  *  *  *  *  *  *  *
        self.new_title_label = Label(window_name, text="Enter new title")
        self.new_title_label.config(bg=BACKGROUND_COLOR)
        self.new_title_label.grid(row=2, column=4)

        self.new_title = Text(window_name, wrap=WORD, height = 1, width = 20, bg = 'light pink')
        self.new_title.grid(row=3, column=4)


#                              *  *  *  *  *  *  *  *  - ADD NEW WORD -   *  *  *  *  *  *  *  *  *
        self.new_word_label = Label(window_name, text="Enter a new word")
        self.new_word_label.config(bg=BACKGROUND_COLOR)
        self.new_word_label.grid(row=4, column=4)

        self.new_word = Text(window_name, wrap=WORD, height = 1, width = 20, bg = 'light yellow')
        self.new_word.grid(row=5, column=4)


#                               *  *  *  *  *  *  *  *  - ADDING NEW DEFINITION -  *  *  *  *  *  *  *  *
        self.new_definition_label = Label(window_name, text="Enter a new definition")
        self.new_definition_label.config(bg=BACKGROUND_COLOR)
        self.new_definition_label.grid(row=6, column=4)

        self.new_definition = Text(window_name, wrap=WORD, height = 10, width = 50, bg = 'light blue')
        self.new_definition.grid(row=7, column=4)

        self.delete_set = tk.Button(window_name, height = 2,width = 20,text ="Delete selection", command=lambda: self.word_delete())
        self.delete_set.grid(row=8, column=1)

        self.current_words.bind('<<ListboxSelect>>', self.word_edit_on_click)


    def create_functions(self, window_name):
#                              *  *  *  *  *  *  *  *  - CREATE BUTTONS - *  *  *  *  *  *  *  *
        self.add_button = tk.Button(window_name, height = 2,width = 20,text ="Add card", command=lambda: self.add('create'))
        self.add_button.grid(row=8, column=4)

        self.save_button = tk.Button(window_name, height = 2,width = 20,text ="Save set", command=lambda: [save(self.dictionary, self.new_title), quit(window_name), list_select()])
        self.save_button.grid(row=8, column=2)


    def edit_functions(self, window_name, a_current_set, a_val_list, a_key_list):
        self.a_current_set = a_current_set                          #the current set thats been selected
        self.val_list = a_val_list
        self.key_list = a_key_list


#                              *  *  *  *  *  *  *  *  - POPULATIIN TEXT BOXES - *  *  *  *  *  *  *  *
        self.new_title.insert(INSERT, self.a_current_set)             #inserts the current title of the set
        for values in a_val_list:
            self.current_words.insert('end', values)                #adds all current words
        for keys in a_key_list:
            self.current_definitions.insert('end', keys)            #adds all current definitions


#                              *  *  *  *  *  *  *  *  - EDIT BUTTONS - *  *  *  *  *  *  *  *
        self.add_button = tk.Button(window_name, height = 2,width = 20,text ="Add card", command=lambda: self.add('edit'))
        self.add_button.grid(row=8, column=4)
        self.save_button = tk.Button(window_name, height = 2,width = 20,text ="save set", command=lambda: [edit_save(self.dictionary, self.new_title), quit(window_name), list_select()])
        self.save_button.grid(row=8, column=2)


    def word_edit_on_click(self, event):                            #user can select word from list to edit word/definition
        selection = event.widget.curselection()
        index = selection[0]
        data = event.widget.get(index)
        self.new_word.delete("1.0", "end")                          #clears previous selection
        self.new_word.insert(INSERT, data)
        definition = create_dict_list(self.dictionary, data)        #gives definition of selected word
        self.new_definition.delete("1.0", "end")
        self.new_definition.insert(INSERT, definition)


    def word_delete(self):                                          #user can delete selected entry
        cursor_selection = self.current_words.curselection()
        word = str(self.new_word.get("1.0", "end").strip())
        definition = self.new_definition.get("1.0", "end").strip()
        self.current_words.delete(cursor_selection)
        self.current_definitions.delete(cursor_selection)
        del self.dictionary[definition]


    def update(self):                                               #adds words to current word/definition box and working dictionary
        self.added_word = self.new_word.get("1.0", "end").strip()
        self.added_definition = self.new_definition.get("1.0", "end").strip()
        self.dictionary.update({self.added_definition:self.added_word})
        self.current_words.insert('end', self.added_word)
        self.current_definitions.insert('end', self.added_definition)
        self.new_word.delete("1.0", "end")
        self.new_definition.delete("1.0", "end")


    def add(self, method):
        if method == 'create':
            self.update()
        else:
            with open(self.a_current_set, 'a') as fp:
                self.update()


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~  - END OF TOP LEVEL INTERFACE -  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~  - TOP LEVEL UI FUNCTIONS -  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
def create_dict_list(dictionary, word):
    val_list = list(dictionary.values())                            #creates a list of the values (word)
    key_list = list(dictionary.keys())                              #creates a list of the keys (definitions)
    definition = key_list[val_list.index(word)]                     #turns the dictionary into a list
    return definition

def database_insert(a_set_name, a_new_dict, a_comp_list, a_study_list):
    cursor.execute(f"""INSERT INTO flash_cards(title, flash_dict, flash_compare_list, flash_study_list)VALUES(?,?,?,?)""", (a_set_name, a_new_dict, a_comp_list, a_study_list,)) # passing a dictionary and not a string
    connection.commit()

def database_delete(a_set_name, a_new_dict, a_comp_list, a_study_list):
    cursor.execute("DELETE FROM flash_cards WHERE title = ?",(a_set_name,))
    database_insert(a_set_name, a_new_dict, a_comp_list, a_study_list)

def database_update():
    global sel_list_name, compare_list, words_to_study
    json_comp_list = json.dumps(compare_list)
    json_study_list = json.dumps(words_to_study)
    cursor.execute("UPDATE flash_cards SET flash_compare_list = ?, flash_study_list = ? WHERE title = ?",(json_comp_list, json_study_list, sel_list_name))
    connection.commit()

def on_closing():
    global compare_list
    if box.askokcancel("Quit", "Do you want to quit?"):
        database_update()
        window.destroy()


def save(dict_name, title):                                         #saves and updates file with user inputted file name and closes window
    set_name = str(title.get("1.0", "end").strip())
    new_dict = json.dumps(dict_name)
    comp_list = json.dumps([])
    stdy_list = json.dumps([])
    database_insert(set_name, new_dict, comp_list, stdy_list)


    flash_card_set_list.insert('end', set_name)

def edit_save(dict_name, title):
    set_name = str(title.get("1.0", "end").strip())
    new_dict = json.dumps(dict_name)
    comp_list = json.dumps([])
    stdy_list = json.dumps([])
    database_delete(set_name, new_dict, comp_list, stdy_list)
    flash_card_set_list.delete(tk.ANCHOR)
    flash_card_set_list.insert('end', set_name)

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~  - END OF TOP LEVEL UI FUNCTIONS -  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~  - DISPLAY -  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#  *  *  *  *  *  *  *  *  - FLASH CARD SETS -  *  *  *  *  *  *  *  *

flash_card_set_list.pack(side = LEFT)
frame.pack(padx = 30, pady = 30)

#  *  *  *  *  *  *  *  *  - WORDS TO LEARN -  *  *  *  *  *  *  *  *
words_to_study_box.pack(side=RIGHT)
frame.pack(padx=30, pady=30)
words_to_study_label = Label(window, text='Words to learn', bg=BACKGROUND_COLOR)
words_to_study_label.place(x=525, y=5)
#  *  *  *  *  *  *  *  *  - CORRECT WORDS -  *  *  *  *  *  *  *  *
correct_words.pack(side=RIGHT)
frame.pack(padx=30, pady=30)
correct_words_label = Label(window, text='Correct Words', bg=BACKGROUND_COLOR)
correct_words_label.place(x=400, y=5)



#  *  *  *  *  *  *  *  *  - CURRENT WORDS -  *  *  *  *  *  *  *  *
displayed_word = Text(window, wrap=WORD, state='normal', height = 5, width = 20, bg = 'light yellow')
displayed_word.pack(fill="none", expand=TRUE)


#  *  *  *  *  *  *  *  *  - HIDDEN ANSWER -  *  *  *  *  *  *  *  *
correct_definition = Text(window, wrap=WORD, state='normal', height = 5, width = 100, bg = 'light green')
if show == True:
    correct_definition.pack(fill="none", expand=TRUE)


#  *  *  *  *  *  *  *  *  - USER INPUT -  *  *  *  *  *  *  *  *
input_definition = Text(window, wrap=WORD, state='normal', height = 5, width = 100, bg = 'light cyan')
input_definition.pack(fill="none", expand=TRUE)
input_definition.bind('<Return>', lambda event:show_definition(correct_definition))


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~  - END OF DISPLAY -  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~  - BUTTONS -  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#  *  *  *  *  *  *  *  *  - DELETE SELECTED SET -  *  *  *  *  *  *  *  *
delete_button = Button(frame, text = 'Delete set', command=lambda: [list_select(), confirm_delete()])
delete_button.pack(side = BOTTOM , padx = 5, pady = 5)

#  *  *  *  *  *  *  *  *  - CREATE NEW SET -  *  *  *  *  *  *  *  *
create_button = Button(frame, text = 'Create set', command=create_card)
create_button.pack(side = BOTTOM , padx = 5, pady = 10)

#  *  *  *  *  *  *  *  *  - SELECT A FLASH SET -  *  *  *  *  *  *  *  *
select_button = Button(frame, text = 'Select set', command=lambda: [database_update(), list_select(), create_dict(), show_word()])
select_button.pack(side = TOP , padx = 5, pady = 5)

#  *  *  *  *  *  *  *  *  - EDIT SELECTED SET -  *  *  *  *  *  *  *  *
edit_button = Button(frame, text = 'Edit set', command=lambda: [list_select(), create_dict(), edit_list()])
edit_button.pack(side = TOP , padx = 5, pady = 10)


#  *  *  *  *  *  *  *  *  - CHECK ANSWER -  *  *  *  *  *  *  *  *
answer_button = Button(window, height = 2, width = 20, state='normal', text ="Check answer", command=lambda: show_definition(correct_definition))
answer_button.pack(side = LEFT)


#  *  *  *  *  *  *  *  *  - NEXT WORD -  *  *  *  *  *  *  *  *
next_word = Button(window, height = 2,width = 20,text ="Next word", command=lambda: [clear(), hide_definition(correct_definition)])
next_word.pack(side = RIGHT)


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~  - END OF BUTTONS -  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #

window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
