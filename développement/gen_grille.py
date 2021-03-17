from random import randint,choice
from os import system
import time 

def the_grille():
	grille=[
		[" "," "," "," "," "," "," "," "," "],
		[" "," "," "," "," "," "," "," "," "],
		[" "," "," "," "," "," "," "," "," "],
		[" "," "," "," "," "," "," "," "," "],
		[" "," "," "," "," "," "," "," "," "],
		[" "," "," "," "," "," "," "," "," "],
		[" "," "," "," "," "," "," "," "," "],
		[" "," "," "," "," "," "," "," "," "],
		[" "," "," "," "," "," "," "," "," "]
		]
	return grille

def grille_test():
	grille=[
		[" ","4","6"," "," ","7","8"," "," "],
		[" "," ","8","9"," "," ","7"," "," "],
		["5"," "," "," ","2"," "," "," "," "],
		[" "," "," "," ","6","2"," "," ","4"],
		["4"," "," "," "," "," "," "," ","7"],
		[" "," "," "," ","5"," "," ","1"," "],
		[" "," ","2"," "," "," "," "," "," "],
		[" ","1","5"," "," "," "," ","2"," "],
		[" "," "," "," "," ","8"," ","6"," "]
		]



	return grille

def affichage_grille(grille):
	print('    ',end='')
	for i in range(len(grille[0])):
		print(i+1,'  ',end='')
	print()
	for ligne in grille:
		print('   ',end='')
		for i in range(len(ligne)):
			print("----",end="")
		print()
		print((grille.index(ligne)+1),"| ",end="")
		for elem in ligne:
			print(elem+" | ",end="")
		print()
	print('   ',end='')
	for i in range(len(ligne)):
		print("----",end="")
	print()
	print('__________________________________________________')
	pass

def calc_proba(liste_element):
	liste_size=[]
	for element in liste_element:
		liste_size.append(len(element))
	
	return multi(liste_size)


def multi(liste):
	bob=1
	for lol in liste:
		bob*=lol
	return bob




def init_grille():
	position=0
	while position<9:
		if position==0:
			grille=the_grille()
			liste_corner=check_corner(grille)
			no_move=dont_touch(liste_corner)

		no_good,error=True,False
		liste_element=intel(position,grille)
		proba=calc_proba(liste_element)
		corner=liste_corner[position]		
		turn,pos=0,0
		if proba!=0:
			while no_good:
				turn+=1
				for i in range(len(corner)):
					if not i in no_move[liste_corner.index(corner)]:					
						corner[i]=choice(liste_element[i])

				liste_verif =[]
				for elem in corner:			
					liste_verif.append(elem in corner[corner.index(elem)+1:])
				if sum(liste_verif)==0:
					no_good= verification(maj(position,corner,grille))

				pass
			position+=1
			grille=maj(liste_corner.index(corner),corner,grille)
			#affichage_grille(grille)
			pos+=1	
		else:
			position=0

	#affichage_grille(grille)
	return grille
			

def data_base(grille):
	fichier = open("db.txt", "a")
	fichier.write('\n'+str(grille))
	fichier.close()
	pass



def intel(place,grille):
	liste_chiffres,grille_mod=[str(i) for i in range(1,10)],new_grille(grille)
	liste_ligne,liste_colone,final_liste=[],[],[]

	for i in range(len(grille[0])):
		av=[]
		for chiffres in liste_chiffres:
			if not chiffres in grille[(i//3)+3*(place//3)] and not chiffres in grille_mod[i%3+3*(place%3)]:
				av.append(chiffres)
		final_liste.append(av)

	return final_liste




def maj(place,corner,grille):
	#print(place,corner)
	for element in corner:
		grille[(corner.index(element)//3)+3*(place//3)][(corner.index(element)%3)+(3*(place%3))]=str(element)

	#affichage_grille(grille)
	return grille


def new_grille(grille):
	grille_mod=[]
	for i in range(len(grille)):
		mod=[]
		for j in range(len(grille[i])):
			mod.append(grille[j][i])
		grille_mod.append(mod)
	return grille_mod


def dont_touch(liste_corner):
	no_move=[]
	for corner in liste_corner:
		no=[]
		for case in corner:
			if case!=" ":
				no.append(corner.index(case))
		no_move.append(no)
	return no_move


def verification(grille):
	verif=False
	liste_grille=[new_grille(grille),grille,check_corner(grille)]	
	
	for grill in liste_grille:	
		for i in range(len(grill)):
			for elem in grill[i]:
				if elem!=" ":
					verif=elem in grill[i][grill[i].index(elem)+1:]
					if verif:
						#print(grill[i],elem)
						return verif 

def check_diag(grille):
	liste_diag=[[],[]]
	for i in range(9):
		liste_diag[0].append(grille[i][i])
		liste_diag[1].append(grille[8-i][i])
	return liste_diag

def check_corner(grille):
	liste_corner=[]
	ligne,colone=0,0
	for i in range(9):
		coint=[]
		for j in range(ligne,ligne+3):
			for o in range(colone,colone+3):
				coint.append(grille[j][o])

		liste_corner.append(coint)
		colone+=3
		if colone==9:
			ligne+=3
			colone=0
	return liste_corner




def compteur(grille):
	nb=0
	for ligne in grille:
		for elem in ligne:
			if elem==' ':
				nb+=1
	return nb


def add_db(rep):
	liste_time=[]
	i=0
	while i<rep:
		start_time = time.time()
		init_grille()
		liste_time.append((time.time() - start_time))
		print("Temps d execution : "+str(time.time() - start_time)+"s\nTemps max : "+str(liste_time[liste_time.index(max(liste_time))])+"s\n Temps min : "+str(liste_time[liste_time.index(min(liste_time))])+"s\n Temps moyen : "+str(sum(liste_time)/len(liste_time))+"s")
		print()
		i+=1
	print("temps max d'attente ",liste_time[max(liste_time)])
	print("temps min d'attente ",liste_time[min(liste_time)])
	print("temps moyen d'attente ",sum(liste_time)/2000)
	pass

# Debut du decompte du temps






