#!/usr/bin/env python

from hermes_python.hermes import Hermes
import sys
import soco
import pprint

zones = list(soco.discover())

def dump():
	pp = pprint.PrettyPrinter(indent=4)
	zones =soco.discover()
	for z in zones:
		print '======================'
		pp.pprint(z.player_name)
		print "coordinator: " + str(z.is_coordinator)
		print "bridge: " + str(z.is_bridge)
		pp.pprint(z.get_speaker_info())
		pp.pprint(z.get_current_transport_info())
		pp.pprint(z.get_current_track_info())

		print "group:"
		pp.pprint(z.group)

def music_handler_resume(hermes,intentMessage):
	try:
		#dump()
		hermes.publish_end_session(intentMessage.session_id, "")
		#if the Snips intent has a value for the device_name slot, start only the designated player
	        if len(intentMessage.slots.device_name)>0:
        	        device_name = intentMessage.slots.device_name[0].slot_value.value.value
			print "start: " + device_name
	                try:
        	                device = soco.discovery.by_name(device_name)
                	        status = device.get_current_transport_info()
                        	if status['current_transport_state'] != 'PLAYING':

					#find if a device is already playing; if yes, join it
					for zone in zones:
						status = zone.get_current_transport_info()
						if status['current_transport_state'] == 'PLAYING':
							print '...join: ' + zone.player_name
							device.join(zone)
							device.play()
							break

		                        device.play()
        	        except:
                	        print sys.exc_info()

		#else start in party mode
		else:
			try:
				print "playing all devices in party mode"
				#dump()
				zones = soco.discover()
				for z in zones:
					try:
						if (z.is_coordinator):
							print "set party mode from zone:" + z.player_name
							z.partymode()
							z.play()
							break
					except:
						print sys.exc_info()

			except:
				print sys.exc_info()
	except:
		print sys.exec_info()

def music_handler_pause(hermes,intentMessage):
	#dump()

	hermes.publish_end_session(intentMessage.session_id, "")

	#stop designated device(s) if there is something in the device_name slot
	if len(intentMessage.slots.device_name)>0:
		device_name = intentMessage.slots.device_name[0].slot_value.value.value
		#for attr in dir(device_name):
		#	print("obj.%s = %r" % (attr,getattr(device_name,attr)))
		print 'pause: ' + device_name
		try:
			device = soco.discovery.by_name(device_name)

#			if not device.is_coordinator:
			device.unjoin()

			device.pause()

		except: #soco.exceptions.SoCoException:
			print sys.exc_info() #soco.exceptions.SoCoException

	#stop all devices
	else:
		print 'pause all devices'
	        for zone in zones:
			try:
				if (zone.is_coordinator):
					zone.pause()
			except:
				print sys.exc_info()

def music_handler_volume_up(hermes,intentMessage):
	hermes.publish_end_session(intentMessage.session_id, "")
	for zone in zones:
		try:
			if len(intentMessage.slots.volume_higher)>0:
				volume = intentMessage.slots.volume_higher.first().value
			else:
				volume = 5

			#prevent accidental increasing of volume by a large number
			if (volume>20):
				volume = 20

			zone.volume += volume
		except:
			print sys.exc_info()

def music_handler_volume_down(hermes,intentMessage):
	hermes.publish_end_session(intentMessage.session_id, "")
	for zone in zones:
		try:
                        if len(intentMessage.slots.volume_lower)>0:
                                volume = intentMessage.slots.volume_lower.first().value
			else:
				volume = 5
			zone.volume -= volume
		except:
			print sys.exc_info()

def music_handler_next(hermes,intentMessge):
	hermes.publish_end_session(intentMessage.session_id, "")
	for zone in zones:
		try:
			if (zone.is_coordinator):
				zone.next()
		except:
			print sys.exc_info()

def music_handler_radio(hermes,intentMessage):
	hermes.publish_end_session(intentMessage.session_id, "")
	try:
		sonos.turn_on_radio("arnaud #4")
	except:
		print sys.exc_info()

if __name__ == "__main__":
	print "started SONOS snips handler"
	with Hermes("localhost:1883") as h:
		h.subscribe_intent("arnadu:resumeMusic",music_handler_resume) \
		.subscribe_intent("arnadu:speakerInterrupt",music_handler_pause) \
		.subscribe_intent("arnadu:volumeUp",music_handler_volume_up) \
		.subscribe_intent("arnadu:volumeDown",music_handler_volume_down) \
		.subscribe_intent("arnadu:nextSong",music_handler_next) \
		.subscribe_intent("arnadu:radioOn",music_handler_radio) \
		.start()


