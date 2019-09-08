import tkinter
import cv2
import PIL.Image, PIL.ImageTk
from functools import partial
import threading
import imutils
import time

SET_WIDTH = 650  # width of frame
SET_HEIGHT = 368  # height of frame
stream = cv2.VideoCapture("clip.mp4")


# function section that handle all process
def frame_over():
    canvas.create_text(325, 159, fill="red", font="Times 45 italic bold", text="Video Finished !")


def flashcolour(colour_index):
    colors = ('black', 'red')
    canvas.create_text(150, 30, fill=colors[colour_index], font="Times 26 italic bold", text="Decision Pending")
    canvas.after(500, flashcolour, 1 - colour_index)


def play_normal():
    grabbed, frame = stream.read()
    if not grabbed:
        frame_over()
    else:
        image_fetch(frame, "nvideo")
        flashcolour(0)


def re_play_normal():
    stream.set(cv2.CAP_PROP_POS_FRAMES, 0)
    play_normal()


def play(speed):  # function of controlling video speed
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1+speed)
    grabbed, frame = stream.read()
    if not grabbed:
        frame_over()
    else:
        image_fetch(frame, "video")
        flashcolour(0)


def image_fetch(imagename, type):
    if type == 'image':
        frame = cv2.cvtColor(cv2.imread(f"{imagename}.png"), cv2.COLOR_BGR2RGB)  # display the image screeb
    else:
        frame = imagename

    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)

    if type == 'nvideo':
        canvas.after(10, play_normal)


def pending(decision):
    # display decision pending screen first, then wait for some time and give actual decision
    image_fetch("pending", 'image')  # decision pending screen
    time.sleep(3)  # wait for some time to display the decision
    image_fetch("sponsor", 'image')  # sponsor screen
    time.sleep(2)  # wait for some time to display the decision
    image_fetch(decision, 'image')  # decision screen


def out():  # function that gives output screen
    thread = threading.Thread(target=pending, args=("out",))  # make a thread so program will not break and the function call the pending function
    thread.daemon = 1
    thread.start()


def not_out():  # function that gives not out screen
    thread = threading.Thread(target=pending, args=("not_out",))  # make a thread so program will not break and the function call the pending function
    thread.daemon = 1
    thread.start()


window = tkinter.Tk()  # tkinter gui start from here.
window.title("DRS System By Sagar Davara")
cv_img = cv2.cvtColor(cv2.imread("welcome.png"), cv2.COLOR_BGR2RGB)

# canvas section
canvas = tkinter.Canvas(window, width=SET_WIDTH, height=SET_HEIGHT)
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))  # read image from opencv with array
image_on_canvas = canvas.create_image(0, 0, anchor=tkinter.NW, image=photo)  # put image on canvas
canvas.pack()

# button that control DRS
btn = tkinter.Button(window, text="PLay Normal", width=50, command=play_normal)
btn.pack()
btn = tkinter.Button(window, text="Re-PLay Normal", width=50, command=re_play_normal)
btn.pack()
btn = tkinter.Button(window, text="<< Previous (fast)", width=50, command=partial(play, -6))
btn.pack()
btn = tkinter.Button(window, text="<< Previous (slow)", width=50, command=partial(play, -2))
btn.pack()
btn = tkinter.Button(window, text="Next (slow) >>", width=50, command=partial(play, 2))
btn.pack()
btn = tkinter.Button(window, text="Next (fast) >>", width=50, command=partial(play, 6))
btn.pack()
btn = tkinter.Button(window, text="Give Out", width=50, command=out)
btn.pack()
btn = tkinter.Button(window, text="Give Not Out", width=50, command=not_out)
btn.pack()
window.mainloop()
