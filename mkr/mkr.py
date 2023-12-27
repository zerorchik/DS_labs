from PIL import Image, ImageDraw
from matplotlib import pyplot as plt
from PIL.ImageFilter import (
	BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
	EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN)

# Зчитування зображення
def image_read(file_name):
	# Відкриття файлу зображення
	image = Image.open(file_name)
	# Інструмент для малювання
	draw = ImageDraw.Draw(image)
	# Ширина зображення
	width = image.size[0]
	# Висота зображення
	height = image.size[1]
	# Значення пікселей для зображення
	pix = image.load()

	# Початкові характеристики
	print(f'\nПочаткове зображення: "{file_name}"')
	print(f'r = {pix[1, 1][0]},\tg = {pix[1, 1][1]},\tb = {pix[1, 1][2]}')

	# Виведення зображення
	plt.imshow(image)
	plt.show()
	image_info = {'image_file': image, 'image_draw': draw, 'image_width': width, 'image_height': height, 'image_pix': pix}

	return image_info

# Монохромне зображення
def monochrome(file_name_start):
	image_info = image_read(f'{file_name_start}.jpg')
	image = image_info['image_file']
	draw = image_info['image_draw']
	width = image_info['image_width']
	height = image_info["image_height"]
	pix = image_info['image_pix']

	print('Оберіть коефіціент монохромності:')
	factor = int(input('factor:'))

	for i in range(width):
		for j in range(height):
			a = pix[i, j][0]
			b = pix[i, j][1]
			c = pix[i, j][2]
			S = a + b + c
			# Рішення до якого з 2 кольорів поточне значення кольору ближче
			if (S > (((255 + factor) // 2) * 3)):
				a, b, c = 255, 255, 255
			else:
				a, b, c = 0, 0, 0
			draw.point((i, j), (a, b, c))

	# Виведення зображення
	plt.imshow(image)
	plt.show()

	# Кінцеві характеристики
	print(f'Кінцеве зображення: "{file_name_start}.jpg"')
	print(f'r = {pix[1, 1][0]},\tg = {pix[1, 1][1]},\tb = {pix[1, 1][2]}')

	# Збереження зображення
	file_name_stop = f'{file_name_start}_mono.jpg'
	image.save(file_name_stop, 'JPEG')
	del draw

	return

# Фільтрація
def filter(file_name_start, mode):
	image_info = image_read(f'{file_name_start}.jpg')
	image = image_info['image_file']
	draw = image_info['image_draw']

	# Фільтрація за обраним режимом
	image_filter = image.filter(filters[mode])

	# Виведення зображення
	plt.imshow(image_filter)
	plt.show()

	# Отримання значень пікселей для картинки
	pix = image_filter.load()

	# Кінцеві характеристики
	print(f'Кінцеве зображення: "{file_name_start}.jpg"')
	print(f'r = {pix[1, 1][0]},\tg = {pix[1, 1][1]},\tb = {pix[1, 1][2]}')

	# Збереження зображення
	file_name_stop = f'{file_name_start}_{filter_names[mode]}.jpg'
	image.save(file_name_stop, 'JPEG')
	del draw

	return

# Головні виклики
if __name__ == "__main__":

	file_name = 'img/friren'
	filters = [BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE, EMBOSS, FIND_EDGES, SHARPEN, SMOOTH, SMOOTH_MORE]
	filter_names = ['BLUR', 'CONTOUR', 'DETAIL', 'EDGE_ENHANCE', 'EDGE_ENHANCE_MORE', 'EMBOSS', 'FIND_EDGES', 'SHARPEN','SMOOTH', 'SMOOTH_MORE']

	print('\nОберіть режим роботи програми:')
	print('1 - Монохромне зображення')
	print('2 - Фільтрація')
	mode = int(input('mode:'))
	# Якщо режим існує
	if mode in range(1, 3):
		# Монохромне зображення
		if (mode == 1):
			monochrome(file_name)
		# Фільтрація
		if (mode == 2):
			print('\nОберіть варіант фільтрації:')
			for i in range(len(filters)):
				print(f'{i + 1} - {filter_names[i]}')
			mode = int(input('mode:'))
			# Якщо режим існує
			if mode in range(1, 11):
				filter(file_name, mode - 1)