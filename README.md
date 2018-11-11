# snips-sonos-skill
Handler code to interact with a SONOS system through a SNIPS chatbot

Still very buggy :-)

The SNIPS skill is available at:
https://console.snips.ai/store/en/skill_E6bDzoEgkV02

References:<br>
https://snips.gitbook.io/getting-started/
<br>
https://github.com/SoCo/SoCo

This library should be installed in /var/lib/snips/skills/snips-sonos-skill
<br>Run ./setup.sh to create the python virtual environment in venv

It uses the SOCO library, which should be installed separately. 

The code will be automaticall called through snips-skill-server. 
<br>In order to run it manually and debug:
<br>sudo systemctl stop snips-skill-server
<br>source venv/bin/activate
<br>./action-sonos.py

The program listens to SNIPS's message queue and handles commands to control a SONOS music system.
