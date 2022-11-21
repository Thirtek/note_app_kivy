from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from datetime import datetime
import plyer
import sqlite3


connection = sqlite3.connect("notes.db")
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, title STRING NOT NULL, contents STRING)''')
cursor.execute('''SELECT * from notes''')
notes = cursor.fetchall()


class WindowManager(ScreenManager):
    def _init__(self, **kwargs):
        super().__init__(**kwargs)

        self.current = "main"

class MainWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.note_id = None

        for note in notes:
            note_model = NoteModel(id=note[0], title=note[1], description=note[2])
            self.ids["note_window"].add_widget(note_model)

    def new_note(self):
        self.parent.manager.current = "new_note"

    def show_note(self, id, title, description):
        self.parent.manager.current = "note_window"
        self.parent.manager.screens[2].children[0].note_id = id
        self.parent.manager.screens[2].children[0].ids["note_title"].text = title
        self.parent.manager.screens[2].children[0].ids["description_update"].text = description


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add_widget(MainWindow())


class NoteWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class NewNoteWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_note(self):
        title = self.ids["title_input"].text
        description = self.ids["description_input"].text


        cursor.execute(f'''INSERT INTO notes
        (title, contents)
        VALUES
        (?, ?);''', (title, description))
        connection.commit()

        self.parent.manager.current = "main"

class NewNoteScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add_widget(NewNoteWindow())


class NoteModel(BoxLayout):
    def __init__(self, id=None, title=None, description=None, **kwargs):
        super().__init__(**kwargs)

        self.add_widget(Button(text=title, size_hint_x=0.9, background_color=[1,1,1,1], on_press=lambda x: self.parent.parent.show_note(id, title, description)))
        self.add_widget(Button(background_normal="assets/trash.png", size_hint_x=0.1, on_press=lambda x: self.parent.remove_widget(self)))


class NoteWindowModel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.note_id = None

    def update_note(self):
        updated_description = self.ids["description_update"].text
        cursor.execute('''UPDATE notes SET contents= ? WHERE id= ? ''', (updated_description, self.note_id))
        connection.commit()
        self.parent.manager.current = "main"

class NoteWindowScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add_widget(NoteWindowModel())

class MainApp(App):
    def build(self):
        manager = WindowManager()
        manager.add_widget(MainScreen(name="main"))
        manager.add_widget(NewNoteScreen(name="new_note"))
        manager.add_widget(NoteWindowScreen(name="note_window"))
        return manager


if __name__ == "__main__":
    MainApp().run()
cursor.close()
