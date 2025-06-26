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

if [ -z "$DIRECTORIO" ]; then
        DIRECTORIO="."
fi

if [ ! -d "$DIRECTORIO" ]; then
	echo "Error: '$DIRECTORIO' no es un directorio valido" >&2
	exit 2
fi

#Chequeo de opciones y argumento

echo "Directorio: $DIRECTORIO"
echo "Crear_Log: $Crear_Log"
echo "Bash: $Bash"

#Creacion de archivos de log y tar
Fecha=$(date +"%m-%d-%y_%H-%M-%S")
Logs="Logs_Caminos_${Fecha}.rep"
Tar="Backups_${Fecha}.tar.gz"

#Archivo log

if [ "$Crear_Log"=true ]; then
        if [ "$Bash"=true ]; then
                echo "Caminos a los scripts encontrados solo de bash:" > "$Logs"
        else
                echo "Caminos a los scripts encontrados:" > "$Logs"
        fi
fi

#Inicializacion de array

Scripts_encotrados=()

#Buscar ejecutables y guardarlos en array


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

#Agregar log al archivo de backup

if [ "Crear_Log"=true ]; then
        echo "agregando log al array: $Logs"
        Scripts_encontrados+=("$Logs")

fi

#Agregar archivos al backup

if [ ${#Scripts_encontrados[@]} -gt 0 ]; then
        tar -czf "$Tar" "${Scripts_encontrados[@]}"
        echo "Back creado: $Tar"
else
        echo "No se encontraron archivos. Backup no creado." 
fi
