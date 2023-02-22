### Metagenomics

Preparing Virtual Machine

Install Lubuntu (22.04.1 LTS) in a virtual machine using VirtualBox (2 cores, 4 Gb of RAM and 25 Gb disk space).

#### Install Guest Additions

sudo apt-get update  
sudo apt-get install gcc  
sudo apt-get install make  

Go to menu bar, click on Devices -> Insert Guest additions CD  
In temrinal:  
```
cd /media/${USER}/VBox_GAs_7.0.6  
sudo ./VBoxLinuxAdditions.run  
```
Reboot system.


#### Install Miniconda

``` 
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod +x Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
``` 

