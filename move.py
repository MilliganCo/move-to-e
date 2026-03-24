import os
import shutil
import subprocess

# Папки, которые хотим перенести
folders = [
    ".conda", ".anaconda", ".continuum", ".android", ".cache", ".gradle",
    ".matplotlib", ".ollama", ".qiskit", ".VirtualBox", ".vscode",
    ".insightface", ".venv"
]

user_profile = os.environ["USERPROFILE"]
target_root = "E:\\UsersData"

os.makedirs(target_root, exist_ok=True)

for folder in folders:
    src = os.path.join(user_profile, folder)
    dst = os.path.join(target_root, folder)

    if not os.path.exists(src):
        print(f"Пропущено (не найдено): {src}")
        continue

    # Перемещаем
    try:
        shutil.move(src, dst)
        print(f"Перемещено: {folder}")
    except Exception as e:
        print(f"Ошибка при перемещении {folder}: {e}")
        continue

    # Создаем симлинк
    try:
        subprocess.run(['cmd', '/c', f'mklink /D "{src}" "{dst}"'], check=True)
        print(f"Символическая ссылка создана: {folder}")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при создании симлинка для {folder}: {e}")
