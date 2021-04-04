import tkinter as tk
import test_text


class Application(tk.Tk):

    def __init__(self, testing_text, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Typing speed test")

        self.tag_highlight = 'highlight'
        self.tag_writing_correct = 'writing_correct'
        self.tag_writing_wrong = 'writing_wrong'
        self.tag_word_correct = 'word_correct'
        self.tag_word_wrong = 'word_wrong'
        self.start_index = '1.0'
        self.start_index_before = '1.0'
        self.end_index = '1.0'
        self.current_word = ''
        self.first_search = True
        self.working = False

        self.right_words = tk.IntVar()
        self.wrong_words = tk.IntVar()
        self.right_characters = tk.IntVar()
        self.right_CPM = tk.IntVar()
        self.time_left = tk.IntVar()
        self.time_left.set(60)

        self.working_panel = tk.Frame(self)
        self.working_panel.grid(row=0, column=0, sticky=(tk.E + tk.W), padx=2, pady=2)

        self.label_right_words = LabelVar(self.working_panel, "Right words: ", self.right_words)
        self.label_right_words.grid(row=0, column=0, sticky=(tk.E + tk.W), padx=2, pady=2)

        self.label_right_characters = LabelVar(self.working_panel, "Right chars: ", self.right_characters)
        self.label_right_characters.grid(row=0, column=1, sticky=(tk.E + tk.W), padx=2, pady=2)

        self.label_right_CPM = LabelVar(self.working_panel, "Right CPM: ", self.right_CPM)
        self.label_right_CPM.grid(row=0, column=2, sticky=(tk.E + tk.W), padx=2, pady=2)

        self.label_right_characters = LabelVar(self.working_panel, "Time left: ", self.time_left)
        self.label_right_characters.grid(row=0, column=3, sticky=(tk.E + tk.W), padx=2, pady=2)

        self.reset_button = tk.Button(self.working_panel, text='Reset', command=self.reset)
        self.reset_button.grid(row=0, column=4, sticky=(tk.E + tk.W), padx=2, pady=2)

        self.text = tk.Text(self)
        # width and height in characters!!!
        self.text.config(width=36, height=3, wrap='word', font=('Lucida Sans', 23))
        self.text.grid(row=1, column=0, sticky=(tk.E + tk.W), padx=5, pady=5)

        self.text.insert('1.0', testing_text)
        self.text.tag_config(self.tag_highlight, background='#B8E069')
        self.text.tag_config(self.tag_writing_correct, foreground='white')
        self.text.tag_config(self.tag_writing_wrong, foreground='#C10000')
        self.text.tag_config(self.tag_word_wrong, foreground='#C10000')
        self.text.tag_config(self.tag_word_correct, foreground='#0000FF')

        self.input_var = tk.StringVar()
        self.input_var.trace_add("write", self.trace_input)

        self.user_input = tk.Entry(textvariable=self.input_var)
        self.user_input.grid(row=2, column=0, sticky=(tk.E + tk.W), padx=5, pady=5)
        self.user_input.focus_set()

    def trace_input(self, variable, index, mode):

        if self.first_search:
            self.start()

        if not self.working:
            return

        self.text.tag_remove(self.tag_writing_correct, '1.0', tk.END)
        self.text.tag_remove(self.tag_writing_wrong, '1.0', tk.END)

        current_word_as_list = [x for x in self.current_word]
        current_input = self.input_var.get()
        current_input_length = len(current_input)

        if current_input_length == 0:
            return

        # IF 'SPACE' THEN CLEAR INPUT AND HIGHLIGHT NEXT WORD AND PROCESS TAGS
        if current_input[-1] == ' ':
            if self.current_word.strip() == current_input.strip():
                self.right_words.set(self.right_words.get() + 1)
                self.right_characters.set(self.right_characters.get() + len(self.current_word.strip()))

                time_left = self.time_left.get()
                if time_left == 60:
                    time_left = 59
                self.right_CPM.set(int(self.right_characters.get() * 60 / (60-time_left)))
                self.text.tag_add(self.tag_word_correct, self.start_index_before, self.start_index)
            else:
                self.wrong_words.set(self.wrong_words.get() + 1)
                self.text.tag_add(self.tag_word_wrong, self.start_index_before, self.start_index)
            self.input_var.set('')
            self.highlight_next_word()
            return

        current_input_index = -1

        # CHECKING EACH LETTER IN CURRENT INPUT AND COMPARING IT WITH CURRENT WORD
        # WHILE CALCULATING INDEX OF EACH LETTER
        # INDEX = START OF THE CURRENT LETTER + INDEX INSIDE THE WORD
        for current_input_char in current_input:
            current_input_index += 1

            start = self.start_index_before + " + " + str(current_input_index) + " chars "
            stop = self.start_index_before + " + " + str(current_input_index + 1) + " chars "

            if current_input_char == current_word_as_list[current_input_index]:
                self.text.tag_add(self.tag_writing_correct, start, stop)
            else:
                self.text.tag_add(self.tag_writing_wrong, start, stop)

    def highlight_next_word(self):

        if self.end_index == tk.END:
            return

        self.text.tag_remove(self.tag_highlight, '1.0', tk.END)
        # CURRENT SPACE INDEX PLUS ONE CHARACTER
        start_index = self.start_index + (' + 1 chars' if not self.first_search else '')

        # NEXT SPACE INDEX BEGINING FROM THE CURRENT SPACE INDEX PLUS ONE CHARACTER
        end_index = self.text.search(' ', start_index + ' + 1 chars')
        if not end_index:
            end_index = tk.END
        else:
            self.text.see(end_index + ' + 36 chars')

        # HIGHLIGHTING TEXT
        self.text.tag_add(self.tag_highlight, start_index, end_index)

        # SETTING GLOBAL VARIABLES
        self.current_word = self.text.get(start_index, end_index)
        self.start_index_before = start_index
        self.start_index = end_index

        if self.first_search:
            self.first_search = False

    def start(self):
        self.working = True
        self.timer()
        self.highlight_next_word()

    def timer(self):
        # DECREMENTING TIME LEFT
        if self.working and self.time_left.get() > 0:
            self.time_left.set(self.time_left.get() - 1)
            self.after(1000, self.timer)
        else:
            self.working = False

    def reset(self):
        self.working = False
        self.time_left.set(60)
        self.right_words.set(0)
        self.wrong_words.set(0)
        self.right_characters.set(0)
        self.time_left.set(60)
        self.start_index = '1.0'
        self.start_index_before = '1.0'
        self.end_index = '1.0'
        self.current_word = ''
        self.first_search = True
        self.working = False
        self.text.see('1.0')
        self.text.tag_remove(self.tag_writing_correct, '1.0', tk.END)
        self.text.tag_remove(self.tag_writing_wrong, '1.0', tk.END)
        self.text.tag_remove(self.tag_word_correct, '1.0', tk.END)
        self.text.tag_remove(self.tag_highlight, '1.0', tk.END)
        self.input_var.set('')


class LabelVar(tk.Frame):
    def __init__(self, parent, label_name, label_var, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.label_text = tk.Label(self, text=label_name)
        self.label_text.grid(row=0, column=0, sticky=(tk.E + tk.W), padx=2, pady=2)
        self.label_var = tk.Label(self, textvariable=label_var)
        self.label_var.grid(row=0, column=1, sticky=(tk.E + tk.W), padx=2, pady=2)


if __name__ == "__main__":
    root = Application(test_text.text)
    root.mainloop()
