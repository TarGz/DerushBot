

from moviepy.editor import VideoFileClip, ImageClip
from progress.bar import ChargingBar
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import datetime
import sys
import time
import glob
import os.path



class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print ("Folder event")
        if (bot.is_running == False): bot.checkForVideoInPath()

class DerushBot():
	version = "0.0.3"
	folder_todo = "TODO/"
	folder_done = "DONE/"
	is_running = False
	path=""

	def __init__(self):
		print("DerushBot "+self.version)
		self.event_handler = MyHandler()
		self.observer = Observer()

	def listenToFolder(self,arg):
		if len(arg) > 1:
			folder_arg = arg[1]
			if(os.path.isdir(folder_arg)):
				

				self.setPath(folder_arg)	

				# Listen to new files added to the folder			
				self.observer.schedule(self.event_handler, folder_arg+self.folder_todo, recursive=False)
				self.observer.start()

				# Check video in the folder at script launch
				self.checkForVideoInPath()

				try:
					while True:
						time.sleep(1)
				except KeyboardInterrupt:
					self.observer.stop()
				self.observer.join()



			else:
				print(folder_arg + " is not a valid path")
		else:
		    print("you should provide a path")  

	def setPath(self,folder_arg):
		self.path = folder_arg
		print("Working path is "+self.path)
		self.createFolderIfNeeded(self.path)

	def createFolderIfNeeded(self,path):
		todo = path+self.folder_todo
		if not os.path.exists(todo):
			print("creating folder : " + todo)
			os.makedirs(todo)
		done = path+self.folder_done
		if not os.path.exists(done):
			print("I'm creating the folder : " + done)
			print("put your MP4 files inside")
			os.makedirs(done)

	def checkForVideoInPath(self):
		todo = glob.glob(self.path+self.folder_todo+"*.MP4")
		
		if(len(todo) > 0):
			vid = todo[0]
			finename = os.path.basename(vid)
			print("Found a job !! I'm working on %s  " % (finename))
			while True :
				filesize = os.path.getsize(vid)

				time.sleep(2)
				filesize2 = os.path.getsize(vid)

				if(filesize==filesize2):
					print("%s is ready to be analysed" % (finename))
					break
			self.is_running = True
			

			repport = self.seekBlackFrame(finename,self.path)
			dest = self.path+self.folder_done+repport+"-"+finename

			print("Work on %s is is done, i'm moving the file to %s" % (finename,dest))
			os.rename(vid,dest)
			self.is_running = False



	def seekBlackFrame(self,videofile,path,gap=3,cduration=120):
		
		clip = VideoFileClip(path+self.folder_todo+videofile)
		fps= 1/gap
		nframes = clip.duration*fps # total number of frames used
		print("%s as %s frames" % (videofile, int(nframes)))
		sequences=[]
		i=0
		blackframe=0
		report="minoritaire"
		bar = ChargingBar('Searching for event in '+videofile, max=int(clip.duration*fps))


		for frame in clip.iter_frames(fps,dtype=int,progress_bar=False):
			i = i + 1
			bar.next()

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
					clipend = t-(gap*2)
					# print("Saving sublcip")
					# print("clipbegin : "+str(clipbegin))
					# print("clipend : "+str(clipend))

					sequences.append([clipbegin,clipend])

			elif(average == 0): # DETECTING BLACK FRAME
				blackframe=blackframe+1
				
		bar.finish()
		
		if(len(sequences)>0):
			print("I found "+str(len(sequences)) +" Events in " + videofile)
			for seq in sequences:
				clipbegin = seq[0]
				clipend = seq[1]
				# print("extractSequences clipbegin : "+str(clipbegin))
				# print("extractSequences clipend : "+str(clipend))
				clipbegin_str = time.strftime("%M%S", time.gmtime(clipbegin))
				clipend_str = time.strftime("%M%S", time.gmtime(clipend))
				# print("clipbegin_str:"+clipbegin_str)
				# print("clipend_str:"+clipend_str)
			
				begin_time = datetime.timedelta(seconds=clipbegin)
				new_filename = "%s%s-%s->%s.MP4" % (path,videofile,clipbegin_str,clipend_str)
				newclip = clip.subclip(clipbegin,clipend)
				newclip.write_videofile(new_filename,
					codec='libx264', 
					audio_codec='aac', 
					temp_audiofile='temp-audio.m4a', 
					remove_temp=True)
		return 	report



bot = DerushBot()
bot.listenToFolder(sys.argv)








