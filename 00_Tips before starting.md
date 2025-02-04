## Install Miniconda

[Miniconda](https://docs.conda.io/en/latest/index.html) and [Anaconda](https://www.anaconda.com/) are useful tools for software/package and environment management for many programming language (Python, R, Ruby, Lua, Scala, Java, JavaScript, C/ C++, Fortran, etc.).

> Miniconda is minimal installer for conda. Anaconda contains many pre-installed accessory tools and packages that you are probably not going to used, but if so, they can be easily installed in Miniconda (i.e. jupyter notebooks).

Installing some of the programs commonly used in bioinformatics required many packages/libraries to be previously installed, with many, many dependencies... which could become a pain in the neck. Conda is a good solution to cope with all these tasks. It works well most of the times in a Linux-based system (also in *Windows subsystem for linux* in Windows), but sometimes it fails in Mac system due to some incompatibility issues (Mac shell is based on FreeBSD with some proprietary features such as the C compiler and others).

Choose the appropriate Miniconda version [here](https://docs.conda.io/en/latest/miniconda.html), copy the link and install.

```
wget https://repo.anaconda.com/miniconda/Miniconda3-py310_23.1.0-1-Linux-x86_64.sh
chmod +x Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

**Installing process**

> Do you accept the license terms? \[yes|no\]
> \[no\] >>> yes
> 
> Miniconda3 will now be installed into this location:
> /home/arastrojo/miniconda3
> 
> - Press ENTER to confirm the location
> - Press CTRL-C to abort the installation
> - Or specify a different location below
> 
> \[/Users/arastrojo/miniconda3\] >>>
> \[...\]

We can change installation location easily by supplying a different folder path.
After installing the required files in the selected location, conda introduce the following code in *.bash_profile* file (see below *Initiation files*):

```bash
# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/home/arastrojo/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/home/arastrojo/miniconda3/etc/profile.d/conda.sh" ]; then
        . "/home/arastrojo/miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="/home/arastrojo/miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<
```

Essentially, this code is telling the shell system where to find executable files (from programs and packages installed through conda), including the python interpreter.

Although installation seems very sophisticated, the process only copy conda required files to the specified folder and introduce a small piece of code in *.bash_profile*. Therefore, to uninstall Miniconda (and also Anaconda) we only have to remove the folder and delete the code in *.bash_profile*.

> Installing/uninstalling Miniconda/Anaconda in Windows can be performed through a GUI-based interface.

## *Initiation files*

In all linux-based systems (also Mac) there exist hidden *initiation files* that tell the system (shell or command interpreter) where to find programs, libraries, scripts, etc. The name of the *initiation files* files will depend on the operating system and the shell. For instance, in most linux with *bash* shell the file in called *.bashrc*. If we are using, *tsch* instead of *bash*, the file would be *.tcshrc*. In new Mac systems, that use *zsh*, the file is called *.zshrc*.

These *initiation files* are "executed/initiated" when a terminal windows is opened. If your are brave enough you can change the content of these files to add custom commands... But, to avoid problems it is better to add all custom instructions in a different file. Again, the name of these custom *initiation files* depend on the operative system and their version (*.bash_profile* or *.bash_aliases* in linux, *.profile* in mac, etc...). However, we can create a complete custom file and tell the shell to initiate it:

```bash
touch .custom_profile # Add some instructions in the file with vim or nano
source .custom_profile # initiate the file
```

Usually, default custom *initiation files* are initiated just in the terminal opening. However, if we use a custom file name, we need to initiate the file by using *source* command or we can add to *.bashrc* (or the corresponding file) the following line:

```bash
source /path_to_file/.custom_profile
```

This way our custom file is going to be initiated when running a new terminal window.

## Environmental variables

Similar to *initiation files*, there exists several pre-defined shell variables with important information for the system to work properly. For example, the variable _\$HOME_ contains the home directory of the current user, or _\$USER_ is the name of this user, etc. One of the most important environmental variables is _\$PATH_. It contains all the path to folders where the command interpreter (shell) should use to find programs, scripts, libraries, etc.

By default, _\$PATH_ contains important folder for the shell itseft (/usr/local/bin, /usr/bin, /bin, etc.) where most of the commands are stored, including _ls_, _cd_, _mkdir_, etc. Therefore, it is very important not to overwrite the content of this variable. To add a custom folder to the _\$PATH_ variable to tell the system to used this folder to search for binaries, programs, scripts, etc., we can do:

```bash
export $PATH=/home/metag/bin/:$PATH
```

This way, we are adding a new folder. 

**DO NOT USED**:
```bash
PATH=/home/metag/bin/
ls
Command 'ls' is available in the following places
 * /bin/ls
 * /usr/bin/ls
The command could not be located because '/bin:/usr/bin' is not included in the PATH environment variable.
ls: command not found
```

This will overwrite the variable content and therefore the shell is not going to know where to find the commands. Fortunately, this is temporal. If we re-start the terminal windows the _\$PATH_ variable is set again with the default values (some of then included in _.bashrc_). If we want to add permanently a custom folder is the_\$PATH_variable we should add the following line in *.bashrc* or better in *.bash_profile* (or the corresponding custom *initiation file*):

```bash
export $PATH=/home/metag/bin/:$PATH
```

For example, if we have a folder containing scripts we can add this folder to _\$PATH_ to tell the shell to look for

```bash
export $PATH=/home/metag/script/:$PATH

# or
# export $PATH=/$HOME/$USER/script/:$PATH # Using other environmental variables
```

This way, we do not need to put our script in the folder we are trying to run them, the shell *knows* where to find the scripts.
The same can be applied if we want to install a program. I used to create a *software* folder under my home directory:

```bash
mkdir $HOME/$USER/software
wget http://cab.spbu.ru/files/release3.15.5/SPAdes-3.15.5-Linux.tar.gz
tar -xzf SPAdes-3.15.5-Linux.tar.gz
```

Now, we can add *SPAdes* folder to the *$PATH*

```bash
export $PATH=/$HOME/$USER/software/SPAdes-3.15.5/bin/:$PATH
```

Or, we can create a *symbolic link* (a file shortcut) of the executable file (*spades.py*) in a custom *bin* folder:

```bash
mkdir $HOME/$USER/bin
ls -s /$HOME/$USER/software/SPAdes-3.15.5/bin/spades.py $HOME/$USER/bin

# Then add this line to .bash_profile_
export $PATH=/$HOME/$USER/bin/:$PATH
```

If we do this with all programs we install in our system, all executables are going to be in *\$HOME/\$USER/bin* folder, an the shell is going to known where to find them without the need to add multiples lines with different paths to the executables of the different programs we have installed.

## Virtual environment with conda

As it was mentioned before, conda is a very good tool to install programs, as it takes care of all dependencies (libraries, packages, etc.) that the program required. However, sometimes 2 programs could required different version of a particular library/package and we cannot install both programs simulatenously. Additionally, after installing many programs, the conda system could accumulate many trash, temporal files, etc., and start given errors. To solve this, we must make used of the *virtual environments*, which is an encapsulated, let say, *copy* of conda were we can install any program/libraries/packages without changing the main conda system. We can also used a different version of python. To create *virtual environment* we have to do the following:

```bash
conda create -n humann python=2.7
conda activate humann # to enter the virtual env
pip install humann2=2.8.2 # pip -> default python package manager
conda deactivate # to deactivate the virtual env
```

To list all created *virtual environments*:

```bash
conda env list

# or just
ls /$HOME/$USER/miniconda3/envs
```

To delete a *virtual environment*:

```bash
conda env remove -n humann

# or just
rm -fr /$HOME/$USER/miniconda3/envs/humann
```

> We can also create *virtual enviroments* in python:
> python3 -m venv entorno_python
> source entorno_python/bin/activate
> pip install pandas
> deactivate

#### Problematic programs (for instance STAMP)

If you try to install STAMP your going to be in troubles... It required python 2.7 that is not mantained anymore and the python 2.7 libraries are completely out of date. So, how to used STAMP? Porting the STAMP virtual environment create before python 2.7 become obsolate... To do so, we need to install [conda-pack](https://conda.github.io/conda-pack/) in the machine we have STAMP installed and then pack the virtual environment:

```
conda install conda-pack
# or --> conda install -c conda-forge conda-pack
# or --> pip install conda-pack
conda pack -n stamp -o stamp.tar.gz
```

Now, on the new machine (target) we only need to decompress the packed file:

```bash
pip install gdown # to download files from googledrive
gdown 1ANLUfRcoudLWH40CFUomd0Ma50h4mAAn
# md5 (stamp.tar.gz) = 3160a72c735bf6fe6a391ce5b749bba1
mkdir /home/metag/miniconda3/envs/stamp
tar -xzf stamp.tar.gz -C /home/metag/miniconda3/envs/stamp
```

> IMPORTANT: we can only port environments between same operating system (for linux to linux, from mac to mac, etc.)
