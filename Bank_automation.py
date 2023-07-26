import email
from inspect import modulesbyfile
from math import comb
from ssl import MemoryBIO
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from sqlite3 import *

win=Tk()
win.state('zoomed')
win.configure(bg='powder blue')
win.resizable(width=False, height=False)
lbl_title=Label(win, text="Bank Automation",bg='powder blue',font=('',50,'bold'))
lbl_title.pack()

#photo=PhotoImage(file='logo.png')
#lbl_img=Label(win, image=photo)
#lbl_img.place(x=0,y=15)
    
def home_screen(pfrm=None):
    if pfrm!=None:
        pfrm.destroy()
    frm=Frame(win)
    frm.configure(bg='pink')
    frm.place(x=0,y=100, relwidth=1, relheight=1)


    lbl_user=Label(frm,text="Username:", font=('',20,'bold'),bg='pink')
    entry_user=Entry(frm, font=('',20,'bold'),bg='white',bd=10)
    lbl_user.place(relx=.3, rely=.1)
    entry_user.place(relx=.45,rely=.1)
    entry_user.focus()
    
    lbl_pass=Label(frm,text="Password:", font=('',20,'bold'),bg='pink')
    entry_pass=Entry(frm,show='*', font=('',20,'bold'),bg='white',bd=10)
    lbl_pass.place(relx=.3, rely=.2)
    entry_pass.place(relx=.45,rely=.2)

    lbl_type=Label(frm,text="User Type:", font=('',20,'bold'),bg='pink')
    lbl_type.place(relx=.3, rely=.3)

    combo_type=ttk.Combobox(frm,
                            value=[
                                "---Select user---",
                                "Customer",
                                "Admin"
                                ],font=('',20,''))
    combo_type.current(0)
    combo_type.place(relx=.45, rely=.3)
    
    login_btn=Button(frm,command=lambda:welcome_screen(frm,entry_user,entry_pass,combo_type),width=10,text="Login",bd=10,font=('',20,'bold'),bg='powder blue')
    login_btn.place(relx=.4,rely=.45)

    reset_btn=Button(frm,width=10,command=lambda:reset_home(entry_user,entry_pass,combo_type),text="Reset",bd=10,font=('',20,'bold'),bg='powder blue')
    reset_btn.place(relx=.55,rely=.45)

    open_btn=Button(frm,command=lambda:open_screen(frm),text="Open Account",bd=10,font=('',20,'bold'),bg='powder blue')
    open_btn.place(relx=.36,rely=.55)

    fp_btn=Button(frm,command=lambda:fp_screen(frm),text="Forgot password",bd=10,font=('',20,'bold'),bg='powder blue')
    fp_btn.place(relx=.55,rely=.55)


def logout(pfrm):
    option=messagebox.askyesno(title='logout', message="do you really want to logout")
    if option==True:
        home_screen(pfrm)
    else:
        pass
    
def welcome_screen(pfrm,entry_user,entry_pass,combo_type):
    user=entry_user.get()
    pwd=entry_pass.get()
    tp=combo_type.get()
    if(tp=="---Select user---"):
        messagebox.showwarning("warning","please select type")
        return
    elif(tp=="Customer"):
        con=connect("bank.db")
        cur=con.cursor()
        cur.execute("select name,bal,type from useraccount where acn=? and pass=?",(user,pwd))
        tup=cur.fetchone()
        if(tup==None):
            messagebox.showerror("fail","Invalid username/password")
            return
        else:
            pfrm.destroy()
            frm=Frame(win)
            frm.configure(bg='pink')
            frm.place(x=0,y=140,relwidth=1,relheight=1)

            logout_btn=Button(frm,command=lambda:logout(frm),text="logout",font=('',20,'bold'),bg='powder blue',bd=10)
            logout_btn.place(relx=.9,rely=.001)

            left_frm=Frame(frm)
            left_frm.configure(bg='pink')
            left_frm.place(x=5,y=10,relwidth=.2,relheight=1)

            check_btn=Button(frm,width=10,command=lambda:checkbal_frame(),text="check bal",font=('',20,'bold'),bg='powder blue',bd=10)
            check_btn.place(relx=.001,rely=.1)

            deposit_btn=Button(frm,width=10,command=lambda:deposit_frame(),text="deposit",font=('',20,'bold'),bg='powder blue',bd=10)
            deposit_btn.place(relx=.001,rely=.25)

            withdraw_btn=Button(frm,width=10,command=lambda:withdraw_frame(),text="withdraw",font=('',20,'bold'),bg='powder blue',bd=10)
            withdraw_btn.place(relx=.001,rely=.4)

            transfer_btn=Button(frm,width=10,command=lambda:transfer_frame(),text="transfer",font=('',20,'bold'),bg='powder blue',bd=10)
            transfer_btn.place(relx=.001,rely=.55)

            txnhist_btn=Button(frm,width=10,command=lambda:txnhistory_frame(),text="txn history",font=('',20,'bold'),bg='powder blue',bd=10)
            txnhist_btn.place(relx=.001,rely=.7)
    else:
        messagebox.showinfo("welcome","Admin is underconstruction")
        return
    def checkbal_frame():
        f=Frame(frm)
        f.configure(bg='wheat')
        f.place(x=250,y=20, relwidth=.7, relheight=.6)

        lbl_name=Label(f,text=f"Name:{tup[0]}",font=('',20,'bold'),fg='green',bg='pink')
        lbl_bal=Label(f,text=f"Balance:{tup[1]}",font=('',20,'bold'),fg='green',bg='pink')
        lbl_type=Label(f,text=f"Type:{tup[2]}",font=('',20,'bold'),fg='green',bg='pink')
        lbl_name.place(x=100,y=100)
        lbl_bal.place(x=100,y=200)
        lbl_type.place(x=100,y=300)
    def deposit_frame():
        f=Frame(frm)
        f.configure(bg='wheat')
        f.place(x=250,y=20, relwidth=.7, relheight=.6)

        lbl_amt=Label(f,text="Amount", fg='green',font=('',20,'bold'),bg='pink')
        entry_amt=Entry(f,font=('',20,'bold'),bd=10)
        sub_btn=Button(f,width=10,text="submit", font=('',20,'bold'),bd=10,bg="powder blue")
        reset_btn=Button(f,width=10,text='reset',font=('',20,'bold'),bd=10,bg='powder blue')

        lbl_amt.place(x=100,y=100)
        entry_amt.place(x=300,y=100)
        sub_btn.place(x=150,y=200)
        reset_btn.place(x=350,y=200)
    def withdraw_frame():
        f=Frame(frm)
        f.configure(bg='wheat')
        f.place(x=250,y=20, relwidth=.7, relheight=.6)

        lbl_amt=Label(f,text="Amount", fg='green',font=('',20,'bold'),bg='pink')
        entry_amt=Entry(f,font=('',20,'bold'),bd=10)
        sub_btn=Button(f,width=10,text="withdraw", font=('',20,'bold'),bd=10,bg="powder blue")
        reset_btn=Button(f,width=10,text='reset',font=('',20,'bold'),bd=10,bg='powder blue')

        lbl_amt.place(x=100,y=100)
        entry_amt.place(x=300,y=100)
        sub_btn.place(x=150,y=200)
        reset_btn.place(x=350,y=200)
    def transfer_frame():
        f=Frame(frm)
        f.configure(bg='wheat')
        f.place(x=250,y=20, relwidth=.7, relheight=.6)

        lbl_amt=Label(f,text="Amount", fg='green',font=('',20,'bold'),bg='pink')
        entry_amt=Entry(f,font=('',20,'bold'),bd=10)

        lbl_acc=Label(f,text="To Acc", fg='green',font=('',20,'bold'),bg='pink')
        entry_acc=Entry(f,font=('',20,'bold'),bd=10)
        
        trans_btn=Button(f,width=10,text="Transfer", font=('',20,'bold'),bd=10,bg="powder blue")
        reset_btn=Button(f,width=10,text='reset',font=('',20,'bold'),bd=10,bg='powder blue')

        
        lbl_amt.place(x=100,y=100)
        entry_amt.place(x=300,y=100)
        lbl_acc.place(x=100,y=200)
        entry_acc.place(x=300,y=200)
        trans_btn.place(x=150,y=300)
        reset_btn.place(x=350,y=300)
    def txnhistory_frame():
        f=Frame(frm)
        f.configure(bg='wheat')
        f.place(x=250,y=20, relwidth=.7, relheight=.6)

    checkbal_frame()

def fp_screen(pfrm):
    pfrm.destroy()
    frm=Frame(win)
    frm.configure(bg='pink')
    frm.place(x=0,y=100, relwidth=1, relheight=1)
    
    back_btn=Button(frm,command=lambda:home_screen(frm),text="Back",bd=10,font=('',20,'bold'),bg='powder blue')
    back_btn.place(relx=.001,rely=.01)

    lbl_acn=Label(frm,text="Accno", fg='green',font=('',20,'bold'),bg='pink')
    entry_acn=Entry(frm,font=('',20,'bold'),bd=10)

    lbl_mob=Label(frm,text="Mob", fg='green',font=('',20,'bold'),bg='pink')
    entry_mob=Entry(frm,font=('',20,'bold'),bd=10)
        
    recv_btn=Button(frm,width=10,command=lambda:recover_pass(frm,entry_acn,entry_mob,),text="Recover", font=('',20,'bold'),bd=10,bg="powder blue")
    reset_btn=Button(frm,width=10,text='reset',font=('',20,'bold'),bd=10,bg='powder blue')

    lbl_acn.place(x=300,y=100)
    entry_acn.place(x=500,y=100)
    lbl_mob.place(x=300,y=200)
    entry_mob.place(x=500,y=200)
    recv_btn.place(x=350,y=300)
    reset_btn.place(x=550,y=300)    
    
def open_screen(pfrm):
    pfrm.destroy()
    frm=Frame(win)
    frm.configure(bg='pink')
    frm.place(x=0,y=100, relwidth=1, relheight=1)

    back_btn=Button(frm,command=lambda:home_screen(frm),text="Back",bd=10,font=('',20,'bold'),bg='powder blue')
    back_btn.place(relx=.001,rely=.01)

    lbl_acn=Label(frm,text="Accno:", fg='green',font=('',20,'bold'),bg='pink')
    entry_acn=Entry(frm,font=('',20,'bold'),bd=10,state='disable')

    lbl_mob=Label(frm,text="Mob:", fg='green',font=('',20,'bold'),bg='pink')
    entry_mob=Entry(frm,font=('',20,'bold'),bd=10)

    lbl_email=Label(frm,text="email:", fg='green',font=('',20,'bold'),bg='pink')
    entry_email=Entry(frm,font=('',20,'bold'),bd=10)

    lbl_name=Label(frm,text="Name:", fg='green',font=('',20,'bold'),bg='pink')
    entry_name=Entry(frm,font=('',20,'bold'),bd=10)

    lbl_pass=Label(frm,text="Password:", fg='green',font=('',20,'bold'),bg='pink')
    entry_pass=Entry(frm,show='*',font=('',20,'bold'),bd=10)

    lbl_type=Label(frm,text="Type:", fg='green',font=('',20,'bold'),bg='pink')
    combo_type=ttk.Combobox(frm,
                            value=[
                                "saving",
                                "current"
                                ],font=('',20,''))
    combo_type.current(0)
    
    open_btn=Button(frm,command=lambda:openacn_db(frm,entry_mob,entry_email,entry_name,entry_pass,combo_type),width=10,text="OpenAcc", font=('',20,'bold'),bd=10,bg="powder blue")
    reset_btn=Button(frm,width=10,text='reset',font=('',20,'bold'),bd=10,bg='powder blue')

    #lbl_acn.place(x=300,y=90)
    #entry_acn.place(x=500,y=90)
    lbl_mob.place(x=300,y=180)
    entry_mob.place(x=500,y=180)
    lbl_email.place(x=300,y=270)
    entry_email.place(x=500,y=270)
    lbl_name.place(x=300,y=360)
    entry_name.place(x=500,y=360)
    lbl_pass.place(x=300,y=450)
    entry_pass.place(x=500,y=450)
    lbl_type.place(x=300,y=540)
    combo_type.place(x=500,y=540)
    open_btn.place(x=350,y=630)
    reset_btn.place(x=550,y=630)    


def openacn_db(pfrm,entry_mob,entry_email,entry_name,entry_pass,combo_type):
    con=connect("bank.db")
    cur=con.cursor()
    cur.execute("select max(acn) from useraccount")
    tup=cur.fetchone()
    acn=tup[0]
    acn=acn+1
    con.close()
    
    
    #acn=int(entry_acn.get())
    #acn=1
    mob=entry_mob.get()
    email=entry_email.get()
    name=entry_name.get()
    pwd=entry_pass.get()  
    tp=combo_type.get()
    bal=1000
    status='active'
    
    con=connect("bank.db")
    cur=con.cursor()
    cur.execute("insert into useraccount values(?,?,?,?,?,?,?,?)",(name,pwd,email,mob,acn,bal,tp,status))
    con.commit()
    con.close() 
    messagebox.showinfo("Account Opening",f"your Account is opened with Acn:{acn}")
    home_screen(pfrm)

def recover_pass(frm,entry_acn,entry_mob):
    acn=int(entry_acn.get())
    mob=entry_mob.get()

    con=connect("bank.db")
    cur=con.cursor()
    cur.execute("select pass from useraccount where acn=? and mob=?",(acn,mob))
    tup=cur.fetchone()
    if (tup==None):
        messagebox.showwarning("password","Invalid Acn No/Mob No.")
        return
    else:
        pwd=tup[0]
        messagebox.showinfo("password",f"your password:{pwd}")
    
    con.close()
    home_screen(frm)
def reset_home(entry_user,entry_pass, combo_type):
    entry_user.delete(0,END)
    entry_pass.delete(0,END)
    combo_type.current(0)
    entry_user.focus(0)



home_screen()

win.mainloop()
