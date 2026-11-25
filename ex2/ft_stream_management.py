import sys
import typing


def print_error(message: str) -> None:
    print(f"[STDERR] {message}", file=sys.stderr)


def open_file(file_name: str, mode: str = "r") -> typing.IO[str] | None:
    try:
        return open(file_name, mode, encoding="utf-8")
    except OSError as e:
        print_error(f"Error opening file '{file_name}': {e}")
        return None


def read_file(file_name: str) -> str | None:
    file = open_file(file_name)
    if file is None:
        return None
    try:
        return file.read()
    except (OSError, UnicodeDecodeError) as e:
        print_error(f"Error reading file '{file_name}': {e}")
        return None
    finally:
        file.close()


def transform(content: str) -> str:
    result = ""
    for char in content:
        if char == "\n":
            result += "#\n"
        else:
            result += char
    if content and not content.endswith("\n"):
        result += "#"
    return result


def save_file(file_name: str, content: str) -> bool:
    file = open_file(file_name, "w")
    if file is None:
        return False
    try:
        file.write(content)
        return True
    except OSError as e:
        print_error(f"Error writing file '{file_name}': {e}")
        return False
    finally:
        file.close()


def show(content: str) -> None:
    print("---")
    print(content, end="")
    if content and not content.endswith("\n"):
        print()
    print("---")


def ask_file_name() -> str:
    print("Enter new file name (or empty): ", end="")
    sys.stdout.flush()
    line = sys.stdin.readline()
    if line == "":
        print()
    return line.strip()


def main() -> None:
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
    print(f"File '{name}' closed.")
    new_content = transform(content)
    print("Transform data:")
    show(new_content)
    new_name = ask_file_name()
    if new_name == "":
        print("Not saving data.")
        return
    print(f"Saving data to '{new_name}'")
    if save_file(new_name, new_content):
        print(f"Data saved in file '{new_name}'.")
    else:
        print("Data not saved.")


if __name__ == "__main__":
    main()
