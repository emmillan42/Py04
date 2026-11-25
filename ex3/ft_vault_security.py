DEMO_FILE = "vault_demo.txt"
COPY_FILE = "vault_demo_copy.txt"
DEMO_TEXT = (
    "[FRAGMENT 001] Digital preservation protocols established 2087\n"
    "[FRAGMENT 002] Knowledge must survive the entropy wars\n"
    "[FRAGMENT 003] Every byte saved is a victory against oblivion\n"
)


def secure_archive(
    file_name: str,
    action: str = "r",
    content: str = "",
) -> tuple[bool, str]:
    if action not in ("r", "w"):
        return (False, f"Invalid action '{action}'. Use 'r' or 'w'.")
    try:
        with open(file_name, action, encoding="utf-8") as file:
            if action == "r":
                return (True, file.read())
            file.write(content)
            return (True, "Content successfully written to file")
    except (OSError, UnicodeDecodeError) as e:
        return (False, str(e))


def main() -> None:
    print("=== Cyber Archives Security ===\n")

    print("Using 'secure_archive' to create a demo file:")
    print(secure_archive(DEMO_FILE, "w", DEMO_TEXT))

    print("\nUsing 'secure_archive' to read from a nonexistent file:")
    print(secure_archive("/not/existing/file"))

    print("\nUsing 'secure_archive' to read from an inaccessible file:")
    for path in ("/etc/master.passwd", "/etc/sudoers"):
        print(secure_archive(path))

    print("\nUsing 'secure_archive' to read from a regular file:")
    success, text = secure_archive(DEMO_FILE)
    print((success, text))

    print("\nUsing 'secure_archive' to write previous content to a new file:")
    if success:
        print(secure_archive(COPY_FILE, "w", text))
    else:
        print((False, "No content to write"))

    print("\nUsing 'secure_archive' with an invalid action:")
    print(secure_archive(DEMO_FILE, "x"))


if __name__ == "__main__":
    main()
