import tkinter as tk
from tkinter import filedialog, scrolledtext
import threading
import asyncio

from chatbot import ChatBot
from message_history import MessageHistory
from screenshot_tool import ScreenshotTool
from api_tool import ApiTool

class ChatBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg="#CFE6EF")
        root.title("ChatBot")
        root.geometry('1000x600')

        self.attachment: None|str = None
        self.attachment_type: None|str = None

        self.screenshot_tool = None

        self.chatbot = ChatBot()

        self.message_history = MessageHistory(database_name="message_history.db", current_conversation="1")

        self.api_tool = ApiTool(root=root)

        self.frame1 = tk.Frame(master=self.root, bg="#CFE6EF") #left (conversation selection)
        self.frame2 = tk.Frame(master=self.root, bg="#CFE6EF") #middle
        self.frame3 = tk.Frame(master=self.root, bg="#CFE6EF") #right

        self.frame2_top = tk.Frame(master=self.frame2, bg="#CFE6EF")
        self.frame2_bottom = tk.Frame(master=self.frame2, bg="#CFE6EF")

        self.chat_history = scrolledtext.ScrolledText(master=self.frame2_top, width=80, height=20, font=("Arial", 12), state='disabled')
        self.input_frame = tk.Frame(master=self.frame2_bottom, bg="#CFE6EF")
        self.input_label = tk.Label(master=self.input_frame, text="Kysy mitä vain!", font=("Arial", 12), bg="#CFE6EF")
        self.input_entry = tk.Entry(master=self.input_frame, width=40, font=("Arial", 12))
        self.send_button = tk.Button(master=self.input_frame, text="➦", command=self.send_message, font=("Arial", 12), bg="#4D4A98", fg="#FFFFFF")
        self.image_upload_button = tk.Button(master=self.frame2_bottom, text="Liitä kuvatiedosto", command=lambda: self.upload_attachment(attachment_type="image"), font=("Arial", 12), bg="#4D4A98", fg="#FFFFFF")
        self.audio_upload_button = tk.Button(master=self.frame2_bottom, text="Liitä äänitiedosto", command=lambda: self.upload_attachment(attachment_type="audio"), font=("Arial", 12), bg="#4D4A98", fg="#FFFFFF")
        self.video_upload_button = tk.Button(master=self.frame2_bottom, text="Liitä videotiedosto", command=lambda: self.upload_attachment(attachment_type="video"), font=("Arial", 12), bg="#4D4A98", fg="#FFFFFF")
        self.screenshot_button = tk.Button(master=self.frame2_bottom, text="Liitä kuvankaappaus", command=lambda: self.create_screenshot_thread(), font=("Arial", 12), bg="#4D4A98", fg="#FFFFFF")

        self.conversation_button_list = []
        for i in range(6):
            i = i + 1
            button = tk.Button(
                master=self.frame1, 
                text=f"{i}", 
                command=lambda id=i: self.switch_conversation(
                    id=id,
                ), 
                font=("Arial", 12), 
                bg="#8e9091"
            )
            self.conversation_button_list.append(button)
            self.message_history.create_new_conversation()

        self.api_selection_variable = tk.StringVar()
        self.api_selection_variable.set("-")
        self.api_selection_button = tk.OptionMenu(
            self.frame3,
            self.api_selection_variable,
            *self.api_tool.get_api_choices(),
            command=self.handle_api_selection_button_pressed
        )



        #dividing the window into three sections
        self.root.columnconfigure(index=0, weight=1)
        self.root.columnconfigure(index=1, weight=3)
        self.root.columnconfigure(index=2, weight=1)
        self.root.rowconfigure(index=0, weight=1)

        self.frame1.grid(row=0, column=0, sticky='nsew')
        self.frame2.grid(row=0, column=1, sticky='nsew')
        self.frame3.grid(row=0, column=2, sticky='nsew')

        #diving frame2 into two sections
        self.frame2.columnconfigure(index=0, weight=1)
        self.frame2.rowconfigure(index=0, weight=1)
        self.frame2.rowconfigure(index=1, weight=1)

        self.frame2_top.grid(row=0, column=0, sticky='nsew')
        self.frame2_bottom.grid(row=1, column=0, sticky='nsew')

        self.chat_history.pack(fill='x', padx=10, pady=10, expand=True)
        self.input_frame.pack(fill='both')
        self.input_entry.pack(side=tk.LEFT)
        self.send_button.pack(side=tk.LEFT)
        self.image_upload_button.pack(side=tk.LEFT)
        self.audio_upload_button.pack(side=tk.LEFT)
        self.video_upload_button.pack(side=tk.LEFT)
        self.screenshot_button.pack(side=tk.LEFT)

        for button in self.conversation_button_list:
            button.pack()

        self.api_selection_button.pack(side=tk.TOP)

        self.initialize_chat()



    def messages_from_database_to_conversation(self):
        for message in self.message_history.get_messages():
            self.chat_history.configure(state='normal')

            text = ""

            if message['sender'] == 'user':
                text = "Kysymyksesi: " + message['message']
            else:
                text = "Chatbot: " + message['message']

            self.chat_history.insert(index=tk.END, chars=f"{text}\n\n\n")
            self.chat_history.configure(state='disabled')   

    def initialize_chat(self):
        if self.message_history.is_database_empty() == False:
            self.messages_from_database_to_conversation()

    def store_message_into_database(self, message: str, sender: str, attachment: str | None):
        message = {"message": message, "sender": sender}
        self.message_history.insert_message(message=message, attachment=attachment)

    def send_message(self):
        question = self.input_entry.get().strip()

        print("\n")
        print("Before get_response")
        print("\n")

        response = self.chatbot.get_response(
            question=question,
            previous_messages=self.message_history.get_messages(),
            attachment_type=self.attachment_type,
            attachment=self.attachment
        )

        print("\n")
        print("After get_response")
        print("\n")

        self.store_message_into_database(message=question, sender="user", attachment=self.attachment)
        self.store_message_into_database(message=response, sender="assistant", attachment=None)

        question = "Kysymyksesi: {}\n\n".format(question)
        response = "ChatBot: {}\n\n".format(response)
    
        self.chat_history.configure(state='normal')
        self.chat_history.insert(tk.END, question) 
        self.chat_history.insert(tk.END, "\n\n")
        self.chat_history.insert(tk.END, response)
        self.chat_history.insert(tk.END, "\n\n")
        self.chat_history.configure(state='disabled')
        self.input_entry.delete(0, tk.END)

        self.attachment = None
        self.attachment_type = None

    def upload_attachment(self, attachment_type):
        self.attachment_type = attachment_type
        self.attachment = filedialog.askopenfilename()



    async def handle_screenshot(self):
        screenshot_tool = ScreenshotTool(root=root)

        await screenshot_tool.wait_until_screenshot_taken()

        self.attachment_type = "screenshot"

        screenshot = screenshot_tool.get_path_to_screenshot()

        self.attachment = screenshot

        screenshot_tool.quit()

    def create_screenshot_thread(self):
        thread = threading.Thread(
            target=asyncio.run,
            args=(self.handle_screenshot(),)
        )
        thread.start()
        
        



    def switch_conversation(self, id: int):
        self.chat_history.configure(state='normal')
        self.chat_history.delete(index1=1.0, index2=tk.END)
        self.chat_history.configure(state='disabled')
        
        self.message_history.change_current_conversation(conversation_name=id)
        
        self.messages_from_database_to_conversation()


    def handle_api_selection_button_pressed(self, value):
        self.api_tool.choose_api(value=value)
        #TODO: something to do with the endpoints, choosing the endpoint? getting the endpoints?




root = tk.Tk()
app = ChatBotGUI(root=root)
root.mainloop()