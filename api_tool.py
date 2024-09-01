import requests
import tkinter as tk
from tkinter import scrolledtext

class ApiTool:
    def __init__(self, root):
        self.window = tk.Toplevel(master=root)
        self.window.geometry('600x600')
        self.window.title("API tool")

        self.__api_dict = {
            "vipunen": {
                "url_root": "https://api.vipunen.fi/api/",
                "path_to_endpoints": "resources"
            },
        }
        self.__api_name: None|str = None
        self.__endpoints: list = []

        self.window_upper_half = tk.Frame(master=self.window)
        self.window_lower_half = tk.Frame(master=self.window)

        self.window.columnconfigure(index=0, weight=1)
        self.window.rowconfigure(index=0, weight=1)
        self.window.rowconfigure(index=1, weight=3)

        self.window_upper_half.grid(row=0, column=0, sticky='nsew')
        self.window_lower_half.grid(row=1, column=0, sticky='nsew')

        self.api_choice = tk.StringVar()
        self.api_choice.set("initial")

        self.api_choice_dropdown_menu = tk.OptionMenu(
            self.window_upper_half,
            self.api_choice,
            *[choice for choice in self.get_api_choices()],
            command=self.api_and_endpoint_logic)

        self.api_choice_dropdown_menu.pack(side=tk.TOP)

        self.api_endpoint_checkbox_list = []

    def __get__api_dict(self):
        return self.__api_dict

    def __set__api_name(self, value):
        if value == None:
            self.__api_name = None
            return
        
        value = value.strip().lower()

        for key in self.api_dict:
            if key == value:
                self.__api_name = value
                break

    def __get__api_name(self):
        return self.__api_name
    
    def __set__endpoints(self, value):
        self.__endpoints = value

    def __get__endpoints(self):
        return self.__endpoints

    api_dict = property(fget=__get__api_dict)
    api_name = property(fget=__get__api_name, fset=__set__api_name)
    endpoints = property(fget=__get__endpoints, fset=__set__endpoints)



    def quit(self):
        self.window.destroy()

    def get_api_choices(self) -> list:
        choices = []

        for choice in self.api_dict:
            choices.append(choice)
        
        return choices

    def handle_api_endpoints():
        #fetch_api_endpoints
        #make an endpoint selection appear
          ##pack a scrollable view and a checkbox inside it
        pass



    def choose_api(self, api_name):
        self.api_name = api_name

    def fetch_api_endpoints(self):
        url = self.api_dict[self.api_name]["url_root"] + self.api_dict[self.api_name]["path_to_endpoints"]
        
        try:
            response = requests.get(url)

            if response.status_code == 200:
                posts = response.json()

                self.endpoints.extend(posts)

        except requests.exceptions.RequestException as e:
            print("Error: ", e)

    def display_api_endpoint_checkboxes(self):
        self.api_endpoint_checkbox_list = []

        #scrollbar = tk.Scrollbar(master=self.window_lower_half).pack(side=tk.RIGHT, fill=tk.Y)
        #canvas = tk.Canvas(master=self.window_lower_half, yscrollcommand=scrollbar, background="red", ).pack(side=tk.TOP)

        scrollable_checkboxes = scrolledtext.ScrolledText(
            master=self.window_lower_half,
            width=80,
            height=20,
            state="normal"
        ).pack()

        for endpoint in self.endpoints:
            self.api_endpoint_checkbox_list.append(
                tk.Checkbutton(
                    master=scrollable_checkboxes,
                    text=endpoint,
                    var=tk.IntVar(),
                    onvalue=1,
                    offvalue=0,
                    anchor="w"
                ).pack(side=tk.TOP)
            )

    def api_and_endpoint_logic(self, api_name):
        self.choose_api(api_name=api_name)
        self.fetch_api_endpoints()
        self.display_api_endpoint_checkboxes()
        


    def choose_api_endpoint(self):
        pass

    def get_data_from_desired_endpoint(self):
        pass