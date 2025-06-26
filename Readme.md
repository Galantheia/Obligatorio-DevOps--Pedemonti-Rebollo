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


### Extra

- En la realizacion y pruebas de los siguientes scripts se conto con el uso de una carpeta de entorno virtual en el cual se contuvo las librerias de "boto3" y "python-dotenv"

---

## Desglose del Contenido de los Scripts

### backup_setuid.sh




### bucketS3andLogs.py

Este script requiere ingresar dos parametros numericos para usarse. Se espera el numero de estudiante de dos personas.

Este script tiene como objetivo crear un bucket en Amazon S3 y subir un archivo generado previamente (generalmente un log).

 - **Bloque 1:**
Realiza la validacion de los parametros ingresados por linea de comandos:

        - Numero de estudiante 1

        - Numero de estudiante 2.

Además, busca el ultimo archivo generado cuyo nombre empieze por "Backups".

- **Bloque 2:**

Se encarga de la creacion del bucket en S3. El nombre del bucket se construye dinamicamente combinando un prefijo predefinido (BUCKET_PREFIX tomado del .env) y los numeros de estudiante. Si el bucket ya existe y es propiedad del usuario, se continua sin error.

- **Bloque 3:**

Define el nombre que tendra el archivo dentro del bucket en función de la fecha actual y realiza la subida al bucket correspondiente. Se informa por pantalla si la operación fue exitosa o si ocurrió un error.


### MySQLandRDS.py

Su función es automatizar la creación de una instancia EC2 configurada con MySQL y también generar una base de datos administrada en Amazon RDS.

- **Bloque 1:**

Lanza una instancia EC2 basada en Ubuntu 22.04

Configura la seguridad para permitir accesos por los puertos 22 (SSH) y 3306 (MySQL)

Dentro del script de inicialización (UserData) donde :

        - Se instala MySQL Server en la EC2

        - Se habilita y se inicia el servicio

        - Se transfiere el contenido del archivo obli.sql a la instancia y se ejecuta automáticamente para configurar la base de datos localmente.

- **Bloque 2:**

Crea una instancia de base de datos administrada en RDS utilizando el motor MySQL.

Define el tamaño, usuario administrador, contraseña y configuración básica.