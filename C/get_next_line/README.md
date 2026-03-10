*Este proyecto ha sido creado como parte del currículo de 42 por cmelero-.*

# Descripción
Función get_next_line en C. Sirve para leer líneas  desde un descriptor de forma secuencial. El objetivo es poder leer línea por línea sin conocer de antemano el tamaño de la entrada, gestionando la memoria de forma dinámica y respetando el macro de compilación `BUFFER_SIZE`.

# Instrucciones

- Compilar con cc junto a un pograma que lo llame:
  ```
    cc -Wall -Wextra -Werror -D BUFFER_SIZE=10 get_next_line.c get_next_line_utils.c main.c -o main
  ```

# Algoritmo y justificación
La `get_next_line` hace una primera lectura del fichero utilizando el tamaño de BUFFER_SIZE.
El bucle principal simula una lectura caraceter a caracter llamando a una función ft_read_char(). Esa función se encarga de mantener una variable estática que contiene el valor entre lecturas y de leer el fichero cuando sea necesario.

Existe una lista enlazada que contiene un string del mismo tamañao que el buffer + 1. 

En cada llamada a 'ft_read_char', se almacena un nuevo caracter en el nodo inicial, cuando el nodo se llena, se crea otro.

Al terminar, se llama a la función 'ft_create_out()' que recorre, caracter a caracter componiendo el string de salida.

Ante cualquier error, se puede llamar a `ft_lst_clear` para limipiar la memoria desde cualquier punto del código.

Justificación:
- Utilziar una lista enlazada con bloques fijos permite acumular datos sin usar 'malloc()' ni reallocs.
- El último y único malloc devuelve una cadena con el tamaño exacto.

# Recursos
Compañeros de 42 y documentación sobre cómo usar listas y lectura de ficheros.
Uso de IA:
- Se ha usado IA (ChatGPT) para redactar y estructurar este README, aunque al final lo he rescrito todo :).

