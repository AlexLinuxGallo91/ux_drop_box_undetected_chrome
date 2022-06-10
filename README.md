# Script experiencia de usuario en Drop Box

Script desarrollado en lenguaje Python con el fin de simular una experiencia de usuario por medio del uso del framework
Selenium. Como dato importante, solamente se ha probado en el navegador:
**Google Chrome/Chromium**.

## Comandos de ejecución

Se recomienda ejecutarlo desde un contenedor docker, para ello dentro del repositorio se encuentra el Dockerfile con las dependencias necesarias. Para ello solamente contruya la imagen con el siguiente comando:

```sh
docker build -t dropbox_ux .
```

Teniendo el contenedor arriba, podemos ejecutar de manera simplificada el script, pasando los siguientes argumentos en formato json

```json
{
  "user": "correodummy@gmail.com",
  "password": "soyunpassword",
  "pathImage": "/home/dummy/descargas"
}
```

Cada una de las propiedades en el json son vitales para la ejecucion del script, ya que son las credenciales necesarias
para poder acceder a la plataforma de drop box por medio del acceso con google. En cuanto a la propiedad "pathImage" en
el directorio en donde se almacenaran todas las descargas realizadas en el script.

**Ejecucion de script desde el contenedor Docker:**

A continuacion se muestra el ejemplo de ejecucion de la experiencia de usuario:

```bash
docker run -it --shm-size="2g" --user seluser -p 7900:7900 dropbox_ux /app/env/bin/python3 inicio_ux_dropbox.py '{"user":"dummy@gmail.com", "password":"dummy","pathImage": "/app/img25mb.png"}'
```





