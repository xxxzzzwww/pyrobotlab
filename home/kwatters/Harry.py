from java.lang import String
import threading
from org.myrobotlab.opencv import OpenCVFilterTranspose
from org.myrobotlab.opencv import OpenCVFilterFaceRecognizer

#############################################################
# This is the Harry script
# Harry is an InMooved powered by a Ras PI2
# Initially we'll start simple
# It will use ProgramAB & Webkit for all interactions with
# the bot.
#############################################################
# All bot specific hardware configuration goes here.
leftPort = "/dev/ttyACM0"
rightPort = "/dev/ttyACM1"
headPort = leftPort

gesturesPath = "/home/pi/github/pyrobotlab/home/kwatters/harry/gestures"
calibrationPath = "/home/pi/github/pyrobotlab/home/kwatters/harry/calibration.py"

aimlPath = "/home/pi/github/pyrobotlab/home/kwatters/harry"
aimlBotName = "harry"
aimlUserName = "Kevin"
botVoice = "Rod"

# toggle to only load program ab  and skip the inmoov services
startInMoov = True

######################################################################
# helper function help debug the recognized text from webkit/sphinx
######################################################################
def heard(data):
  print "Speech Recognition Data:"+str(data)

######################################################################
#
# MAIN ENTRY POINT  - Start and wire together all the services.
#
######################################################################

# launch the swing gui?
# gui = Runtime.createAndStart("gui", "GUIService");

######################################################################
# Create ProgramAB chat bot ( This is the inmoov "brain" )
######################################################################
harry = Runtime.createAndStart("harry", "ProgramAB")
harry.setPath(aimlPath)
harry.startSession(aimlUserName, aimlBotName)

######################################################################
# Html filter to clean the output from programab.  (just in case)
htmlfilter = Runtime.createAndStart("htmlfilter", "HtmlFilter")

######################################################################
# mouth service, speech synthesis
mouth = Runtime.createAndStart("i01.mouth", "NaturalReaderSpeech")
mouth.setVoice(botVoice)

######################################################################
# the "ear" of the inmoov TODO: replace this with just base inmoov ear?
ear = Runtime.createAndStart("i01.ear", "WebkitSpeechRecognition")
ear.addListener("publishText", python.name, "heard");
ear.addMouth(mouth)

######################################################################
# MRL Routing webkitspeechrecognition/ear -> program ab -> htmlfilter -> mouth
######################################################################
ear.addTextListener(harry)
harry.addTextListener(htmlfilter)
htmlfilter.addTextListener(mouth)

######################################################################
# Start up the inmoov and attach stuff.
######################################################################
i01 = Runtime.createAndStart("i01", "InMoov")
i01.setMute(True)
if startInMoov:
  i01.startAll(leftPort, rightPort)
else:
  i01.mouth = mouth
    
# Harry doesn't have a forward servo, but i'm adding it here as a 
# place holder
forwardServo = Runtime.start("forwardServo","Servo")

######################################################################
# Launch the web gui and create the webkit speech recognition gui
# This service works in Google Chrome only with the WebGui
#################################################################
# webgui = Runtime.createAndStart("webgui","WebGui")

######################################################################
# END MAIN SERVICE SETUP SECTION
######################################################################


######################################################################
# Helper functions and various gesture definitions
######################################################################

# some globals that are used by the gestures..  (they shouldn't be!)
isRightHandActivated = True
isLeftHandActivated = True
isRightArmActivated = True
isLeftArmActivated = True
isHeadActivated = True
isTorsoActivated = True
isEyeLidsActivated = False

i01.loadGestures(gesturesPath)

sleep(1)

i01.loadCalibration(calibrationPath)


# Open CV calibrati0n

# i01.opencv.setFrameGrabberType("org.bytedeco.javacv.FFmpegFrameGrabber")
# i01.opencv.setInputSource("imagefile")
# i01.opencv.setInputFileName("/dev/video0")

i01.opencv.setFrameGrabberType("org.myrobotlab.opencv.MJpegFrameGrabber")
i01.opencv.setInputFileName("http://192.168.4.117:8080/?action=stream")
i01.opencv.setInputSource("network")
# i01.opencv.setStreamerEnabled(False)

# add 3 transposes..  would be nice to add one going counter clock.
tr1 = OpenCVFilterTranspose("tr1")
tr2 = OpenCVFilterTranspose("tr2")
tr3 = OpenCVFilterTranspose("tr3")

i01.opencv.addFilter(tr1)
i01.opencv.addFilter(tr2)
i01.opencv.addFilter(tr3)

i01.opencv.capture()
# face recognizer
# fr = OpenCVFilterFaceRecognizer("fr")
# i01.opencv.addFilter(fr)
# fr.load("/home/pi/github/pyrobotlab/home/kwatters/harry/faceModel.bin")
 

# now start the webgui
webgui = Runtime.create("webgui", "WebGui")

webgui.autoStartBrowser(False)
webgui.startService()
webgui.startBrowser("http://localhost:8888/#/service/i01.ear")


gui.undockTab("python")
gui.undockTab("i01.opencv")


i01.headTracking.pid.setPID("x", 25,5.0,1.0)
i01.headTracking.pid.setPID("y", 50,5.0,1.0)

i01.head.rothead.rest()
i01.head.neck.rest()

trackHumans()



