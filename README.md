# Лабораторная работа 2. Бинаризация

## Метод обработки

**Вариант 11**

Исходное RGB-изображение предварительно переводится в полутоновое вручную по формуле:

`Y = 0.3R + 0.59G + 0.11B`

После этого выполняется адаптивная бинаризация **методом Феня и Тана**.  
Размер локального окна обработки — **3×3**.

## Что делает программа

1. Берёт цветные изображения из папки `input_images`
2. Переводит их в полутоновое изображение вручную
3. Выполняет бинаризацию
4. Сохраняет результаты в папку `output_images`

## Как подготовить проект
Рядом с `lab2.py` должны быть папки и файлы:



В папку `input_images` нужно положить исходные цветные изображения формата:
- `.png`
- `.bmp`

Пример:


1. `01_original.png`
![01_original.png](input_images/01_original.png)

2. `zhest_01.png`
![zhest_01.png](input_images/zhest_01.png)

## Запуск
Запуск из терминала:

```bash
python lab2.py
```

Если используется виртуальное окружение:

```bash
source .venv/bin/activate
python lab2.py
```

## Результат
После запуска в папке `output_images` для каждого входного изображения появятся 3 файла:

- `имя_файла_gray.bmp` — полутоновое изображение
- `имя_файла_binary.png` — бинарное изображение
- `имя_файла_result.png` — итоговая картинка, где рядом показаны:
  - исходное изображение
  - полутоновое изображение
  - бинарное изображение

Пример:
1.1 `01_original_gray.bmp`

![01_original_gray.bmp](output_images/01_original_gray.bmp)

2.1 `zhest_01_gray.bmp`![zhest_01_gray.bmp](output_images/zhest_01_gray.bmp)


1.2 `01_original_binary.png`

![01_original_binary.png](output_images/01_original_binary.png)

2.2 `zhest_01_binary.png`

![zhest_01_binary.png](output_images/zhest_01_binary.png)

1.3 `01_original_result.png`

![01_original_result.png](output_images/01_original_result.png)

2.3 `zhest_01_result.png`

![zhest_01_result.png](output_images/zhest_01_result.png)