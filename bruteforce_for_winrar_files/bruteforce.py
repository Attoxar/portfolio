import rarfile
import string
import itertools
import tempfile
import os
import concurrent.futures
from PyQt5.QtWidgets import QInputDialog


def getTextInput(title, message):
    answer = QInputDialog.getText(None, title, message)
    if answer[1]:
        print(answer[0])
        return answer[0]
    else:
        return None


def brute_force_rar(file_path, max_password_length):
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for length in range(1, max_password_length + 1):
                for password in generate_passwords(length):
                    futures.append(executor.submit(extract_and_verify, file_path, password))

            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    print(f"Success! Password found: {result}")
                    return result

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except rarfile.Error as e:
        print(f"RAR file error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    print("Brute force attack failed. Password not found.")
    return None


def extract_and_verify(file_path, password):
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            with rarfile.RarFile(file_path) as rf:
                rf.extractall(path=temp_dir, pwd=password)
                if os.listdir(temp_dir):  # Check if any file is extracted
                    return password
        except rarfile.RarCRCError:
            pass  # Incorrect password
        except Exception as e:
            print(f"Extraction error with password {password}: {e}")
    return None


def generate_passwords(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    for password in itertools.product(characters, repeat=length):
        yield "".join(password)


if __name__ == "__main__":
    file_path = input("Enter the path to the RAR file: ")
    max_password_length = int(input("Enter the maximum password length to try: "))

    brute_force_rar(file_path, max_password_length)
