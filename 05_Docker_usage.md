<!--

---
aliases:
  - "# 🧬 Docker Environment for Metagenomics / Entorno Docker para Metagenómica"
---


**Image / Imagen:** `migredon/bioinformatica-master`
-->


Este documento detalla la configuración necesaria para desplegar el entorno de la asignatura, permitiendo el uso de herramientas gráficas (STAMP) y el entorno de desarrollo RStudio Server.


## Castellano

### 1. Instalación de Docker

Antes de manejar la imagen de la asignatura, debes tener instalado Docker en tu ordenador.

1. **Descarga:** Ve a la página oficial de [Docker Desktop](https://www.google.com/search?q=https://www.docker.com/products/docker-desktop "null").
    
2. **Instalación:**
    
    - **Windows:** Descarga el instalador para Windows. Durante la instalación, asegúrate de que la opción "Use WSL 2 instead of Hyper-V" esté marcada. Al finalizar, es posible que debas reiniciar el equipo.
        
    - **macOS:** Descarga la versión correspondiente a tu procesador (Chip de Apple "M1/M2/M3" o Intel). Arrastra Docker a tu carpeta de Aplicaciones.
        
3. **Verificación:** Abre la aplicación Docker Desktop y espera a que el icono de la ballena en la barra de tareas esté estático (en verde).
    

### 2. Descarga de la Imagen (Pull)

Una vez instalado Docker, abre una terminal y descarga la imagen oficial:

```
docker pull --name bioinfo smigredon/bioinformatica-master
```

### 3. Configuración del Servidor Gráfico (X11)

Para visualizar ventanas de programas (como STAMP), necesitas un servidor X11.

#### **En Windows (VcXsrv)**

1. Descarga e instala **VcXsrv**: [Enlace de descarga](https://sourceforge.net/projects/vcxsrv/ "null")
    
2. Ejecuta **XLaunch** y configura:
    
    - **Display number:** 0
        
    - **Start no client**.
        
    - ✅ Marca **"Disable access control"** (Paso crítico).
        
    - Finaliza y mantén el programa en segundo plano.
        

#### **En macOS (XQuartz)**

1. Descarga e instala **XQuartz**: [xquartz.org](https://www.google.com/search?q=https://www.xquartz.org/ "null")
    
2. Abre XQuartz, ve a **Preferencias > Seguridad**.
    
3. ✅ Marca **"Permitir conexiones de clientes de red"**.
    
4. **Reinicia tu sesión** y ejecuta en la terminal: `xhost +localhost`
    

### 4. Ejecución del Contenedor

**Windows (PowerShell):**

```
docker stop bioinfo
docker rm bioinfo
docker run -d -p 8787:8787 -e DISPLAY=host.docker.internal:0.0 --name bioinfo migredon/bioinformatica-master
```

**macOS (Terminal):**

```
docker stop bioinfo
docker rm bioinfo
docker run -d -p 8787:8787 -e DISPLAY=docker.for.mac.host.internal:0 --name bioinfo migredon/bioinformatica-master
```

### 5. Acceso a las Herramientas

#### **A. RStudio Server (Navegador)**

- **URL:** `http://localhost:8787`
    
- **Usuario:** `rstudio` | **Contraseña:** `rstudio`
    

#### **B. STAMP (Interfaz Gráfica)**

```
docker exec -it bioinfo bash
conda activate stamp
STAMP.py
```

