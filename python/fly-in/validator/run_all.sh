#!/usr/bin/env bash

set -u

MAPS_ROOT="../maps"
SOLUTIONS_DIR="./soluciones"
VALIDATOR="./validate_simulation.py"
PROGRAM="./fly-in.py"

mkdir -p "$SOLUTIONS_DIR"

if [ ! -f "$PROGRAM" ]; then
    echo "Error: no existe $PROGRAM"
    exit 1
fi

if [ ! -f "$VALIDATOR" ]; then
    echo "Error: no existe $VALIDATOR"
    exit 1
fi

for level in easy medium hard challenger; do
    dir="$MAPS_ROOT/$level"

    if [ ! -d "$dir" ]; then
        echo "Aviso: no existe el directorio $dir"
        continue
    fi

    find "$dir" -maxdepth 1 -type f -name "*.txt" | sort | while IFS= read -r mapfile; do
        base="$(basename "$mapfile" .txt)"
        solution_file="$SOLUTIONS_DIR/${level}__${base}.out"

        echo "========================================"
        echo "Mapa: $mapfile"
        echo "Salida: $solution_file"

        if python3 "$PROGRAM" "$mapfile" > "$solution_file"; then
            echo "Simulación generada correctamente"
        else
            status=$?
            echo "Error al ejecutar $PROGRAM con $mapfile (exit $status)"
            continue
        fi

        if python3 "$VALIDATOR" "$mapfile" "$solution_file"; then
            echo "Validación OK"
			echo "Turnos: " $( cat "$solution_file" | wc -l)
        else
            status=$?
            echo "Validación FALLIDA para $mapfile (exit $status)"
        fi
    done
done