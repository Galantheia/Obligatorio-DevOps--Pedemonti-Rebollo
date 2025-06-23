#!/usr/bin/env python3
import boto3
import os
import sys
from datetime import datetime

# ------------------ BLOQUE 1: Validación de parámetros ------------------
if len(sys.argv) != 4:
    print("Uso: python3 subir_a_s3.py <nro_estudiante1> <nro_estudiante2> <ruta_al_archivo>", file=sys.stderr)
    sys.exit(1)

nro1 = sys.argv[1]
nro2 = sys.argv[2]
archivo_local = sys.argv[3]

if not os.path.isfile(archivo_local):
    print(f"Error: El archivo {archivo_local} no existe.", file=sys.stderr)
    sys.exit(2)

# ------------------ BLOQUE 2: Crear bucket S3 ------------------
s3 = boto3.client('s3')
bucket_name = f"el-maligno-{nro1}-{nro2}".lower()

try:
    region = boto3.session.Session().region_name
    s3.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={'LocationConstraint': region}
    )
    print(f"Bucket {bucket_name} creado en región {region}.")
except s3.exceptions.BucketAlreadyOwnedByYou:
    print(f"Bucket {bucket_name} ya existe. Continuando...")
except Exception as e:
    print(f"Error creando el bucket: {e}", file=sys.stderr)
    sys.exit(3)

# ------------------ BLOQUE 3: Subida del archivo ------------------
fecha = datetime.now().strftime("%d-%m-%Y")
nombre_remoto = f"Log_{fecha}"

try:
    s3.upload_file(archivo_local, bucket_name, nombre_remoto)
    print(f"Archivo subido como {nombre_remoto} al bucket {bucket_name}.")
except Exception as e:
    print(f"Error subiendo el archivo: {e}", file=sys.stderr)
    sys.exit(4)

