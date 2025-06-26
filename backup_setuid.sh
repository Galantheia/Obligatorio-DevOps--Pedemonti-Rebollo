#!bin/bash

Crear_Log=False
Bash=False

while getopts ":cb" opt; do
        case $opt in
                c) Crear_Log=true ;;
                b) Bash=true ;;
                \?) echo "Opcion invalida: -$OPTARG" >&2; exit 1 ;
        esac
done

# Primer argumento que no es opcion
DIRECTORIO="${@:$OPTIND:1}"

if [ ! -d "$DIRECTORIO" ]; then
        DIRECTORIO="."
fi

#Chequeo de opciones y argumento

echo "Directorio: $DIRECTORIO"
echo "Crear_Log: $Crear_Log"
echo "Bash: $Bash"

#Creacion de archivos de log y tar
Fecha=$(date +"%m-%d-%y_%H-%M-%S")
Logs="Logs_Caminos_${Fecha}.rep"
Tar="Backups_${Fecha}.tar.gz"



#Buscar ejecutables


#find "$DIRECTORIO" -type f -perm -4000 -perm -0001 | while read -r archivo; do
#        echo "Analizando archivo: $archivo"
#        if head -n 1 "$archivo" | grep -qE '^#!'; then
#               echo "script encontrado: $archivo"
#        fi
#done


while IFS= read -r archivo; do
        if $Bash; then
                head -n 1 "$archivo" | grep -q '^#!/bin/bash'
        fi
        echo "Script bash encontrado: $archivo"
        if $Crear_Log; then
                echo "$archivo" >> "$Logs"
        fi

        Scripts_encontrados+=("$archivo")

done < <(find "$DIRECTORIO" -type f -perm -4000 -perm -0001)


