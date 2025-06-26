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
-  obli.sql

---

## Configuraciones Previas Requeridas y Cosas a Tener en Cuenta

 - **AWS Cli**

 - **Boto3**

 - **Cuenta Activa de AWS :** 

 - **Usuario IAM** con permisos de S3, EC2 y RDS o en su defecto
 
 - **Clave EC2** dreada Previamente en AWS

 - **Python-dotenv**



---

## Desglose del Contenido de los Scripts

### backup_setuid.sh

Este script busca archivos ejecutables con el permiso SetUID activado, comenzando desde un directorio especificado (o desde el directorio actual si no se especifica ninguno).

Permite generar un archivo de log con los caminos encontrados y filtrar solo scripts de Bash. Todos los archivos encontrados se comprimen en un archivo .tar.gz.

## Uso

./backup_setuid.sh [-c] [-b] [directorio]

- -c: genera un log (.rep) con los caminos absolutos de los archivos encontrados.
- -b: filtra solo scripts de Bash (que comiencen con #!/bin/bash).
- directorio: (opcional) directorio desde el cual comenzar la búsqueda. Si no se especifica, se usa el directorio actual.

## Ejemplo

./backup_setuid.sh -c -b /

Esto busca desde la raíz (/), genera un log y solo incluye scripts de Bash con permisos setuid y ejecución para otros usuarios.

El resultado será un archivo .tar.gz con los archivos encontrados y el archivo de log.

![image](https://github.com/user-attachments/assets/a5e74a1e-5042-4c99-ab17-8a2757ea47cb)

## Requisitos

- Bash
- Permisos para acceder a los archivos en el sistema

## Códigos de salida

- 0: ejecución exitosa
- 1: opción inválida
- 2: directorio inválido


### bucketS3andLogs.py

Este script tiene como objetivo crear un bucket en S3 y subir un archivo generado previamente por el script anterior.

- **Bloque 1:** Realiza la validacion de los parametros que deben ser ingresados (ambos numeros de estudiante y el archivo generado previamente). Verifica que el archivo exista en el sistema.

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
