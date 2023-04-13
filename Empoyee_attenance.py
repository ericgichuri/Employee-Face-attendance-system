from tkinter import *
import numpy as np
import cv2 as cv
import time,os
import mysql.connector
from tkinter import ttk,messagebox
from PIL import Image,ImageTk

win=Tk()
# defined width and height

# screen width
screen_w=win.winfo_screenwidth()
screen_h=win.winfo_screenheight()

# screen height
win_width=1100
win_height=600

# coordinates
x_cord=(screen_w-win_width)//2
y_cord=(screen_h-win_height)//2

# geometry
win.geometry("%dx%d+%d+%d"%(win_width,win_height,x_cord,y_cord))
win.title("Employee Attendance")

# fonts
font_title=("times",15,"bold")
fomt_button=("times",12)
font_label=("times",12)
font_entry=("times",11)

# colors
col_cyan="#d5d5c3"
col_black="#000000"
col_white="#FFFFFF"

# defined width
button_width=15
button_height=2
label_width=10
entry_width=25
btn_width2=8

#check available folders
cur_folder=os.getcwd()
images_folder=f'{cur_folder}\\Employee_images'
if not os.path.exists(images_folder):
	os.makedirs(images_folder)


#----create database and tables
database_name="Employee_attendance"
conn=mysql.connector.connect(host="localhost",user="root",password="")
try:
	cursor=conn.cursor()
	sql="CREATE DATABASE IF NOT EXISTS %s"%(database_name)
	cursor.execute(sql)
	conn.commit()
except Exception as e:
	conn.rollback()
	messagebox.showerror("Error",str(e))
conn=mysql.connector.connect(host="localhost",user="root",password="",database=database_name)
def func_db_functions():
	try:
		cursor=conn.cursor()
		sql="""CREATE TABLE IF NOT EXISTS employee(
			empid int NOT NULL AUTO_INCREMENT,
			employee_name varchar(60) NOT NULL,
			empno varchar(10) NOT NULL,
			phoneno varchar(20) NOT NULL,
			email varchar(50) NOT NULL,
			idno varchar(20) NOT NULL,
			profession varchar(30) NOT NULL,
			salary double NOT NULL,
			PRIMARY KEY(empid),
			UNIQUE KEY(phoneno),
			UNIQUE KEY(email),
			UNIQUE KEY(idno),
			UNIQUE KEY(empno)
		)"""
		cursor.execute(sql)
		conn.commit()
	except Exception as e:
		messagebox.showerror("Error",str(e))


# call function db function
func_db_functions()

# theme
style=ttk.Style()
style.theme_use('clam')

# functions on side bar
def func_toaddEmployee():
	notebook1.select(0)
def func_toviewEmployee():
	notebook1.select(1)
def func_toEmployeeAttendance():
	notebook1.select(2)

# defined files
face_classifier=cv.CascadeClassifier("haarcascade_frontalface_default.xml")

# place objects
lbl_title=Label(win,text="Employee Attendance System",font=font_title,bg=col_cyan,fg=col_black,height=2)
lbl_title.pack(side=TOP,fill=X)

# side bar
frame_sidebar=Frame(win,bg=col_cyan)
frame_sidebar.pack(side=LEFT,fill=Y)

lbl=Label(frame_sidebar,text="Menu",font=font_title,fg=col_black,bg=col_cyan)
lbl.pack(side=TOP,pady=10)
btn_AddEmployee=Button(frame_sidebar,text="Add Employee",width=button_width,height=button_height,border=0,bg=col_black,fg=col_cyan,activebackground=col_black,activeforeground=col_cyan,cursor="hand2",command=func_toaddEmployee)
btn_AddEmployee.pack(side=TOP,pady=10,padx=20)
btn_ViewEmployee=Button(frame_sidebar,text="View Employee",width=button_width,height=button_height,border=0,bg=col_black,fg=col_cyan,activebackground=col_black,activeforeground=col_cyan,cursor="hand2",command=func_toviewEmployee)
btn_ViewEmployee.pack(side=TOP,pady=10,padx=20)
btn_EmployeeAttendance=Button(frame_sidebar,text="Attendance",width=button_width,height=button_height,border=0,bg=col_black,fg=col_cyan,activebackground=col_black,activeforeground=col_cyan,cursor="hand2",command=func_toEmployeeAttendance)
btn_EmployeeAttendance.pack(side=TOP,pady=10,padx=20)

# main container
frame_mainholder=Frame(win,bg=col_white)
frame_mainholder.pack(side=LEFT,fill=BOTH,expand=True)

notebook1=ttk.Notebook(frame_mainholder)
notebook1.pack(side=TOP,fill=BOTH,expand=True)

frame_AddEmployee=Frame(notebook1,bg=col_white)
frame_AddEmployee.place(x=0,y=0,relwidth=1,relheight=1)
frame_ViewEmployee=Frame(notebook1,bg=col_white)
frame_ViewEmployee.place(x=0,y=0,relwidth=1,relheight=1)
frame_EmployeeAttendance=Frame(notebook1,bg=col_white)
frame_EmployeeAttendance.place(x=0,y=0,relwidth=1,relheight=1)
notebook1.add(frame_AddEmployee,text="Add Employee")
notebook1.add(frame_ViewEmployee,text="View Employee")
notebook1.add(frame_EmployeeAttendance,text="Attendance")

# add employee

# function open camera
def func_open_camera():
	global cap,camera_image
	try:
		cap=cv.VideoCapture(0)
		while True:
			ret,frame=cap.read()
			if ret:
				camera_image=cv.cvtColor(frame,cv.COLOR_BGR2RGB)
				img=cv.cvtColor(frame,cv.COLOR_BGR2RGB)
				#camera_image=img
				gray_img=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
				face_rect=face_classifier.detectMultiScale(gray_img,1.1,10)
				for (x,y,w,h) in face_rect:
					cv.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
					func_capture_photos()
				img=Image.fromarray(img)
				img=img.resize((500,400))
				img=ImageTk.PhotoImage(img)
				#cv.imshow("Image",frame)
				lbl_camera.configure(text="",image=img)
				
				win.update()
			else:
				break
		cap.release()
		cv.destroyAllWindows()
	except Exception as e:
		messagebox.showerror("Error",str(e))
# function off camera
def func_close_camera():
	try:
		global cap
		cap.release()
		cv.destroyAllWindows()
		lbl_camera.configure(text="Camera Image",image="")
	except:
		pass
	
# function to save employee
def func_save_employee():
	if txt_EmpName.get()=="" or txt_EmpNo.get()=="" or txt_EmpPhoneno.get()=="" or txt_EmpEmail.get()=="" or txt_EmpIDNo.get()=="" or txt_EmpProfession.get()=="" or txt_EmpSalary.get()=="":
		messagebox.showerror("Warning","Every field must be filled")
	else:
		try:
			cursor=conn.cursor()
			sql="INSERT INTO employee(employee_name,empno,phoneno,email,idno,profession,salary) VALUES('%s','%s','%s','%s','%s','%s','%s')"
			values=(txt_EmpName.get(),txt_EmpNo.get(),txt_EmpPhoneno.get(),txt_EmpEmail.get(),txt_EmpIDNo.get(),txt_EmpProfession.get(),txt_EmpSalary.get())
			cursor.execute(sql%values)
			conn.commit()
			messagebox.showinfo("Success","Employee data saved succcesfully")
			func_viewemployees()
			func_clear_form()
		except Exception as e:
			conn.rollback()
			messagebox.showerror("Error",str(e))
def func_clear_form():
	txt_EmpName.delete(0,END)
	txt_EmpNo.delete(0,END)
	txt_EmpPhoneno.delete(0,END)
	txt_EmpEmail.delete(0,END)
	txt_EmpIDNo.delete(0,END)
	txt_EmpProfession.delete(0,END)
	txt_EmpSalary.delete(0,END)

def func_capture_photos():
	global camera_image
	if txt_EmpNo.get()=="":
		func_close_camera()
	else:
		Temployee_folder=f'{images_folder}'+"\\"+txt_EmpNo.get()
		if not os.path.exists(Temployee_folder):
			os.makedirs(Temployee_folder)
		else:
			pass
		rename_profile_pic=f'{Temployee_folder}'+"\\profile.png"
		if not os.path.exists(rename_profile_pic):
			image=Image.fromarray(camera_image)
			image.save(rename_profile_pic)
		else:
			photo_rename=time.strftime("%Y%m%d%H%M%S")+".png"
			image=Image.fromarray(camera_image)
			image.save(Temployee_folder+"\\"+photo_rename)
		
def train_images():
	employees=[]
	DIR=f'{os.getcwd()}\\Employee_images\\'
	for i in os.listdir(DIR):
	    employees.append(i)

	face_cascade=cv.CascadeClassifier('haarcascade_frontalface_default.xml')

	features=[]
	labels=[]

	def create_train():
	    for employee in employees:
	        path=os.path.join(DIR,employee)
	        label=employees.index(employee)
	        for img in os.listdir(path):
	            #get each student photo
	            img_path=os.path.join(path,img)
	            #read images
	            img_array=cv.imread(img_path)
	            #gray image
	            gray_img=cv.cvtColor(img_array,cv.COLOR_BGR2GRAY)
	            #detect face from an image
	            face_rect=face_cascade.detectMultiScale(gray_img,1.1,10)
	            #get region of interest ROI
	            for (x,y,w,h) in face_rect:
	                face_roi=gray_img[y:y+h,x:x+w]
	                features.append(face_roi)
	                labels.append(label)

	try:
	    create_train()
	except Exception as e:
	    messagebox.showerror("Error",str(e))
	#convert features to array
	def save_trains():
	    feature=np.array(features,dtype='object')
	    labelss=np.array(labels)

	    face_recognizer=cv.face.LBPHFaceRecognizer_create()
	    face_recognizer.train(feature,labelss)
	    face_recognizer.save('faces_trained.yml')
	    np.save('features.npy',feature)
	    np.save("labels.npy",labelss)

	try:
	    save_trains()
	    messagebox.showinfo("Success","Training done")
	except Exception as e:
	    messagebox.showerror("Error",str(e))
	    
# place objects on the frame add employee
lbl=Label(frame_AddEmployee,text="Add Employee",font=font_title,fg=col_black)
lbl.pack(side=TOP,fill=X)
frame_formadd_Emp=LabelFrame(frame_AddEmployee,text="Form Add Employee")
frame_formadd_Emp.pack(side=LEFT,fill=BOTH,expand=True)
lbl=Label(frame_formadd_Emp,text="Name: ",width=label_width,font=font_label,justify=RIGHT,anchor=E)
lbl.grid(column=0,row=0,padx=5,pady=10)
txt_EmpName=Entry(frame_formadd_Emp,width=entry_width,border=2,font=font_entry)
txt_EmpName.grid(column=1,row=0,padx=5,pady=10)
lbl=Label(frame_formadd_Emp,text="Employee No: ",width=label_width,font=font_label,justify=RIGHT,anchor=E)
lbl.grid(column=0,row=1,padx=5,pady=10)
txt_EmpNo=Entry(frame_formadd_Emp,width=entry_width,border=2,font=font_entry)
txt_EmpNo.grid(column=1,row=1,padx=5,pady=10)
lbl=Label(frame_formadd_Emp,text="Phone No: ",width=label_width,font=font_label,justify=RIGHT,anchor=E)
lbl.grid(column=0,row=2,padx=5,pady=10)
txt_EmpPhoneno=Entry(frame_formadd_Emp,width=entry_width,border=2,font=font_entry)
txt_EmpPhoneno.grid(column=1,row=2,padx=5,pady=10)
lbl=Label(frame_formadd_Emp,text="Email: ",width=label_width,font=font_label,justify=RIGHT,anchor=E)
lbl.grid(column=0,row=3,padx=5,pady=10)
txt_EmpEmail=Entry(frame_formadd_Emp,width=entry_width,border=2,font=font_entry)
txt_EmpEmail.grid(column=1,row=3,padx=5,pady=10)
lbl=Label(frame_formadd_Emp,text="ID No: ",width=label_width,font=font_label,justify=RIGHT,anchor=E)
lbl.grid(column=0,row=4,padx=5,pady=10)
txt_EmpIDNo=Entry(frame_formadd_Emp,width=entry_width,border=2,font=font_entry)
txt_EmpIDNo.grid(column=1,row=4,padx=5,pady=10)
lbl=Label(frame_formadd_Emp,text="Profession: ",width=label_width,font=font_label,justify=RIGHT,anchor=E)
lbl.grid(column=0,row=5,padx=5,pady=10)
txt_EmpProfession=Entry(frame_formadd_Emp,width=entry_width,border=2,font=font_entry)
txt_EmpProfession.grid(column=1,row=5,padx=5,pady=10)
lbl=Label(frame_formadd_Emp,text="Salary: ",width=label_width,font=font_label,justify=RIGHT,anchor=E)
lbl.grid(column=0,row=6,padx=5,pady=10)
txt_EmpSalary=Entry(frame_formadd_Emp,width=entry_width,border=2,font=font_entry)
txt_EmpSalary.grid(column=1,row=6,padx=5,pady=10)

btn_saveEmployee=Button(frame_formadd_Emp,text="Save",width=button_width,border=0,bg=col_cyan,fg=col_black,font=fomt_button,cursor="hand2",activebackground=col_cyan,activeforeground=col_black,command=func_save_employee)
btn_saveEmployee.grid(column=1,row=7,padx=5,pady=(15,5))
btn_saveClearForm=Button(frame_formadd_Emp,text="Clear",width=button_width,border=0,bg=col_black,fg=col_white,font=fomt_button,cursor="hand2",activebackground=col_black,activeforeground=col_white,command=func_clear_form)
btn_saveClearForm.grid(column=1,row=8,padx=5,pady=(5,10))

frame_capture_Emp_photo=LabelFrame(frame_AddEmployee,text="Capture Employee Photo")
frame_capture_Emp_photo.pack(side=LEFT,fill=BOTH,expand=True)
lbl_camera=Label(frame_capture_Emp_photo,text="Camera Image",font=font_label,image="")
lbl_camera.pack(side=TOP,fill=BOTH,expand=True)
frame_camera_operation=Frame(frame_capture_Emp_photo)
frame_camera_operation.pack(side=TOP)
btn_ON_camera=Button(frame_camera_operation,text="ON",width=btn_width2,border=1,cursor="hand2",fg=col_black,bg=col_cyan,activeforeground=col_black,activebackground=col_cyan,command=func_open_camera)
btn_ON_camera.grid(column=0,row=0,padx=4,pady=5)
btn_CAPTURE_Image=Button(frame_camera_operation,text="Capture",width=btn_width2,border=1,cursor="hand2",fg=col_black,bg=col_cyan,activeforeground=col_black,activebackground=col_cyan,command=func_capture_photos)
btn_CAPTURE_Image.grid(column=1,row=0,padx=4,pady=5)
btn_OFF_camera=Button(frame_camera_operation,text="OFF",width=btn_width2,border=1,cursor="hand2",fg=col_black,bg=col_cyan,activeforeground=col_black,activebackground=col_cyan,command=func_close_camera)
btn_OFF_camera.grid(column=2,row=0,padx=4,pady=5)
btn_trainimages=Button(frame_camera_operation,text="Train",width=btn_width2,border=1,cursor="hand2",fg=col_black,bg=col_cyan,activeforeground=col_black,activebackground=col_cyan,command=train_images)
btn_trainimages.grid(column=3,row=0,padx=4,pady=5)

# view employee
def func_viewemployees():
	try:
		cursor=conn.cursor()
		sql="SELECT * FROM employee"
		cursor.execute(sql)
		results=cursor.fetchall()
		if results:
			for records in table_employee.get_children():
				table_employee.delete(records)
			for i in results:
				table_employee.insert('',END,values=i)
	except Exception as e:
		messagebox.showerror("Error",str(e))
# place objects on the frame view employee
lbl=Label(frame_ViewEmployee,text="View Employee",font=font_title,fg=col_black)
lbl.pack(side=TOP,fill=X)
table_employee=ttk.Treeview(frame_ViewEmployee)
table_employee.pack(side=LEFT,fill=BOTH,expand=True)
scroll_tableviewemployee=Scrollbar(frame_ViewEmployee,command=table_employee.yview)
scroll_tableviewemployee.pack(side=LEFT,fill=Y)
table_employee.configure(yscrollcommand=scroll_tableviewemployee.set)
table_employee['show']="headings"
table_employee['columns']=(0,1,2,3,4,5,6,7)
table_employee.heading(0,text="Emp ID")
table_employee.heading(1,text="Name")
table_employee.heading(2,text="Emp No")
table_employee.heading(3,text="Phoneno")
table_employee.heading(4,text="Email")
table_employee.heading(5,text="ID No")
table_employee.heading(6,text="Profession")
table_employee.heading(7,text="Salary")
table_employee.column(0,width=50,anchor=CENTER)
table_employee.column(1,width=100)
table_employee.column(2,width=60,anchor=CENTER)
table_employee.column(3,width=80)
table_employee.column(4,width=100)
table_employee.column(5,width=70,anchor=CENTER)
table_employee.column(6,width=90)
table_employee.column(7,width=50,anchor=CENTER)
func_viewemployees()

# employee Attendance
# open camera for atteandance
def func_open_camera_Attendance():
	global cap
	if os.path.exists('faces_trained.yml'):
		face_recognizer=cv.face.LBPHFaceRecognizer_create()
		face_recognizer.read('faces_trained.yml')
		employees=[]
		DIR=f'{os.getcwd()}\\Employee_images\\'
		for i in os.listdir(DIR):
			employees.append(i)
		img_id=0
		try:
			cap=cv.VideoCapture(0)
			while True:
				ret,frame=cap.read()
				if ret:
					camera_image=cv.cvtColor(frame,cv.COLOR_BGR2RGB)
					img=cv.cvtColor(frame,cv.COLOR_BGR2RGB)
					gray_img=cv.cvtColor(camera_image,cv.COLOR_BGR2GRAY)
					face_rect=face_classifier.detectMultiScale(gray_img,1.1,10)
					for (x,y,w,h) in face_rect:
						face_roi=gray_img[y:h+h,x:x+w]
						confidence=0
						try:
							label,confidence=face_recognizer.predict(face_roi)
						except:
							pass
						if confidence>=60:
							cv.rectangle(img,(x,y),(x+w,y+h),(0,255,255),2)
							cv.putText(img,str(employees[label]),(x,y-4),cv.FONT_HERSHEY_SIMPLEX,0.8,(0,255,255),1,cv.LINE_AA)
							cv.putText(img,str(round(confidence,2)),(x,y+h+20),cv.FONT_HERSHEY_SIMPLEX,0.8,(0,255,255),1,cv.LINE_AA)
							func_get_employeedata(employees[label])
						else:
							cv.putText(img,str(round(confidence,2)),(x,y+h+20),cv.FONT_HERSHEY_SIMPLEX,0.8,(0,255,255),1,cv.LINE_AA)
							cv.rectangle(img,(x,y),(x+w,y+h),(0,255,255),2)
							func_clear_recognized_data()
					img=Image.fromarray(img)
					img=img.resize((500,400))
					img=ImageTk.PhotoImage(img)
					lbl_camera1.configure(text="",image=img)
					
					win.update()
				else:
					break
			cap.release()
			cv.destroyAllWindows()
		except Exception as e:
			messagebox.showerror("Error",str(e))
# function off camera
def func_close_camera_Attendance():
	try:
		global cap
		cap.release()
		cv.destroyAllWindows()
		lbl_camera1.configure(text="Camera Image",image="")
	except:
		pass
def func_get_employeedata(empno):
	global id_empno,id_empname
	try:
		cursor=conn.cursor()
		sql="SELECT empno,employee_name,profession FROM employee WHERE empno='%s'"%(empno)
		cursor.execute(sql)
		results=cursor.fetchall()
		if results:
			lbl_empno.configure(text=f"Employee No: {results[0][0]}")
			lbl_empname.configure(text=f"Employee Name: {results[0][1]}")
			lbl_empprofession.configure(text=f"Profession: {results[0][2]}")

			#get profile
			img=Image.open(f'{images_folder}\\{empno}\\profile.png')
			img=img.resize((200,200))
			img=ImageTk.PhotoImage(img)
			lbl_empprofile.configure(image=img,text="")
			lbl_empprofile.img=img
			id_empno=results[0][0]
			id_empname=results[0][1]
	except Exception as e:
		messagebox.showerror("Error",str(e))
def func_clear_recognized_data():
	global id_empno,id_empname
	lbl_empno.configure(text=f"Employee No:")
	lbl_empname.configure(text=f"Employee Name: ")
	lbl_empprofession.configure(text=f"Profession: ")
	lbl_empprofile.configure(image="",text="Employee Profile")
	id_empno=""
	id_empname=""

def func_checkin():
	global id_empno,id_empname
	if id_empno=="" and id_empname=="":
		messagebox.showwarning("Warning","You have not been identified")
	else:
		msg=messagebox.askyesno("Confirm",f"Do you want to Check IN? \nEmp No: {id_empno} \nName: {id_empname}")
		if msg==True:
			messagebox.showinfo("Success","Check IN succcesfully")
			func_clear_recognized_data()
			func_close_camera_Attendance()


def func_chekout():
	global id_empno,id_empname
	if id_empno=="" and id_empname=="":
		messagebox.showwarning("Warning","You have not been identified")
	else:
		msg=messagebox.askyesno("Confirm",f"Do you want to Check OUT? \nEmp No: {id_empno} \nName: {id_empname}")
		if msg==True:
			messagebox.showinfo("Success","Check OUT succcesfully")
			func_clear_recognized_data()
			func_close_camera_Attendance()

# place objects on the frame attendance employee
frame_capture_Emp_photo1=LabelFrame(frame_EmployeeAttendance,text="Capture Employee Photo")
frame_capture_Emp_photo1.pack(side=LEFT,fill=BOTH,expand=True)
lbl_camera1=Label(frame_capture_Emp_photo1,text="Camera Image",font=font_label,image="")
lbl_camera1.pack(side=TOP,fill=BOTH,expand=True)
frame_camera_operation1=Frame(frame_capture_Emp_photo1)
frame_camera_operation1.pack(side=TOP)
btn_ON_camera1=Button(frame_camera_operation1,text="ON",width=btn_width2,border=1,cursor="hand2",fg=col_black,bg=col_cyan,activeforeground=col_black,activebackground=col_cyan,command=func_open_camera_Attendance)
btn_ON_camera1.grid(column=0,row=0,padx=4,pady=5)
btn_OFF_camera1=Button(frame_camera_operation1,text="OFF",width=btn_width2,border=1,cursor="hand2",fg=col_black,bg=col_cyan,activeforeground=col_black,activebackground=col_cyan,command=func_close_camera_Attendance)
btn_OFF_camera1.grid(column=1,row=0,padx=4,pady=5)

frame_captured_Emp_data=LabelFrame(frame_EmployeeAttendance,text="Employee Data")
frame_captured_Emp_data.pack(side=LEFT,fill=BOTH,expand=True)
lbl_empprofile=Label(frame_captured_Emp_data,text="Employee Profile")
lbl_empprofile.pack(side=TOP,expand=True)

frame_attendance_empdata=Frame(frame_captured_Emp_data)
frame_attendance_empdata.pack(side=TOP,fill=X)
lbl_empno=Label(frame_attendance_empdata,text="Employee No: ",font=font_label,justify=LEFT,anchor=E)
lbl_empno.grid(column=0,row=0,padx=5,pady=10,sticky=W)
lbl_empname=Label(frame_attendance_empdata,text="Employee Name: ",font=font_label,justify=LEFT,anchor=E)
lbl_empname.grid(column=0,row=1,padx=5,pady=10,sticky=W)
lbl_empprofession=Label(frame_attendance_empdata,text="Profession: ",font=font_label,justify=LEFT,anchor=E)
lbl_empprofession.grid(column=0,row=2,padx=5,pady=10,sticky=W)

id_empno=""
id_empname=""

frame_attendance_operation=Frame(frame_captured_Emp_data)
frame_attendance_operation.pack(side=TOP)
btn_CheckIN=Button(frame_attendance_operation,text="Check IN",width=button_width,border=1,cursor="hand2",fg=col_black,bg=col_cyan,activeforeground=col_black,activebackground=col_cyan,command=func_checkin)
btn_CheckIN.grid(column=0,row=0,padx=4,pady=5)
btn_CheckOUT=Button(frame_attendance_operation,text="Check Out",width=button_width,border=1,cursor="hand2",fg=col_black,bg=col_cyan,activeforeground=col_black,activebackground=col_cyan,command=func_chekout)
btn_CheckOUT.grid(column=1,row=0,padx=4,pady=5)

win.mainloop()