

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
import subprocess

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
	version = "0.0.7"
	folder_todo = "/Users/julienterraz/Documents/_TarGz/DERUSH/TODO/"
	folder_done = "/Users/julienterraz/Documents/_TarGz/DERUSH/DONE/"
	folder_error = "/Users/julienterraz/Documents/_TarGz/DERUSH/ERROR/"
	folder_item = "/Volumes/YELLOW/Dropbox/Photos/BIKE/CABALANCEPASMAL/_DATABASE/_NEW/"
	is_running = False
	path=""



	def __init__(self):
		cprint("  _____  ______ _____  _    _  _____ _    _  ____   ____ _______ 	",'magenta',attrs=['bold'])
		cprint(" |  __ \|  ____|  __ \| |  | |/ ____| |  | ||  _ \ / __ \__   __|	",'magenta',attrs=['bold'])
		cprint(" | |  | | |__  | |__) | |  | | (___ | |__| || |_) | |  | | | |   	",'magenta',attrs=['bold'])
		cprint(" | |  | |  __| |  _  /| |  | |\___ \|  __  ||  _ <| |  | | | |   	",'magenta',attrs=['bold'])
		cprint(" | |__| | |____| | \ \| |__| |____) | |  | || |_) | |__| | | |   	",'magenta',attrs=['bold'])
		cprint(" |_____/|______|_|  \_\\_____/|_____/|_|  |_||____/ \____/  |_|   ",'magenta',attrs=['bold'])
		cprint("                                                                   	",'magenta',attrs=['bold'])
		                                                                   
		cprint("Version "+self.version, 'magenta', attrs=['bold','underline'])
		self.event_handler = MyHandler()
		self.observer = Observer()




	def listenToFolder(self,arg):

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


	def checkForVideoInPath(self):
		todo = glob.glob(self.folder_todo+"*.MP4")
		
		if(len(todo) > 0):
			vid = todo[0]
			file = os.path.basename(vid)
			videoID, file_extension = os.path.splitext(file)
			print(" ")
			print("Working on %s  " % colored(file, 'blue', attrs=['underline']))
			print("videoID %s  " % colored(videoID, 'blue', attrs=['underline']))
			print("file_extension %s  " % colored(file_extension, 'blue', attrs=['underline']))
			
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
			
			try:
				report = self.seekBlackFrame(file)
				dest = self.folder_done+videoID+"-"+report+file_extension
				print("\nWorking on "+file + " is " +colored("finished", 'green') )

				shutil.move(vid,dest)

			except:
				e = sys.exc_info()
				print("Error  :	" + colored( e, 'red') )
				print ("\nUnable work on : "+file+"\n moving it to error folder")	
				dest = self.path+self.folder_error+"-"+file
				os.rename(vid,dest)


				log_file_txt = open(dest+".log", "w")
				log_file_txt.write(format(e))
				log_file_txt.close()

			self.is_running = False



	def seekBlackFrame(self,videofile,gap=3,cduration=60):
		
		clip = VideoFileClip(self.folder_todo+videofile)
		fps= 1/gap
		nframes = clip.duration*fps # total number of frames used
		sequences=[]
		i=0
		blackframe=0
		report="minoritaire"

		for frame in clip.iter_frames(fps,dtype=int,progress_bar=True):
			i = i + 1
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
					if(clipbegin < 0): clipbegin = 2

					if(len(sequences)>0) : # Avoiding overlap 
						pre_end_time = (sequences[len(sequences)-1][1])
						begin_time = datetime.timedelta(seconds=clipbegin)
						if(begin_time < pre_end_time):
							clipbegin = pre_end_time # TODO : Add gap  
					clipend = t-(gap*2)

					begin_time = datetime.timedelta(seconds=clipbegin)
					end_time = datetime.timedelta(seconds=clipend)
					sequences.append([(begin_time),(end_time)])

			elif(average == 0): # DETECTING BLACK FRAME
				blackframe=blackframe+1
				
		# bar.finish()
		
		if(len(sequences)>0):
			print(" ")
			print("Sequences founds")
			print(sequences)
			print("I founded %s" % colored( str(len(sequences))+" majority repport", 'red') )
			for seq in sequences:
				begin_time 		= str(seq[0])
				end_time 		= str(seq[1])
				print("begin_time",begin_time)
				print("end_time",end_time)
				new_filename 	= "%s%s-%s->%s.MP4" % (self.folder_item,videofile,begin_time,end_time)
				# FFMEPG
				print("Exporting video to  :  %s" % colored("%s-%s->%s.MP4" % (videofile,begin_time,end_time), 'green'))
				print(" ")
				os.chdir(self.folder_todo)
				try:
				    subprocess.check_output([ 'ffmpeg','-ss',begin_time,'-i',videofile,'-to','0:01:00','-c','copy',new_filename])
				    # subprocess.check_output([ 'ffmpeg','-ss',begin_time,'-i',videofile,'-to',end_time,'-c','copy',new_filename], stderr=subprocess.STDOUT)
				except subprocess.CalledProcessError:
					e = sys.exc_info()
					print("Error  :	" + colored( str(len(e)), 'red', attrs=['reverse']) )
					print ("\nUnable to ffmpeg : "+videofile+"\n !")	

		else:
			print(" ")
			print("Reckon as a   %s" % colored("minority repport", 'red'))
		return 	report


os.system('cls' if os.name == 'nt' else 'clear')
bot = DerushBot()
bot.listenToFolder(sys.argv)










