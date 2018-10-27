# Annapolis-Gourmet
###### Tianrui Zhang
## Project Description
This is a web-application project that integrates Flask, CRUD and authentication. It provides a list of dishes within a variety of selections as well as provides a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.
## Instruction
1. Download and install [Vagrant](https://www.vagrantup.com/downloads.html), the virtual machine.
2. Download Vagrant [configuration file](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip).
3. Assuming the configuration file is located inside your **Downloads** folder, change to the **vagrant** directory in the terminal with `cd Downloads/FSND-Virtual-Machine/vagrant`.
4. Start Vagrant by running the command `vagrant up`.
5. Run `vagrant ssh` to log in to the newly installed Linux Virtual Machine.
6. Change to the shared directory by running `cd /vagrant`.
7. Type `git clone https://github.com/TianruiZhang/Annapolis-Gourmet.git` and press **Enter**. Your local clone will be created.
8. Type `python3 database_setup.py` and press **Enter**.
9. Type `python3 lotsofmenus.py` and press **Enter**.
10. Type `python3 project.py` and press **Enter**.
11. Type `http://localhost:8000/home/` in the address bar in your browser.
