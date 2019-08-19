#!/bin/bash

#Este script inicia el todos los sistemas locales de forma adecuada

function modoUso() {
    echo "start.sh -m archivo -p directorio -d direcotrio"
    echo "OPCIONES:"
    echo "   -m archivo: archivo con direcciones mac de alumos"
    echo "   -p directorio: plantilla de directorio a copiar para cada alumno"
    echo "   -d directorio donde se crearan directorios de alumnos"
}

function validarParams() {
    [[ ! -f "$1" ]] || [[ ! -d "$2" ]] || [[ ! -d "$3" ]] || [[ "$2" == "$3" ]] && { modoUso; exit 1; }
}

opcionM=""
paramM=""
opcionP=""
paramP=""
opcionD=""
paramD=""

while getopts ":m:p:d:" opt; do
    case $opt in
	m)
	    opcionM="1";
	    paramM="$OPTARG"
	    ;;
	p)
	    opcionP="1";
	    paramP="$OPTARG"
	    ;;
	d)
	    opcionD="1";
	    paramD="$OPTARG"
	    ;;
	"?")
	    echo "Opción inválida -$OPTARG";
	    exit 1;
	    ;;
	:)
	    echo "Se esperaba un parámetro en -$OPTARG";
	    exit 1;
	    ;;
    esac
done

shift $((OPTIND-1)) #borrar todos los params que ya procesó getopts

validarParams $paramM $paramP $paramD

for nombre in "$(cat "$paramM" | cut -d ',' -f 2)"; do
    out="$paramD/$nombre"
    mkdir -p "$out"
    cp -R "$paramP" "$out"
done

# Reiniciar BD sandboxer
rm sandboxer/app/db.sqlite3 2> /dev/null
python sandboxer/app/manage.py migrate

# Quitar contenedores ttyd
docker stop $(docker ps | grep cplus | egrep -o "^[a-zA-Z0-9]{12}") 2> /dev/null

# Lanzar monitor
trap 'kill $BGPID; exit' INT
python monitor/monitor.py $paramM $paramD  &
BGPID=$!

# Lanzar sandboxer

python sandboxer/app/manage.py runserver 0.0.0.0:8181
