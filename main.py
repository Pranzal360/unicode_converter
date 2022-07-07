import npttf2utf
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.core.clipboard import Clipboard
from kivy.lang.builder import Builder
from kivymd.toast import toast
import json

"""
Here the implementation of unbreakable devnagari character remains
i hope i'll be able to solve the issue very soon !
"""

mapper = npttf2utf.FontMapper("map.json")

class Converter(MDApp):

    state = 0
    # 0 refers to the normal state
    dialog = None

    def build(self):
        
        self.kv = Builder.load_file('main.kv')
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Purple" 

        return self.kv
    
    
    def unicode(self,text):
    
        print(text)
    
        if text == "":
            toast("Can't be empty !",duration=2)

        else:
            toast("Converted !",duration=2)
                                                    
            if self.state == 0:
                
                print(self.state)
                
                returned_unicode = mapper.map_to_preeti(text,from_font="Unicode")
                
                self.root.ids.outField.text = returned_unicode
                
                print(returned_unicode)
            
            else :
            
                print(self.state)
            
                returned_unicode = mapper.map_to_unicode(text,from_font="Preeti")
            
                self.root.ids.outField.text = returned_unicode
            
                print(returned_unicode)


    def pasteBtn(self,data):
        
        print(data)
        
        toast("Pasted !",duration=2)
       
        self.root.ids.inField.text = data
        " paste btn "

    def contentCopy(self,textOfOutField):
        "content copy"
        
        if textOfOutField == "":
        
            toast("is empty")
        
        else:
        
            Clipboard.copy(textOfOutField)
            toast("Copied successfully !",duration = 2)
            
    
    def callback(self): 

        toast("Devanagari characters aren't loaded nicely i know that ! trying to fix it !")


    def change(self):
        """Change sec"""
        self.root.ids.inField.text = ""
        
        self.root.ids.outField.text = ""
        
        if self.state == 0:
        
            print(self.state)
        
            self.state = 1
        
            print(self.state)

            self.root.ids.toolbar.title = "preeti to unicode"
        
            self.root.ids.inField.hint_text = "Enter Preeti"
        
        else:
        
            print(self.state)

            self.state = 0
        
            print(self.state)

            self.root.ids.toolbar.title = "unicode to preeti"
        
            self.root.ids.inField.hint_text = "Enter Unicode"

    
    def clearField(self):
        "Field clear"
        
        self.root.ids.inField.text = ""
        
        self.root.ids.outField.text = ""
        
        toast("Cleared !",duration=2)
    
    
    def donotShow(self,*args):
        """"""
        dict = {
            "open":False
        }

        with open('setting.json','a') as outfile:
            json.dump(dict,outfile)
        
        self.close()

    
    def close(self,*args):
        
        self.dialog.dismiss()
    
    
    def dialogBox(self):
    
        if not self.dialog:
    
            self.dialog = MDDialog(
    
                text="Note : Unicode is a devanagari character whereas Preeti is alphabetical one",
    
                buttons=[
                    MDFlatButton(
                        text="DO NOT SHOW AGAIN",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_press = self.donotShow
                    ),
    
                    MDFlatButton(
                        text="CLOSE",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_press= self.close
                    ),
                ],
            )
 
        self.dialog.open()

    
    def on_start(self):
 
        print("Started")
 
        "Dialouge box for do not show again"
 
        try:
            with open('setting.json', 'r') as openfile:
 
                json_object = json.load(openfile)

            file = json_object.items()

    # Reading from json file

            for key,value in file:

                if value == False:

                    print("user doesn't wants too see")

                else:

                    print()

                    self.dialogBox()
        except Exception as e:

            self.dialogBox()

            print(e)
    

Converter().run()