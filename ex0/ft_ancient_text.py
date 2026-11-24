import sys
import typing


def open_file(file_name: str) -> typing.IO[str] | None:
    try:
        return open(file_name, "r", encoding="utf-8")
    except OSError as e:
        print(f"Error opening file '{file_name}': {e}")
        return None


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: ft_ancient_text.py <file>")
        return
    name = sys.argv[1]
    print("=== Cyber Archives Recovery ===")
    print(f"Accessing file '{name}'")
    file = open_file(name)
    if file is None:
        return
    try:
        content = file.read()
    except (OSError, UnicodeDecodeError) as e:
        print(f"Error reading file '{name}': {e}")
    else:
        print("---")
        print(content, end="")
        if content and not content.endswith("\n"):
            print()
        print("---")
    finally:
        file.close()
        print(f"File '{name}' closed.")


if __name__ == "__main__":
    main()
