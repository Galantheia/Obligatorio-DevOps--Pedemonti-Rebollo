#!/usr/bin/env python3

import boto3
import time
import sys

# ------------------ BLOQUE 1: Creacion de instancia EC2 ------------------
ec2 = boto3.resource('ec2')

install_SQL = '''#!/bin/bash
sudo apt update
sudo apt install -y mysql-server
sudo systemctl start mysql
sudo systemctl enable mysql
'''

try:
    print("Lanzando instancia EC2...")
    instance = ec2.create_instances(
        ImageId='ami-0c02fb55956c7d316',  # AMI Publica de Ubuntu [Server 22.04 LTS (us-east-1)]
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.micro',
        KeyName='DevOps_Sysadmin.pemR',
        SecurityGroups=['default'], 
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
rds = boto3.client('rds')

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
        PubliclyAccessible=True
    )

    waiter = rds.get_waiter('db_instance_available')
    print("Esperando que RDS quede disponible...")
    waiter.wait(DBInstanceIdentifier='Maligno-DB')
    print("La instancia RDS ha sido creada y esta lista.")

except Exception as e:
    print(f"Error al crear instancia RDS: {e}", file=sys.stderr)
    sys.exit(2)

