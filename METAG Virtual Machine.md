### Metagenomics

Preparing Virtual Machine / local machine

Install Lubuntu/Ubuntu/Xubuntu (20.04.X LTS) in a virtual machine using VirtualBox (2 cores, 4 Gb of RAM and 50 Gb disk space) or in your local machine.

```
# Some updates
sudo apt-get update
sudo apt-get install gcc
sudo apt-get install make
```

#### Install Miniconda

```
wget https://repo.anaconda.com/miniconda/Miniconda3-py310_23.1.0-1-Linux-x86_64.sh
chmod +x Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

### Instalación de los entornos necesarios

#### humann

```bash
conda create -n humann python=2.7
conda activate humann
pip install humann2=2.8.2
conda deactivate
```

#### Spades

```bash
conda create -n spades
conda activate spades
conda install -c bioconda spades=3.13.0
conda deactivate
```

#### Megan

```bash
conda create -n megan
conda activate megan
conda install -c bioconda megan=6.24.20
conda deactivate
```
#### Picrust

Lo importo de la máquina virtual de Miguel (Metagenomica.ova, md5=8263d0bcfab2fecd697cc25f1e80a8b2) usando conda-pack (ver abajo)

```bash
wget ////picrust.tar.gz
mkdir /media/DiscoLocal/BioInformatica/miniconda3/envs/picrust
tar -xzf picrust.tar.gz -C /media/DiscoLocal/BioInformatica/miniconda3/envs/picrust
```

#### STAMP

Lo importo de la máquina virtual de Miguel (Metagenomica.ova, md5=8263d0bcfab2fecd697cc25f1e80a8b2) usando conda-pack (ver abajo)

```bash
wget ///stamp.tar.gz
mkdir /media/DiscoLocal/BioInformatica/miniconda3/envs/stamp
tar -xzf stamp.tar.gz -C /media/DiscoLocal/BioInformatica/miniconda3/envs/stamp
```

#### Qiime2

Lo importo de la máquina virtual de Miguel (Metagenomica.ova, md5=8263d0bcfab2fecd697cc25f1e80a8b2) usando conda-pack (ver abajo)

```bash
wget ///qiime2.tar.gz
mkdir /media/DiscoLocal/BioInformatica/miniconda3/envs/Qiime2
tar -xzf qiime2.tar.gz -C /media/DiscoLocal/BioInformatica/miniconda3/envs/qiime2
```


#### Porting enviroments

[On the source machine (already done)](https://conda.github.io/conda-pack/):
```
conda install conda-pack
# or --> conda install -c conda-forge conda-pack
# or --> pip install conda-pack
conda pack -n stamp -o stamp.tar.gz
```

On the target machine:
```
cd /home/${USER}/miniconda3/envs
mkdir -p stamp
tar -xzf stamp.tar.gz -C /home/${USER}/miniconda3/envs/stamp
```

NOTA: los entornos portados así sólo se pueden volver a montar en el mismo tipo de sistema operativo. Si se crearon en linux, no van a funcionar en mac o windows.  


#### Install VirtualBox Guest Additions (optinal)

Guest Additions allow virtual machine window to fit your screen, share clipboard, etc.

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

