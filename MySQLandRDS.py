#!/usr/bin/env python3

import boto3
import time
import sys
import os
import base64
from dotenv import load_dotenv

load_dotenv(".env")

os.environ['AWS_ACCESS_KEY_ID'] = os.getenv('AWS_ACCESS_KEY_ID')
os.environ['AWS_SECRET_ACCESS_KEY'] = os.getenv('AWS_SECRET_ACCESS_KEY')
os.environ['AWS_SESSION_TOKEN'] = os.getenv('AWS_SESSION_TOKEN')

# ------------------ BLOQUE 1: Creacion de instancia EC2 ------------------
# ------------------ BLOQUE 1: Creacion de instancia EC2 ------------------
ec2 = boto3.resource('ec2', region_name=os.getenv('AWS_DEFAULT_REGION'))

try:
    with open('obli.sql', 'r') as f:
        sql_content = f.read()
except Exception as e:
    print(f"Error al leer obli.sql: {e}", file=sys.stderr)
    sys.exit(1)

sql_b64 = base64.b64encode(sql_content.encode('utf-8')).decode('utf-8')

install_SQL = f'''#!/bin/bash
set -e

sudo yum update -y
sudo yum install -y mariadb

sudo systemctl start mariadb
sudo systemctl enable mariadb
'''

try:
    print("Lanzando instancia EC2...")
    instance = ec2.create_instances(
        ImageId='ami-09e6f87a47903347c',
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.micro',
        KeyName=os.getenv('KEY_NAME'),
        SecurityGroups=['DevOps_Obligatorio'],
        TagSpecifications=[{
            'ResourceType': 'instance',
            'Tags': [{'Key': 'Name', 'Value': 'Maligno-SRV'}]
        }],
        UserData=install_SQL
    )[0]

    instance.wait_until_running()
    instance.reload()
    print(f"Instancia EC2 lanzada. ID: ' {instance.id} ', IP: ' {instance.public_ip_address} '.")

except Exception as e:
    print(f"Error al lanzar EC2: {e}", file=sys.stderr)
    sys.exit(1)

# ------------------ BLOQUE 2: Creacion de base de datos RDS ------------------

rds = boto3.client('rds', region_name=os.getenv('AWS_REGION'))

try:
    print("Creando instancia RDS...")
    rds.create_db_instance(
        DBName='malignodb',
        DBInstanceIdentifier='Maligno-DB',
        AllocatedStorage=20,
        DBInstanceClass='db.t3.micro',
        Engine='mysql',
        MasterUsername='sysadmin',
        MasterUserPassword='sysadmin',
        BackupRetentionPeriod=7,
        PubliclyAccessible=True,
        VpcSecurityGroupIds=[
                'sg-0410bc391773c4334'
    ]
    )

    waiter = rds.get_waiter('db_instance_available')
    print("Esperando que RDS quede disponible...")
    waiter.wait(DBInstanceIdentifier='Maligno-DB')
    print("La instancia RDS ha sido creada y esta lista.")

except Exception as e:
    print(f"Error al crear instancia RDS: {e}", file=sys.stderr)
    sys.exit(2)

# ------------------ BLOQUE 3: Ejecutar obli.sql en RDS ------------------


try:
    rds_description = rds.describe_db_instances(DBInstanceIdentifier='Maligno-DB')
    rds_endpoint = rds_description['DBInstances'][0]['Endpoint']['Address']
    print(f"Endpoint de RDS: {rds_endpoint}")

    print("Esperando 180 segundos adicionales para garantizar que RDS responda...")
    time.sleep(180)

    with open('obli.sql', 'r') as f:
        sql_commands = f.read()

    print("Conectando al RDS y ejecutando el script...")
    conn = mysql.connector.connect(
        host=rds_endpoint,
        user='sysadmin',
        password='sysadmin',
        database='malignodb'
    )

    cursor = conn.cursor()

    for statement in sql_commands.strip().split(';'):
        if statement.strip():
            cursor.execute(statement + ';')

    conn.commit()
    cursor.close()
    conn.close()
    print("Script SQL ejecutado exitosamente en el RDS.")

except Exception as e:
    print(f"Error al ejecutar el script en el RDS: {e}", file=sys.stderr)
    sys.exit(3)
