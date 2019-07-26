#!/bin/bash


echo $TOKEN > /tmp/token

su -c 'ttyd -m 1 bash' alumno
