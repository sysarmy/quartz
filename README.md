# Dockerfile

Armé un Dockerfile para poder correr quartz en un container.

Traté de hacer modificaciones mínimas al .py para no romper nada a otras personas que puedan estar usandolo, las únicas 2 líneas que agrego no deberían afectar en ejecuciones que ya estén croneadas o a #110. El resto de las features (ponele) las implementé en un wrapper en ✨bash✨.

En el run el container espera las 3 variables de entorno necesarias para quartz. Asumiendo que la imagen se llama sysarmy/quartz:0.1, sería:

docker run \
> -e QUARTZ_API_KEY="n0h4yb4cKuP" \
> -e QUARTZ_URL="https://httpbin.org/post" \
> -e QUARTZ_ISP="Telecentro" \
> sysarmy/quartz:0.1
Se puede cronear directamente el contenedor, pero también le metí un cron file full latino cada 5 min a la imagen para que si se quiere dejar el container running pisando el CMD también se pueda. El único requisito acá es startear cron cuando levantemos el container. Ejemplo de en un docker-compose que queda corriendo:

quartz:
    image: sysarmy/quartz:0.1
    environment:
        QUARTZ_API_KEY: "n0h4yb4cKuP"
        QUARTZ_URL: "https://httpbin.org/post"
        QUARTZ_ISP: "Telecentro"
    command: /bin/bash -c "cron start && tail -F /app/quartz.log"
    restart: always
Y también va guardando un log en /app/quartz.log:

$ tail -5 /app/quartz.log
2022-02-17 01:10:20,848 - quartz - INFO - Datos subidos. Status code: 200
2022-02-17 01:15:45,985 - quartz - ERROR - El archivo /root/.config/quartz.conf tiene valores dummy.
2022-02-17 01:15:45,985 - quartz - ERROR - Revisá haber pasado las variables de entorno correctas al docker run.
2022-02-17 01:20:20,511 - quartz - INFO - Subiendo datos a https://httpbin.org/post.
2022-02-17 01:20:21,338 - quartz - INFO - Datos subidos. Status code: 200
Probado y funcionando bien en:

$ lsb_release -a
No LSB modules are available.
Distributor ID: Raspbian
Description:    Raspbian GNU/Linux 11 (bullseye)
Release:        11
Codename:       bullseye
$ lsb_release -a
LSB Version:    n/a
Distributor ID: ManjaroLinux
Description:    Manjaro Linux
Release:        21.2.3
Codename:       Qonos
