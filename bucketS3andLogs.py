#!/usr/bin/env python3

import boto3
import glob
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(".env")

os.environ['AWS_ACCESS_KEY_ID'] = os.getenv('AWS_ACCESS_KEY_ID')
os.environ['AWS_SECRET_ACCESS_KEY'] = os.getenv('AWS_SECRET_ACCESS_KEY')
os.environ['AWS_SESSION_TOKEN'] = os.getenv('AWS_SESSION_TOKEN')

# ------------------ BLOQUE 1: Validacion de parámetros ------------------

if len(sys.argv) != 3:
    print("Uso: python3 subir_a_s3.py <nro_estudiante1> <nro_estudiante2>", file=sys.stderr)
    sys.exit(1)

nro1 = sys.argv[1]
nro2 = sys.argv[2]

backups = glob.glob('Logs*')

if not backups:
    print("No se encontraron archivos que comiencen con 'Backups'.", file=sys.stderr)
    sys.exit(2)

archivo_log = max(backups, key=os.path.getctime)
print(f"Archivo más reciente encontrado: {archivo_log}")

# ------------------ BLOQUE 2: Creacion de bucket ------------------

s3 = boto3.client('s3')
bucket_prefix = os.getenv('BUCKET_PREFIX')
bucket_name = f"{bucket_prefix}-{nro1}-{nro2}".lower()
region = os.getenv('AWS_DEFAULT_REGION')

try:
    if region == 'us-east-1':
        s3.create_bucket(Bucket=bucket_name)
    else:
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': region}
        )
    print(f"El bucket '{bucket_name}' ha sido creado en la region '{region}'.")
except s3.exceptions.BucketAlreadyOwnedByYou:
    print(f"El bucket '{bucket_name}' ya existe. Continuando...")
except Exception as e:
    print(f"Error en la creacion el bucket: {e}", file=sys.stderr)
    sys.exit(3)

# ------------------ BLOQUE 3: Subida de archivo ------------------

fecha = datetime.now().strftime("%d-%m-%Y")
nombre_remoto = f"Log_{fecha}"

try:
    s3.upload_file(archivo_log, bucket_name, nombre_remoto)
    print(f"El archivo se ha subido como: ' {nombre_remoto} ' al bucket: ' {bucket_name} .")
except Exception as e:
    print(f"Error al subir el archivo: {e}", file=sys.stderr)
    sys.exit(4)

