from random import *
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter import *
from pymysql import *
import cv2
import numpy
import re
from PIL import Image, ImageFont, ImageDraw, ImageTk
import textwrap

try:
    from Tkinter import Label
except ImportError:
    from tkinter import Label
    
def truetype_font(font_path, size):
    return ImageFont.truetype(font_path, size)

class CustomFont_Label(Label):
    def __init__(self, master, text, foreground="black", truetype_font=None, font_path=None, family=None, size=None, **kwargs):   
        if truetype_font is None:
            if font_path is None:
                raise ValueError("Font path can't be None")
                
            # Initialize font
            truetype_font = ImageFont.truetype(font_path, size)
        
        width, height = truetype_font.getsize(text)

        image = Image.new("RGBA", (width, height), color=(0,0,0,0))
        draw = ImageDraw.Draw(image)

        draw.text((0, 0), text, font=truetype_font, fill=foreground)
        
        self._photoimage = ImageTk.PhotoImage(image)
        Label.__init__(self, master, image=self._photoimage, **kwargs)


class CustomFont_Message(Label):
    def __init__(self, master, text, width, foreground="black", truetype_font=None, font_path=None, family=None, size=None, **kwargs):   
        if truetype_font is None:
            if font_path is None:
                raise ValueError("Font path can't be None")
                
            
            truetype_font = ImageFont.truetype(font_path, size)
    
        lines = textwrap.wrap(text, width=width)

        width = 0
        height = 0
        
        line_heights = []
        for line in lines:
            line_width, line_height = truetype_font.getsize(line)
            line_heights.append(line_height)
            
            width = max(width, line_width)
            height += line_height

        image = Image.new("RGBA", (width, height), color=(0,0,0,0))
        draw = ImageDraw.Draw(image)

        y_text = 0
        for i, line in enumerate(lines):
            draw.text((0, y_text), line, font=truetype_font, fill=foreground)
            y_text += line_heights[i]

        self._photoimage = ImageTk.PhotoImage(image)
        Label.__init__(self, master, image=self._photoimage, **kwargs)
def clear():
	destroy_list=frame.grid_slaves()
	for i in destroy_list:
		i.destroy()
def login():
	name=entered_name.get()
	password=entered_pass.get()
	if(check_login(name,password)):
		mainpage()
def check_login(name,password):
	status=Label(  frame,text="").grid(row=0,column=3,padx=10,pady=10)
	status=Label(  frame,text="").grid(row=1,column=3,padx=10,pady=10)
	status=Label(  frame,text="").grid(row=3,column=1,padx=10,pady=10)
	status=Label(  frame,text="").grid(row=3,column=0,padx=10,pady=10)
	if(name=="" or password==""):
		if(name==""):
			start()
			status=Label(frame,text="Name field cannot be empty").grid(row=0,column=3,padx=10,pady=10)
			return False
			
		if(password==""):
			start()
			status=Label(frame,text="Password field cannot be empty").grid(row=1,column=3,padx=10,pady=10)
			return False
			
	else:

		lower_name=name.lower()
		try:
			sql=('select * from id where email="%s" OR email="%s" OR username="%s"' %(lower_name,name,name))
			cursor.execute(sql)
			result=cursor.fetchone()
			if(password == result[3]):
				
				
				status=Label(  frame,text="Login Successful").grid(row=3,column=0,padx=10,pady=10,columnspan=3)
				
				return True
			else :
				start()
				status=Label(  frame,text="Invalid details").grid(row=3,column=0,padx=10,pady=10,columnspan=3)
				return False
				
		except Exception as e:
			start()
			
			status=Label(  frame,text="Email or Username is not registered").grid(row=0,column=3,padx=10,pady=10)
			return False
def signup():
	clear()
	textforshowbutton.set("Show")
	back_button=Button(frame,text="Back To Login Page",command=back,relief="solid").grid(row=5,column=0,padx=10,pady=10)
	name_label=CustomFont_Label( frame,text="Name",font_path="C:\Windows\Fonts\BebasNeue-Regular.otf",size=22).grid(row=1,column=0,padx=10,pady=10)
	username_label=CustomFont_Label(  frame,text="Username",font_path="C:\Windows\Fonts\BebasNeue-Regular.otf",size=22).grid(row=2,column=0,padx=10,pady=10)
	email_label=CustomFont_Label(  frame,text="Email",font_path="C:\Windows\Fonts\BebasNeue-Regular.otf",size=22).grid(row=3,column=0,padx=10,pady=10)
	password_label=CustomFont_Label(  frame,text="Password",font_path="C:\Windows\Fonts\BebasNeue-Regular.otf",size=22).grid(row=4,column=0,padx=10,pady=10)
	name_entry=Entry(  frame,textvariable=entered_name).grid(row=1,column=1,padx=10,pady=10)
	username_entry=Entry(  frame,textvariable=entered_user).grid(row=2,column=1,padx=10,pady=10)
	email_entry=Entry(  frame,textvariable=entered_email).grid(row=3,column=1,padx=10,pady=10)
	create_account=Button(  frame,text="Create my account!",command= create,relief="solid").grid(row=5,column=1,padx=10,pady=10)
	show=Button(  frame,textvariable=textforshowbutton,command= show_signup,relief="solid").grid(row=4,column=2,padx=10,pady=10)
	password_entry=Entry( frame,textvariable=entered_pass,show="%s"%text).grid(row=4,column=1,padx=10,pady=10)
	entered_name.set('')
	entered_pass.set('')
	entered_email.set('')
	entered_user.set('')
def show_login( ):
	if(textforshowbutton.get()=="Hide"):
		text='*'
		textforshowbutton.set("Show")
		password_entry=Entry(  frame,textvariable=entered_pass,show="%s"%text).grid(row=1,column=1,padx=10,pady=10)
	elif(textforshowbutton.get()=="Show"):
		text=''
		entered_pass.set(entered_pass.get())
		password_entry=Entry(  frame,textvariable=entered_pass,show="%s"%text).grid(row=1,column=1,padx=10,pady=10)
		textforshowbutton.set("Hide")   
def show_signup( ):
	if(textforshowbutton.get()=="Hide"):
		text='*'
		textforshowbutton.set("Show")
		password_entry=Entry(  frame,textvariable=entered_pass,show="%s"%text).grid(row=4,column=1,padx=10,pady=10)
	elif(textforshowbutton.get()=="Show"):
		text=''
		entered_pass.set(entered_pass.get())
		password_entry=Entry(  frame,textvariable=entered_pass,show="%s"%text).grid(row=4 ,column=1,padx=10,pady=10)
		textforshowbutton.set("Hide")
def create( ):
	name=entered_name.get()
	user=entered_user.get()
	email=entered_email.get()
	password=entered_pass.get()
	if(check_name(name)):
		if(check_username(user)):
			if(check_email(email)):
				if(check_password(password)):
					 
					status=Label(   frame,text="Account has been created!").grid(row=5,column=1,padx=10,pady=10)
					sql=("INSERT INTO id(name,username,email,password) VALUES('%s','%s','%s','%s')" %(name,user,email,password))
					cursor.execute(sql)
					connection.commit()
	
def check_name(name):
	
	status=Label(frame,text="",bg=mycolor).grid(row=1,column=2,padx=10,pady=10)
	
	if(name==""):
		 
		status=Label(   frame,text="Name field is empty").grid(row=1,column=2,padx=10,pady=10)
		return False
	if re.search(r'\d', name):
		 
		status=Label(   frame,text="Name cannot consist of digits").grid(row=1,column=2,padx=10,pady=10)
		return False
	if re.match("^[a-zA-Z]*$", name):
		return True
	else:
		 
		status=Label(   frame,text="Name cannot consist of special characters").grid(row=1,column=2,padx=10,pady=10)
		return False
def check_username(username):
	
	status=Label(   frame,text="",bg=mycolor).grid(row=1,column=2,padx=10,pady=10)
	
	if(username==""):
		 
		status=Label(   frame,text="Username field is empty").grid(row=2,column=2,padx=10,pady=10)
		return False
	if " "  in username:
		 
		status=Label(   frame,text="Username cannot consist of spaces").grid(row=2,column=2,padx=10,pady=10)
		return False
	try:
		sql=('select * from id where username="%s"' %(username))
		cursor.execute(sql)
		result=cursor.fetchone()
		if(username==result[1]):
			 
			status=Label(   frame,text="Username already exists!").grid(row=2,column=2,padx=10,pady=10)
			return False
	except:
		return True
	return True
def check_email(email):
	
	status=Label(   frame,text="",bg=mycolor).grid(row=1,column=2,padx=10,pady=10)

	
	if(email==""):
		status=Label(   frame,text="Email field is empty").grid(row=3,column=2,padx=10,pady=10)
		return False
	try:
		sql=('select * from id where email="%s"' %(email))
		cursor.execute(sql)
		result=cursor.fetchone()
		if(re.findall(r'[\w\.-]+@[\w\.-]+(\.[\w]+)+',email)):
			return True
		else:
		 
			status=Label(   frame,text="Email format is invalid").grid(row=3,column=2,padx=10,pady=10)
			return False
		if(email==result[2]):
			 
			status=Label(   frame,text="Email already exists!").grid(row=3,column=2,padx=10,pady=10)
			return False
	except:
		return True
	
def check_password(password):
	
	status=Label(   frame,text="",bg=mycolor).grid(row=1,column=2,padx=10,pady=10)
	
	if(password==""):
		 
		status=Label(   frame,text="Password field is empty").grid(row=4,column=3,padx=10,pady=10)
	if re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', password):
		return True
	else:
		 
		status=Label(   frame,text="Password format is invalid").grid(row=4,column=3,padx=10,pady=10)
		return False
def start():
	clear()
	CustomFont_Label(frame,text="Username or Email",font_path="C:\Windows\Fonts\BebasNeue-Regular.otf", size=22).grid(row=0,column=0,padx=10,pady=10)
	CustomFont_Label(frame,text="Password",font_path="C:\Windows\Fonts\BebasNeue-Regular.otf", size=22).grid(row=1,column=0,padx=10,pady=10)
	username_entry=Entry(frame,textvariable=entered_name).grid(row=0,column=1,padx=10,pady=10)
	show=Button(frame,textvariable=textforshowbutton,command= show_login,relief="solid").grid(row=1,column=2,padx=10,pady=10)
	password_entry=Entry(frame ,textvariable=entered_pass,show="%s"%text).grid(row=1,column=1,padx=10,pady=10)
	login_button=Button(frame,text="Login",command= login,relief="solid").grid(row=2,column=0,padx=10,pady=10,ipadx=20,ipady=2)
	
	signup_button=Button(frame,text="Sign Up",command= signup,relief="solid").grid(row=2,column=1,padx=10,pady=10,ipady=2,ipadx=20)
def back( ):
	entered_name.set('')
	entered_pass.set('')
	entered_email.set('')
	entered_user.set('')
	start()
def mainpage():
	clear()
	scrollbar.grid(row=0,column=4,padx=10,pady=10,sticky=N+S+E)
	msg_list.grid(row=0,column=1,padx=10,pady=10)
	entry_field =Entry(frame, textvariable=my_msg,width=100)
	entry_field.bind("<Return>", send)
	entry_field.grid(row=5,column=1,padx=10,pady=10)
	send_button = Button(frame, text="Send", command=send,relief="solid").grid(row=5,column=0,padx=10,pady=10)
	logout=Button(frame,text="Logout",command=back,relief="solid").grid(row=0,column=5,padx=10,pady=10,sticky=N)
def receive():
	while True:
		try:
			msg = client_socket.recv(BUFSIZ).decode("utf8")
			msg_list.insert(END, msg)
			file.write(msg+"\n")
		except OSError:  # Possibly client has left the chat.
			break
def send(event=None):  
	msg = my_msg.get()
	my_msg.set("")  # Clears input field.
	msg_list.yview(END)
	msg_list.see(END)

	client_socket.send(bytes(msg, "utf8"))
	'''msg_list.yview(END)
				msg_list.see(END)'''

	if msg == "{quit}":
		client_socket.close()
		top.quit()
def on_closing(event=None):
	my_msg.set("{quit}")
	send()
if __name__ == "__main__":
	top = Tk()
	top.title("Chat App")
	height_screen=top.winfo_screenheight()
	width_screen=top.winfo_screenwidth()
	width_frame=900
	height_frame=500
	x=width_screen/2-width_frame/2
	y=height_screen/2-height_frame/2
	top.resizable(False, False)
	top.geometry("%dx%d+%d+%d" %(width_frame,height_frame,x,y))
	z=choice(range(1,13))
	s='background'+str(z)+'.gif'
	p='background'+str(z)+'.jpeg'
	filename = PhotoImage(file = s)
	background_label = Label(top, image=filename).grid()
			
		

	connection=connect(host="localhost",user="root",passwd='',db='mainDataList')
	cursor=connection.cursor()
	client_socket = socket(AF_INET, SOCK_STREAM)
	entered_name=StringVar()
	entered_user=StringVar()
	entered_email=StringVar()
	entered_pass=StringVar()
	textforshowbutton=StringVar()
	textforshowbutton.set("Show")
	text='*'

	my_msg =  StringVar()
	my_msg.set("")
	title=CustomFont_Label(top,text="Chat App",font_path="C:\Windows\Fonts\BebasNeue-Regular.otf", size=40)

	frame=Frame(background_label,highlightbackground="black", highlightcolor="black", highlightthickness=3, width=100, height=100, bd= 0)
	scrollbar=Scrollbar(frame) 
	msg_list=Listbox(frame, height=20, width=100)
	msg_list['yscrollcommand']=scrollbar.set
	scrollbar['command']=msg_list.yview

	
	fi=open("ChatList.txt","r") 
	for i in fi: 
		msg_list.insert(END,i)
	f=open("ChatList.txt")
	s=f.read()
	file=open("ChatList.txt","w")
	file.write(s)

	HOST = "localhost"
	PORT = 33000

	BUFSIZ = 1024
	ADDR = (HOST, PORT)
	client_socket = socket(AF_INET, SOCK_STREAM)
	client_socket.connect(ADDR)
	receive_thread = Thread(target=receive)
	receive_thread.start()
	
	myimg = cv2.imread(p)
	avg_color_per_row = numpy.average(myimg, axis=0)
	avg_color = numpy.average(avg_color_per_row, axis=0)
	mycolor = '#%02x%02x%02x' % (int(avg_color[2]), int(avg_color[1]), int(avg_color[0]))
	frame.configure(background=mycolor)

	frame.place( anchor="c", relx=.5, rely=.5)

	start()
	top.mainloop() 
	file.close()
