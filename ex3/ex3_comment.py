# Constantes de la demo: nombres propios para no pisar ficheros ajenos.
DEMO_FILE = "vault_demo.txt"
COPY_FILE = "vault_demo_copy.txt"
DEMO_TEXT = (
    "[FRAGMENT 001] Digital preservation protocols established 2087\n"
    "[FRAGMENT 002] Knowledge must survive the entropy wars\n"
    "[FRAGMENT 003] Every byte saved is a victory against oblivion\n"
)


# Unica funcion que toca ficheros. Devuelve (exito, contenido_o_mensaje).
# tuple[bool, str] funciona en Python 3.10 sin importar typing.
# action: "r" (leer) o "w" (escribir); coincide con el modo de open().
def secure_archive(
    file_name: str,
    action: str = "r",
    content: str = "",
) -> tuple[bool, str]:
    # Validamos ANTES de abrir: asi un modo raro ("a", "rb"...) nunca llega
    # a open() y la anotacion de tipo (texto) no puede mentir.
    if action not in ("r", "w"):
        return (False, f"Invalid action '{action}'. Use 'r' or 'w'.")
    # with NO captura excepciones: solo garantiza el cierre. Por eso el
    # try/except va ALREDEDOR del with (open() y read() pueden fallar).
    try:
        with open(file_name, action, encoding="utf-8") as file:
            # Dentro del bloque: file.closed es False.
            if action == "r":
                # return dentro del with: el fichero se cierra igualmente.
                return (True, file.read())
            # "w" crea el fichero o LO VACIA si existe (al hacer open()).
            file.write(content)
            return (True, "Content successfully written to file")
    except (OSError, UnicodeDecodeError) as e:
        # OSError: Errno 2 (no existe), 13 (permisos), 21 (directorio)...
        # UnicodeDecodeError es un ValueError: fichero no UTF-8 (binario).
        # El subject muestra str(e) a secas, sin prefijo.
        return (False, str(e))
    # RECODING TASK (la scale pide demostrar que with cierra solo):
    # 'file' sigue existiendo tras el with. Anadiendo
    #     print(file.closed)   # dentro del with  -> False
    #     print(file.closed)   # justo despues    -> True
    # se ve el cierre automatico. Para hacerlo en el "read" hay que guardar
    # el resultado en una variable y hacer el return despues del with.


def main() -> None:
    print("=== Cyber Archives Security ===\n")

    # Preparamos un fichero regular con la propia funcion: el repo solo
    # contiene este .py, asi que no podemos suponer que ya exista uno.
    print("Using 'secure_archive' to create a demo file:")
    print(secure_archive(DEMO_FILE, "w", DEMO_TEXT))

    print("\nUsing 'secure_archive' to read from a nonexistent file:")
    print(secure_archive("/not/existing/file"))

    # /etc/master.passwd existe en macOS/BSD (ejemplo del subject); en Linux
    # no existe (Errno 2). /etc/sudoers es ilegible para un usuario normal
    # en ambos (Errno 13). Se ejecuta como usuario normal, nunca con sudo.
    print("\nUsing 'secure_archive' to read from an inaccessible file:")
    for path in ("/etc/master.passwd", "/etc/sudoers"):
        print(secure_archive(path))

    print("\nUsing 'secure_archive' to read from a regular file:")
    success, text = secure_archive(DEMO_FILE)
    # print de la tupla: los "\n" del contenido salen escapados (repr).
    print((success, text))

    # Escribimos el contenido leido antes, como pide el subject; solo si la
    # lectura fue bien (si no, text seria un mensaje de error).
    print("\nUsing 'secure_archive' to write previous content to a new file:")
    if success:
        print(secure_archive(COPY_FILE, "w", text))
    else:
        print((False, "No content to write"))

    # Caso invalido extra: accion desconocida -> (False, mensaje), sin crash.
    print("\nUsing 'secure_archive' with an invalid action:")
    print(secure_archive(DEMO_FILE, "x"))


if __name__ == "__main__":
    main()
