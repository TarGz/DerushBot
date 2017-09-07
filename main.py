print("Derushbot V0.0.1")

from moviepy.editor import VideoFileClip, ImageClip
import datetime
#clip = VideoFileClip("sample.mp4")
clip = VideoFileClip("sample2.MP4")
gap=3
fps= 1/gap
cduration=30
nframes = clip.duration*fps # total number of frames used
print(nframes)
#total_image = sum(clip.iter_frames(fps,dtype=float,progress_bar=True))

# for frame in clip.iter_frames(fps,dtype=float,progress_bar=True):
# 	# print(frame[0,:,0])
# 	# print(frame[0,:,0].max())
# 	print(frame[0,:,0])
# 	print(frame[1,:,1])
# 	print(frame[2,:,2])


#print("Total image : {}".format(total_image))
#1average_image = ImageClip(total_image/ nframes)
#average_image.save_frame("output.png")



i=0
blackframe=0
for frame in clip.iter_frames(fps,dtype=int,progress_bar=False):
	i = i + 1
	# print(frame[0,:,0])
	# print(frame[0,:,0].max())
	red = frame[400,:,0].max();
	# print(red)
	green = frame[400,:,1].max();
	# print(green.sum())
	blue = frame[400,:,2].max();
	# print(blue)
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

			new_filename = "sample2->%s->%s.mp4" % (str(clipbegin),str(clipend))
			newclip = clip.subclip(clipbegin,clipend)
			newclip.write_videofile(new_filename)

		else:
			print("searching at "+timestamp+"s :"+str(average))

	elif(average == 0):
		blackframe=blackframe+1
		print("blackframe found at "+str(timestamp)+"s :"+str(average))





