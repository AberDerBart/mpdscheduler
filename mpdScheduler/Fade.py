import mpd
import time

def fade(client,fadeTime,startVol,endVol):
	"""fades for [fadeTime] seconds from [startVol] to [endVol] (synchronously)"""

	sleepInterval=fadeTime/float(abs(endVol-startVol))

	if(endVol > startVol):
		step=1
	elif(endVol < startVol):
		step=-1
	else:
		return

	print("Fading for "+str(fadeTime)+"s from volume at "+str(startVol)+"% to "+str(endVol)+"%")

	for vol in range(startVol, endVol, step):
		print("Setting volume to "+str(vol)+"%")
		client.setvol(vol)
		time.sleep(sleepInterval)
	print("Setting volume to "+str(endVol)+"%")
	client.setvol(endVol)
