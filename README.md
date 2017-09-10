
## Purpose

A script help me derush my bike camera by searching for 5 secondes black frame and copy the two previous minutes to a new file


## Instalation 


- Install pyton3.6
https://www.python.org/downloads/

- Install Ffmpeg
	- For Raspberry
	`sudo apt-get install ffmpeg`
	- For Mac
	`brew install ffmpeg`

Install required modules

```` python
python3.6 -m pip install moviepy
python3.6 -m pip install progress
python3.6 -m pip install watchdog
````


## Usage 

Create a folder for example : /home/derush
and then two folder inside TODO and DONE

- /home/derush/TODO
- /home/derush/DONE

The put you rush inside the TODO folder and run the script like that

``` python
python3.6 main.py /home/derush/

```

