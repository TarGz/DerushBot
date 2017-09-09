

from moviepy.editor import VideoFileClip, ImageClip
from progress.bar import ChargingBar
import datetime
import sys
import time
import glob
import os.path

folder_todo = "TODO/"
folder_done = "DONE/"



def createfolderifneeded(path):
	todo = path+folder_todo
	if not os.path.exists(todo):
		print("creating folder : " + todo)
		os.makedirs(todo)
	done = path+folder_done
	if not os.path.exists(done):
		print("I'm creating the folder : " + done)
		print("put your MP4 files inside")
		os.makedirs(done)

def getFileList(path):
	print(path)
	todo = glob.glob(path+folder_todo+"*.MP4")
	print("%s MP4 files found in %s " % (len(todo),path+folder_todo))
	for vid in todo:
		# print(vid)
		finename = os.path.basename(vid)
		# print(finename)
		repport = seekBlackFrame(finename,path)
		dest = path+folder_done+repport+"-"+finename
		# print(dest)
		
		os.rename(vid,dest)



def seekBlackFrame(videofile,path,gap=3,cduration=120):
	
	clip = VideoFileClip(path+folder_todo+videofile)
	fps= 1/gap
	nframes = clip.duration*fps # total number of frames used
	print("seekBlackFrame %s as %s frames" % (videofile, nframes))
	sequences=[]
	i=0
	blackframe=0
	report="minoritaire"
	bar = ChargingBar('Searching black frames in '+videofile, max=int(clip.duration*fps))


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
		print("founded "+str(len(sequences)) +" black frame")
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


# getFileList("/Users/jterraz/Desktop/DERUSH/")

print("Derushbot V0.0.2")



if len(sys.argv) > 1:
	folder_arg = sys.argv[1]
	if(os.path.isdir(folder_arg)):
		createfolderifneeded(folder_arg)
		getFileList(folder_arg)
	else:
		print(folder_arg + " is not a valid path")
else:
    print("you should provide a path")  






