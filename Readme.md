# Obligatorio - Programacion para DevOps

## Integrantes

- Giuliana Pedemonti - 325718
- Alvaro Rebollo - 317384

---

## Contenido del Repositorio


- Readme.md

### Scripts

#### Bash
- backup_setuid.sh

#### Python
- bucketS3andLogs.py
    
- MySQLandRDS.py

### Contenido Adicional
-  


---

## Desgloce del contenido de los Scripts

### backup_setuid.sh




### bucketS3andLogs.py

Este script tiene como objetivo crear un bucket en S3 y subir un archivo generado previamente por el script anterior.

- **Bloque 1:** Realiza la validacion de los parametros que deben ser ingresados (ambos numeros de estudiante y el archivo generado previamente).
    
    Se controla tanto el ingreso de 3 parametros como el tipo de dato ingresado

- **Bloque 2:**

- **Bloque 3:** Define el nombre que debe tener el archivo dentro del Bucket y lo sube
gene


### MySQLandRDS.py

Su funcion es crear una instancia EC2 con MySQL instalado y generar una base de datos MySQL RDS

- **Bloque 1:**
     Lanza la EC2 con
        - Ubuntu 22.04
        - Grupo de seguridad que permite los puertos 22 (SSH) y 3306 (MySQL)

- **Bloque 2:** Crea la base de datos RDS