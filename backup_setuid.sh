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



#Buscar ejecutables


find "$DIRECTORIO" -type f -perm -4000 -perm -0001 | while read -r archivo; do
        echo "Analizando archivo: $archivo"
        if head -n 1 "$archivo" | grep -qE '^#!'; then
               echo "script encontrado: $archivo"
        fi

