print("Derushbot V0.0.2")

from moviepy.editor import VideoFileClip, ImageClip
import datetime
import glob
import os.path

folder_todo = "TODO/"
folder_done = "DONE/"



def getFileList(path):
	print(path)
	todo = glob.glob(path+folder_todo+"*.MP4")
	print("%s MP4 files found in %s " % (len(todo),path+folder_todo))
	for vid in todo:
		print(vid)
		finename = os.path.basename(vid)
		print(finename)
		dest = path+folder_done+finename
		print(dest)
		seekBlackFrame(finename,path)
		os.rename(vid,dest)


def seekBlackFrame(videofile,path,gap=3,cduration=120):
	
	clip = VideoFileClip(path+folder_todo+videofile)
	fps= 1/gap
	nframes = clip.duration*fps # total number of frames used
	print("seekBlackFrame %s as %s frames" % (videofile, nframes))

	i=0
	blackframe=0
	for frame in clip.iter_frames(fps,dtype=int,progress_bar=False):
		i = i + 1

		red = frame[400,:,0].max();
		green = frame[400,:,1].max();
		blue = frame[400,:,2].max();
		average=int((red+green+blue)/3)
		time = i / fps
		timestamp = str(datetime.timedelta(seconds=time))

		if(average>0):
			
			if(blackframe>0):
				blackframe=0
				clipbegin = time-cduration-gap
				if(clipbegin < 0): clipbegin = 0
				clipend = time-(gap*2)
				print("Saving sublcip")
				print("clipbegin"+str(clipbegin))
				print("clipend"+str(clipend))

				new_filename = "%s%s->%s->%s.mp4" % (path,videofile,str(clipbegin),str(clipend))
				newclip = clip.subclip(clipbegin,clipend)
				newclip.write_videofile(new_filename)

			else:
				print("searching at "+timestamp+"s :"+str(average))

		elif(average == 0):
			blackframe=blackframe+1
			print("blackframe found at "+str(timestamp)+"s :"+str(average))



#seekBlackFrame("FILE0404.MP4","/Users/jterraz/Desktop/DERUSH/",3)
getFileList("/Users/jterraz/Desktop/DERUSH/")

