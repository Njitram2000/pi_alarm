init:
	pip install -r requirements.txt

run:
	python .\pi_alarm.py

mpd:
	cd .\tools\mpd-0.21.24\ && mpd.exe mpd.conf