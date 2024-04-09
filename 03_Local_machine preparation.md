We are going to try to install the required software in your own machines, which are very different among them, so it is very likely to find several problems. However, this is one of the most important challenges a bioinformatian should face... So let's try. 

### Linux users

If you have already installed linux in your own machine, congratulations. The only additional thing we need to do before starting to install bioinformatic programs is to install _wget_ to allow us to download things from the Internet (it is not included in all Linux distributions):

```bash
apt-get install wget
```

If you did not do it but you would like to try, you can find thousands of tutorial in the Internet. But, here you have a suggestion:

- For Windows: https://linuxsimply.com/linux-basics/os-installation/dual-boot/
- For Mac: https://linuxsimply.com/linux-basics/os-installation/dual-boot/ubuntu-on-mac/

Following these tutorial you will be able to install Ubuntu using dual boot, which means that you will be able to access your original operative system (Windows or Mac OS). 

### Windows users

If you have a Windows machine you can try to install the complete Ubuntu operative system using dual boot as describe above, but we can also have Ubuntu command line system (shell terminal) as a regular Windows application. This is call _Windows Subsystem for Linux_ (WSL) and it will allow us to run most of the linux command we need to perform for our bioinformatics. 

To obtain WSL we only need to open _PowerShell_ app as administrator and run the following command:
```powershell
wsl --install
```

By default, this command installs all the requirements to run Ubuntu as an app in your Windows system. 

### Mac users

Under Mac operative system there is a linux-like (based on FreeBSB) running. So, if you have a Mac you have essentually a linux machine. Most of the linux commands are going to work is Mac os shell, but there are some exceptions that complicate the things (as usually with Apple's products). To be able to use properly this linux system (called darwin) we need to install a few things:

1. From the app store install Xcode (it will take while, because is a 25-30Gb program)
2. Then we need to install "Xcode Command Line Tools" by entering the following command in the _Terminal_:
```bash
 xcode-select --install
# And follow the instructions
```
3. Install [Brew](https://brew.sh/) which is a package manager for mac similar to apt-get from ubuntu:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
4. Finally, using _brew_ we can install _wget_:
```bash
brew install wget
```
