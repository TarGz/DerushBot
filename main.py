

from moviepy.editor import VideoFileClip, ImageClip
from progress.bar import ChargingBar
from progress.spinner import Spinner
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import datetime
import sys
import time
import glob
import os.path
from termcolor import colored, cprint
import shutil

class color:
	HEADER = '\033[95m'
	BLUE ='\033[94m'
	GREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

class Logger():
	def log(msg,decorator):
		print(decorator + msg + color.ENDC)

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if (bot.is_running == False): bot.checkForVideoInPath()

class DerushBot():
	version = "0.0.5"
	folder_todo = "/Users/julienterraz/Documents/_TarGz/DERUSH/TODO/"
	folder_done = "/Volumes/BIG/BIKING/_DONE/"
	folder_error = "/Users/julienterraz/Documents/_TarGz/DERUSH/ERROR/"
	folder_item = "/Users/julienterraz/Dropbox/Photos/BIKE/CABALANCEPASMAL/_DATABASE/_NEW/"
	is_running = False
	path=""



	def __init__(self):
		cprint("  _____  ______ _____  _    _  _____ _    _    ____   ____ _______ 	",'magenta',attrs=['bold'])
		cprint(" |  __ \|  ____|  __ \| |  | |/ ____| |  | |  |  _ \ / __ \__   __|	",'magenta',attrs=['bold'])
		cprint(" | |  | | |__  | |__) | |  | | (___ | |__| |  | |_) | |  | | | |   	",'magenta',attrs=['bold'])
		cprint(" | |  | |  __| |  _  /| |  | |\___ \|  __  |  |  _ <| |  | | | |   	",'magenta',attrs=['bold'])
		cprint(" | |__| | |____| | \ \| |__| |____) | |  | |  | |_) | |__| | | |   	",'magenta',attrs=['bold'])
		cprint(" |_____/|______|_|  \_\\_____/|_____/|_|  |_|  |____/ \____/  |_|   	",'magenta',attrs=['bold'])
		cprint("                                                                   	",'magenta',attrs=['bold'])
		                                                                   
		cprint("Version "+self.version, 'magenta', attrs=['bold','underline'])
		self.event_handler = MyHandler()
		self.observer = Observer()




	def listenToFolder(self,arg):
		# if len(arg) > 1:
		# 	folder_arg = arg[1]
		# 	if(os.path.isdir(folder_arg)):
				

				# self.setPath(folder_arg)	

				# Listen to new files added to the folder			
				self.observer.schedule(self.event_handler, self.folder_todo, recursive=False)
				self.observer.start()

				# Check video in the folder at script launch
				self.checkForVideoInPath()

				try:
					while True:
						time.sleep(1)
				except KeyboardInterrupt:
					self.observer.stop()
				self.observer.join()



		# 	else:
		# 		cprint('ERROR :'+folder_arg + " is not a valid path",'red')
		# else:
		#     cprint("ERROR : you should provide a path",'red')  

	# def setPath(self,folder_arg):
	# 	self.path = folder_arg
	# 	print(" ")
	# 	print("Working path is " + colored(self.path, 'green', attrs=['underline']))
	# 	self.createFolderIfNeeded(self.path)

	# def createFolderIfNeeded(self,path):
	# 	todo = path+self.folder_todo
	# 	if not os.path.exists(todo):
	# 		print("creating folder : " + colored(self.path, 'red', attrs=['reverse']))
	# 		os.makedirs(todo)
	# 	done = path+self.folder_done
	# 	if not os.path.exists(done):
	# 		print("I'm creating the folder : " + colored(done, 'red', attrs=['reverse']))
	# 		print("put your MP4 files inside")
	# 		os.makedirs(done)
	# 	error = path+self.folder_error
	# 	if not os.path.exists(error):
	# 		print("I'm creating the folder : " + colored(error, 'red', attrs=['reverse']))
	# 		print("check for file with issues here")
	# 		os.makedirs(error)

	def checkForVideoInPath(self):
		todo = glob.glob(self.folder_todo+"*.MP4")
		
		if(len(todo) > 0):
			vid = todo[0]
			finename = os.path.basename(vid)
			print(" ")
			print("Working on %s  " % colored(finename, 'blue', attrs=['underline']))
			
			print(" ")
			spinner = Spinner('Waiting for file... ')
			while True :
				filesize = os.path.getsize(vid)
				for x in range(0, 10):
					spinner.next()
					time.sleep(1)

				filesize2 = os.path.getsize(vid)
				if(filesize==filesize2):
					break
			self.is_running = True
			
			# try:
			
			repport = self.seekBlackFrame(finename)
			dest = self.folder_done+repport+"-"+finename
			print("\nWorking on "+finename + " is " +colored("finished", 'green', attrs=['reverse']) )

			# os.rename(vid,dest)
			shutil.move(vid,dest)

			# except:
			# 	e = sys.exc_info()
			# 	print("Error  :	" + colored(e, 'white',  'on_blue'))
			# 	print ("\nUnable work on : "+finename+"\n moving it to error folder")	
			# 	dest = self.path+self.folder_error+"-"+finename
			# 	os.rename(vid,dest)

			self.is_running = False



	def seekBlackFrame(self,videofile,gap=3,cduration=60):
		
		clip = VideoFileClip(self.folder_todo+videofile)
		fps= 1/gap
		nframes = clip.duration*fps # total number of frames used
		sequences=[]
		i=0
		blackframe=0
		report="minoritaire"


		#bar = ChargingBar(colored("Scanning for events", 'blue', attrs=['underline']), max=int(nframes))


		for frame in clip.iter_frames(fps,dtype=int,progress_bar=True):
			i = i + 1
			# bar.next()

			red = frame[400,:,0].max();
			green = frame[400,:,1].max();
			blue = frame[400,:,2].max();
			average=int((red+green+blue)/3)
			t = i / fps
			timestamp = str(datetime.timedelta(seconds=t))

			if(average>0):
				
				if(blackframe>0):
					blackframe=0
					report="majoritaire"
					clipbegin = t-cduration-gap
					if(clipbegin < 0): clipbegin = 0

					if(len(sequences)>0) : # Avoiding overlap 
						prevEndFrame = sequences[len(sequences)-1][1]
						# print("prevEndFrame" + str(prevEndFrame))
						if(clipbegin < prevEndFrame):
							clipbegin = prevEndFrame  + gap

					clipend = t-(gap*2)
					sequences.append([clipbegin,clipend])

			elif(average == 0): # DETECTING BLACK FRAME
				blackframe=blackframe+1
				
		# bar.finish()
		
		if(len(sequences)>0):
			print(" ")
			print("Sequences founds")
			print(sequences)
			print("I founded %s" % colored( str(len(sequences))+" majority repport", 'red', attrs=['reverse']) )
			for seq in sequences:
				clipbegin 		= seq[0]
				clipend 		= seq[1]
				clipbegin_str 	= time.strftime("%M%S", time.gmtime(clipbegin))
				clipend_str 	= time.strftime("%M%S", time.gmtime(clipend))
				begin_time 		= datetime.timedelta(seconds=clipbegin)
				new_filename 	= "%s%s-%s->%s.MP4" % (self.folder_item,videofile,clipbegin_str,clipend_str)
				#temp_audio 		= "%s%s-%s->%s.m4a" % (self.folder_item,videofile,clipbegin_str,clipend_str)
				newclip 		= clip.subclip(clipbegin,clipend)
				print(" ")
				print("Exporting video to  :  %s" % colored("%s-%s->%s.MP4" % (videofile,clipbegin_str,clipend_str), 'green', attrs=['reverse']))
				print(" ")
				newclip.write_videofile(new_filename,
					codec='libx264', 
					audio_codec='aac', 
					temp_audiofile='%stemp-audio.m4a' %(self.folder_item), 
					remove_temp=True,progress_bar=True,verbose=False)
		else:
			print(" ")
			print("Reckon as a   %s" % colored("minority repport", 'grey', attrs=['reverse']))
		return 	report


os.system('cls' if os.name == 'nt' else 'clear')
bot = DerushBot()
bot.listenToFolder(sys.argv)










