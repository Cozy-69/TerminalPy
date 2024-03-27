import os
from pathlib import Path
import subprocess
# from tkinter import *
from tkinter import *
from tkinter import ttk
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, filedialog, messagebox,END
from tkinter.messagebox import askyesno
from tkinter.simpledialog import askstring

folder_selected = None
file_selected = None
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets/frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()
window.title("TerminalPy")
window.geometry("1187x794")
window.configure(bg = "#222944")


## Fonctions
#################################################################################

def openDirectory():
    entry_1.delete(0.0,END)
    global folder_selected
    folder_selected= filedialog.askdirectory()
    result = subprocess.run(['ls', folder_selected], stdout=subprocess.PIPE)

    result = result.stdout.decode('utf-8')
    result = result.splitlines()

    result1 = subprocess.run(['ls', '-l', folder_selected], stdout=subprocess.PIPE)
    result1 = result1.stdout.decode('utf-8').splitlines()
    for i in range(len(result)):
        if result1[i+1][0]=="-":
            result[i] = "       "+result[i]
    result = "\n".join(result)
    result = result+"\n"
    entry_1.delete(0.0, END)
    entry_1.insert(0.0, result)

def renameDirectory():
    global folder_selected
    if folder_selected:

        name = askstring('Nom', 'Quel est le nouveau nom du répertoire')
        try:
            print("mv "+ folder_selected+" " + folder_selected[:folder_selected.rfind("/")]+"/"+name)
            os.system("mv "+ folder_selected+" " + folder_selected[:folder_selected.rfind("/")]+"/"+name)

            folder_selected = folder_selected[:folder_selected.rfind("/")] + "/" + name
            messagebox.showinfo("Success", "votre répertoire a été renommé")
        except Exception as e:
            messagebox.showerror("Error","Quelque chose s'est mal passé")
    else:
        messagebox.showerror("Error", "aucun répertoire n'est sélectionné")

def deleteDirectory():
    global folder_selected
    if folder_selected:
        confirm = askyesno(title='confirmation',message='tu veux vraiment le supprimer ??')
        if confirm:
            try:
                os.system("rm -rf "+folder_selected)

                folder_selected = None
                messagebox.showinfo("Success", "votre répertoire a été supprimer")
            except Exception as e:
                messagebox.showerror("Error", "Quelque chose s'est mal passé")
    else:
        messagebox.showerror("Error", "aucun répertoire n'est sélectionné")


def voirPermissions():
    global folder_selected
    if folder_selected:
        result = subprocess.run(['ls', '-l', folder_selected[:folder_selected.rfind("/")]], stdout=subprocess.PIPE)
        result = result.stdout.decode('utf-8').splitlines()
        for folder in result:
            if folder.find(folder_selected[folder_selected.rfind("/")+1:])!=-1:
                info = folder
                break

        perms = info[1:info.find(" ")]
        info = info[info.find(" ")+1:]
        x = info[:info.find(" ")]
        info = info[info.find(" ") + 1:]
        user = info[:info.find(" ")]
        info = info[info.find(" ") + 1:]
        group = info[:info.find(" ")]
        messagebox.showinfo("Info", "Permission:"+perms+'\n'+"utilisateur:"+user+'\n'+"group:"+group+'\n')
    else:
        messagebox.showerror("Error", "aucun répertoire n'est sélectionné")


def createfolder():
    global folder_selected
    if folder_selected:

        name = askstring('Nom', 'Quel est le  nom du votre nouveau répertoire')
        try:

            os.system("mkdir "+ folder_selected+"/"+name)
            entry_1.delete(0.0, END)
            result = subprocess.run(['ls', folder_selected], stdout=subprocess.PIPE)
            result = result.stdout.decode('utf-8')
            result = result.splitlines()
            result1 = subprocess.run(['ls', '-l', folder_selected], stdout=subprocess.PIPE)
            result1 = result1.stdout.decode('utf-8').splitlines()
            for i in range(len(result)):
                if result1[i + 1][0] == "-":
                    result[i] = "       " + result[i]
            result = "\n".join(result)
            result = result + "\n"
            entry_1.insert(0.0, result)

            messagebox.showinfo("Success", "votre répertoire a été creer")
        except Exception as e:
            messagebox.showerror("Error","Quelque chose s'est mal passé")
    else:
        messagebox.showerror("Error", "aucun répertoire n'est sélectionné")

def modifypermission():
    if folder_selected:
        popupWin = Toplevel()
        popupWin.title("Continue?")
        popupWin.geometry("200x200")
        popupWin.resizable(False, False)

        global r
        r = IntVar()
        w = IntVar()
        x = IntVar()
        lbl = Label(popupWin, text="nouvelles permissions?")
        lbl.pack()

        checkbox = Checkbutton(popupWin, text="Read", variable=r, onvalue=1, offvalue=0, )

        checkbox.pack()
        checkbox1 = Checkbutton(popupWin, text="Write", variable=w, onvalue=1, offvalue=0, )
        checkbox1.pack()

        checkbox2 = Checkbutton(popupWin, text="Execute", variable=x, onvalue=1, offvalue=0, )
        checkbox2.pack()

        def save():
            popupWin.destroy()
            r1 = "r" if r.get()==1 else ""
            w1 = "w" if w.get()==1 else ""
            x1 = "x" if x.get()==1 else ""
            try:
                os.system("chmod uog="+r1+w1+x1+" "+folder_selected)

                messagebox.showinfo("Success", "votre permissions a été modifier")
            except Exception as e:
                messagebox.showerror("Error", "Quelque chose s'est mal passé")

        button = Button(popupWin, text="Save", command=save)
        button.pack()

    else:
        messagebox.showerror("Error", "aucun répertoire n'est sélectionné")



def ouvrirfichier():

    global file_selected
    file_selected = filedialog.askopenfilename()
    result = subprocess.run(['cat', file_selected], stdout=subprocess.PIPE, shell=False)
    result = result.stdout.decode('utf-8')
    entry_2.delete(0.0, END)
    entry_2.insert(0.0, result)
    canvas.itemconfig(fileText,text="Fichier sélectionné: "+file_selected[file_selected.rfind("/")+1:])



def renamefile():
    global file_selected
    if file_selected:

        name = askstring('Nom', 'Quel est le nouveau nom du répertoire')
        try:

            os.system("mv " + file_selected + " " + file_selected[:file_selected.rfind("/")] + "/" + name)

            file_selected = file_selected[:file_selected.rfind("/")] + "/" + name
            canvas.itemconfig(fileText, text="Fichier sélectionné: " + name)
            messagebox.showinfo("Success", "votre répertoire a été renommé")
        except Exception as e:
            messagebox.showerror("Error", "Quelque chose s'est mal passé")
    else:
        messagebox.showerror("Error", "aucun fichier n'est sélectionné")



def supprimerfichier():
    global file_selected
    if file_selected:
        confirm = askyesno(title='confirmation', message='tu veux vraiment le supprimer ??')
        if confirm:
            try:
                os.system("rm " + file_selected)

                file_selected = None
                entry_2.delete(0.0, END)
                messagebox.showinfo("Success", "votre fichier a été supprimer")
            except Exception as e:
                messagebox.showerror("Error", "Quelque chose s'est mal passé")
    else:
        messagebox.showerror("Error", "aucun fichier n'est sélectionné")

def voirPermission():
    global file_selected
    if file_selected:
        result = subprocess.run(['ls', '-l', file_selected[:file_selected.rfind("/")]], stdout=subprocess.PIPE)
        result = result.stdout.decode('utf-8').splitlines()
        for folder in result:
            if folder.find(file_selected[file_selected.rfind("/") + 1:]) != -1:
                info = folder
                break

        perms = info[1:info.find(" ")]
        info = info[info.find(" ") + 1:]
        x = info[:info.find(" ")]
        info = info[info.find(" ") + 1:]
        user = info[:info.find(" ")]
        info = info[info.find(" ") + 1:]
        group = info[:info.find(" ")]
        messagebox.showinfo("Info",
                            "Permission:" + perms + '\n' + "utilisateur:" + user + '\n' + "group:" + group + '\n')
    else:
        messagebox.showerror("Error", "aucun fichier n'est sélectionné")

def modifierperms():
    if file_selected:
        popupWin = Toplevel()
        popupWin.title("Continue?")
        popupWin.geometry("200x200")
        popupWin.resizable(False, False)

        global r
        r = IntVar()
        w = IntVar()
        x = IntVar()
        lbl = Label(popupWin, text="nouvelles permissions?")
        lbl.pack()

        checkbox = Checkbutton(popupWin, text="Read", variable=r, onvalue=1, offvalue=0, )

        checkbox.pack()
        checkbox1 = Checkbutton(popupWin, text="Write", variable=w, onvalue=1, offvalue=0, )
        checkbox1.pack()

        checkbox2 = Checkbutton(popupWin, text="Execute", variable=x, onvalue=1, offvalue=0, )
        checkbox2.pack()

        def save():
            popupWin.destroy()
            r1 = "r" if r.get()==1 else ""
            w1 = "w" if w.get()==1 else ""
            x1 = "x" if x.get()==1 else ""
            try:
                os.system("chmod uog="+r1+w1+x1+" "+file_selected)

                messagebox.showinfo("Success", "votre permissions a été modifier")
            except Exception as e:
                messagebox.showerror("Error", "Quelque chose s'est mal passé")

        button = Button(popupWin, text="Save", command=save)
        button.pack()

    else:
        messagebox.showerror("Error", "aucun file n'est sélectionné")

def CreateFile():
    global folder_selected
    global file_selected
    if folder_selected:

        name = askstring('Nom', 'Quel est le  nom du votre nouveau fichier')
        try:

            os.system("touch " + folder_selected + "/" + name)


            file_selected = folder_selected + "/" + name

            result = subprocess.run(['cat', file_selected], stdout=subprocess.PIPE, shell=False)
            result = result.stdout.decode('utf-8')
            entry_2.delete(0.0, END)
            entry_2.insert(0.0, result)
            entry_1.delete(0.0, END)
            result = subprocess.run(['ls', folder_selected], stdout=subprocess.PIPE)
            result = result.stdout.decode('utf-8')
            result = result.splitlines()
            canvas.itemconfig(fileText, text="Fichier sélectionné: " + name)
            result1 = subprocess.run(['ls', '-l', folder_selected], stdout=subprocess.PIPE)
            result1 = result1.stdout.decode('utf-8').splitlines()
            for i in range(len(result)):
                if result1[i + 1][0] == "-":
                    result[i] = "       " + result[i]
            result = "\n".join(result)
            result = result + "\n"
            entry_1.insert(0.0, result)



            messagebox.showinfo("Success", "votre fichier a été creer")
        except Exception as e:
            messagebox.showerror("Error", "Quelque chose s'est mal passé")
    else:
        messagebox.showerror("Error", "aucun répertoire n'est sélectionné")

def trier():

    global file_selected
    if file_selected:
        try:
            result = subprocess.run(['sort', file_selected], stdout=subprocess.PIPE, shell=False)
            result = result.stdout.decode('utf-8')
            entry_2.delete(0.0, END)
            entry_2.insert(0.0, result)
        except Exception as e:
            messagebox.showerror("Error", "Quelque chose s'est mal passé")
    else:
        messagebox.showerror("Error", "aucun fichier n'est sélectionné")

def info():
    global file_selected
    if file_selected:
        words = subprocess.run(['wc', '-w', file_selected], stdout=subprocess.PIPE)
        words = words.stdout.decode('utf-8').split(" ")[0]
        lignes = subprocess.run(['wc', '-l', file_selected], stdout=subprocess.PIPE)
        lignes = lignes.stdout.decode('utf-8').split(" ")[0]
        carac = subprocess.run(['wc', '-m', file_selected], stdout=subprocess.PIPE)
        carac = carac.stdout.decode('utf-8').split(" ")[0]



        messagebox.showinfo("Info",
                            "Numero de mots:" + words + '\n' + "Numero de lignes:" + lignes + '\n' + "numero de caracteres:" + carac + '\n')
    else:
        messagebox.showerror("Error", "aucun fichier n'est sélectionné")



def CreerUtilisateur():
    name = askstring('Nom', 'Quel est le nouveau nom du utilisateur?')
    try:
        os.system("useradd "+name)
        messagebox.showinfo("Success", "Utilisateur créé avec succès")
    except Exception as e:
        messagebox.showerror("Error", "Quelque chose s'est mal passé")

def CreerGroupe():
    name = askstring('Nom', 'Quel est le nouveau nom du Groupe?')
    try:
        os.system("groupadd "+name)
        messagebox.showinfo("Success", "Groupe créé avec succès")
    except Exception as e:
        messagebox.showerror("Error", "Quelque chose s'est mal passé")

def voirUserGroup():

    words = subprocess.run(['cat', '/etc/group'], stdout=subprocess.PIPE)
    words = words.stdout.decode('utf-8').split(" ")[0]
    messagebox.showinfo("Utilisateur et Groupes", "Groupes:\n \n"+words)
    words = subprocess.run(['cat', '/etc/passwd'], stdout=subprocess.PIPE)
    words = words.stdout.decode('utf-8').split(" ")[0]
    messagebox.showinfo("Utilisateur et Groupes", "Utilisateur:\n \n"+words)

def deplacerRepertoire():
    global folder_selected

    if folder_selected:
        move_folder= filedialog.askdirectory()
        try:
            os.system("mv "+folder_selected+" "+move_folder)
            messagebox.showinfo("Success", "votre répertoire a été deplcaer")
        except Exception as e:
            messagebox.showerror("Error", "Quelque chose s'est mal passé")




    else:
        messagebox.showerror("Error", "aucun repertoire n'est sélectionné")

def deplacerFichier():
    global folder_selected
    global file_selected
    if file_selected:
        move_folder = filedialog.askdirectory()
        try:
            os.system("mv " + file_selected + " " + move_folder)
            messagebox.showinfo("Success", "votre répertoire a été deplcaer")
        except Exception as e:
            messagebox.showerror("Error", "Quelque chose s'est mal passé")




    else:
        messagebox.showerror("Error", "aucun fichier n'est sélectionné")
## Tkinter Code
#########################################################################
canvas = Canvas(
    window,
    bg = "#222944",
    height = 794,
    width = 1187,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: openDirectory(),
    relief="flat"
)
button_1.place(
    x=53.0,
    y=223.0,
    width=125.0,
    height=41.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: CreerUtilisateur(),
    relief="flat"
)
button_2.place(
    x=335.35528564453125,
    y=128.0,
    width=149.38600158691406,
    height=30.265634536743164
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: CreerGroupe(),
    relief="flat"
)
button_3.place(
    x=508.314208984375,
    y=128.3304443359375,
    width=149.38600158691406,
    height=30.265634536743164
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: voirUserGroup(),
    relief="flat"
)
button_4.place(
    x=681.2731323242188,
    y=128.3304443359375,
    width=149.38600158691406,
    height=30.265634536743164
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: ouvrirfichier(),
    relief="flat"
)
button_5.place(
    x=597.0,
    y=219.0,
    width=125.0,
    height=41.0
)

button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: trier(),
    relief="flat"
)
button_6.place(
    x=1084.0,
    y=226.0,
    width=66.0,
    height=28.0
)

button_image_7 = PhotoImage(
    file=relative_to_assets("button_7.png"))
button_7 = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: info(),
    relief="flat"
)
button_7.place(
    x=1084.0,
    y=270.0,
    width=66.0,
    height=28.0
)

button_image_8 = PhotoImage(
    file=relative_to_assets("button_8.png"))
button_8 = Button(
    image=button_image_8,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: renameDirectory(),
    relief="flat"
)
button_8.place(
    x=53.0,
    y=298.0,
    width=125.0,
    height=41.0
)

button_image_9 = PhotoImage(
    file=relative_to_assets("button_9.png"))
button_9 = Button(
    image=button_image_9,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: renamefile(),
    relief="flat"
)
button_9.place(
    x=597.0,
    y=298.0,
    width=125.0,
    height=41.0
)

button_image_10 = PhotoImage(
    file=relative_to_assets("button_10.png"))
button_10 = Button(
    image=button_image_10,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: deleteDirectory(),
    relief="flat"
)
button_10.place(
    x=53.0,
    y=373.0,
    width=125.0,
    height=41.0
)

button_image_11 = PhotoImage(
    file=relative_to_assets("button_11.png"))
button_11 = Button(
    image=button_image_11,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: supprimerfichier(),
    relief="flat"
)
button_11.place(
    x=597.0,
    y=377.0,
    width=125.0,
    height=41.0
)

button_image_12 = PhotoImage(
    file=relative_to_assets("button_12.png"))
button_12 = Button(
    image=button_image_12,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: modifypermission(),
    relief="flat"
)
button_12.place(
    x=53.0,
    y=448.0,
    width=125.0,
    height=41.0
)

button_image_13 = PhotoImage(
    file=relative_to_assets("button_13.png"))
button_13 = Button(
    image=button_image_13,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: voirPermissions(),
    relief="flat"
)
button_13.place(
    x=51.0,
    y=523.0,
    width=125.0,
    height=41.0
)

button_image_14 = PhotoImage(
    file=relative_to_assets("button_14.png"))
button_14 = Button(
    image=button_image_14,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: voirPermission(),
    relief="flat"
)
button_14.place(
    x=597.0,
    y=523.0,
    width=125.0,
    height=41.0
)

button_image_15 = PhotoImage(
    file=relative_to_assets("button_15.png"))
button_15 = Button(
    image=button_image_15,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: createfolder(),
    relief="flat"
)
button_15.place(
    x=51.0,
    y=598.0,
    width=125.0,
    height=41.0
)

button_image_16 = PhotoImage(
    file=relative_to_assets("button_16.png"))
button_16 = Button(
    image=button_image_16,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: CreateFile(),
    relief="flat"
)
button_16.place(
    x=597.0,
    y=598.0,
    width=125.0,
    height=41.0
)

button_image_17 = PhotoImage(
    file=relative_to_assets("button_17.png"))
button_17 = Button(
    image=button_image_17,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: modifierperms(),
    relief="flat"
)
button_17.place(
    x=597.0,
    y=456.0,
    width=125.0,
    height=41.0
)
button_image_18 = PhotoImage(
    file=relative_to_assets("button_18.png"))
button_18 = Button(
    image=button_image_18,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: deplacerRepertoire(),
    relief="flat"
)
button_18.place(
    x=51.0,
    y=659.0,
    width=125.0,
    height=41.0
)
button_image_19 = PhotoImage(
    file=relative_to_assets("button_19.png"))
button_19 = Button(
    image=button_image_19,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: deplacerFichier(),
    relief="flat"
)
button_19.place(
    x=597.0,
    y=659.0,
    width=125.0,
    height=41.0
)
canvas.create_text(
    35.0,
    754.0,
    anchor="nw",
    text="Créé Par Marzouki Mouaid",
    fill="#FFFFFF",
    font=("Inter ExtraBold", 12 * -1)
)

canvas.create_rectangle(
    200.9999772700781,
    192.0,
    202.0,
    713.0,
    fill="#8EBBFF",
    outline="")

canvas.create_rectangle(
    581.999977270078,
    192.0,
    583.0,
    713.0,
    fill="#8EBBFF",
    outline="")

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    392.0,
    467.0,
    image=entry_image_1
)
entry_1 = Text(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=226.0,
    y=222.0,
    width=332.0,
    height=488.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    912.0,
    465.0,
    image=entry_image_2
)
entry_2 = Text(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=746.0,
    y=220.0,
    width=332.0,
    height=488.0
)

canvas.create_text(
    226.0,
    199.0,
    anchor="nw",
    text="Repertoire",
    fill="#FFFFFF",
    font=("Inter ExtraBold", 14 * -1)
)

fileText = canvas.create_text(
    752.0,
    199.0,
    anchor="nw",
    text="Fichier sélectionné: ",
    fill="#FFFFFF",
    font=("Inter ExtraBold", 14 * -1)
)

canvas.create_rectangle(
    0.0,
    0.0,
    1187.0,
    75.0,
    fill="#030C36",
    outline="")

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    81.0,
    42.0,
    image=image_image_1
)

canvas.create_text(
    112.0,
    28.0,
    anchor="nw",
    text="TerminalPy",
    fill="#FFFFFF",
    font=("Inter Black", 24 * -1)
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    114.0,
    734.0,
    image=image_image_2
)
window.resizable(False, False)
window.mainloop()
