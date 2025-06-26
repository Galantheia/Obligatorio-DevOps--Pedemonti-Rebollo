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


#Buscar ejecutables


find "$DIRECTORIO" -type f -perm -4000 -perm -0001 | while read -r archivo; do
        echo "Analizando archivo: $archivo"
        if head -n 1 "$archivo" | grep -qE '^#!'; then
               echo "script encontrado: $archivo"
        fi

