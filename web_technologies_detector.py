from colorama import init, Fore, Back, Style
init()

import warnings
warnings.filterwarnings("ignore")

from builtwith import *
from tkinter import *

import sys

import re

def version():
	return "0.12"

def banner():
	import pyfiglet as pyg 
	banner= pyg.figlet_format("Web\nTechnologies\nDetector")   
	version = pyg.figlet_format("v - 0 . 12")   
	print('***********************************************************')  
	print(banner)  
	print(Fore.BLUE)
	print(version)  
	print(Fore.WHITE)
	print("Detect technologies of website using Wappalyzer and / or Builtwith\n")
	print(Fore.RED)
	print("Aref Shaheed \nhttps://github.com/aref2008/ \n01-Jun-2022")
	print(Style.RESET_ALL)
	print('***********************************************************')  

def usage():
	print('***********************************************************')  
	print ('          															  ')
	print (" Usage:")
	print (" \t-g: to run this tool as GUI")
	print (" \t-u: url")
	print (" \t-s: used service (0,1,2 for Wappalyzer, Builtwith, and Both respectively")
	print ('          															  ')
	print (" example: web_technologies_detector.py -u http://wordpress.com -s 2")
	print ('          															  ')
	print ('          															  ')
	print('***********************************************************')  

def wappalyzer_detector_terminal(url):
	from Wappalyzer import Wappalyzer, WebPage
	wappalyzer = Wappalyzer.latest()
	webpage = WebPage.new_from_url(url)
	technologies = wappalyzer.analyze_with_versions_and_categories(webpage)

	print(Style.RESET_ALL)
	print(Fore.GREEN  + "[+] " + str(len(technologies)) + ' technologies detected by Wappalyzer!')
	print(Fore.BLACK + Back.WHITE )
	print("{:<50} {:<50} {:<50}".format('Technology','Version','Categories'))
	print(Style.RESET_ALL)
	for technology, details in technologies.items():
		print("{:} {:<50} {:} {:<50} {:<50}".format(Fore.YELLOW, technology, Fore.WHITE, ', '.join(details['versions']), ', '.join(details['categories'])))

def builtwith_detector_terminal(url):
	technologies = builtwith(url)
	technologies_counter = 0
	for category, technology in technologies.items():
		technologies_counter += len(technology)
	print(Style.RESET_ALL)
	print(Fore.GREEN  + "[+] " + str(technologies_counter) + ' technologies detected by Builtwith!')
	print(Fore.BLACK + Back.WHITE )
	print("{:<50} {:<50}".format('Categories', 'Technologies'))
	print(Style.RESET_ALL)
	for category, technology in technologies.items():
		print("{:} {:<50} {:} {:<50}".format(Fore.WHITE, category, Fore.YELLOW, ', '.join(technology)))

def detector_terminal(url, service=2):
	if (not isValidURL(url)):
		print('\n\n'+Fore.RED  + '[-] URL is not valid\n')
	else:
		print('\n\n'+Fore.BLUE  + '[+] Scanning URL: ' + Fore.BLACK + Back.WHITE + url + '\n')
		print(Style.RESET_ALL)
		if(service == 0):
			wappalyzer_detector_terminal(url)
		elif(service == 1):
			builtwith_detector_terminal(url)
		else:
			wappalyzer_detector_terminal(url)
			builtwith_detector_terminal(url)


def gui():

	import tkinter as tk
	from tkinter import ttk

	from tkinter.filedialog import askopenfilename

	global is_help_opened
	is_help_opened = False
	def help():
		global is_help_opened
		global top

		def on_closing():
			global is_help_opened
			is_help_opened = False
			top.destroy()

		if(is_help_opened):
			is_help_opened = False
			top.destroy()
		else:	
			is_help_opened = True
			top= tk.Toplevel(root)
			top.geometry("750x250")
			top.protocol("WM_DELETE_WINDOW", on_closing)
			top.title("About")
			tk.Label(top, text= "Web technologies detector v-0.1!", font=('Arial')).place(x=150,y=80)
			tk.Label(top, text= "Aref Shaheed", font=('Mistral 18 bold')).place(x=150,y=120)
			tk.Label(top, text= "https://github.com/aref2008/", font=('Calibri')).place(x=150,y=150)
		
	root = tk.Tk()
	menu = tk.Menu(root)
	root.config(menu=menu)
	root.title('Web technologies detector v-0.1')
	root.geometry("800x600")
	root.resizable(0, 0)

	# configure the grid
	root.columnconfigure(0, weight=1)
	root.columnconfigure(1, weight=5)

	filemenu = tk.Menu(menu)
	menu.add_cascade(label="Menu", menu=filemenu)
	filemenu.add_command(label="Help", command=help)
	filemenu.add_separator()
	filemenu.add_command(label="Exit", command=root.quit)


	url_label = ttk.Label(root, text="URL:")
	url_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

	global url_entry
	url_entry = ttk.Entry(root)
	url_entry.grid(column=1, row=0, sticky=tk.N+tk.S+tk.E+tk.W, padx=5, pady=5)


	service_label = ttk.Label(root, text="Service:")
	service_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

	global service_variable
	service_variable = tk.StringVar(root, "1")
	 
	tk.Radiobutton(root, text = "Wappalyzer", variable = service_variable, value = 0).grid(column=1, row=1, sticky=tk.W, padx=5, pady=5)
	tk.Radiobutton(root, text = "Builtwith", variable = service_variable, value = 1).grid(column=1, row=2, sticky=tk.W, padx=5, pady=5)
	tk.Radiobutton(root, text = "Both", variable = service_variable, value = 2).grid(column=1, row=3, sticky=tk.W, padx=5, pady=5)


	button = tk.Button(root, text="Scan", fg="green", command=run_detector_for_gui).grid(column=0, row=4, sticky=tk.N+tk.S+tk.E+tk.W, padx=5, pady=5)

	results_label = ttk.Label(root, text="Results:")
	results_label.grid(column=0, row=5, sticky=tk.W, padx=5, pady=5)

	global results
	results = tk.Text(root, height = 20, width = 50)
	results.grid(column=1, row=6, sticky=tk.N+tk.S+tk.E+tk.W, padx=5, pady=5)


	root.mainloop()

def wappalyzer_detector_gui(url):
	from Wappalyzer import Wappalyzer, WebPage
	wappalyzer = Wappalyzer.latest()
	webpage = WebPage.new_from_url(url)
	technologies = wappalyzer.analyze_with_versions_and_categories(webpage)

	output = ''
	output += "[+] " + str(len(technologies)) + ' technologies detected by Wappalyzer!\n'
	output += "{:<20} {:<20} {:<20}".format('Technology','Version','Categories')
	output += "\n"
	
	for technology, details in technologies.items():
		output += " {:<20} {:<20} {:<20}".format(technology, ', '.join(details['versions']), ', '.join(details['categories']))
		output += "\n"

	output += "\n"
	output += "\n"
	return output

def builtwith_detector_gui(url):
	technologies = builtwith(url)
	technologies_counter = 0
	for category, technology in technologies.items():
		technologies_counter += len(technology)
	output = ''
	output += "[+] " + str(technologies_counter) + ' technologies detected by Builtwith!\n'
	output += "{:<50} {:<50}\n".format('Categories', 'Technologies')
	for category, technology in technologies.items():
		output += "{:<50} {:<50}".format(category, ', '.join(technology))
		output += '\n'
	
	return output

def detector_gui(url, service=2):
	if (not isValidURL(url)):
		return ('\n\n[-] URL is not valid\n')
	else:
		output = ''
		output += '\n\n[+] Scanning URL: ' + url + '\n'
		if(service == 0):
			output += wappalyzer_detector_gui(url)
		elif(service == 1):
			output += builtwith_detector_gui(url)
		else:
			output += wappalyzer_detector_gui(url)
			output += builtwith_detector_gui(url)

	global results

	results.delete(1.0,END)
	results.insert(1.0,output)

def run_detector_for_gui():
	global url_entry
	global service_variable
	url = url_entry.get()
	service = int(service_variable.get())
	if (isValidURL(url)):
		output = detector_gui(url, service)





# Function to validate URL
def isValidURL(str):

	regex = ("((http|https)://)(www.)?" +
			"[a-zA-Z0-9@:%._\\+~#?&//=]" +
			"{2,256}\\.[a-z]" +
			"{2,6}\\b([-a-zA-Z0-9@:%" +
			"._\\+~#?&//=]*)")
	

	p = re.compile(regex)


	if (str == None):
		return False

	if(re.search(p, str)):
		return True
	else:
		return False


def start(argv):
	banner()
	#extract parameters
	if len(sys.argv) < 2:
		usage()
		sys.exit()
	try:
		opts = {}		
		for i in range(0, len(argv), 2):
			if(argv[i] != '-g'):
				opts[argv[i]] =  argv[i+1]
			else:
				opts[argv[i]] =  True

	except :
		print ("Error in arguments")
		usage()
		sys.exit()

	url = 0 
	service = 2
	is_gui = False
	for opt in opts:
		if opt == '-g':
			is_gui = True
		elif opt == '-u':
			url = opts[opt]
		elif opt == '-s':
			service = int(opts[opt])

	try:
		if(is_gui):
			gui()
		if url == 0:
			print ("pass url")
			usage()
			sys.exit()
		else:
			detector_terminal(url, service)
	except Exception as e:
		print('Exception !!')
		print(e)


if __name__ == "__main__":
	try:
		start(sys.argv[1:])
	except KeyboardInterrupt:
		print ("KeyboardInterrupt Exception !! Bye :)")






















					