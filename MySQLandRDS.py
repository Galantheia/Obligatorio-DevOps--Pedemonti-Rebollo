#!/usr/bin/env python3
import boto3
import time
import sys

# ------------------ BLOQUE 1: Crear instancia EC2 ------------------
ec2 = boto3.resource('ec2')

user_data_script = '''#!/bin/bash
sudo apt update
sudo apt install -y mysql-server
sudo systemctl start mysql
sudo systemctl enable mysql
'''

try:
    print("Lanzando instancia EC2...")
    instance = ec2.create_instances(
        ImageId='ami-0c02fb55956c7d316',  # Ubuntu Server 22.04 LTS (us-east-1)
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.micro',
        KeyName='tu-clave-ec2',  # 🔁 REEMPLAZAR con tu clave
        SecurityGroups=['default'],  # 🔁 Asegurate que permita SSH y MySQL
        TagSpecifications=[{
            'ResourceType': 'instance',
            'Tags': [{'Key': 'Name', 'Value': 'Maligno-SRV'}]
        }],
        UserData=user_data_script
    )[0]

    instance.wait_until_running()
    instance.reload()
    print(f"Instancia EC2 lanzada. ID: {instance.id}, IP: {instance.public_ip_address}")

except Exception as e:
    print(f"Error al lanzar EC2: {e}", file=sys.stderr)
    sys.exit(1)

# ------------------ BLOQUE 2: Crear base de datos RDS ------------------
rds = boto3.client('rds')

try:
    print("Creando instancia RDS...")
    rds.create_db_instance(
        DBName='malignodb',
        DBInstanceIdentifier='Maligno-DB',
        AllocatedStorage=20,
        DBInstanceClass='db.t3.micro',
        Engine='mysql',
        MasterUsername='admin',
        MasterUserPassword='Admin123456!',  # 🔐 Recomendado cambiarla después
        BackupRetentionPeriod=7,
        PubliclyAccessible=True
    )

    waiter = rds.get_waiter('db_instance_available')
    print("Esperando que RDS esté disponible...")
    waiter.wait(DBInstanceIdentifier='Maligno-DB')
    print("Instancia RDS 'Maligno-DB' creada y lista.")

except Exception as e:
    print(f"Error al crear RDS: {e}", file=sys.stderr)
    sys.exit(2)

