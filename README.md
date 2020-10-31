# apk_challenge
This package is a challenge test from Amn Pardazan Kavir. This service stores excess index documents from Elasticsearch into syslog and then deletes them from Elasticsearch.

Use the package manager pip to install requirements.txt

```bash
pip3 install -r requirements.txt
```

To run this package use the command below.

```bash
python main.py -C [config file address] -H [remote syslogserver ip]
```

For using this project as a systemd service, make a file in /etc/systemd/system and write these into it.

```bash
[Unit]
Description=APK Service
After=multi-user.target
Conflicts=getty@tty1.service

[Service]
ExecStart=/usr/bin/python3  <ABSOLUTE PATH OF main.py>

[install]
WantedBy=multi-user.target
```
then run this commands.

```bash
systemctl daemon-reload
systemctl enable apk.service
systemctl start apk.service
```
You can update config file by this command.
```bash
curl -XPOST -H 'Content-Type=application/json' 127.0.0.1:3000/configapi -d '{DATA IN JSON FORMAT}'
```

## Installation
You can also install .deb package.
 ```bash
 dpkg -i apk_1.0_all.deb
 ```
After that the package's files will be stored in /usr/share/apk
and apk.service will be started.

I used python 3.8.5 for this package.
