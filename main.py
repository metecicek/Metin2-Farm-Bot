import cv2
import os
import time
import pydirectinput

from ekranyakala import ekranYakala
from vision import Vision


os.chdir(os.path.dirname(os.path.abspath(__file__)))

# WINDOW FIND
baslik = (
    "Rohan2 - İlk Günkü Tutku ile! | Discord : https://discord.gg/sGJhpvG",
    "Rohan2 - Tüm Teçhizatlarını Son Seviyeye Getir! | Forum: https://board.rohan2.global",
)

wincap = None
for i in baslik:
    try:
        wincap = ekranYakala(i)
        print("Pencere bulundu:", i)
        break
    except:
        continue

if not wincap:
    raise Exception("Window not found")

# DETECTOR
cascade = cv2.CascadeClassifier(os.path.join(os.getcwd(), "cascade", "cascade.xml"))
vision = Vision(None)

# STATE MACHINE
STATE = "SEARCH"
target = None
last_move_time = 0


def move_to_target(t):
    """
    HOLD MOVEMENT (kritik fix)
    """
    pydirectinput.moveTo(t[0], t[1])
    time.sleep(0.1)


def attack():
    """
    stable click attack
    """
    pydirectinput.click()
    time.sleep(1.2)


def explore():
    """
    real movement simulation (E/F spam yerine)
    """
    pydirectinput.keyDown("w")
    time.sleep(0.4)
    pydirectinput.keyUp("w")

    # random turn (camera değil movement assist)
    pydirectinput.moveRel(30, 0)
    time.sleep(0.1)


print("AI STARTED")

while True:

    frame = wincap.get_screenshot()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    rects = cascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5
    )

    cv2.imshow("view", frame)

    # =========================
    # STATE MACHINE
    # =========================

    if STATE == "SEARCH":

        if len(rects) > 0:
            points = vision.get_click_points(rects)
            target = wincap.get_screen_position(points[0])
            STATE = "MOVE"

        else:
            explore()

    elif STATE == "MOVE":

        if target:
            move_to_target(target)
            STATE = "ATTACK"

    elif STATE == "ATTACK":

        attack()
        STATE = "SEARCH"

    # EXIT
    if cv2.waitKey(1) == ord("q"):
        break

cv2.destroyAllWindows()