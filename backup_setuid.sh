#!bin/bash

#Compruebo que se haya ingresado un solo argumento

if [ $# != 1 ]; then
        echo "Debe ingresar un solo parametro"
        echo "USO: ./backup_setuid.sh <directorio>"
        exit 1
fi


#Compruebo que se haya dado como argumento un directorio

if [ ! -d $1 ]; then
        echo "El parametro ingresado no es un directorio"
        echo "USO: ./backup_setuid.sh <directorio>"
        exit 2
fi


"------------------"
