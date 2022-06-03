# Script experiencia de usuario en Drop Box

Script desarrollado en lenguaje Python con el fin de simular una experiencia de usuario por medio del uso del framework
Selenium. Como dato importante, solamente se ha probado en dos navegadores y por los cuales recomiendo solamente:
**Google Chrome/Chromium y Mozilla Firefox**.

## Comandos de ejecución

Una vez instalado el proyecto con todas las dependencias se necesita pasar como argumento una cadena json con cada una
de las siguientes propiedades:

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

A continuacion se muestran ejemplos de como se ejecutan en distintos entornos ya sea en un ambiente de test/produccion o
en cualquier IDE:

**IDE Pycharm en Windows:**

```
"{\"user\":\"correodummy@gmail.com\",
\"password\":\"soyunpassword\",
\"pathImage\":\"C:\\Users\\dummy\\Desktop\\img_25mb.png\"}"
```

**Ambiente Linux:**

```bash
python3 '{"user":"dummy@gmail.com",
"password":"dummy","pathImage":
"/home/dummy/images/img_25mb.png"}'
```

