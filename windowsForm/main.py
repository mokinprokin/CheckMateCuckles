
from distutils.core import setup_keywords
from tkinter.messagebox import showerror
from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
from customtkinter import *
from PIL import Image
import PIL
import DbHelper
from io import BytesIO
import requests
from datetime import datetime
from random import shuffle
import bs4



ctk.FontManager.load_font("Softie Cyr.ttf")



class history():
    def __init__(self,login,header,description,date):
        self.login=login
        self.header=header
        self.description=description
        self.date=date

class News():
    def __init__(self,header,date):
        self.header=header
        self.date=date

class MainApp(ctk.CTk):
    def __init__(self):
        CTk.__init__(self)
        global app
        #Db_Data
        #icons/Images
        self.imageHome =ctk.CTkImage(Image.open("Icons/icon_home.png"),size=(60, 60))
        self.imageInfo =ctk.CTkImage(Image.open("Icons/icon_info.png"),size=(60, 60))
        self.imageAdd =ctk.CTkImage(Image.open("Icons/icon_add.png"),size=(60, 60))
        self.imageNews =ctk.CTkImage(Image.open("Icons/icon_news.png"),size=(60, 60))
        self.arrowRight=ctk.CTkImage(Image.open("Icons/arrow.png"),size=(70,70))
        self.arrowLeft=ctk.CTkImage(Image.open("Icons/arrow.png").transpose(PIL.Image.FLIP_LEFT_RIGHT),size=(70,70))

        self.counter=0
        self.NewsCounter=0

        #colors
        self.color="transparent"
        self.SelectedColor="#505050"
        self.BorderColor="#707070"
        self.UnActiveColor="#404040"
        self.HoverColor = "#202020"

        #config
        self.title("app")
        self.geometry(f"200x200")
        self.configure(fg_color='#252525') 

        #Drawing on Window NavMenu
        self.NavMenu=ctk.CTkFrame(master=self,bg_color="transparent",fg_color="#343434")
        self.NavMenu.grid(row=0,column=0,padx=(10,0),pady=10,sticky="NSWE",rowspan=3)

        self.NavMenu.grid_rowconfigure(0,weight=1)
        self.NavMenu.grid_rowconfigure(1, weight=1)
        self.NavMenu.grid_rowconfigure(2, weight=1)
        self.NavMenu.grid_rowconfigure(3, weight=1)
        self.NavMenu.grid_rowconfigure(4,weight=1)
        self.NavMenu.grid_rowconfigure(5,weight=10)
        self.NavMenu.grid_columnconfigure(0,weight=1)

        self.NavMenuHeader=ctk.CTkLabel(master=self.NavMenu,text="Checkmate\nChuckles",fg_color=self.color,bg_color=self.color,font=("Softie Cyr",45),text_color="white")
        self.NavMenuHeader.grid(row=0, column=0, padx=(0,0), pady=(10,3), sticky="NSWE")
        self.button=ctk.CTkButton(master=self.NavMenu,image=self.imageInfo, text=" Профиль",corner_radius=0,bg_color=self.color,font=("Softie Cyr",38),fg_color=self.color,hover_color=self.HoverColor,command=lambda: self.change_button_color(self.button))
        self.button.grid(row=1, column=0, padx=(0,0), pady=(7,3), sticky="NSWE")

        self.button1 =ctk.CTkButton(master=self.NavMenu, text=" Главная",corner_radius=0,bg_color=self.color,font=("Softie Cyr",38),fg_color=self.SelectedColor,image=self.imageHome,hover_color=self.HoverColor,command=lambda: self.change_button_color(self.button1))
        self.button1.grid(row=2, column=0,padx=(0,0), pady=7, sticky="NSWE")

        self.button2 =ctk.CTkButton(master=self.NavMenu, text=" Создать",corner_radius=0,bg_color=self.color,fg_color=self.color,font=("Softie Cyr",38),image=self.imageAdd,hover_color=self.HoverColor,command=lambda: self.change_button_color(self.button2))
        self.button2.grid(row=3, column=0, padx=(0,0), pady=3, sticky="NSWE")

        self.button3=ctk.CTkButton(master=self.NavMenu, text=" Новости",corner_radius=0,bg_color=self.color,fg_color=self.color,font=("Softie Cyr",38),image=self.imageNews,hover_color=self.HoverColor,command=lambda: self.change_button_color(self.button3))
        self.button3.grid(row=4, column=0, padx=(0,0), pady=3, sticky="NSWE")
        #Drawing on Window Info Label
        self.InfoFrame=ctk.CTkFrame(master=self,bg_color="transparent",fg_color="#343434",)
        self.InfoFrame.grid_columnconfigure(0,weight=1)
        self.InfoFrame.grid_rowconfigure(0,weight=5)
        self.InfoFrame.grid_rowconfigure(1,weight=1)
        self.InfoFrame.grid_columnconfigure(1,weight=1)
        self.InfoFrame.grid_rowconfigure(2,weight=2)
        self.InfoFrame.grid_rowconfigure(3,weight=20)
        self.InfoFrame.grid_rowconfigure(4,weight=1)

        self.InfoHeader=ctk.CTkLabel(master=self.InfoFrame,text="Ваш профиль",fg_color=self.UnActiveColor,bg_color=self.color,font=("Softie Cyr",55),text_color="white")
        self.InfoHeader.grid(row=0,padx=10,pady=(10,0),column=0,columnspan=2,sticky="NSWE")

        self.InfoChangeButton=ctk.CTkButton(master=self.InfoFrame, text="Изменить",corner_radius=100,bg_color=self.color,font=("Softie Cyr",38),fg_color=self.SelectedColor,hover_color=self.HoverColor,command=self.setRegister)
        self.InfoChangeButton.grid(row=2, column=0,padx=10,sticky="NSWE",columnspan=2)

        self.EntryLogin=ctk.CTkEntry(master=self.InfoFrame,placeholder_text="Введите логин",corner_radius=0,font=("Softie Cyr",38),bg_color=self.color,fg_color=self.UnActiveColor,text_color="white")
        self.EntryLogin.grid(row=1,column=0,padx=(10,5),pady=10,sticky="NSWE")

        self.EntryPassword=ctk.CTkEntry(master=self.InfoFrame,placeholder_text="Введите пароль",corner_radius=0,font=("Softie Cyr",38),bg_color=self.color,fg_color=self.UnActiveColor,text_color="white")
        self.EntryPassword.grid(row=1,padx=(5,10),pady=10,column=1,sticky="NSWE")

        self.LoginHeader=ctk.CTkLabel(master=self.InfoFrame,text="Логин:",fg_color=self.UnActiveColor,bg_color=self.color,font=("Softie Cyr",50),text_color="white")
        self.LoginHeader.grid(row=3,padx=10,pady=(10,10),column=0,sticky="NSWE")
        self.wrap_text_based_on_screen(self.LoginHeader)

        self.PasswordHeader=ctk.CTkLabel(master=self.InfoFrame,text="Пароль: ",state="normal",fg_color=self.UnActiveColor,bg_color=self.color,font=("Softie Cyr",50),text_color="white",anchor="center")
        self.PasswordHeader.grid(row=3,padx=10,pady=(10,10),column=1,sticky="NSWE")

        self.wrap_text_based_on_screen(self.PasswordHeader)

        # self.LikesHeader=ctk.CTkLabel(master=self.InfoFrame,corner_radius=10,text=f"Лайки: {0}",state="normal",fg_color=self.UnActiveColor,bg_color=self.color,font=("Softie Cyr",50),text_color="white",anchor="center")
        # self.LikesHeader.grid(row=4,padx=10,pady=(10,10),column=0,columnspan=2,sticky="NSWE")

        if(self.GetId()!=""):
            data=DbHelper.getData(self.GetId())
            self.UpdateRegisterValues(data[1],data[2])

        self.InfoFrame.grid_forget()

        #Drawing on Window Home Label
        self.HomeFrame=ctk.CTkFrame(master=self,bg_color="transparent",fg_color="#343434",)
        self.HomeFrame.grid_columnconfigure(0,weight=2)
        self.HomeFrame.grid_columnconfigure(1,weight=1)
        self.HomeFrame.grid_columnconfigure(2,weight=8)
        self.HomeFrame.grid_columnconfigure(3,weight=1)
        self.HomeFrame.grid_columnconfigure(4,weight=2)
        self.HomeFrame.grid_rowconfigure(0,weight=3)
        self.HomeFrame.grid_rowconfigure(1,weight=1)
        self.HomeFrame.grid_rowconfigure(2,weight=3)

        self.HistoryFrame=ctk.CTkFrame(master=self.HomeFrame,bg_color="transparent",fg_color=self.UnActiveColor)
        self.HistoryFrame.grid(row=0,column=2,rowspan=3,sticky="NSEW",pady=20)
        self.HistoryFrame.grid_rowconfigure(0,weight=0)
        self.HistoryFrame.grid_rowconfigure(1,weight=1)
        self.HistoryFrame.grid_rowconfigure(2,weight=18,minsize=200)
        self.HistoryFrame.grid_rowconfigure(3,weight=3)
        self.HistoryFrame.grid_rowconfigure(4,weight=3)
        self.HistoryFrame.grid_columnconfigure(0,weight=1)
        self.HistoryFrame.grid_columnconfigure(1,weight=1)


        self.Header=ctk.CTkTextbox(master=self.HistoryFrame,corner_radius=0,border_width=3,border_spacing=10,font=("Softie Cyr",50),text_color="white",bg_color=self.color,fg_color=self.SelectedColor)
        self.Header.grid(row=1,column=0,columnspan=2,sticky="NSEW",padx=10)

        self.Description=ctk.CTkTextbox(master=self.HistoryFrame,corner_radius=0,border_width=3,border_spacing=10,font=("Softie Cyr",30),text_color="white",bg_color=self.color,fg_color=self.SelectedColor)
        self.Description.grid(row=2,column=0,columnspan=2,sticky="NSEW",pady=10,padx=10)

        self.Date=ctk.CTkTextbox(master=self.HistoryFrame,corner_radius=0,border_width=3,border_spacing=10,font=("Softie Cyr",30),text_color="white",bg_color=self.color,fg_color=self.SelectedColor)
        self.Date.grid(row=3,column=1,sticky="NSEW",pady=10,padx=10)

        self.Login=ctk.CTkTextbox(master=self.HistoryFrame,corner_radius=0,border_width=3,border_spacing=10,font=("Softie Cyr",30),text_color="white",bg_color=self.color,fg_color=self.SelectedColor)
        self.Login.grid(row=3,column=0,sticky="NSEW",pady=10,padx=10)

        self.arrHistories=[]

        self.buttonHomeLeft=ctk.CTkButton(master=self.HomeFrame,text="",border_color=self.SelectedColor,border_width=10,corner_radius=0,bg_color=self.color,font=("Softie Cyr",38),fg_color=self.color,image=self.arrowLeft,hover_color=self.SelectedColor,command=lambda:self.Left(self.counter,self.arrHistories))
        self.buttonHomeLeft.grid(row=1,column=1,sticky="NSEW",pady=20,padx=(0,10))
        self.buttonHomeRight=ctk.CTkButton(master=self.HomeFrame,text="",border_width=10,border_color=self.SelectedColor,corner_radius=0,bg_color=self.color,font=("Softie Cyr",38),fg_color=self.color,image=self.arrowRight,hover_color=self.SelectedColor,command=lambda:self.Right(self.counter,self.getAllHeaders(),self.arrHistories))
        self.buttonHomeRight.grid(row=1,column=3,sticky="NSEW",pady=20,padx=(10,0)) 


        # self.commentsHome=ctk.CTkButton(master=self.HistoryFrame,text="Коментарии",border_color=self.SelectedColor,border_width=10,corner_radius=0,bg_color=self.color,font=("Softie Cyr",38),fg_color=self.color,hover_color=self.SelectedColor,command=self.ShowComments)
        # self.commentsHome.grid(row=4,column=0,columnspan=2,sticky="NSEW",padx=10,pady=(0,10))



        # self.CommentsFrame=ctk.CTkFrame(master=self.HomeFrame,bg_color="transparent",fg_color=self.UnActiveColor)
        # self.CommentsFrame.grid_columnconfigure(0,weight=1)
        # self.CommentsFrame.grid_columnconfigure(1,weight=1)
        # self.CommentsFrame.grid_rowconfigure(0,weight=16)
        # self.CommentsFrame.grid_rowconfigure(1,weight=4)
        # self.CommentsFrame.grid_rowconfigure(2,weight=3)
        # self.CommentsFrame.grid_rowconfigure(3,weight=1)

        # self.ComentsScroll=ctk.CTkScrollableFrame(master=self.CommentsFrame,bg_color="transparent",fg_color=self.UnActiveColor,border_color=self.SelectedColor,border_width=10,corner_radius=0)
        # self.ComentsScroll.grid(row=0,column=0,columnspan=2,padx=10,pady=10,sticky="NSEW")
        # self.ComentsScroll.grid_columnconfigure(0,weight=1)

        # self.comment=ctk.CTkTextbox(master=self.ComentsScroll,bg_color="transparent",fg_color=self.UnActiveColor,border_color=self.SelectedColor,border_width=10,corner_radius=0,border_spacing=10,font=("Softie Cyr",34),text_color="white")

        # self.EntryComment=ctk.CTkEntry(master=self.CommentsFrame,corner_radius=0,border_width=3,font=("Softie Cyr",50),text_color="white",bg_color=self.color,fg_color=self.SelectedColor)
        # self.EntryComment.grid(row=1,column=0,columnspan=2,sticky="NSEW",padx=10)

        # self.CommentButton=ctk.CTkButton(master=self.CommentsFrame,text="Опубликовать",border_color=self.SelectedColor,border_width=10,corner_radius=0,bg_color=self.color,font=("Softie Cyr",28),fg_color=self.color,hover_color=self.SelectedColor,command=self.SetComment)
        # self.CommentButton.grid(row=2,column=0,columnspan=2,sticky="NSEW",padx=10,pady=(10,10))

        # self.BackCommentButton=ctk.CTkButton(master=self.CommentsFrame,text="Назад",border_color=self.SelectedColor,border_width=10,corner_radius=0,bg_color=self.color,font=("Softie Cyr",38),fg_color=self.color,hover_color=self.SelectedColor,command=self.BackToHome)
        # self.BackCommentButton.grid(row=3,column=0,columnspan=2,sticky="NSEW",padx=10,pady=(0,10))
        

        # self.CommentsFrame.grid_forget()

        self.HomeFrame.grid_forget()


        #Drawing on Window Add Label
        self.AddFrame=ctk.CTkFrame(master=self,bg_color="transparent",fg_color="#343434",)
        self.AddFrame.grid_rowconfigure(0,weight=1)
        self.AddFrame.grid_rowconfigure(1,weight=1)
        self.AddFrame.grid_rowconfigure(2,weight=6)
        self.AddFrame.grid_rowconfigure(3,weight=1)
        self.AddFrame.grid_rowconfigure(4,weight=1)
        self.AddFrame.grid_columnconfigure(0,weight=1)
        self.AddFrame.grid_columnconfigure(1,weight=7)
        self.AddFrame.grid_columnconfigure(2,weight=1)

        self.addbtn=ctk.CTkButton(master=self.AddFrame, text="add",corner_radius=0,bg_color=self.color,font=("Softie Cyr",38),border_color=self.BorderColor,fg_color=self.SelectedColor,hover_color=self.HoverColor,border_width=2,command=lambda:self.writeHistoryToDb(self.getTextEntry(self.EntryHeader),self.getTextBox(self.EntryDescription)))
        self.addbtn.grid(row=3, column=1,sticky="NSEW",pady=10)

        # self.InfoAddHeader=ctk.CTkTextbox(master=self.AddFrame,fg_color=self.UnActiveColor,bg_color=self.color,font=("Softie Cyr",50),text_color="white",border_spacing=10)
        # self.InfoAddHeader.grid(row=0,pady=(10,10),column=1,sticky="NSWE")
        # self.InfoAddHeader.tag_config("center", justify="center")
        # self.InfoAddHeader.insert("0.0", "Изображение генерируется\nавтоматически","center")
        # self.InfoAddHeader.configure(state="disabled")

        self.EntryHeader=ctk.CTkEntry(master=self.AddFrame,placeholder_text="Введите заголовок",corner_radius=0,font=("Softie Cyr",40),bg_color=self.color,fg_color=self.UnActiveColor,text_color="white")
        self.EntryHeader.grid(row=1,column=1,pady=10,sticky="NSWE")
        self.EntryHeader.delete("0", "end")

        self.EntryDescription=ctk.CTkTextbox(master=self.AddFrame,corner_radius=0,border_width=3,border_spacing=10,font=("Softie Cyr",34),bg_color=self.color,fg_color=self.UnActiveColor,text_color="#C7C7C7")
        self.EntryDescription.grid(row=2,pady=10,column=1,sticky="NSWE")
        self.EntryDescription.delete("0.0", "end")
        self.AddFrame.grid_forget()

        #Drawing on window newsFrame
        self.NewsFrame=ctk.CTkFrame(master=self,bg_color="transparent",fg_color="#343434",)
        self.NewsFrame.grid_columnconfigure(0,weight=2)
        self.NewsFrame.grid_columnconfigure(1,weight=1)
        self.NewsFrame.grid_columnconfigure(2,weight=8)
        self.NewsFrame.grid_columnconfigure(3,weight=1)
        self.NewsFrame.grid_columnconfigure(4,weight=2)
        self.NewsFrame.grid_rowconfigure(0,weight=3)
        self.NewsFrame.grid_rowconfigure(1,weight=1)
        self.NewsFrame.grid_rowconfigure(2,weight=3)

        self.HistoryNewsFrame=ctk.CTkFrame(master=self.NewsFrame,bg_color="transparent",fg_color=self.UnActiveColor)
        self.HistoryNewsFrame.grid(row=0,column=2,rowspan=3,sticky="NSEW",pady=20)
        self.HistoryNewsFrame.grid_rowconfigure(0,weight=0)
        self.HistoryNewsFrame.grid_rowconfigure(1,weight=1)
        self.HistoryNewsFrame.grid_rowconfigure(2,weight=20)
        self.HistoryNewsFrame.grid_rowconfigure(3,weight=1)
        self.HistoryNewsFrame.grid_columnconfigure(0,weight=1)
        self.HistoryNewsFrame.grid_columnconfigure(1,weight=1)

        self.DescriptionNews=ctk.CTkTextbox(master=self.HistoryNewsFrame,corner_radius=0,border_width=3,border_spacing=10,font=("Softie Cyr",30),text_color="white",bg_color=self.color,fg_color=self.SelectedColor)
        self.DescriptionNews.grid(row=2,column=0,columnspan=2,sticky="NSEW",pady=10,padx=10)

        self.DescriptionNews.tag_config("center", justify="center")
        self.DescriptionNews.delete("0.0","end")
        self.DescriptionNews.configure(state="disabled")


        self.DateNews=ctk.CTkTextbox(master=self.HistoryNewsFrame,corner_radius=0,border_width=3,border_spacing=10,font=("Softie Cyr",30),text_color="white",bg_color=self.color,fg_color=self.SelectedColor)
        self.DateNews.grid(row=3,column=0,columnspan=2,sticky="NSEW",pady=10,padx=10)

        self.DateNews.tag_config("center", justify="center")
        self.DateNews.delete("0.0","end")
        self.DateNews.configure(state="disabled")


        self.buttonNewsLeft=ctk.CTkButton(master=self.NewsFrame,text="",border_color=self.SelectedColor,border_width=10,corner_radius=0,bg_color=self.color,font=("Softie Cyr",38),fg_color=self.color,image=self.arrowLeft,hover_color=self.SelectedColor,command=self.LeftNews)
        self.buttonNewsLeft.grid(row=1,column=1,sticky="NSEW",pady=20,padx=(0,10))
        self.buttonNewsRight=ctk.CTkButton(master=self.NewsFrame,text="",border_width=10,border_color=self.SelectedColor,corner_radius=0,bg_color=self.color,font=("Softie Cyr",38),fg_color=self.color,image=self.arrowRight,hover_color=self.SelectedColor,command=self.RightNews)
        self.buttonNewsRight.grid(row=1,column=3,sticky="NSEW",pady=20,padx=(10,0))
        self.NewsData=self.parceNews()

        self.NewsFrame.grid_forget()



    def change_button_color(self,button):
        new_colorBtn = "#FF5733" 

        buttons=[self.button,self.button1,self.button2,self.button3]
        button.configure(fg_color=self.SelectedColor)  
        if(button==self.button):
            self.ShowInfo()
        else:
            self.foget(self.InfoFrame)
        if(button==self.button1):
            self.ShowHome()
        else:
            self.foget(self.HomeFrame)

        if(button==self.button2):
            self.ShowAdd()
        else:
            self.foget(self.AddFrame)

        if(button==self.button3):
            self.ShowNews()
        else:
            self.foget(self.NewsFrame)

        

        for widget in buttons:
            if isinstance(widget, ctk.CTkButton) and widget is not button:
                widget.configure(fg_color=self.color) 

    def ShowInfo(self):
        self.SetConfigureFrame(7,16,7,1,3,1)
        self.InfoFrame.grid(row=0,column=2,padx=20,pady=20,sticky="NSWE",rowspan=3)

    # def BackToHome(self):
    #     self.HistoryFrame.grid(row=0,column=2,rowspan=3,sticky="NSEW",pady=20)
    #     self.CommentsFrame.grid_forget()
    #     self.buttonHomeLeft.grid(row=1,column=1,sticky="NSEW",pady=20,padx=(0,10))
    #     self.buttonHomeRight.grid(row=1,column=3,sticky="NSEW",pady=20,padx=(10,0)) 


    def ShowHome(self):
        self.SetConfigureFrame(1,25,1,1,5,1)
        self.HomeFrame.grid(row=1,column=2,padx=10,sticky="NSWE")
        self.counter=0
        self.arrHistories=self.getHistories(True)

        # self.BackToHome()


        if(len(self.arrHistories)>0):
            self.drawHistory(self.arrHistories[self.counter].header,self.arrHistories[self.counter].description,self.arrHistories[self.counter].date,self.arrHistories[self.counter].login,counter=self.counter)
        
    # def ShowComments(self):
    #     self.HistoryFrame.grid_forget()
    #     self.buttonHomeLeft.grid_forget()
    #     self.buttonHomeRight.grid_forget()
    #     self.CommentsFrame.grid(row=0,column=2,rowspan=3,sticky="NSEW",pady=20)
    #     self.ShowCommentaries()

    def ShowNews(self):
        self.SetConfigureFrame(1,25,1,1,5,1)
        self.NewsFrame.grid(row=1,column=2,padx=10,sticky="NSWE")
        self.drawNews()

    def ShowAdd(self):
        self.SetConfigureFrame(4,16,4,1,10,1)
        self.AddFrame.grid(row=1,column=2,padx=10,sticky="NSWE")





    def foget(self,obj):
        obj.grid_forget()

    def  getTextEntry(self,obj):
        return obj.get()

    def getTextBox(self,obj):
        return obj.get("0.0", "end")
    

        
    def SetConfigureFrame(self,column1,column2,column3,row1,row2,row3):
        self.grid_columnconfigure(1,weight=column1)
        self.grid_columnconfigure(2,weight=column2)
        self.grid_columnconfigure(3,weight=column3)

        self.grid_rowconfigure(0,weight=row1)
        self.grid_rowconfigure(1,weight=row2)
        self.grid_rowconfigure(2,weight=row3)

    def UpdateRegisterValues(self,login,password):
        self.LoginHeader.configure(text="Логин:\n"+login)
        self.wrap_text_based_on_screen(self.PasswordHeader)
        self.PasswordHeader.configure(text="Пароль:\n"+password)

    def setRegister(self):
        isValidLogin=True
        login=self.EntryLogin.get()
        password=self.EntryPassword.get()
        if(login==password or len(login)>8 or len(password)>8 or login.isspace()==True or password.isspace()==True or len(password)<2 or len(login)<2):
            isValidLogin=False
            self.show_error("Проверьте правильность заполнения полей !")
        data=DbHelper.getAllData()
        for i in data:
            for j in i:
                if(login==j):
                    isValidLogin=False
                    self.show_error("Логин уже существует !")
        if(isValidLogin):
            if(self.GetId()==""):
                with open('id.txt', 'w') as f:
                    f.write(str(id(login)))
                DbHelper.add_user(self.GetId())
                self.show_info("Пользователь успешно создан!")
            
            DbHelper.registration(login=login,password=password,id=self.GetId())
            self.UpdateRegisterValues(login=login,password=password)
            self.show_info("Пользователь успешно обновлён!")
        

        
    def GetId(self):
        result=""
        with open('id.txt', 'r') as f:
            for line in f:
                result+=line.strip()
            
        return result
    
    def wrap_text_based_on_screen(self,label):
        current_width = self.LoginHeader.winfo_width()
        text = label.cget("text")
        
        # Определяем максимальную длину строки в пикселях, которая влезет в Label
        max_line_length = current_width // 8  # Примерное значение для длины строки
        
        # Делаем разбиение текста на строки с переносами
        wrapped_text = ""
        current_line_length = 0
        
        for word in text.split(" "):
            if current_line_length + len(word) <= max_line_length:
                wrapped_text += word + " "
                current_line_length += len(word) + 1
            else:
                wrapped_text = wrapped_text.rstrip() + "\n" + word + " "
                current_line_length = len(word) + 1
        
        # Обновляем текст в Label с переносами
        label.configure(text=wrapped_text)
    def imageUploader(self,label):
            fileTypes = [("Image files", "*.png;*.jpg;*.jpeg")]
            path = ctk.filedialog.askopenfilename(filetypes=fileTypes)
        
            # if file is selected
            if len(path):
                img = Image.open(path)
                pic = ctk.CTkImage(img,size=(90,90))
        
                # re-sizing the app window in order to fit picture
                # and buttom
                app.geometry("560x300")
                label.configure(image=pic)
                label.image = pic    
            # if no file is selected, then we are displaying below message
            else:
                print("No file is Choosen !! Please choose a file.")
    
    def writeHistoryToDb(self,textHeader,textDescription):
        date=datetime.now()
        dateTxt=f"{date.year}:{date.month}:{date.day}"
        isValidHistory=True
        if(self.GetId()!=""):
            if(textHeader=="" or textDescription=="\n" or self.remove_newlines_from_end(textDescription)=="" or len(self.remove_newlines_from_end(textDescription))<10 or len(self.remove_newlines_from_end(textHeader))<5):
                isValidHistory=False
            if(isValidHistory):
                self.EntryHeader.delete("0","end")
                self.EntryDescription.delete("0.0", "end")
                DbHelper.history(textHeader,textDescription,dateTxt,self.GetId())
                self.show_info("История успешно создана!")

            else:
                self.show_error("Поля не должны быть пустые или в них мало символов !")
        else:
            self.show_error("Вы ещё не зарегистрированы !")
    
    def show_error(self,str):
    # Show some error message
        CTkMessagebox(title="Error", message=str, icon="cancel")

    def show_info(self,str):
    # Default messagebox for showing some information
        CTkMessagebox(message=str,icon="check")
    def getAllHeaders(self):
        date=DbHelper.getAllData()
        headers=[]

        for i in date:
            if(i[3]!=None):
                for j in i[3]:
                    headers.insert(0,j)
        return headers
    

    
    def getAllDescriptions(self):
        date=DbHelper.getAllData()
        descriptions=[]
        for i in date:
            if(i[4]!=None):
                for j in i[4]:
                    descriptions.insert(0,j)
        return descriptions
    def getAllDates(self):
        date=DbHelper.getAllData()
        dates=[]
        for i in date:
            if(i[3]!=None):
                for j in i[5]:
                    dates.insert(0,j)
        return dates
    def getAllLogins(self):
        data=DbHelper.getAllData()
        logins=[]
        for i in data:
            if(i[3]!=None):
                for j in i[4]:
                    logins.insert(0,i[1])
        return logins
    
    # def getAllComments(self):
    #     commentsHistoies=[]
    #     data=DbHelper.getAllData()
    #     for i in data:
    #         if(i[6]!=None):
    #             for j in i[6]:
    #                 commentsHistoies.append(j)
    #                 print(j)
    #     comments=commentsHistoies[self.counter].split("\n")


    def getHistories(self,isShuffle):
        logins=self.getAllLogins()
        headers=self.getAllHeaders()
        descriptions=self.getAllDescriptions()
        dates=self.getAllDates()
        data=[]
        for i in range(0,len(headers)):
            data.append(history(login=logins[i],header=headers[i],description=descriptions[i],date=dates[i]))
        # if(isShuffle==True):
        #     shuffle(data)
        return data



    def drawHistory(self,headers,descriptions,dates,logins,counter):
        self.Header.configure(state="normal")
        self.Header.tag_config("center", justify="center")
        self.Header.delete("0.0","end")
        self.Header.insert("0.0", f"{headers}","center")
        self.Header.configure(state="disabled")

        self.Description.configure(state="normal")
        self.Description.tag_config("center", justify="center")
        self.Description.delete("0.0","end")
        self.Description.insert("0.0", f"Описание:{descriptions}","center")
        self.Description.configure(state="disabled")
        self.Date.configure(state="normal")
        self.Date.tag_config("center", justify="center")
        self.Date.delete("0.0","end")
        self.Date.insert("0.0", f"Дата записи:{dates}","center")
        self.Date.configure(state="disabled")
        self.Login.configure(state="normal")
        self.Login.tag_config("center", justify="center")
        self.Login.delete("0.0","end")
        self.Login.insert("0.0", f"Пользователь:{logins}","center")
        self.Login.configure(state="disabled")

    def drawNews(self):
        data=self.NewsData
        self.DescriptionNews.configure(state="normal")
        self.DescriptionNews.tag_config("center", justify="center")
        self.DescriptionNews.delete("0.0","end")
        self.DescriptionNews.insert("0.0", f"Описание:{data[self.NewsCounter].header}","center")
        self.DescriptionNews.configure(state="disabled")
        self.DateNews.configure(state="normal")
        self.DateNews.tag_config("center", justify="center")
        self.DateNews.delete("0.0","end")
        self.DateNews.insert("0.0", f"Дата записи:{data[self.NewsCounter].date}","center")
        self.DateNews.configure(state="disabled")



    def Left(self,counter,arr):
        if(counter>0):
            self.counter-=1
            data=arr[self.counter]
            self.drawHistory(data.header,data.description,data.date,data.login,counter=self.counter)
    def Right(self,counter,headers,arr):
        if(counter<len(headers)-1):
            self.counter+=1
            data=arr[self.counter]
            self.drawHistory(data.header,data.description,data.date,data.login,counter=self.counter)

    def remove_newlines_from_end(self,text):
        while text.endswith('\n'):
            text = text.rstrip('\n')
        return text
    
    def LeftNews(self):
        if(self.NewsCounter>0):
            self.NewsCounter-=1
            self.drawNews()
    def RightNews(self):
        if(self.NewsCounter<len(self.NewsData)-2):
            self.NewsCounter+=1
            self.drawNews()

    

    def parceNews(self):
        response=requests.get("https://ria.ru/chess/?ysclid=luqilqdhmv954280551")
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        items=soup.find_all("div",class_="list-item")
        newsArray=[]
        for data in items:
            header=data.find('div', class_='list-item__content').find('a', class_='list-item__title color-font-hover-only')
            dates=data.find('div', class_='list-item__info').find('div', class_='list-item__date') 
            newsArray.append(News(header.text,dates.text))

        return newsArray
    
    # def SetComment(self):
    #     id=self.GetId()
    #     if(len(id)>0):
    #         myLogin=self.LoginHeader.cget("text")
    #         login=myLogin.split("\n")
    #         comment=self.getTextEntry(self.EntryComment)+f"  from:{login[1]}"+"\n"
    #         if(comment!="\n"):
    #             data=DbHelper.getAllData()
    #             comments=""
    #             for i in data:
    #                 if(i[6]!=None):
    #                     for j in i[6]:
    #                         comments+=j+"\n"
    #             c=comment+comments
    #             DbHelper.WriteComment(c,self.counter,id)
    #             self.show_info("Коментарий успешно добавлен!")
    #             self.ShowCommentaries()
            
    #         else:
    #             self.show_error("Коментарий не должен быть пустой!")
    #     else:
    #         self.show_error("Вы ещё не зарегистрированы!")

    # def ShowCommentaries(self):
    #     data=DbHelper.getAllData()
    #     comments=self.getAllComments()

    #     for comment in range(0,len(comments)-1):
    #         if(comments[comment]!=""):
    #             self.comment=ctk.CTkTextbox(master=self.ComentsScroll,bg_color="transparent",fg_color=self.UnActiveColor,border_color=self.SelectedColor,border_width=10,corner_radius=0,border_spacing=10,font=("Softie Cyr",34),text_color="white")
    #             self.comment.configure(state="normal")
    #             self.comment.tag_config("center", justify="center")
    #             self.comment.delete("0.0","end")
    #             self.comment.insert("0.0",comments[comment],"center")
    #             self.comment.configure(state="disabled")
    #             self.comment.grid(row=comment,column=0,padx=10,pady=10,sticky="NSEW")










app=MainApp()
app.grid_rowconfigure(0,weight=1)
app.grid_columnconfigure(0,weight=1)
app.grid_columnconfigure(1,weight=8)
app.grid_columnconfigure(2,weight=14)
app.grid_columnconfigure(3,weight=8)


app.after(0, lambda:app.state('zoomed'))
if __name__ == '__main__':
    app.mainloop()
    print("xxx")
