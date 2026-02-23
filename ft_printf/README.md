*Este proyecto ha sido creado como parte del currículo de 42 por cmelero-.*
## Descripción
Esta es una versión sencilla de printf. El objetivo es aprender a autilizar parámetros variables replicando el comportamiento de `printf` para  (c, s, p, d, i, u, x, X, %) usando argumentos variables. 

## Instrucciones

Compilar la biblioteca (desde la raíz del repositorio):
```sh
make
```
La regla `all` para generar `libftprintf.a`.

Compilar enlazando la biblioteca, por ejemplo:
```sh
cc -I. main.c -L. -lftprintf -o test_ft_printf
./test_ft_printf
```

Explicación del comando:
`cc -I. main.c -L. -lftprintf -o test_ft_printf`

- cc: invoca el compilador (gcc/clang).
- -I.: añade el directorio actual a la búsqueda de cabeceras (para `#include "ft_printf.h"`).
- main.c: archivo fuente que contiene tu función `main`.
- -L.: añade el directorio actual a la búsqueda de librerías en tiempo de enlace.
- -lftprintf: enlaza contra la librería `libftprintf` (busca `libftprintf.a` o `libftprintf.so`).
- -o test_ft_printf: nombre del binario generado.

## Algoritmo y elección de estructuras de datos

Resumen del algoritmo:
- El texto se mira carácter a carácter. Por cada uno se comprueba si es un `%`. Si no lo es, se escribe directamente con `write`.
- Si se detecta `%`, se llaman a diferentes funciones dependiendo del caracter encontrado: `c`, `s`, `p`, `d` o `i` (usan la misma), `u`, `x`, `X`, y `%%`.
- Para conversiones enteras (`d`/`i` y `u`) se convierten los valores numéricos a cadenas con funciones auxiliares.
- Para punteros se usa `uintptr_t` y una función recursiva (`ft_write_hex`) que imprime dígitos hexadecimales de más alto a más bajo orden.
- Para cadenas y caracteres se usan `write` iterativo o directo, con cuidados para `NULL` (imprime `(null)` para strings nulos y `(nil)` para punteros nulos).

Justificación:
- Las instrucciones del ejercicio indican que no se debe implementar el buffer de `printf`, por eso `ft_printf` utiliza directamente write.
- Conversión numérica a cadenas: simplifica la impresión y permite reutilizar la misma rutina de escritura; la memoria dinámica (malloc/free) se usa sólo temporalmente, manteniendo el consumo de memoria limitado.
- `uintptr_t` para punteros: garantiza que la representación en entero sin signo tiene tamaño suficiente para contener la dirección de memoria en plataformas estándares.
- Recursión para hex: implementación limpia y compacta para imprimir dígitos de más a menos significativo sin buffers intermedios grandes.

Limitaciones y consideraciones:
- No se implementan flags, anchuras, precisiones ni longitud de modificadores.
## Recursos
Referencias útiles para comprender y extender el proyecto:
- Documentación de C estándar y stdarg.
- Manual de printf y especificadores.
- Uso de uintptr_t: https://en.cppreference.com/w/c/types/integer
- Francinette para pruebas extremas.

Uso de IA:
- Para generar ideas para README, como el apartado "Recursos"
- Pregunta sobre funcionamientos específicos de printf y discusiones que me sirvieron para aprender porque se equivoda mucho y me obliga a razonar :)
