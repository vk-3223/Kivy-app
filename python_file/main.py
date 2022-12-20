from datetime import datetime
import glob
from importlib.resources import path
from pathlib import Path
import json
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.uix.gridlayout  import GridLayout
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior 
import random
from hoverable import HoverBehavior


Builder.load_file('desing.kv')

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current ="sign_up_screen"

    def login(self,username,password):
        with open("user.json")as file:
            user = json.load(file)

        if username in user and user[username]['password']==password:
            self.manager.current = "login_screen_success"
        else:
            self.ids.login_wrong.text = "Wrong username or password !!"    


class RootWidget(ScreenManager):
    pass

class SignUpScreen(Screen):
    def add_user(self,username,password):
        with open("user.json") as file:
            user = json.load(file)

        user[username] = {'username':username,'password':password,'created':datetime.now().strftime("%Y-%m-%d %H-%M-%S")}
        
        
        with open("user.json",'w')as file:
            json.dump(user,file)
        self.manager.current = "sign_up_screen_success"    

class SignUpScreenSuccess(Screen):
    def go_to_login(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"
    def get_quote(self,feel):
        feel = feel.lower()
        avlable_file = glob.glob("quotes/*txt")
        
        avlable_file = [Path(file_name).stem for file_name in avlable_file]
        
        if feel in avlable_file:
            with open(f"quotes/{feel}.txt",encoding="utf8")as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = "Try another Feeling"

class ImageButton(ButtonBehavior,HoverBehavior,Image):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__==("__main__"):
    MainApp().run()
