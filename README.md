# apk_challenge

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

## Installation
You can also install .deb package.
 ```bash
 dpkg -i apk_1.0_all.deb
 ```
After that the package's files will be stored in /usr/share/apk
and apk.service will be started.

I used python 3.8.5 for this package.
