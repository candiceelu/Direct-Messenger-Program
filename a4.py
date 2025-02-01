import tkinter as tk
from tkinter import ttk, filedialog
from pathlib import Path
from Profile4 import Profile, SentMessages, ReceivedMessage
from ds_messenger import DirectMessenger

class Body(tk.Frame):
    def __init__(self, root, recipient_selected_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = []
        self._messages = {}
        self._sent = {}
        self.typed_msg = ''
        self.new_insert = []
        self.new_contact = []
        self._select_callback = recipient_selected_callback
        self._draw()


    def node_select(self, entry):
        index = int(self.posts_tree.selection()[0])
        user = self._contacts[index]
        if self._select_callback is not None:
            self._select_callback(user)
        self.entry_editor.delete(1.0, tk.END)
        all_messages = []
        if user in self._messages.keys():
            all_messages.extend(self._messages[user])
        if user in self._sent.keys():
            all_messages.extend(self._sent[user])
        chat = sorted(all_messages, key=lambda x: x['timestamp'])
        for entry in chat:
            if entry not in self.new_insert:
                if 'sent_msg' in entry.keys():
                    self.insert_user_message(entry['sent_msg'])
                elif 'msg' in entry.keys():
                    self.insert_contact_message(entry['msg'])
        self.new_insert.clear()


    def insert_contact(self, contact: str):
        self._contacts.append(contact)
        id = len(self._contacts) - 1
        self._insert_contact_tree(id, contact)


    def _insert_contact_tree(self, id, contact: str):
        if len(contact) > 25:
            entry = contact[:24] + "..."
        id = self.posts_tree.insert('', id, id, text=contact)


    def insert_user_message(self, message:str):
        self.entry_editor.insert(tk.END, message + '\n', 'entry-right')


    def insert_contact_message(self, message:str):
        self.entry_editor.insert(tk.END, message + '\n', 'entry-left')


    def get_text_entry(self) -> str:
        return self.message_editor.get('1.0', 'end').rstrip()


    def set_text_entry(self, text:str):
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)


    def _draw(self):
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP,
                             expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        message_frame = tk.Frame(master=self, bg="yellow")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)

        self.message_editor = tk.Text(message_frame, width=0, height=5)
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                                 expand=True, padx=0, pady=0)

        self.entry_editor = tk.Text(editor_frame, width=0, height=5)
        self.entry_editor.tag_configure('entry-right', justify='right')
        self.entry_editor.tag_configure('entry-left', justify='left')
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                               expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame,
                                              command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT,
                                    expand=False, padx=0, pady=0)

class Footer(tk.Frame):
    def __init__(self, root, send_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._draw()


    def send_click(self):
        if self._send_callback is not None:
            self._send_callback()


    def _draw(self):
        save_button = tk.Button(master=self, text="Send", width=20,
                                command=self.send_click)
        # You must implement this.
        # Here you must configure the button to bind its click to
        # the send_click() function.
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)

class EditProfile(tk.simpledialog.Dialog):
    def __init__(self, root, title=None, user=None, pwd=None, server=None):
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        super().__init__(root, title)


    def body(self, frame):
        self.server_label = tk.Label(frame, width=50, text="DS Server Address")
        self.server_label.pack()
        self.server_entry = tk.Entry(frame, width=30)
        self.server_entry.insert(tk.END, self.server)
        self.server_entry.pack()

        self.username_label = tk.Label(frame, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.insert(tk.END, self.user)
        self.username_entry.pack()

        self.password_label = tk.Label(frame, width=30, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(frame, width=30)
        self.password_entry.insert(tk.END, self.user)
        self.password_entry['show'] = '*'
        self.password_entry.pack()


    def apply(self):
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()

class NewProfile(tk.simpledialog.Dialog):
    def __init__(self, root, title=None):
        self.root = root
        self.server = ''
        self.user = ''
        self.pwd = ''
        self.directory = ''
        super().__init__(root, title)


    def body(self, frame):
        content_frame = tk.Frame(frame)
        content_frame.pack(padx=10, pady=10)

        self.username_label = tk.Label(content_frame, width=30, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(content_frame, width=30)
        self.username_entry.insert(tk.END, self.user)
        self.username_entry.pack()

        self.password_label = tk.Label(content_frame, width=30, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(content_frame, width=30)
        self.password_entry.insert(tk.END, self.user)
        self.password_entry.pack()

        self.server_label = tk.Label(content_frame, width=30, text="Server IP Address:")
        self.server_label.pack()
        self.server_entry = tk.Entry(content_frame, width=30)
        self.server_entry.insert(tk.END, self.user)
        self.server_entry.pack()

        self.choose_dir = tk.Button(content_frame, text="Open File", width=20,
                                    command=self.open_file)
        self.choose_dir.pack(side='bottom', pady=10)


    def open_file(self):
        directory = filedialog.asksaveasfilename(
                        initialdir="/", title="Choose Profile Location",
                        defaultextension=".dsu")
        self.directory = directory


    def apply(self):
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()


class MainApp(tk.Frame):
    def __init__(self, root):
        self.root = root
        self.username = ''
        self.password = ''
        self.server = ''
        self.recipient = ''
        self.profile = None
        self.path = None
        self.direct_messenger = None
        self.body = None

        self._draw()


    def error_msg(self):
        tk.messagebox.showerror("ERROR", 'UNABLE TO SEND MESSAGE')


    def send_message(self):
        try:
            recipient = self.recipient
            message = self.body.get_text_entry()
            if recipient and message:
                send = self.direct_messenger.send(message, recipient)
                assert send is True, 'ERROR: Failed to send message'
                sent_msg = SentMessages(message)
                self.body.insert_user_message(message)

            if recipient in self.body._sent.keys() and recipient in self.profile._sent.keys():
                self.profile.add_sent_message(sent_msg, recipient)
                self.profile.save_profile(self.path)
                self.body._sent[recipient].append(sent_msg)

            elif recipient not in self.body._sent.keys() and recipient not in self.profile._sent.keys():
                self.profile.add_sent_message(sent_msg, recipient)
                self.body._sent[recipient] = [sent_msg]

            self.body.set_text_entry('')

        except AssertionError as e:
            print('Assertion Error: ', e)
            self.error_msg()


    def load_profile(self):
        print('Loading Profile...')
        profile_path = filedialog.askopenfilename()
        profile = Profile()
        profile.load_profile(profile_path)
        self.username, self.password = profile.username, profile.password
        self.server = profile.dsuserver
        self.profile, self.path = profile, profile_path
        self.direct_messenger = DirectMessenger(self.server, self.username, self.password)
        for friend in profile._friends:
            self.body.insert_contact(friend)
            if friend in profile._received.keys():
                self.body._messages[friend] = profile._received[friend]
            if friend in profile._sent.keys():
                self.body._sent[friend] = profile._sent[friend]
        print('Done loading profile!')


    def new_profile(self):
        profile = NewProfile(self.root, "New Profile")
        self.username, self.password = profile.user, profile.pwd
        self.server = profile.server
        p = Path(profile.directory)
        p.touch()
        self.profile = Profile(username=self.username, password=self.password,
                               dsuserver=self.server)
        self.path = p
        self.profile.save_profile(p)
        self.direct_messenger = DirectMessenger(self.server, self.username, self.password)


    def add_contact(self):
        user = tk.simpledialog.askstring("Add Friend", "User: ")
        self.profile.add_friend(user)
        self.profile.save_profile(self.path)
        self.body.insert_contact(user)
        self.body.new_contact.append(user)
        print('Added new Contact:', self.body.new_contact)


    def recipient_selected(self, recipient):
        self.recipient = recipient


    def edit_profile(self):
        ud = EditProfile(self.root, "Edit Profile",
                              self.username, self.password, self.server)
        self.username = ud.user
        self.password = ud.pwd
        self.server = ud.server


    def check_new(self):
        try:
            print('Checking new...')
            messages = self.direct_messenger.retrieve_new() # change to retrieve_new
            if messages == []:
                print('No new messages!')
            else:
                print("New Messages: ", messages)
                for message in messages:
                    user = message['from']
                    msg = message['message']
                    timestamp = message['timestamp']
                    received_message = ReceivedMessage(msg, timestamp)
                    if user not in self.body._messages.keys() and user not in self.profile._received.keys():
                        if user not in self.profile._friends:
                            self.profile.add_friend(user)
                        self.profile.add_message(received_message, user)
                        self.profile.save_profile(self.path)
                        print('Sender:', user)
                        print('New Contact List:', self.body.new_contact)
                        if user not in self.body._contacts:
                            self.body.insert_contact(user)
                        self.body._messages[user] = [received_message]
                    elif user in self.body._messages.keys() and user in self.profile._received.keys():
                        self.profile.add_message(received_message, user)
                        self.profile.save_profile(self.path)
                        self.body._messages[user].append(received_message)
                    if self.recipient == user:
                        self.body.insert_contact_message(msg)
                        self.body.new_insert.append(received_message)
            self.root.after(2000, self.check_new)
        except AttributeError:
            self.root.after(2000, self.check_new)


    def _draw(self):
        self.body = Body(self.root,
                         recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)

        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)

        menu_bar.add_cascade(menu=menu_file, label = 'Profile')
        menu_file.add_command(label='New Profile',
                              command=self.new_profile)
        menu_file.add_command(label='Load Profile',
                              command=self.load_profile)

        settings_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=settings_file, label = 'Settings')
        settings_file.add_command(label='Add Contact',
                                command=self.add_contact)
        settings_file.add_command(label='Edit Profile',
                                command=self.edit_profile)

if __name__ == '__main__':
    main = tk.Tk()
    main.title("ICS 32 Distributed Social Messenger")
    main.geometry("720x480")
    main.option_add('*tearOff', False)
    app = MainApp(main)
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    id = main.after(2000, app.check_new)
    print(id)
    main.mainloop()
    