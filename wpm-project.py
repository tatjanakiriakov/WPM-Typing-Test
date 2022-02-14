import curses #allows to do the styling in the terminal 
from curses import wrapper 
import time
import random 


def startScreen(stdscr):
	stdscr.clear() 
	stdscr.addstr( "Welcome to the Speed Typing Test") 
	stdscr.addstr( "\nPress any key to start the test!")
	stdscr.refresh() 
	stdscr.getkey()



def displayText(stdscr, old, current, wpm=0): #wpm=0 is an optional parameter, which means that i don't have to pass it 
		stdscr.addstr(old)
		stdscr.addstr(1, 0, f"WPM: {wpm}") # f allows us to embed python expressions directly into the string, in this case the {wpm}

		for i, char in enumerate(current):
			correct_char = old[i]

			#check if the char that was just typed in was correct and if it wasnt color it in red
			color = curses.color_pair(1)
			if char != correct_char:
				color = curses.color_pair(2)

			stdscr.addstr(0, i, char, color) #place current text on top of the old text


def load_text():
	with open("text.txt", "r") as file:
		lines = file.readlines()
		return random.choice(lines).strip() #randomly choose a random line of the file, strip removes all the white characters



def wpm_test(stdscr):
	oldtext = load_text()
	currenttext = []
	wpm = 0
	start_time = time.time() #tells us what the current time is when we started doing this, tells the "starting time"
	stdscr.nodelay(True) # do not delay waiting for a user to type sth --> if the user stops typing, the wpm are still counting on 


	while True:
		time_elapsed = max(time.time() - start_time, 1) #max function and the "1" helps us not to get a 0-division error
		wpm = round((len(currenttext) / (time_elapsed / 60)) / 5) #e.g. 30 characters in 30 seconds --> (30) / (30 / 60) --> wpm would be 60
															# divided by 5 means words per minute instead of characters per minute, we assume that the average word has 5 characters in a word
															# we use "round" to get a prettier number


		stdscr.clear()
		displayText(stdscr, oldtext, currenttext, wpm)
		stdscr.refresh()

		#checks if the user has typed the whole sentence correctly
		if "".join(currenttext) == oldtext: #takes a list as an argument and converts it to a string
			stdscr.nodelay(False)
			break


		#makes sure that the line "key = stdscr.getkey() doesnt crash and if it does we just continue"
		try:
			key = stdscr.getkey() 
		except:
			continue #brings us to the top of the while loop and skips everything underneath



		if ord(key) == 27: #ASCII representation, 27 means the escape key
			break

		if key in ("KEY_BACKSPACE", '\b', "\x7f"): #x7f is the backspace key, the three things all represent the backspace key
			if len(currenttext) > 0:
				currenttext.pop()
		elif len(currenttext) < len(oldtext): #means that we are not able to add more text than the old sentence 
			currenttext.append(key)




def main(stdscr): #standart source, allows us to write things on the screen 
	curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK) #colors of the text and background
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK) #colors of the text and background
	curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK) #colors of the text and background

	startScreen(stdscr)

	while True:
		wpm_test(stdscr)
		stdscr.addstr(2, 0, "you completed the text, press any key to continiue!")
		key = stdscr.getkey()

		if ord(key) == 27:
			break




wrapper(main)