from tkinter import Tk,Label,Frame,Entry,Button,messagebox
from tkinter.ttk import Combobox
from tkintertable import TableCanvas, TableModel
import time
import random
import project_tables
import sqlite3
import gmail


win=Tk()
win.state('zoomed')
win.resizable(width=False,height=False)
win.configure(bg='pink')

title=Label(win,text='Banking Automation',font=('arial',20,'bold','underline'),bg='pink')
title.pack()

date=time.strftime("%d-%B-%Y")
currdate=Label(win,text=date,font=('arial',20),bg='pink')
currdate.pack(pady=10)

footer=Label(win,text='By Shahnawaz Malik @8999045062\n Ducat Noida, sector 16',font=('arial',20,'bold'),bg='pink')
footer.pack(side='bottom')

def main_scr():
    
    frm=Frame(win,highlightbackground='black',highlightthickness=2)
    frm.place(relx=0,rely=.12,relwidth=1,relheight=.76)

    
    code_cap=''
    for i in range(3):
        i=random.randint(65,90)
        c=chr(i)
        j=random.randint(0,9)
        code_cap=code_cap+str(j)+c
    
    
        
    def reset():
        frm.destroy()
        main_scr()
    
    def forgot_pass():
        frm.destroy()
        forgotpass_screen()
        
    def login():
        choice=com_box.get()    
        acno=entry_acn_no.get()
        pwd=entry_password.get()
        user_cap=captcha_entry.get()
        if acno=="" or pwd=="" :
            messagebox.showerror("login","Empty fields are not allowed")
            return
        if choice=='admin' and acno=='1001' and pwd=='admin':
            if user_cap==code_cap:
                frm.destroy()
                admin_screen()
            else:
                messagebox.showerror("login","invalid captcha")
        elif choice=='user':
            if user_cap==code_cap:
                conobj=sqlite3.connect('Banking.sqlite')
                curobj=conobj.cursor()
                curobj.execute('select * from users where users_acno=? and users_pass=?',(acno,pwd))
                tup=curobj.fetchone()
                if tup==None:
                    messagebox.showerror("Login","Invalid ACN/Pass")
                    return
                else:
                    global welcome_user,user_acno
                    user_acno=tup[0]
                    welcome_user=tup[1]
                    frm.destroy()
                    user_screen()
                    
            else:
                messagebox.showerror("login","invalid captcha")
        else:
            messagebox.showerror("login","invalid acn or password")
       
     
    acn_type=Label(frm,text='Acn Type',font=('arial',20,'bold'),bg='pink')
    acn_type.place(relx=.3,rely=.1)
    
    com_box=Combobox(frm,values=['-----Select Acc.. Type-----','user','admin'],font=('arial',20,))
    com_box.current(0)
    com_box.place(relx=.45,rely=.1)
    
    acn_no=Label(frm,text='Acc.. No',font=('arial',20,'bold'),bg='pink')
    acn_no.place(relx=.3,rely=.2)
    
    entry_acn_no=Entry(frm,font=('arial',20,'bold'))
    entry_acn_no.place(relx=.45,rely=.2)
    entry_acn_no.focus()
    
    password=Label(frm,text='Password',font=('arial',20,'bold'),bg='pink')
    password.place(relx=.3,rely=.3)
    
    entry_password=Entry(frm,font=('arial',20,'bold'),show='*')
    entry_password.place(relx=.45,rely=.3)
   
    lbl_captcha=Label(frm,text=f"Captcha\t{code_cap}",font=('arial',20,'bold'),bg='white',fg='black')
    lbl_captcha.place(relx=.5,rely=.45)    
    
    btn_refresh=Button(frm,text='R/F',font=('arial',20,'bold'),bg='powder blue',command=main_scr)
    btn_refresh.place(relx=.7,rely=.45,relheight=.05,relwidth=.04)
    
    
    lbl_captcha2=Label(frm,text='Enter Captcha',font=('arial',20,'bold'),bg='white',fg='black')
    lbl_captcha2.place(relx=.3,rely=.55)
    
    captcha_entry=Entry(frm,font=('arial',20,'bold'),bd=5)
    captcha_entry.place(relx=.458,rely=.55)
    
    
    btn_submit=Button(frm,text='Submit',font=('arial',20,'bold'),bg='pink',command=login)
    btn_submit.place(relx=.5,rely=.7)
    
    btn_reset=Button(frm,text='Reset',font=('arial',20,'bold'),bg='pink',command=reset)
    btn_reset.place(relx=.6,rely=.7)
    
    btn_forgotpassword=Button(frm,text='Forgot Password',font=('arial',20,'bold'),bg='pink',command=forgot_pass)
    btn_forgotpassword.place(relx=.5,rely=.85)
    
    def forgotpass_screen():
        frm=Frame(win,highlightbackground='black',highlightthickness=2)
        frm.configure(bg='pink')
        frm.place(relx=0,rely=.13,relwidth=1,relheight=.78)
        frm_title=Label(win,text='Password Recovery Screen',font=('arial',30,'bold'))
        frm_title.pack() 
        def back():
            frm.destroy()
            main_scr()
        
        def forgotpass_db():
            acc_no=e_no.get()
            mo_no=entry_num.get()
            mail=e_email.get()
            
            conobj=sqlite3.connect('Banking.sqlite')
            curobj=conobj.cursor()
            curobj.execute('select users_name,users_pass from users where users_acno=? and users_email=? and users_mob=?',(acc_no,mail,mo_no))
            tup=curobj.fetchone()
            if tup==None:
                messagebox.showerror("Forgot password","Invalid Details")
                return
            else:
                global upass,uname
                uname=tup[0]
                upass=tup[1]
                otp=random.randint(1000,9999)
                
                try:
                    con=gmail.GMail('shahnawazmlik009@gmail.com','nuop nhht xqgh outj')
                    utext=f'''Hello,{uname},
                    otp for password recovery is{otp}

                    Thanks
                    ABC Bank Corp
                    '''
                    msg=gmail.Message(to=mail,subject='Account opened successfully',text=utext)
                    con.send(msg)
                    messagebox.showinfo('Password recovery','Mail sent successfully')
                       
                    lbl_otp=Label(frm,text='OTP',font=('arial',20,'bold'),bg='pink')
                    lbl_otp.place(relx=.3,rely=.6)

                    ottp=Entry(frm,font=('arial',20,'bold'))
                    ottp.place(relx=.4,rely=.6)
                    
                    def show_pass():
                        if otp==int(ottp.get()):
                            messagebox.showinfo('Show Pass',f'Your Pass is :\t{upass}')
                        else:
                            messagebox.showerror('OTP',f'invalid OTP')
                    
                    btn_forgot=Button(text='Show_pass',font=('arial',20,'bold'),bg='red',command=show_pass)
                    btn_forgot.place(relx=.0,rely=.7) 
                                           

                   
                except:
                    messagebox.showerror('Network Problem','Something went wrong with network')    

        
        btn_back=Button(frm,text='back',font=('arial',20,'bold'),command=back)
        btn_back.place(relx=.0,rely=.0)
        
        acn_num=Label(frm,text='Acn..no',font=('arial',20,'bold'),bg='pink')
        acn_num.place(relx=.3,rely=.15)
        
        e_no=Entry(frm,font=('arial',20,'bold'))
        e_no.place(relx=.4,rely=.15)
        e_no.focus()
        
        mob_num=Label(frm,text='Mob..no',font=('arial',20,'bold'),bg='pink')
        mob_num.place(relx=.3,rely=.25)
        
        entry_num=Entry(frm,font=('arial',20,'bold'))
        entry_num.place(relx=.4,rely=.25)
        
        email=Label(frm,text='Email',font=('arial',20,'bold'),bg='pink')
        email.place(relx=.3,rely=.35)
        
        e_email=Entry(frm,font=('arial',20,'bold'))
        e_email.place(relx=.4,rely=.35)
        
        btn_forgot=Button(text='Show_pass',font=('arial',20,'bold'),command=forgotpass_db)
        btn_forgot.place(relx=.45,rely=.5)
        
        btn_cancel=Button(text='Cancel',font=('arial',20,'bold'))
        btn_cancel.place(relx=.55,rely=.5)
        
    def admin_screen():
        frm=Frame(win,highlightbackground='black',highlightthickness=2)
        frm.configure(bg='pink')
        frm.place(relx=0,rely=.13,relwidth=1,relheight=.78)
        frm_title=Label(win,text='Welcome Admin Screen',font=('arial',30,'bold'))
        frm_title.place(relx=.35,rely=.135) 
        
        def back():
            frm.destroy()
            main_scr()
        
        def logout():
            frm.destroy()
            main_scr()
            
        def account_open():
            frm.destroy()
            new_account()
            
        def delete_page():
            delete_screen()
            
        def user_acn_view():
            view_user_acn()
                
        btn=Button(frm,text='Back',font=('arial',20,'bold'),command=back)
        btn.place(relx=.0,rely=.0)
        
        btn_acnopen=Button(frm,text='Open Account',font=('arial',20,'bold'),bg='light green',command=account_open)
        btn_acnopen.place(relx=.0,rely=.2,relwidth=.2)
    
        btn_delacn=Button(frm,text='Delete Account',font=('arial',20,'bold'),bg='red',command=delete_page)
        btn_delacn.place(relx=.0,rely=.4,relwidth=.2) 
        
        btn_view_acn=Button(frm,text='View Account',font=('arial',20,'bold'),bg='blue',fg='white',command=user_acn_view)
        btn_view_acn.place(relx=.0,rely=.6,relwidth=.2)    
            
        
        btn=Button(frm,text='logout',font=('arial',20,'bold'),command=logout)
        btn.place(relx=.915,rely=.0)   
            
    def new_account():
        frm=Frame(win,highlightbackground='black',highlightthickness=2)
        frm.configure(bg='pink')
        frm.place(relx=0,rely=.13,relwidth=1,relheight=.78)
        frm_title=Label(win,text='New Account Opening',font=('arial',30,'bold'))
        frm_title.place(relx=.35,rely=.135)   
        
        def back():
            frm.destroy()
            admin_screen()
        
        def logout():
            frm.destroy()
            main_scr()
        def reset():
            frm.destroy()
            new_account()
            
        def newuser_db():
            uname=e_name.get()
            unum=e_num.get()
            uemail=e_email.get()
            uaadhar=e_aadhar.get()   
            ubal=0
            upass=''
            for i in range (3):
                i=random.randint(65,90)
                c=chr(i)
                j=random.randint(0,9)
                upass=upass+str(j)+c
            
            conobj=sqlite3.connect(database='Banking.sqlite')   
            curobj=conobj.cursor()
            curobj.execute('insert into users(users_name,users_pass,users_mob,users_email,users_aadar,users_bal,users_opendate)values(?,?,?,?,?,?,?)',(uname,upass,unum,uemail,uaadhar,ubal,date))
            conobj.commit()
            conobj.close()

            conobj=sqlite3.connect(database='Banking.sqlite')   
            curobj=conobj.cursor()
            curobj.execute('select max(users_acno) from users')
            uacn=curobj.fetchone()[0]
            conobj.close()
            
            messagebox.showinfo('New account',f'Your account is opened with ACNo:{uacn} & Password:{upass} ')
            try:
                con=gmail.GMail('shahnawazmlik009@gmail.com','nuop nhht xqgh outj')
                utext=f'''Hello,{uname},
                Your account is opened in ABC bank,
                your account no is:{uacn}
                Your Password is {upass}


                Thanks
                ABC Bank Corp
                '''
                msg=gmail.Message(to=uemail,subject='Account opened successfully',text=utext)
                con.send(msg)
                messagebox.showinfo('New Account','Mail sent successfully')
                    
            except:
                    messagebox.showerror('Network Problem','Something went wrong with network')    
                    
            
        btn=Button(frm,text='logout',font=('arial',20,'bold'),command=logout)
        btn.place(relx=.915,rely=.0)  
        
        btn=Button(frm,text='Back',font=('arial',20,'bold'),command=back)
        btn.place(relx=.0,rely=.0)    
       
        user_name=Label(frm,text='Name',font=('arial',20,'bold'),bg='pink')
        user_name.place(relx=.3,rely=.15)
        
        e_name=Entry(frm,font=('arial',20,'bold'))
        e_name.place(relx=.4,rely=.15)
        e_name.focus()
        
        mob_num=Label(frm,text='Mob..no',font=('arial',20,'bold'),bg='pink')
        mob_num.place(relx=.3,rely=.25)
        
        e_num=Entry(frm,font=('arial',20,'bold'))
        e_num.place(relx=.4,rely=.25)
        
        email=Label(frm,text='Email',font=('arial',20,'bold'),bg='pink')
        email.place(relx=.3,rely=.35)
        
        e_email=Entry(frm,font=('arial',20,'bold'))
        e_email.place(relx=.4,rely=.35)
        
        aadhar_no=Label(frm,text='Aad_no',font=('arial',20,'bold'),bg='pink')
        aadhar_no.place(relx=.3,rely=.45)
        
        e_aadhar=Entry(frm,font=('arial',20,'bold'))
        e_aadhar.place(relx=.4,rely=.45)
        
        btn_open=Button(frm,text='Open Acn',font=('arial',20,'bold'),bg='light green',command=newuser_db)
        btn_open.place(relx=.35,rely=.6)
             
        btn_reset=Button(frm,text='Reset',font=('arial',20,'bold'),bg='red',command=reset)
        btn_reset.place(relx=.6,rely=.6)
    

    
    
    def admin_screen():
        #new_account()
        frm=Frame(win,highlightbackground='black',highlightthickness=2)
        frm.configure(bg='pink')
        frm.place(relx=0,rely=.13,relwidth=1,relheight=.78)
        frm_title=Label(win,text='Welcome Admin Screen',font=('arial',30,'bold'))
        frm_title.place(relx=.35,rely=.135) 
        
        def back():
            frm.destroy()
            main_scr()
        
        def logout():
            frm.destroy()
            main_scr()
            
        def account_open():
            frm.destroy()
            new_account()
            
        def delete_page():
            frm1=Frame(frm)
            frm1.configure(bg='pink')
            frm1.place(relx=.2,rely=.1,relwidth=.8,relheight=.9)
            frm_title=Label(win,text='Delete Screen',font=('arial',30,'bold'))
            frm_title.place(relx=.35,rely=.135,relwidth=.4) 
            
            def delete_acn_db():
                number=entry_num.get()
                conobj=sqlite3.connect('Banking.sqlite')
                curobj=conobj.cursor()
                curobj.execute('delete from users where users_acno=?',(number,))
                conobj.commit()
                conobj.close()
                messagebox.showinfo('Delete',"Account Deleted")
            
            acn_num=Label(frm1,text='Acn..no',font=('arial',20,'bold'),bg='pink')
            acn_num.place(relx=.2,rely=.15)
            
            entry_num=Entry(frm1,font=('arial',20,'bold'))
            entry_num.place(relx=.3,rely=.15)
            entry_num.focus()
            
            btn_delete=Button(frm1,text='Delete',font=('arial',20,'bold'),bg='red',command=delete_acn_db)
            btn_delete.place(relx=.4,rely=.25)  
              
        def view_user_acn():
            frmm=Frame(frm)
            frmm.configure(bg='pink')
            frmm.place(relx=.2,rely=.1,relwidth=.9,relheight=.897)
            frm_title=Label(win,text='View Screen',font=('arial',30,'bold'))
            frm_title.place(relx=.35,rely=.135,relwidth=.4)
            
            def view():
                acnum=entry_num.get() 
                
                conobj=sqlite3.connect('Banking.sqlite')
                curobj=conobj.cursor()
                curobj.execute('select * from users where users_acno=?',(acnum,))
                tup=curobj.fetchone()
                conobj.close()
                if tup==None:
                    messagebox.showerror('View','Accout does not exist.')
                    return
                
                
                acnum=Label(frmm,text='Acno',font=('arial',15,'bold'))
                acnum.place(relx=.1,rely=.3)
                
                acnum_value=Label(frmm,text=tup[0],font=('arial',15),bg='green',fg='white')
                acnum_value.place(relx=.3,rely=.3)
                
                name=Label(frmm,text='Name',font=('arial',15,'bold'))
                name.place(relx=.5,rely=.3)
                
                name_value=Label(frmm,text=tup[1],font=('arial',15),bg='green',fg='white')
                name_value.place(relx=.65,rely=.3)
                
                mob=Label(frmm,text='Mob',font=('arial',15,'bold'))
                mob.place(relx=.1,rely=.5)
                
                mob_value=Label(frmm,text=tup[3],font=('arial',15),bg='green',fg='white')
                mob_value.place(relx=.3,rely=.5)
                
                aadhar=Label(frmm,text='Aadhar',font=('arial',15))
                aadhar.place(relx=.5,rely=.5)
                
                aadhar_value=Label(frmm,text=tup[6],font=('arial',15),bg='green',fg='white')
                aadhar_value.place(relx=.65,rely=.5)
                
                opendate=Label(frmm,text='Opendate',font=('arial',15,'bold'))
                opendate.place(relx=.1,rely=.7)
                
                opendate_value=Label(frmm,text=tup[7],font=('arial',15),bg='green',fg='white')
                opendate_value.place(relx=.25,rely=.7)
                
                bal=Label(frmm,text='Balance',font=('arial',15,'bold'))
                bal.place(relx=.5,rely=.7)
                
                bal_value=Label(frmm,text=tup[5],font=('arial',15),bg='green',fg='white')
                bal_value.place(relx=.65,rely=.7)
                       
            acn_num=Label(frmm,text='Acn..no',font=('arial',20,'bold'),bg='pink')
            acn_num.place(relx=.2,rely=.15)
            
            entry_num=Entry(frmm,font=('arial',20,'bold'))
            entry_num.place(relx=.3,rely=.15)
            entry_num.focus()
            
            btn_view=Button(frmm,text='View',font=('arial',20,'bold'),bg='blue',command=view)
            btn_view.place(relx=.4,rely=.25)    
              
                   
        btn=Button(frm,text='Back',font=('arial',20,'bold'),command=back)
        btn.place(relx=.0,rely=.0)
        
        btn_acnopen=Button(frm,text='Open Account',font=('arial',20,'bold'),bg='light green',command=account_open)
        btn_acnopen.place(relx=.0,rely=.2,relwidth=.2)
    
        btn_deleteacn=Button(frm,text='Delete Account',font=('arial',20,'bold'),bg='red',command=delete_page)
        btn_deleteacn.place(relx=.0,rely=.4,relwidth=.2) 
        
        btn_view_acn=Button(frm,text='View Account',font=('arial',20,'bold'),bg='blue',fg='white',command=view_user_acn)
        btn_view_acn.place(relx=.0,rely=.6,relwidth=.2)    
            
        
        btn=Button(frm,text='logout',font=('arial',20,'bold'),command=logout)
        btn.place(relx=.915,rely=.0) 
        
            
    def user_screen():
        frm=Frame(win,highlightbackground='black',highlightthickness=2)
        frm.configure(bg='pink')
        frm.place(relx=0,rely=.13,relwidth=1,relheight=.78)
        title_heading="welcome user screen"
        frm_title=Label(win,text=title_heading,font=('arial',30,'bold'))
        frm_title.place(relx=.39,rely=.135) 
        
        
        def logout():
            frm.destroy()
            main_scr()
            
        def profile_update():
            title_heading="welcome user screen"
            frm_title.configure(text='Update Profile')
            frmn=Frame(frm)
            def update_db():
                u_pass=e_pass.get()
                u_mob=e_mob.get()
                u_mail=e_email.get()
                conobj=sqlite3.connect('Banking.sqlite')
                curobj=conobj.cursor()
                curobj.execute('update users set users_pass=?,users_mob=?,users_email=? where users_acno=?',(u_pass,u_mob,u_mail,user_acno))
                conobj.commit()
                conobj.close()
                messagebox.showinfo('Update Details','Updated successfully')
                
            frmn.configure(bg='pink')
            frmn.place(relx=.2,rely=.1,relwidth=9,relheight=.897)
            
            acn_name=Label(frmn,text='Pass',font=('arial',20,'bold'),bg='pink')
            acn_name.place(relx=.01,rely=.15)
        
            e_pass=Entry(frmn,font=('arial',20,'bold'))
            e_pass.place(relx=.02,rely=.15)
            e_pass.focus()
        
            acn_mob=Label(frmn,text='Mobile',font=('arial',20,'bold'),bg='pink')
            acn_mob.place(relx=.01,rely=.3)
        
            e_mob=Entry(frmn,font=('arial',20,'bold'))
            e_mob.place(relx=.02,rely=.3)
            
            acn_email=Label(frmn,text='Email',font=('arial',20,'bold'),bg='pink')
            acn_email.place(relx=.01,rely=.45)
        
            e_email=Entry(frmn,font=('arial',20,'bold'))
            e_email.place(relx=.02,rely=.45)
        
            btn_update=Button(frmn,text='Update',font=('arial',20,'bold'),bg='maroon',fg='white',command=update_db)
            btn_update.place(relx=.03,rely=.6)
            
            conobj=sqlite3.connect('Banking.sqlite')
            curobj=conobj.cursor()
            curobj.execute('select users_pass,users_mob,users_email from users where users_acno=?',(user_acno,))
            tup=curobj.fetchone()
            conobj.close()
                
            e_pass.insert(0,tup[0])
            e_mob.insert(0,tup[1])
            e_email.insert(0,tup[2])
            
            
        
        def withdraw_money():
            title_heading="Withdraw Money"
            frm_title.configure(text=title_heading)
            frmn=Frame(frm)
            def withdraw():
                uamt=int(amt_enter.get())

                conobj=sqlite3.connect(database='Banking.sqlite')
                curobj=conobj.cursor()
                curobj.execute('select users_bal from users where users_acno=?',(user_acno,))
                ubal=int(curobj.fetchone()[0])
                conobj.close()
                if ubal>uamt:
                    conobj=sqlite3.connect(database='Banking.sqlite')
                    curobj=conobj.cursor()
                    curobj.execute('update users set users_bal=users_bal-? where users_acno=?',(uamt,user_acno))
                    conobj.commit()
                    conobj.close()

                    conobj=sqlite3.connect(database='Banking.sqlite')
                    curobj=conobj.cursor()
                    curobj.execute('insert into txn(txn_acno,txn_type,txn_amt,txn_bal,txn_date) values(?,?,?,?,?)',(user_acno,'Dr',uamt,ubal-uamt,date))
                    conobj.commit()
                    conobj.close()

                    messagebox.showinfo("Withdraw",f"{uamt} withdrawn,Updated Bal:{ubal-uamt}")
                else:
                    messagebox.showerror("Withdraw",f"Insufficient Bal:{ubal}")
            frmn.configure(bg='pink')
            frmn.place(relx=.2,rely=.1,relwidth=9,relheight=.897)
            
            amt=Label(frmn,text='Withdraw Amount',font=('arial',20,'bold'),bg='pink')
            amt.place(relx=.01,rely=.25)
        
            amt_enter=Entry(frmn,font=('arial',20,'bold'))
            amt_enter.place(relx=.035,rely=.25)
            amt_enter.focus()
        
            btn_withdraw=Button(frmn,text='Withdraw',font=('arial',20,'bold'),bg='light green',command=withdraw)
            btn_withdraw.place(relx=.04,rely=.45)
            
        def deposit_money():
            
            title_heading="welcome Deposit screen"
            frm_title.configure(text=title_heading)
            frm2=Frame(frm)
            def deposit():
                uamt=int(amt_enter.get())
                conobj=sqlite3.connect(database='Banking.sqlite')
                curobj=conobj.cursor()
                curobj.execute('update users set users_bal=users_bal+? where users_acno=?',(uamt,user_acno))
                conobj.commit()
                conobj.close()

                conobj=sqlite3.connect(database='Banking.sqlite')
                curobj=conobj.cursor()
                curobj.execute('select users_bal from users where users_acno=?',(user_acno,))
                ubal=curobj.fetchone()[0]
                conobj.close()

                conectionobj=sqlite3.connect('Banking.sqlite')
                cursorobj=conectionobj.cursor()
                cursorobj.execute('insert into txn(txn_acno,txn_type,txn_amt,txn_bal,txn_date) values(?,?,?,?,?)',(user_acno,'cr',uamt,ubal,date))
                conectionobj.commit()
                conectionobj.close()

                messagebox.showinfo("Deposit",f"{uamt} deposited,Updated Bal:{ubal}")
                
            frm2.configure(bg='pink')
            frm2.place(relx=.2,rely=.1,relwidth=9,relheight=.897)
            
        
            amt=Label(frm2,text='Deposit Amount',font=('arial',20,'bold'),bg='pink')
            amt.place(relx=.01,rely=.25)
        
            amt_enter=Entry(frm2,font=('arial',20,'bold'))
            amt_enter.place(relx=.03,rely=.25)
            amt_enter.focus()
        
            btn_deposit=Button(frm2,text='Deposit',font=('arial',20,'bold'),bg='light green',command=deposit)
            btn_deposit.place(relx=.04,rely=.45)
         
        def money_trans():
            title_heading="welcome user screen"
            frm_title.configure(text='Transfer Money')
            frm3=Frame(frm)
            frm3.configure(bg='pink')
            frm3.place(relx=.2,rely=.1,relwidth=9,relheight=.897) 
          
            def transfer():
                uamt=int(amt_enter.get())
                utoacn=int(receiver.get())

                conobj=sqlite3.connect('Banking.sqlite')
                curobj=conobj.cursor()
                curobj.execute('select * from users where users_acno=?',(utoacn,))
                tup=curobj.fetchone()
                conobj.close()
                if tup==None:
                    messagebox.showerror("Transfer","Invalid To ACN")
                else:
                    conobj=sqlite3.connect(database='Banking.sqlite')
                    curobj=conobj.cursor()
                    curobj.execute('select users_bal from users where users_acno=?',(user_acno,))
                    ubal=int(curobj.fetchone()[0])
                    conobj.close()
                    if ubal>uamt:
                        conobj=sqlite3.connect(database='Banking.sqlite')
                        curobj=conobj.cursor()
                        curobj.execute('update users set users_bal=users_bal-? where users_acno=?',(uamt,user_acno))
                        curobj.execute('update users set users_bal=users_bal+? where users_acno=?',(uamt,utoacn))
                        conobj.commit()
                        conobj.close()

                        conobj=sqlite3.connect(database='Banking.sqlite')
                        curobj=conobj.cursor()
                        curobj.execute('insert into txn(txn_acno,txn_type,txn_amt,txn_bal,txn_date) values(?,?,?,?,?)',(user_acno,'Dr',uamt,ubal-uamt,date))
                        curobj.execute('insert into txn(txn_acno,txn_type,txn_amt,txn_bal,txn_date) values(?,?,?,?,?)',(utoacn,'Cr',uamt,ubal+uamt,date))
                        
                        conobj.commit()
                        conobj.close()

                        messagebox.showinfo("Transfer",f"{uamt} transferd,Updated Bal:{ubal-uamt}")
                    else:
                        messagebox.showerror("Transfer",f"Insufficient Bal:{ubal}")         
          
            receiver=Label(frm3,text='To',font=('arial',20,'bold'),bg='pink')
            receiver.place(relx=.01,rely=.15)
        
            receiver=Entry(frm3,font=('arial',20,'bold'))
            receiver.place(relx=.03,rely=.15)
            receiver.focus()
            
            amt=Label(frm3,text='Enter Amount',font=('arial',20,'bold'),bg='pink')
            amt.place(relx=.01,rely=.25)
        
            amt_enter=Entry(frm3,font=('arial',20,'bold'))
            amt_enter.place(relx=.03,rely=.25)
            
    
        
            btn_withdraw=Button(frm3,text='Transfer',font=('arial',20,'bold'),bg='light green',command=transfer)
            btn_withdraw.place(relx=.04,rely=.45)
         
        def history():
            title_heading="welcome user screen"
            frm_title.configure(text='Trnx History')
            frmn=Frame(frm)
            frmn.configure(bg='pink')
            frmn.place(relx=.2,rely=.1,relwidth=9,relheight=.897)  

            data={}
            conobj=sqlite3.connect("Banking.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select * from txn where txn_acno=?",(user_acno,))
            tups=curobj.fetchall()
            i=1
            for tup in tups:
                data[str(i)]={'Txn Amt':tup[3],'Txn Type':tup[2],'Updated Bal':tup[4],'Txn Date':tup[5],'Txn Id':tup[0]}
                i+=1
                model = TableModel()
                model.importDict(data)

                table_frame=Frame(frmn)
                table_frame.place(relx=.1,rely=.1,relheight=.1,relwidth=.1)

                table = TableCanvas(frmn, model=model,editable=True)
                table.show()
       
        def check_details():
            title_heading="welcome user screen"
            frm_title.configure(text='Balance Enquiry')
            frmbal=Frame(frm)
            frmbal.configure(bg='pink')
            frmbal.place(relx=.2,rely=.1,relwidth=9,relheight=.897)
            
            conobj=sqlite3.connect('Banking.sqlite')
            curobj=conobj.cursor()
            curobj.execute('select * from users where users_acno=?',(user_acno,))
            tup=curobj.fetchone()
            conobj.close()
            
            
            acnum=Label(frmbal,text='Acno',font=('arial',20,'bold'))
            acnum.place(relx=.01,rely=.15)
            
            acnum_value=Label(frmbal,text=tup[0],font=('arial',20),bg='pink')
            acnum_value.place(relx=.03,rely=.15)
            
            name=Label(frmbal,text='Name',font=('arial',20,'bold'))
            name.place(relx=.05,rely=.15)
            
            name_value=Label(frmbal,text=tup[1],font=('arial',20),bg='pink')
            name_value.place(relx=.065,rely=.15)
            
            mob=Label(frmbal,text='Mob',font=('arial',20,'bold'))
            mob.place(relx=.01,rely=.35)
            
            mob_value=Label(frmbal,text=tup[3],font=('arial',20),bg='pink')
            mob_value.place(relx=.03,rely=.35)
            
            aadhar=Label(frmbal,text='Aadhar',font=('arial',20,'bold'))
            aadhar.place(relx=.05,rely=.35)
            
            aadhar_value=Label(frmbal,text=tup[6],font=('arial',20),bg='pink')
            aadhar_value.place(relx=.065,rely=.35)
            
            opendate=Label(frmbal,text='Opendate',font=('arial',20,'bold'))
            opendate.place(relx=.01,rely=.55)
            
            opendate_value=Label(frmbal,text=tup[7],font=('arial',20),bg='pink')
            opendate_value.place(relx=.023,rely=.55)
            
            bal=Label(frmbal,text='Balance',font=('arial',20,'bold'))
            bal.place(relx=.05,rely=.55)
            
            bal_value=Label(frmbal,text=tup[5],font=('arial',20),bg='pink')
            bal_value.place(relx=.065,rely=.55)
        
             
        welcome_lbl=Label(frm,text=f'welcome,{welcome_user}',font=('arial',20,'bold'),bg='red',fg='white')
        welcome_lbl.place(relx=.0,rely=.0)
        
        btn_withdraw=Button(frm,text='Withdraw',font=('arial',20,'bold'),bg='light green',command=withdraw_money)
        btn_withdraw.place(relx=.0,rely=.4,relwidth=.2)
    
        btn_deposit=Button(frm,text='Deposit',font=('arial',20,'bold'),bg='light green',command=deposit_money)
        btn_deposit.place(relx=.0,rely=.53,relwidth=.2) 
        
        btn_transfer=Button(frm,text='Money Transfer',font=('arial',20,'bold'),bg='gray',fg='white',command=money_trans)
        btn_transfer.place(relx=.0,rely=.81,relwidth=.2)
        
        btn_history=Button(frm,text='Tr.History',font=('arial',20,'bold'),bg='purple',fg='white',command=history)
        btn_history.place(relx=.0,rely=.66,relwidth=.2)
        
        btn_update=Button(frm,text='Update Profile',font=('arial',20,'bold'),bg='orange',fg='white',command=profile_update)
        btn_update.place(relx=.0,rely=.12,relwidth=.2)  
    
        
        btn_checkbal=Button(frm,text='Check Details',font=('arial',20,'bold'),bg='blue',fg='white',command=check_details)
        btn_checkbal.place(relx=.0,rely=.26,relwidth=.2)  
            
        
        btn=Button(frm,text='logout',font=('arial',20,'bold'),command=logout)
        btn.place(relx=.915,rely=.0)     
        
            
main_scr()
win.mainloop()