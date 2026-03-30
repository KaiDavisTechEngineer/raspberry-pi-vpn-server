# raspberry-pi-vpn-server
Self-hosted WireGuard VPN on Raspberry Pi for secure remote access
<Callout icon="📘" theme="info">
  # Raspberry Pi 5 Secure Home VPN

  ## Overview

  This project documents the design and deployment of a secure home VPN server using a Raspberry Pi 5 enabling encrypted remote access to a private home network from any external location.

  ## Features

  * Secure remote access
  * Encrypted VPN (WireGuard)
  * Access home network from anywhere
  * Expandable for security tools

  ## Hardware Used

  * Raspberry Pi 5 (8GB)
  * 128GB microSD Card
  * Power Supply
  * Case with Fan
  * HDMI Cable

  ## Hardware Setup

  * Installed Raspberry Pi into case
  * Connected fan
  * Inserted microSD card
  * Connected monitor, keyboard, mouse

  ![IMG_4748](https://github.com/user-attachments/assets/7692fc2d-a742-4e6b-942c-c315e487b2af)

  ## System Setup

  The Raspberry Pi was connected to WiFi and prepared for configuration.

  The system packages were updated and upgraded to ensure the latest software versions were installed.

  Command used:

  ```Bash
  sudo apt update && sudo apt upgrade -y
  ```

  ## SSH Setup

  Enabled SSH for remote access.

  Command used:

  ```Bash
  sudo raspi-config
  ```

  ## Network Info

  Found local IP address.

  Command used:

  ```Bash
  hostname -l
  ```

  ## Testing

  Successfully connected via SSH.

  ## Installing WireGuard

  Installed WireGuard VPN due to its speed, security and efficiency.

  Command used:

  ```Bash
  sudo apt install wireguard -y
  ```

<img width="645" height="1136" alt="View recent photos" src="https://github.com/user-attachments/assets/ebe7af94-d90c-4e81-9181-033c8160cf11" />



  ## Generating Encryption Keys

  WireGuard uses a public and private key pair for secure protection.

  Command used:

  ```Bash
  wg genkey | tee privatekey | wg pubkey > publickey
  ```

  The private key is kept secure on the server while the public key is used for client connections.

  ## Configuring the WireGuard Server

  A configuration file was created to define the VPN interface.

  File created:

  ```Bash
  sudo nano /etc/wireguard/wg0.conf
  ```

  Configuration:

  ```INI
  [Interface]
  Address = 10.0.0.1/24
  ListenPort = 51820
  PrivateKey = hidden
  ```

  ## Enabling IP Forwarding

  IP forwarding was enabled to allow the Raspberry Pi to route VPN traffic.

  Command used:

  ```Bash
  sudo nano /etc/sysctl.conf
  ```

  Moded line:

  ```Bash
  net.ipv4.ip_forward=1
  ```

  Command used:

  ```Bash
  sudo sysctl -p
  ```

  ## Starting the VPN Server

  The WireGuard interface has started to bring the VPN online.

  Command used:

  ```Bash
  sudo wg-quick up wg0
  ```

  Command used:

  ```Bash
  sudo wg
  ```
<img width="645" height="1398" alt="IMG_4824" src="https://github.com/user-attachments/assets/8c68166b-5df4-48ad-a4fc-d598dcbca981" />

  ## Testing and Performance

  A stress test was conducted to ensure the Raspberry Pi operated within safe temperature ranges under load.

  Result:
  •	Maintained stable temperatures under load
  •	Cooling system (fan + case) functioned correctly

![IMG_4783](https://github.com/user-attachments/assets/e4c8c291-aeb8-44cb-9b52-26246d703864)

  ## Features Implemented

  •	Secure encrypted VPN
  •	Remote network access
  •	Lightweight and efficient performance
  •	Secure key-based authentication

  ## Conclusion

  This project successfully demonstrates how to deploy a secure and efficient VPN server using a Raspberry Pi 5. It provides practical experience in networking, cybersecurity, and system administration, making this a “real-world” project. 
  
</Callout>
