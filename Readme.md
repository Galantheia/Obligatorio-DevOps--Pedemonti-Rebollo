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
- .gitignore
- .env.example

---

## Configuraciones Previas Requeridas

- **AWS CLI:** Debe estar instalado y configurado con aws configure ingresando Access Key, Secret Key y región. (_ruta del archivo: ~/.aws/credentials_)

- **Cuenta Activa de AWS:** Requiere una cuenta de AWS valida o acceso a un entorno de laboratorio que permita el uso de EC2, S3 y RDS.

- **Usuario IAM** con permisos de S3, EC2 y RDS o, en su defecto, un **usuario con AdministratorAccess** que debe tener Access Key y Secret Key activos.

- **Clave EC2** creada previamente en AWS: El nombre de la clave debe coincidir con la variable KEY_NAME en el archivo .env.

- **Boto3:** Libreria necesaria para la interaccion con AWS, instalar con pip3 install boto3.

- **Python-dotenv:** Libreria necesaria para cargar variables desde el archivo .env, instalar con pip3 install python-dotenv.

- **Archivo .env:** Debe estar en la misma carpeta que los scripts y contener los campos de las variables con los valores correspondientes.

- **Permisos para acceder a los archivos en el sistema**. Para poder buscar los archivos pertinentes desntro del sistema es necesario tener los permisos adecuados.

### Extra

- En la realizacion y pruebas de los siguientes scripts se conto con el uso de una carpeta de entorno virtual en el cual se contuvo las librerias de "boto3" y "python-dotenv"

---

## Desglose del Contenido de los Scripts

### backup_setuid.sh

Este script busca archivos ejecutables con el permiso SetUID activado, comenzando desde un directorio especificado (o desde el directorio actual si no se especifica ninguno).

Permite generar un archivo de log con los caminos encontrados y filtrar solo scripts de Bash. Todos los archivos encontrados se comprimen en un archivo .tar.gz.

_**Uso:** bash backup_setuid.sh [-c] [-b] [directorio]_

- -c: genera un log (.rep) con los caminos absolutos de los archivos encontrados.
- -b: filtra solo scripts de Bash (que comiencen con #!/bin/bash).
- directorio: (opcional) directorio desde el cual comenzar la búsqueda. Si no se especifica, se usa el directorio actual.

#### Ejemplo

./backup_setuid.sh -c -b /

Esto busca desde la raíz (/), genera un log y solo incluye scripts de Bash con permisos setuid y ejecución para otros usuarios.

El resultado será un archivo .tar.gz con los archivos encontrados y el archivo de log.

![image](https://github.com/user-attachments/assets/a5e74a1e-5042-4c99-ab17-8a2757ea47cb)

#### Códigos de salida

- 0: ejecución exitosa
- 1: opción inválida
- 2: directorio inválido

### bucketS3andLogs.py

- **Bloque 1:**

_**Uso:** python[3] bucketS3andLogs.py [nro_de_estudiante1] [nro_de_estudiante2]_

Este script requiere ingresar dos parametros numericos para usarse. Se espera el numero de estudiante de dos personas.

Tiene como objetivo crear un bucket en Amazon S3 y subir un archivo generado previamente (generalmente un log).


 - **Bloque 1:**

Realiza la validacion de los parametros ingresados por linea de comandos:

        - Numero de estudiante 1

        - Numero de estudiante 2.

Ademas, busca el ultimo archivo generado cuyo nombre empieze por "Logs".

- **Bloque 2:**

Se encarga de la creacion del bucket en S3. El nombre del bucket se construye dinamicamente combinando un prefijo predefinido (BUCKET_PREFIX tomado del `.env`) y los numeros de estudiante. Si el bucket ya existe y es propiedad del usuario, se continua sin error.

- **Bloque 3:**

Define el nombre que tendra el archivo dentro del bucket en función de la fecha actual y realiza la subida al bucket correspondiente. Se informa por pantalla si la operación fue exitosa o si ocurrio un error.


### MySQLandRDS.py

_**Uso:** python[3] MySQLandRDS.py_

Su funcion es automatizar la creación de una instancia EC2 configurada con MySQL y tambien generar una base de datos administrada en Amazon RDS.

- **Bloque 1:**

Lanza una instancia EC2 basada en Amazon Linux 2.

Configura la seguridad (se asume que el Security Group ya permite trafico por los puertos 22 (SSH) y 3306 (MySQL)).

Dentro del script de inicialización (UserData):

        - Se instala el cliente MySQL en la EC2.
        - La EC2 no ejecuta bases de datos locales, solo queda preparada para conectarse al RDS si es necesario.

- **Bloque 2:**

Crea una instancia de base de datos administrada en RDS utilizando el motor MySQL. Define el tamaño, usuario administrador, contraseña y configuracian basica.

Luego espera a que esta quede disponible.

- **Bloque 3:**

Una vez que la RDS esta operativa:

        - El script obtiene el endpoint del RDS.
        - Desde la maquina local donde se ejecuta el script, se conecta al RDS.

        - Se lee y ejecuta el archivo `obli.sql`, que contiene las instrucciones para crear tablas y estructuras en la base de datos.

De esta forma, la base de datos en RDS queda inicializada y lista para ser usada.
