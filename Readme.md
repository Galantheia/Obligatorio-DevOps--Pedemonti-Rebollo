# backup_setuid.sh

Este script busca archivos ejecutables con el permiso SetUID activado, comenzando desde un directorio especificado (o desde el directorio actual si no se especifica ninguno).

Permite generar un archivo de log con los caminos encontrados y filtrar solo scripts de Bash. Todos los archivos encontrados se comprimen en un archivo .tar.gz.

## Uso

./backup_setuid.sh [-c] [-b] [directorio]

- -c: genera un log (.rep) con los caminos absolutos de los archivos encontrados.
- -b: filtra solo scripts de Bash (que comiencen con #!/bin/bash).
- directorio: (opcional) directorio desde el cual comenzar la búsqueda. Si no se especifica, se usa el directorio actual.

## Ejemplo

./backup_setuid.sh -c -b /

Esto busca desde la raíz (/), genera un log y solo incluye scripts de Bash con permisos setuid y ejecución para otros usuarios.

El resultado será un archivo .tar.gz con los archivos encontrados y el archivo de log.

![image](https://github.com/user-attachments/assets/a5e74a1e-5042-4c99-ab17-8a2757ea47cb)

## Requisitos

- Bash
- Permisos para acceder a los archivos en el sistema

## Códigos de salida

- 0: ejecución exitosa
- 1: opción inválida
- 2: directorio inválido
