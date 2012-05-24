from Tkinter import *
import xml.dom.minidom as xml
import os
import tkFileDialog



def create_league():
	
 	#clear the main window
	load_b.pack_forget()
	cleague_b.pack_forget()
	
	#create new league
	lname=Entry(top, justify='center')
	lname.insert(0,"nameofleague")
	
	lname.bind('<Return>', lambda event: get_teamnumber(event,lname))
	lname.pack()

def get_teamnumber(event,lname):
	global leaguename
	leaguename=lname.get()
 	#disable the entry for the leaguename
	lname.config(state='disabled')
	
	
	tnumber = Entry(top, justify='center')	
	tnumber.pack()
	tnumber.insert(0,"10")
	tnumber.bind('<Return>', lambda event: create_teamnames(event, tnumber))

def create_teamnames(event,tnumber):
	number=tnumber.get()
	#disable the entry for the number of teams
	tnumber.config(state='disabled')
	
	tname={}
	
	#create new teams
	for i in range(0,int(number)):
		tname[i]=Entry(top, justify='center')
		tname[i].pack()
		tname[i].insert(0,"teamname"+ str(i+1))
		newname[i]=tname[i].get()

	play2games = IntVar()
        c = Checkbutton(top, text="2 games", variable=play2games)
	c.var= play2games
	c.pack()

	#create create-button ;-)
	cleague_b = Button(top, text="Create!", command=lambda: create(tname,cleague_b,c))	
	cleague_b.pack()


def create(tname,cleague_b,c):
	global doc
	for i in range(0,len(newname)):
		tname[i].config(state='disabled')
	cleague_b.pack_forget()	
	c.config(state='disabled')

	if os.path.isfile("./"+str(leaguename)+".xml"):
		print "This league is already existing !"
	else: 
		tdb_xml = doc.createElement('tdb')
		doc.appendChild(tdb_xml)
		for i in range(0,len(newname)):	
			elem=doc.createElement('team')
			tdb_xml.appendChild(elem)
			#now=strftime("%Y-%m-%d %H:%M:%S", localtime())
			elem.setAttribute('name', newname[i])
			elem.setAttribute('games', "0")
			elem.setAttribute('wins', "0")
			elem.setAttribute('ties', "0")
			elem.setAttribute('losses', "0")
			elem.setAttribute('goals', "0")
			elem.setAttribute('goalsagainst', "0")
			elem.setAttribute('points', "0")
		#create matches
		i= len(newname)
		#matchnumber=0
		#while i >0 :	
		#	matchnumber+=i
		#	i-=1
				
		for i in range(0,len(newname)):	
			for j in range(i,len(newname)):
				elem=doc.createElement('match')
				tdb_xml.appendChild(elem)
				elem.setAttribute('team1', newname[j])
				elem.setAttribute('team2', newname[i])
		play2games=c.var.get()
		if play2games==1:
			for i in range(0,len(newname)):	
				for j in range(i,len(newname)):
					elem=doc.createElement('match')
					tdb_xml.appendChild(elem)
					elem.setAttribute('team1', newname[i])
					elem.setAttribute('team2', newname[j])
	
		#save doc to file for the first time
		xml_file = open("./"+str(leaguename)+".xml", "w")
		tdb_xml.writexml(xml_file)
		xml_file.close()
		#show the league in a table
		show_table(play2games)
	
def show_table(play2games):
	global tdict,doc, tabwin		
	tabwin=Toplevel()
	Button(tabwin, text="Save to xml", command=write_data).grid(row=len(newname)*2+3,column=20,columnspan=2, sticky=W)
	i=0	
	teamelements = doc.getElementsByTagName('team')
	print len(teamelements)
	for elem in teamelements:
		Label(tabwin, text=elem.getAttributeNode("name").nodeValue).grid(row=i+1,column=0, sticky=W)
		Label(tabwin, text=elem.getAttributeNode("name").nodeValue).grid(row=0,column=i*2+1,columnspan=2, sticky=N)
		tdict[i]={}		
		for j in range(0,len(newname)):				
			tdict[i][str(j)+"0"] = Entry(tabwin, justify='center', width=3)
			tdict[i][str(j)+"0"].grid(row=i+1, column=j*2+1, sticky=E)	
			tdict[i][str(j)+"1"] = Entry(tabwin, justify='center', width=3)
			tdict[i][str(j)+"1"].grid(row=i+1, column=j*2+2, sticky=W)	
			if i==j: 
				tdict[i][str(j)+"0"].config(state='disabled')
				tdict[i][str(j)+"1"].config(state='disabled')
			if i<j and play2games==0:
				tdict[i][str(j)+"0"].config(state='disabled')
				tdict[i][str(j)+"1"].config(state='disabled')
			tdict[i][str(j)+"0"].bind('<FocusOut>', set_stats)
			tdict[i][str(j)+"1"].bind('<FocusOut>', set_stats)
			
		i+=1


def set_stats(event):
	global doc,tabwin
	
	nodes=doc.getElementsByTagName('match')
	for i in range(0,len(newname)):
		goals1=0	
		goals2=0
		points=0	
		games= 0	
		wins=0
		ties=0
		losses=0
		
		for j in range(0,len(newname)):	
			
			try: 
				g1=int(tdict[i][str(j)+ "0"].get())
				g2=int(tdict[i][str(j)+ "1"].get())							
			     	goals1 +=g1 
				goals2 +=g2 
				games+=1
				if g1 > g2:
					points+=3
					wins+=1
				elif g1==g2:
					points+=1
					ties+=1
				else:
					losses +=1
				
				#save match
				for elem in nodes:
					print elem.getAttribute('team1'),elem.getAttribute('team2'),newname[i],newname[j]
					if elem.getAttribute('team1')==newname[i] and elem.getAttribute('team2')==newname[j]:
						elem.setAttribute('goals1', str(g1))
						elem.setAttribute('goals2', str(g2))
			except: pass	
			
			
			try: 
				g1=int(tdict[j][str(i)+ "0"].get())
				g2=int(tdict[j][str(i)+ "1"].get())							
			     	goals1 +=g2 
				goals2 +=g1 
				games+=1
				if g1 < g2:
					points+=3
					wins+=1
				elif g1==g2:
					points+=1
					ties+=1
				else:
					losses +=1
				#save match
				for elem in nodes:
					print "second loop:",elem.getAttribute('team1'),elem.getAttribute('team2'),newname[i],newname[j]
					if elem.getAttribute('team1')==newname[i] and elem.getAttribute('team2')==newname[j]:
						elem.setAttribute('goals1', str(g2))
						elem.setAttribute('goals2', str(g1))
			except: pass
		
		#save data to dictionary							
		tdict[i]['goals']= goals1
		tdict[i]['goalsagainst']= goals2
		tdict[i]['points']= points
		tdict[i]['games']= games
		tdict[i]['wins']= wins
		tdict[i]['losses']= losses
		tdict[i]['ties']= ties
		
	#save to doc
	save_data()	
	
	#create sorted table
	nodes= doc.getElementsByTagName('team')
	sortedteams=sorted(nodes, key=lambda x: int(x.attributes['points'].value), reverse=True)	
        i= len(newname)	+ 5
	Label(tabwin, text= "table of " + leaguename,font=("Helvetica", 35),justify='center').grid(row=i,column=1, columnspan= len("table of " + leaguename))
	Label(tabwin, text= "name" ,font=("Helvetica", 35)).grid(row=i+1,column=1, columnspan=4)
	Label(tabwin, text= "games" ,font=("Helvetica", 35)).grid(row=i+1,column=5, columnspan=2)
	Label(tabwin, text= "wins" ,font=("Helvetica", 35)).grid(row=i+1,column=7, columnspan=2)
	Label(tabwin, text= "ties" ,font=("Helvetica", 35)).grid(row=i+1,column=9, columnspan=2)
	Label(tabwin, text= "losses" ,font=("Helvetica", 35)).grid(row=i+1,column=11, columnspan=2)
	Label(tabwin, text= "goals" ,font=("Helvetica", 35)).grid(row=i+1,column=13, columnspan=4)
	Label(tabwin, text= "points" ,font=("Helvetica", 35)).grid(row=i+1,column=17, columnspan=2)

	i+=2
	for elem in sortedteams:
		ltext = elem.getAttribute('name') 
		Label(tabwin, text= ltext,font=("Helvetica", 24),justify='center').grid(row=i,column=1, columnspan=4)
		ltext = str(elem.getAttribute('games')) 
		Label(tabwin, text= ltext,font=("Helvetica", 24),justify='center').grid(row=i,column=5, columnspan=2)
		ltext = str(elem.getAttribute('wins')) 
		Label(tabwin, text= ltext,font=("Helvetica", 24),justify='center').grid(row=i,column=7, columnspan=2)		
		ltext = str(elem.getAttribute('ties')) 
		Label(tabwin, text= ltext,font=("Helvetica", 24),justify='center').grid(row=i,column=9, columnspan=2)
		ltext = str(elem.getAttribute('losses'))
		Label(tabwin, text= ltext,font=("Helvetica", 24),justify='center').grid(row=i,column=11, columnspan=2)
		ltext = str(elem.getAttribute('goals')) + ":"
		Label(tabwin, text= ltext,font=("Helvetica", 24),justify='center').grid(row=i,column=13, columnspan=2, sticky=E)
		ltext = str(elem.getAttribute('goalsagainst'))    
		Label(tabwin, text= ltext,font=("Helvetica", 24),justify='center').grid(row=i,column=15, columnspan=2, sticky=W)
		ltext = str(elem.getAttribute('points')) 
		Label(tabwin, text= ltext,font=("Helvetica", 24),justify='center').grid(row=i,column=17, columnspan=2)
		i+=1

def load_data(tdict):
	global doc
	#clear the main window
	load_b.pack_forget()
	cleague_b.pack_forget()
	
	file = tkFileDialog.askopenfilename(parent=top,title='Choose an appropriate xml file',initialdir='./',defaultextension=".xml",filetypes=[("all files","*.xml")])
	if file != None:
		filename=os.path.basename(file)		

	#load saved teams from xml-file
	try:
		doc= xml.parse(filename)
	except:
		print "No (acceptable) '.xml' found! Select a new one or create a new league!"
        
	nameelements = doc.getElementsByTagName('team')
        for i in range(0,len(nameelements)):
		newname[i]=nameelements[i].getAttribute('name')
	"""	
	
	
	for i in range(0,len(nameelements)):
			#if elem.tagName=="FlashFolder" and not elem.getAttribute('filename')=="":
			#create dictionary for every dictionary element
						
			tdict[i] = { "name": str(nameelements[i].getAttributeNode("name").nodeValue),"points": int(nameelements[i].getAttributeNode("points").nodeValue) }
			tdict[i]['games']= str(nameelements[i].getAttributeNode("games").nodeValue
			tdict[i]['wins']= str(nameelements[i].getAttributeNode("wins").nodeValue
			tdict[i]['ties']= str(nameelements[i].getAttributeNode("ties").nodeValue
			tdict[i]['losses']= str(nameelements[i].getAttributeNode("losses").nodeValue
			tdict[i]['goals']= str(nameelements[i].getAttributeNode("goals").nodeValue
			tdict[i]['goalsagainst']= str(nameelements[i].getAttributeNode("goalsagainst").nodeValue
	print tdict
	"""
	play2games=1 #TODO
	show_table(play2games)

def save_data():
	global doc
	"""
        if not os.path.exists("./"+ leaguename+".xml"):
		print "the file '"+leaguename+".xml' does not exist."
		menu()
	dirFound=False
	for elem in config_xml.childNodes:
		if elem.tagName=="team" and elem.getAttribute('name')==filename:
			elem.setAttribute('lastReviewed', strftime("%Y-%m-%d %H:%M:%S", localtime()))
			dirFound=True
	if not dirFound:
	"""
	
	i=0
	nodes=doc.getElementsByTagName('team')
	for elem in nodes:
		#now=strftime("%Y-%m-%d %H:%M:%S", localtime())
		#elem.setAttribute('name', tdict[i]['name'])
		elem.setAttribute('games', str(tdict[i]['games']))
		elem.setAttribute('wins', str(tdict[i]['wins']))
		elem.setAttribute('ties', str(tdict[i]['ties']))
		elem.setAttribute('losses',str(tdict[i]['losses']))
		elem.setAttribute('goals',str(tdict[i]['goals']))
		elem.setAttribute('points',str(tdict[i]['points']))	
		elem.setAttribute('goalsagainst', str(tdict[i]['goalsagainst']))	
		i+=1

def write_data():	
	global doc
	xml_file = open("./"+ leaguename+".xml", "w")
	doc.writexml(xml_file)
	xml_file.close()

########################################### MAIN ########################################################################
#create Tkinter main window
top = Tk()
top.title("Soccer League Creator and Manager") 

#iconbitmapLocation = "@./.TexFlasher/pictures/icon2.xbm"
#top.iconbitmap(iconbitmapLocation)
#top.iconmask(iconbitmapLocation)


tdict={}
newname={}
doc=xml.Document()


leaguename="default"
Label(top,font=("Helvetica",8),text="Copyright (c) 2012: Alexis Papathanassopoulos").pack()



cleague_b = Button(top, text="Create League", command=create_league)
load_b = Button(top, text="Load League", command=lambda: load_data(tdict))


load_b.pack()
cleague_b.pack()




mainloop()
