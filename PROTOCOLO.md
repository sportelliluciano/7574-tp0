# Protocolo de comunicaciones desarrollado

## Hipótesis y supuestos:
 - Los paquetes no pueden tener más de 8KB de largo
 - Se puede mandar más de una apuesta por request
 - El número a jugar siempre está entre 0000 y 9999.
 - Los nombres se codifican en UTF-8, y como máximo pueden tener hasta 30 caracteres.
 - El documento es un número entero en el rango [0, 4.294.967.295].
 - El encoding a utilizar es "network endian" (big endian).
 - Se asume que el año de nacimiento está entre 0000 y 9999


## Consideraciones adicionales
número - requiere 10 bits para ser representado
DNI - requiere 32 bits para ser representado
tamaño del paquete - requiere 13 bits para ser representado
nacimiento - requiere 10 bits para el año, 5 bits para el día y 5 para el mes -> total = 20 bits.
nombres / apellido: longitud arbitraria, terminados en un caracter nulo.

## Formato general de un paquete de datos
Todos los paquetes enviados y recibidos del servidor tienen un formato general como se observa en el 
siguiente gráfico:

----  2 bytes  -----  N bytes ----- 
|  tag & length  |    payload     |
0 -------------- 2 ------------- N+2

Los primeros dos bytes del paquete forman un entero sin signo de 16 bits codificado en big endian. De
esos 16 bits, los 3 más significativos guardan el tag y los 13 menos significativos la longitud del 
payload.

Por especificación, la longitud del payload está limitada a 8190 bytes, de modo que el paquete entero,
como máximo¸ sea de 8192 bytes.

Los tags indican qué tipo de operación se está realizando. Existen cuatro operaciones que los clientes 
pueden solicitar al servidor:
- `APUESTA` (tag = 0b001): Enviar una única apuesta al servidor
- `BATCH` (tag = 0b010): Enviar un varias apuestas al servidor
- `FIN` (tag = 0b011): Indicar al servidor que la agencia cerró y no enviará más apuestas
- `GANADORES` (tag = 0b100): Obtener el listado de ganadores del servidor

### Codificación del payload de cada comando

#### Apuesta
```
APUESTA (Tag code = 0b001):
    agencia: u8
    numero: u16,
    documento: u32,
    anio_nacimiento: u16,
    mes_nacimiento: u8,
    dia_nacimiento: u8,
    nombre: utf8strz,
    apellido: utf8strz,
```

#### Batch
Cada batch indica una cantidad de apuestas que vienen dentro del batch y después vienen las apuestas codificadas como en
el comando `APUESTA`, una detrás de la otra.

Dado que cada apuesta tiene como máximo, 253 caracteres, podemos aceptar hasta 32 apuestas por batch sin sobrepasar el límite
establecido de 8192 bytes por paquete.

```                u8 + u16 + u32 + u16 + u8 + u8 + 2 * (30 * utf8 char + \0)
MAX_SIZE(APUESTA) = 1 + 2 + 4 + 2 + 1 + 1 + 30 * 4 + 1 + 30 * 4 + 1 = 253 bytes
MAX APUESTAS POR BATCH: floor(8192 / 253) = 32
```

```
BATCH (Tag code = 0b010):
    cantidad: u16,
    APUESTA[]
```


#### Fin

```
FIN (Tag code = 0b011):
    agencia: u8
```

#### Ganadores
El comando ganadores no tiene payload (length = 0).
```
GANADORES (Tag code = 0b100):
```


## Respuestas obtenidas del servidor
Las respuestas se codifican en paquetes de la misma forma que los commandos, con un tag y una longitud de payload. El servidor
devuelve dos posibles respuestas, indicando éxito (`OK`) u error (`ERROR`). En el caso de las respuestas exitosas, un payload
opcional puede contener información extra requerida por el cliente (por ejemplo, la lista de ganadores). Para las respuestas 
erróneas, el servidor agrega en el payload un mensaje describiendo qué falló.


### Codificación de respuesta exitosa

`RESPUESTA` es el payload opcional y depende del comando enviado.
```
OK (Tag code = 0b111):
    RESPUESTA
```

### Codificación de respuesta errónea
```
ERROR (Tag code = 0b110):
    message: utf8strz
```


### Codificación de payload de respuesta GANADORES
```
RESPUESTA (GANADORES):
    cantidad: u32
    documentos: []u32
```