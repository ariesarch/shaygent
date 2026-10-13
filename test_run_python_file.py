
from functions.run_python_file import run_python_file


def main():
    print("Running main.py:")
    print(run_python_file("calculator", "main.py"))

    print("\nRunning main.py with arguments:")
    print(run_python_file("calculator", "main.py", ["3 + 5"]))

    print("\nRunning tests.py:")
    print(run_python_file("calculator", "tests.py"))

    print("\nTrying to execute a file outside the working directory:")
    print(run_python_file("calculator", "../main.py"))

    print("\nTrying to execute a nonexistent file:")
    print(run_python_file("calculator", "nonexistent.py"))

    print("\nTrying to execute a non-Python file:")
    print(run_python_file("calculator", "lorem.txt"))


if __name__ == "__main__":
    main()
