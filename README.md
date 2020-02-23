# Raspi

My Raspberry Pi playground.

## Lessons Learned

- button
    - connect input to a 3.3V pin, not a 5.0V pin
    - connect output to the ground using a 10kΩ resistor
    - connect the other two connectors to a capacitor

## Activate WiFi and SSH Before First Boot

Add the output to `/mnt/etc/wpa/wpa_supplicant.conf` (mount `mmcblkp2):

    wpa_passphrase [ssid] [passphrase]

Create a file `/mnt/ssh` (mount `mmcblkp1`) called `ssh` to enable SSH:

    sudo touch /mnt/ssh
