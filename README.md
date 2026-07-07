# MoveToE

Windows CLI-утилита для переноса выбранных пользовательских каталогов из `%USERPROFILE%` на другой диск с последующим созданием directory symlink.

## Статус аудита

Скрипт раньше сразу перемещал папки и создавал `mklink /D`. Теперь поведение безопаснее: по умолчанию это **dry-run**, реальные изменения выполняются только с `--apply`.

Проект можно рассматривать как public utility candidate после path-safety тестов и full-history scan.

## Что делает

- берёт набор папок из профиля пользователя Windows;
- показывает planned move/link operations;
- при `--apply` перемещает папки в `--target-root`;
- создаёт directory symlink, чтобы программы продолжали видеть каталог по старому пути;
- проверяет, что целевой путь не находится внутри `%USERPROFILE%`.

## Запуск

Dry-run:

```bash
python move.py
```

Реальное применение с подтверждением:

```bash
python move.py --target-root "E:\UsersData" --apply
```

Без интерактивного подтверждения:

```bash
python move.py --target-root "E:\UsersData" --apply --yes
```

Выбор конкретных папок:

```bash
python move.py --folders .cache .gradle .ollama --target-root "E:\UsersData"
```

## Ограничения

- Только Windows.
- Требуются права на создание directory symlink.
- Перед `--apply` сделайте backup важных данных.
- Если target находится на том же диске, место на системном диске может не освободиться.

## License recommendation

MIT после тестов path-safety и full-history scan.
