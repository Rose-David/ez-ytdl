from pytube import YouTube
from youtubesearchpython import VideosSearch
import time
import sys

#User chooses download type, setting variable.
audioorvideo = input('Please select AUDIO, VIDEO, or QUIT: ').lower()
if 'q' in audioorvideo:
  print("Quitting...")
  time.sleep(1.5)
  sys.exit()
elif 'a' in audioorvideo:
  audioonly = True
  print("Audio Only Selected, Proceeding...")
  time.sleep(.5)
elif 'v' in audioorvideo or not audioorvideo:
  audioonly = False
  print("Audio and Video Tracks Selected, Proceeding...")
  time.sleep(.25)
else:
  print("Invalid Option, Quitting!")
  time.sleep(3)
  sys.exit()

#User chooses retrieval type
linkorsearch = input("Please choose LINK, SEARCH or QUIT: ").lower()
time.sleep(.25)
if 'l' in linkorsearch:
  #ask for the link from user
  link = input("Enter the link of YouTube video you want to download: ")
  yt = YouTube(link)
elif 'q' in linkorsearch:
  print("Quitting...")
  time.sleep(1.5)
  sys.exit()
elif 's' in linkorsearch or not linkorsearch:
  #print("This function is not yet supported, quitting...")
  #time.sleep(3)
  #sys.exit()
  query = input('Input Search Query: ')
  searchResults = VideosSearch(query, limit=2)
  print(searchResults.result()['result'][0]['link'])
  yt=YouTube(searchResults.result()['result'][0]['link'])
  print('Using link',searchResults.result()['result'][0]['link']+', Proceeding...')
else:
  print("Invalid Option, Quitting!")
  time.sleep(3)
  sys.exit()
  
time.sleep(.25)

if audioonly:
  ys = yt.streams.get_audio_only()
else:
  while True:
    try:
      resolution = input('Please Choose MAX, MIN, or OTHER: ').lower().strip()
      if "max" in resolution or not resolution:
        print('Working...')
        ys = yt.streams.get_highest_resolution()
        print("Maximum resolution is", yt.streams.order_by('resolution')[-1].resolution+', proceeding...')
        break
      elif 'min' in resolution:
        print('Working...')
        ys=yt.streams.get_lowest_resolution()
        print("Minimum Resolution is", yt.streams.order_by('resolution')[1].resolution + ', Proceeding...')
        break
      elif 'o' in resolution:
        print('Working...')
        availableResolutions=[]
        i=0
        resDict = {'144p':None, '240p':None, '360p':None, '480p':None, '720p':None, '1080p':None, '1440p':None, '2160p':None}
        for x in yt.streams.order_by('resolution').filter(only_audio=False,only_video=False):
          print(x.resolution)
          print(x.itag)
          resDict[x.resolution] = x.itag
          availableResolutions.append(x.resolution)
          i+=1
        availableResolutions=list(dict.fromkeys(availableResolutions))
        print('Available Resolutions Are:',availableResolutions)
        resolution=input('Please Choose a Resolution Now: ')
        print(resDict)
        ys=yt.streams.get_by_itag(resDict[resolution])
        break
      else:
        print(resolution,'Confirmed, Proceeding...')
        ys=yt.streams.filter(res=resolution)[0]
        break
    except AttributeError:
      print('Invalid Resolution, remember maximum manual res is 720p!')



time.sleep(.25)

#Showing details to user to confirm correct stream
print("Title:",yt.title)
print('By:',yt.author)
print("Views:",yt.views)
print("Length:",yt.length,'seconds')
print("Rating:",yt.rating)
print('Filesize:',ys.filesize,'bytes')
print('Contains audio track:',ys.includes_audio_track)
print('Contains video track:',ys.includes_video_track)
confirm = input("Is this correct? ").lower()
if 'y' in confirm or 't' in confirm or not confirm:
  print("Download confirmed, continuing...")
else:
  print('Exiting...')
  time.sleep(2)
  sys.exit()

time.sleep(.25)

#Starting download
print("Downloading",ys.default_filename)
ys.download()
print("Download completed!!")
time.sleep(1.5)
print('Exiting...')
time.sleep(.5)