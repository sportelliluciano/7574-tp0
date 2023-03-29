Hipótesis y supuestos:
 - Los paquetes no pueden tener más de 8KB de largo
 - Se puede mandar más de una apuesta por request
 - El número a jugar siempre está entre 0000 y 9999.
 - Los nombres se codifican en UTF-8, y como máximo pueden tener hasta 100 caracteres.
 - El documento es un número entero en el rango [0, 4.294.967.295].
 - El encoding a utilizar es "network endian" (big endian).
 - Se asume que el año de nacimiento está entre 0000 y 9999


número - requiere 10 bits para ser representado
DNI - requiere 32 bits para ser representado
tamaño del paquete - requiere 13 bits para ser representado
nacimiento - requiere 10 bits para el año, 5 bits para el día y 5 para el mes -> total = 20 bits.
nombres / apellido: longitud arbitraria, terminados en un caracter nulo.

                2 bytes     N bytes
- Paquete: | tag & length | payload |

Tag & Length:
 - Tag = { APUESTA, BATCH, FIN, GANADORES }, 3 bits, 001, 010, 011, 100, el resto es invalido
 - Length = 13 bits (0 - 8190 = 8192 - 2 bytes de tag & length)

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

```
BATCH (Tag code = 0b010):
    APUESTA[]
```

```
FIN (Tag code = 0b011):
```

```
GANADORES (Tag code = 0b100):
```


## Respuestas:

OK(respuesta), ERROR(message)

```
OK (Tag code = 0b111):
    RESPUESTA
```

```
ERROR (Tag code = 0b110):
    message: utf8strz
```

```
RESPUESTA (GANADORES):
    cantidad: u32

RESPUESTA (otros): nada
```