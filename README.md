# 🌐 Quartz
### [Acceso al dasboard](https://p.datadoghq.com/sb/exn9bbykwolqugo9-55d2ee56bac10a8d432eeb3d419d10b7) | ヽ(^-^)ρ┳┻┳°σ(^o^)/
[![](https://img.shields.io/website?down_message=offline&label=dashboard&style=flat-square&up_message=online&url=https%3A%2F%2Fp.datadoghq.com%2Fsb%2Fexn9bbykwolqugo9-55d2ee56bac10a8d432eeb3d419d10b7)](https://p.datadoghq.com/sb/exn9bbykwolqugo9-55d2ee56bac10a8d432eeb3d419d10b7)
![](https://img.shields.io/github/issues/sysarmy/quartz?&style=flat-square)
![](https://img.shields.io/github/workflow/status/sysarmy/quartz/Docker?&style=flat-square)
![](https://img.shields.io/github/license/sysarmy/quartz?label=licencia&style=flat-square)

## ¿Qué es Quartz?

Quartz se armó con la idea de ser un [MRTG](https://es.wikipedia.org/wiki/MRTG) de los proveedores de Internet de Argentina. Es un dashboard público que permite obtener información sobre las conexiones a Internet de diferentes proveedores en diferentes zonas del país. La información se obtiene de clientes que envían de manera periódica ejecuciones del cliente de Quartz, que hace pings a diferentes anchors de [RIPE Atlas](https://en.wikipedia.org/wiki/RIPE_Atlas).

## ¿Cómo contribuyo con información sobre mi ISP?

Para poder sumar información sobre tu conexión al dasboard podés hacerlo de 2 maneras:

### 1. Instalando paquete .deb y armando un cron job

```
WIP
```

### 2. Usando la imagen de Docker de Quartz

Armamos una imagen de Docker que espera 3 variables de entorno en el run:
1. `QUARTZ_URL`: URL del endpoint.
2. `QUARTZ_API_KEY`: la key para pegarle al endpoint.
3. `QUARTZ_ISP`: nombre de tu proveedor de Internet.

Suponiendo que la estas variables sean `https://httpbin.org/post`, `n0h4yb4cKuP` y `Telecentro` respectivamente, se puede usar usar la imagen de Docker de la siguiente manera:

```console
docker run \
> -e QUARTZ_URL="https://httpbin.org/post" \
> -e QUARTZ_API_KEY="n0h4yb4cKuP" \
> -e QUARTZ_ISP="Telecentro" \
> ghcr.io/sysarmy/quartz:main
```

Podés cronear directamente la ejecución o también dejarlo corriendo pisando el `CMD` del propio container, ya que dentro del mismo hay un cron job que ejecuta Quartz cada 5 minutos. El único requisito es levantar cron cuando corarmos el container. Ejemplo de en un docker-compose que queda corriendo:

```yaml
quartz:
    image: sysarmy/quartz:0.1
    environment:
        QUARTZ_URL: "https://httpbin.org/post"
        QUARTZ_API_KEY: "n0h4yb4cKuP"
        QUARTZ_ISP: "Telecentro"
    command: /bin/bash -c "cron start && tail -F /app/quartz.log"
    restart: always
```

Adicionalmente dejando la ejecución automática va a ir guardando un log en `/app/quartz.log`.

## ¿Puedo contribuir con código?

¡Obvio! Si ves algún error o algo que se podría mejorar, toda contribución es bienvenida. Podés fijarte si hay algún issue abierto o directamente [hacer un fork y mandar tu pull request](https://github.com/firstcontributions/first-contributions/blob/master/translations/README.es.md).