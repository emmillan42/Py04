import sys
import typing


# Unico sitio donde se escribe en stderr (fd 2). El prefijo es el que pide
# el subject. file=sys.stderr redirige print() al canal de errores.
def print_error(message: str) -> None:
    print(f"[STDERR] {message}", file=sys.stderr)


# Abre un fichero en el modo indicado ("r" por defecto, "w" escritura).
# Devuelve el objeto fichero o None si open() falla.
def open_file(file_name: str, mode: str = "r") -> typing.IO[str] | None:
    try:
        return open(file_name, mode, encoding="utf-8")
    except OSError as e:
        # OSError cubre Errno 2 (no existe), 13 (permisos), 21 (directorio).
        print_error(f"Error opening file '{file_name}': {e}")
        return None


# Abre, lee y cierra. Devuelve el contenido o None si algo falla.
def read_file(file_name: str) -> str | None:
    file = open_file(file_name)
    if file is None:
        return None
    try:
        # El return dentro del try no salta el finally: close() se ejecuta.
        return file.read()
    except (OSError, UnicodeDecodeError) as e:
        # UnicodeDecodeError es un ValueError: el fichero no es UTF-8 valido.
        print_error(f"Error reading file '{file_name}': {e}")
        return None
    finally:
        file.close()


# Anade "#" al final de cada linea. No imprime nada (solo transforma).
def transform(content: str) -> str:
    result = ""
    for char in content:
        if char == "\n":
            result += "#\n"
        else:
            result += char
    # Ultima linea sin "\n" final: la cerramos con "#" (sin inventar un "\n").
    if content and not content.endswith("\n"):
        result += "#"
    return result


# Escribe content en file_name. Devuelve True si todo fue bien.
def save_file(file_name: str, content: str) -> bool:
    # "w" crea el fichero o LO VACIA si ya existe (en el momento del open).
    file = open_file(file_name, "w")
    if file is None:
        return False
    try:
        # write() copia al buffer; el volcado a disco ocurre en close().
        file.write(content)
        return True
    except OSError as e:
        print_error(f"Error writing file '{file_name}': {e}")
        return False
    finally:
        file.close()


# Imprime el texto entre "---", como el subject.
def show(content: str) -> None:
    print("---")
    # end="" porque el contenido ya acaba en "\n" (evita linea en blanco).
    print(content, end="")
    # Blindaje: si no acaba en "\n", el "---" no debe quedar pegado.
    if content and not content.endswith("\n"):
        print()
    print("---")


# Sustituye a input() (prohibido en este ejercicio) usando sys.stdin.
def ask_file_name() -> str:
    # end="" deja el cursor tras el prompt. stdout tiene buffer: sin flush()
    # el prompt podria no verse antes de que readline() se quede esperando.
    print("Enter new file name (or empty): ", end="")
    sys.stdout.flush()
    # readline() NO quita el "\n": con Enter devuelve "\n"; con Ctrl+D (EOF)
    # devuelve "" y no lanza excepcion (a diferencia de input()).
    line = sys.stdin.readline()
    if line == "":
        # EOF: no hubo salto de linea del usuario, lo imprimimos nosotros.
        print()
    # strip() elimina el "\n" (y espacios sobrantes) de los extremos.
    return line.strip()


def main() -> None:
    # sys.argv[0] es el script, como argv[0] en C. sys.exit() no autorizado.
    if len(sys.argv) != 2:
        print("Usage: ft_stream_management.py <file>")
        return
    name = sys.argv[1]
    print("=== Cyber Archives Recovery & Preservation ===")
    print(f"Accessing file '{name}'")
    content = read_file(name)
    if content is None:
        return
    show(content)
    # El fichero de entrada YA esta cerrado (read_file lo cerro): el
    # mensaje es cierto y podemos sobrescribirlo si el usuario lo pide.
    print(f"File '{name}' closed.")
    new_content = transform(content)
    print("Transform data:")
    show(new_content)
    new_name = ask_file_name()
    # Enter o EOF dan "" tras strip(): en ambos casos no se guarda nada.
    if new_name == "":
        print("Not saving data.")
        return
    print(f"Saving data to '{new_name}'")
    if save_file(new_name, new_content):
        print(f"Data saved in file '{new_name}'.")
    else:
        # El error ya salio por stderr; esto va a stdout, como el subject.
        print("Data not saved.")


if __name__ == "__main__":
    main()
