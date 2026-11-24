import sys
import typing


# Devuelve el fichero abierto, o None si open() falla.
# typing.IO[str] = objeto fichero en modo texto (io.TextIOWrapper).
# "| None": la funcion puede devolver None (Python 3.10+).
def open_file(file_name: str) -> typing.IO[str] | None:
    try:
        # "r" = solo lectura; encoding fija UTF-8 (no depende del locale).
        return open(file_name, "r", encoding="utf-8")
    except OSError as e:
        # OSError agrupa FileNotFoundError (Errno 2), PermissionError
        # (Errno 13), IsADirectoryError (Errno 21), etc.
        # str(e) ya trae el texto "[Errno N] ...: 'nombre'".
        print(f"Error opening file '{file_name}': {e}")
        return None


def main() -> None:
    # sys.argv[0] es el script (como argv[0] en C): se esperan 2 elementos.
    if len(sys.argv) != 2:
        print("Usage: ft_ancient_text.py <file>")
        return  # sys.exit() no esta autorizado en el ex0
    name = sys.argv[1]
    print("=== Cyber Archives Recovery ===")
    print(f"Accessing file '{name}'")
    file = open_file(name)
    if file is None:
        # El error ya se imprimio en open_file; no hay nada que cerrar.
        return
    try:
        # read() devuelve todo el contenido como un unico str.
        content = file.read()
    except (OSError, UnicodeDecodeError) as e:
        # UnicodeDecodeError es un ValueError (no OSError): el fichero se
        # abrio bien pero sus bytes no son UTF-8 validos (p. ej. un binario).
        print(f"Error reading file '{name}': {e}")
    else:
        # El else del try solo se ejecuta si read() NO lanzo excepcion.
        print("---")
        # end="" evita un salto extra: el contenido ya acaba en "\n".
        print(content, end="")
        # Blindaje: si el fichero no acaba en "\n" (y no esta vacio), lo
        # anadimos para que el "---" final no quede pegado a la ultima linea.
        if content and not content.endswith("\n"):
            print()
        print("---")
    finally:
        # finally se ejecuta siempre (con o sin error): cierra el fichero
        # y solo despues avisa. No es "with", que esta prohibido hasta ex3.
        file.close()
        print(f"File '{name}' closed.")


if __name__ == "__main__":
    main()
