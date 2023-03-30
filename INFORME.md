# Informe

Luciano Sportelli Castro, padrón 99.565


## Ejercicio 1

Se agregó un nuevo client al archivo Docker Compose. Utilizando el mismo comando que anteriormente, ahora se iniciarán dos clientes.


## Ejercicio 1.1 | Generador de Docker Compose con N clientes

Para ejecutar el generador, se debe correr el siguiente comando:

```bash
$ ./generate-docker-compose <N_CLIENTES>
```

Donde `N_CLIENTES` es la cantidad de clientes que tendrá el archivo generado.

El resultado se emitirá por la salida estándar. Para guardarlo a un archivo, se puede
aprovechar la redirección de la terminal:

```bash
$ ./generate-docker-compose 5 > docker-compose-with-5-clients.yaml
```

# Ejercicio 3 | Tests con Netcat

Para correr los tests con netcat, se provee un nuevo target en el `Makefile`: `nc_tests`.

Los tests a ejecutar envían blobs de caracteres ASCII al servidor de tamaños 8, 16, 32, 64, 128 y 256.

Ejemplo:

```bash
$ make nc_tests
```