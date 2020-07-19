# pi-alarm
An alarm clock running on a raspberry pi playing music from the network using Music Player Daemon (MPD), using a numpad as input and no screen. Written in Python

## development
I've developed this on windows. For that, you need to be running mpd.exe with a modified version of mpd.conf. Both are in the tools folder  
The tools folder also includes mpc for a simple way to control mpd without pi-alarm  
https://linux.die.net/man/5/mpd.conf  
https://www.musicpd.org/doc/mpc/html/  
https://python-mpd2.readthedocs.io/en/latest/  

## setup
- Install raspberry pi OS
- add file on ssd boot partition simply called "ssh" to enable ssh
- startup pi
- `ping raspberrypi` to find ip (was ipv6)
- `sudo vi /etc/dhcpcd.conf` and uncomment 2 suggested lines for static ip + change address to 192.168.1.3
- `sudo apt-get update`
- `sudo apt-get install mpd`
- `sudo vi /etc/mpd.conf`
	paste config (note that the user is pi)
- `sudo apt-get install python3-pip`
--- https://www.synology.com/en-global/knowledgebase/DSM/tutorial/File_Sharing/How_to_access_files_on_Synology_NAS_within_the_local_network_NFS
- enable NFS on NAS under File Services settings & add NFS permissions to backup folder
- sudo mkdir /mnt/nas_mp3
- create file /home/pi/.smb and add user and password details
	user=pi
	password=raspberry
- `sudo vi /etc/fstab`
	//192.168.1.2/Backup/MP3 /mnt/nas_mp3 cifs uid=1000,gid=1000credentials=/home/pi/.smb,iocharset=utf8,vers=1.0,noperm 0 0
- copy requirements.txt to linux-requirements.txt (line endings are broken, I think)
- `pip3 install -r ./linux-requirements.txt`
- `sudo apt-get install vlc`
- `sed -i 's/geteuid/getppid/' /usr/bin/vlc`
	enables vlc to run as root by fooling it (https://unix.stackexchange.com/questions/125546/how-to-run-vlc-player-in-root)
- turn volume up to % with "alsamixer"
---- note that it has to be run as root because the keyboard module in linux requires root
- create service with
	`sudo ln -s /home/pi/pi-alarm/pi_alarm.service /etc/systemd/system/pi_alarm.service`
- enable service to be run at boot with
	`sudo systemctl enable pi_alarm`
- `sudo reboot` or `systemctl start pi_alarm`
	check if it is running with `systemctl status pi_alarm`

## mpd config
### full version
See mpd.conf

### important parts (tabs to separate keys and values)
music_directory "/mnt/nas_mp3/"  
playlist_directory  "/mnt/nas_mp3/#mpd_playlists"  
log_file  "/var/log/mpd/mpd.log"  
sticker_file  "/var/lib/mpd/sticker.sql"  
user  "pi"  
#bind_to_address (commented!!!)  
audio_output {  
	type		"alsa"  
	name		"My ALSA Device"  
	device		"hw:0,0"	# optional usb output is 1,0. Keep 0,0 if using the Pi audio  
	mixer_type      "software"      # optional, used to be hardware  
	mixer_device	"default"	# optional  
	mixer_control	"PCM"		# optional  
	mixer_index	"0"		# optional  
}  
connection_timeout  "9999999" # Really long timeout of 115 days. You should touch play/pause at least once in that period, right...?  

### troubleshooting
manually control service with  
sudo systemctl stop mpd  
sudo systemctl start mpd  
sudo systemctl status mpd  
  
the mpd log may have root owner because mpd starts as root-ish and then switches to the specified pi user from the conf. chowning the file can help  
sudo chown pi:pi /var/log/mpd/mpd.log  