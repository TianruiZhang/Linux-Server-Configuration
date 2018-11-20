# Linux Server Configuration
## Description
This project integrates the installation, configuration of a Linux server and the deployment of a web application.

#### SSH port: 2200

#### Public IP: 52.221.216.157

#### Project URL: http://52.221.216.157.xip.io<sup>[1](https://classroom.udacity.com/nanodegrees/nd004/parts/b2de4bd4-ef07-45b1-9f49-0e51e8f1336e/modules/56cf3482-b006-455c-8acd-26b37b6458d2/lessons/046c35ef-5bd2-4b56-83ba-a8143876165e/concepts/c4cbd3f2-9adb-45d4-8eaf-b5fc89cc606e)</sup>

## Configuration

### Start a Ubuntu Linux Server Instance
1. Log into [Amazon Lightsail](https://lightsail.aws.amazon.com/) with your AWS account.
2. Click **Crete instance**, choose **Linux/Unix**, **OS Only** and **Ubuntu (18.04 LTS)** and the cheapest plan.
3. Click **Create instance** button on the bottom of the page.

### SSH into the Server from Mac OS
1. Download your default private key (named LightsailDefaultPrivateKey-ap-southeast-1.pem here) from the **Account page** to your local machine (e.g. Downloads/).
2. Open **Terminal** and Run `mv ~/Downloads/LightsailDefaultPrivateKey-ap-southeast-1.pem ~/.ssh/lightsail.rsa`.
3. Run `chmod 600 ~/.ssh/lightsail.rsa` in your Terminal.
4. SSH into the server by running `ssh -i ~/.ssh/lightsail.rsa ubuntu@52.221.216.157` in your Terminal, where "52.221.216.157" is your public IP.
5. Run `yes` when asked whether you are sure you want to continue connecting.

### Update Packages and Cache
1. Run `sudo apt-get update` to update the list of available packages and their versions<sup>[2](https://askubuntu.com/questions/94102/what-is-the-difference-between-apt-get-update-and-upgrade)</sup>.
2. Run `sudo apt-get upgrade` to install newer versions of the packages you have<sup>[2](https://askubuntu.com/questions/94102/what-is-the-difference-between-apt-get-update-and-upgrade)</sup>.
3. Run `sudo apt-get update && sudo apt-get dist-upgrade` if the Ubuntu server indicates that there are still updates available or packages that can be updated<sup>[3](https://serverfault.com/questions/265410/ubuntu-server-message-says-packages-can-be-updated-but-apt-get-does-not-update)</sup>.

### Configure UFW (Uncomplicated Firewall)

1. Run `sudo nano /etc/ssh/sshd_config`, uncomment and change line "#Port 22" to "Port 2200" in the nano editor, save and quit (by pressing Ctrl-X + Y + Enter).
2. Run `sudo service ssh restart` to restart SSH.
3. Run `sudo ufw default deny incoming` so everything coming in is blocked.
4. Run `sudo ufw default allow outgoing` so everything coming out is allowed.
5. Run `sudo ufw allow 2200/tcp` and `sudo ufw deny 22/tcp`. Port 22 is now closed and SSH will use port 2200.
6. To allow HTTP on port 80, Run `sudo ufw allow http`.
7. Run `sudo ufw allow 123/udp`. Incoming connections for NTP (port 123) is now allowed.
8. Run `sudo ufw enable`. Respond to the prompt with `y`. The firewall is now active.
9. Run `sudo ufw status`. The output should be:

<center>

|To|Action|From|
|:- |:- | :-|
|22/tcp|DENY|Anywhere|
|2200/tcp|ALLOW|Anywhere|
|80/tcp|ALLOW|Anywhere|
|123/udp|ALLOW|Anywhere|
|22/tcp (v6)|DENY|Anywhere (v6)|
|2200/tcp (v6)|ALLOW|Anywhere (v6)|
|80/tcp (v6)|ALLOW|Anywhere (v6)|
|123/udp (v6)|ALLOW|Anywhere (v6)|

</center>
10. Manage this Ubuntu instance in [Amazon Lightsail](https://lightsail.aws.amazon.com/). Configure the firewall settings in the **Networking** section. The Configuration should be:

<center>

|Application|Protocol|Port range|
|:- |:- | :-|
|Custom|TCP|2200|
|HTTP|TCP|80|
|Custom|UDP|123|

</center>
11. Close Terminal.
12. Reopen Terminal on your local machine and Run `ssh -i ~/.ssh/lightsail.rsa -p 2200 ubuntu@52.221.216.157`. Now you should be able to connect to Ubuntu again on your local machine.

### Give `grader` Sudo Access
1. Create a new user account named `grader`. Run `sudo adduser grader`. Use the word *grader* in the password field. Name it "Grader" in the full name field. Leave other fields empty. Respond to the prompt with `y`.
2. Run `sudo usermod -aG sudo grader` to add the newly created user to the sudo group.
3. Run `sudo -l -U grader`. Grader has been given access to sudo if "(ALL: ALL) ALL" is seen.

### Allow `grader` to SSH into the Virtual Machine
1. Run `exit` to return to the local machine.
2. On your local machine, Run `ssh-keygen`. Enter `/Users/JamesChang/.ssh/grader.rsa`, which is the file where the key is saved. Leave the passphrase empty.
3. Run `cat /Users/JamesChang/.ssh/grader.rsa.pub` and copy all of its content.
4. In Terminal on your local machine, run `ssh -i ~/.ssh/lightsail.rsa -p 2200 ubuntu@52.221.216.157` to log in.
5. Run `su - grader` and enter the password to change to a different user "grader".
6. Run `mkdir .ssh` to create a new directory called ".ssh".
7. Run `touch .ssh/authorized_keys` to create an empty (zero byte) new file called "authorized_keys".
8. Run `nano .ssh/authorized_keys` to edit *authorized_keys* file. Paste the content copied in step 3. Save and quit (by pressing Ctrl-X + Y + Enter).
9. Run `chmod 700 .ssh`.
10. Run `chmod 644 .ssh/authorized_keys`.
11. Run `exit` **TWICE** to return to your local machine.
12. Run `ssh grader@52.221.216.157 -p 2200 -i ~/.ssh/grader.rsa`.
13. Run `sudo nano /etc/ssh/sshd_config`, change **PasswordAuthentication** to **no** to force key based authentication. Save and quit (by pressing Ctrl-X + Y + Enter).
14. Run `sudo service ssh restart` to restart ssh service.

### Disable `root` Login
1. Run `sudo nano /etc/ssh/sshd_config`.
2. Change **PermitRootLogin** to **no**. Save and quit (by pressing Ctrl-X + Y + Enter).
3. Run `sudo service ssh restart` to restart ssh service.

### Configure Local Timezone to UTC
1. Run `sudo dpkg-reconfigure tzdata` select **None of the above** and press enter.
2. Select **UTC** and press enter.

### Install and Configure Apache
1. Run `sudo apt-get install apache2` to install Apache. Respond to the prompt with `y`.
2. Run `sudo apt-get install libapache2-mod-wsgi-py3` so Apache can serve a Python mod_wsgi application.

### Install and Configure Postgresql
1. Run `sudo apt-get install postgresql` to install Postgresql. Respond to the prompt with `y`.
2. Run `sudo -u postgres createuser -P catalog` to create a Postgresql user named `catalog`. Enter password for new role. Here, the password is `catalog`.
3. Run `sudo -u postgres createdb -O catalog catalog` to create a database named `catalog` which is owned by the user `catalog`.

### Install Python Packages
Run the following commands to install Python packages needed for this project. Respond to any prompt with `y`.

`sudo apt-get install python3-psycopg2`

`sudo apt-get install python3-flask`

`sudo apt-get install python3-sqlalchemy`

`sudo apt-get install python3-pip`

`sudo pip3 install oauth2client`

`sudo pip3 install requests`

`sudo pip3 install httplib2`

### Install Git
Run `sudo apt-get install git` to install git.

### Clone Catalog Project from Github
1. Run `cd /var/www` to switch your directory to `/var/www`.
2. Run `sudo git clone https://github.com/TianruiZhang/Linux-Server-Configuration.git catalog` to clone the catalog project from Github.
3. Make sure the Public IP of your AWS instance matches the ServerName and ServerAlias in `catalog.conf`!
4. In [Google Developer Console](https://console.developers.google.com), add `http://52.221.216.157.xip.io` to Authorised JavaScript origins. Also, add `http://52.221.216.157.xip.io/` and `http://52.221.216.157.xip.io/oauth2callback` to Authorised redirect URIs.
5. Click **Download JSON** and copy the content and copy its content.
6. Run `cd /var/www/catalog/catalog` and `sudo rm client_secrets.json`.
7. Run `sudo nano client_secrets.json` and paste the content in step 5. Save and quit (by pressing Ctrl-X + Y + Enter).

### Configure Apache
1. Run `sudo mv catalog.conf /etc/apache2/sites-available/catalog.conf` to move the virtual host configuration file.
2. Run `sudo a2dissite 000-default.conf` to disable the default virtual host.
3. Run `sudo a2ensite catalog.conf` to enable the virtual host that has just been created.
4. Run `sudo service apache2 restart` to restart Apache2.

### Start the Application
In your browser, type `http://52.221.216.157.xip.io`. You should be able to see the webpage.

## Acknowledgement
Special thanks to the following Udacity students whose projects offered me valuable clues when I got stuck:
* [Alain Boisvert](https://github.com/boisalai/udacity-linux-server-configuration)
* [Emily Zhang](https://github.com/eqlz/fsnd-linux-server-config)
* [Gene Kao](https://github.com/GeneKao/linux-server-configuration)
