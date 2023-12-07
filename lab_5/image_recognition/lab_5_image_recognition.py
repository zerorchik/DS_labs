import cv2
import numpy as np
from matplotlib import pyplot as plt

# Зчитування зображення
def image_read (file_name):
    image = cv2.imread(file_name, cv2.IMREAD_COLOR)
    plt.imshow(image)
    plt.show()

    return image

# Обробка зображення
def image_processing (file_name, image):
    # Перетворити в градації сірого
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Розмиття за допомогою ядра 3 * 3
    gray_blurred = cv2.blur(gray, (3, 3))
    cv2.imwrite(file_name, gray_blurred)
    plt.imshow(gray_blurred)
    plt.show()

    return gray_blurred

# Розпізнавання кругів на зображеннях
def circle_recognition(image, processed_image, file_name, var):
    # Застосування трансформації Хафа до розмитого зображення
    # circles
    if (var == 1):
        detected_circles = cv2.HoughCircles(processed_image,
                                            cv2.HOUGH_GRADIENT, 1, 20, param1=10,
                                            param2=100, minRadius=1, maxRadius=400)
    # jalynka
    elif (var == 2):
        detected_circles = cv2.HoughCircles(processed_image,
                                            cv2.HOUGH_GRADIENT, 1, 20, param1=250,
                                            param2=55, minRadius=1, maxRadius=400)
    # jalynka_2
    else:
        detected_circles = cv2.HoughCircles(processed_image,
                                            cv2.HOUGH_GRADIENT, 1, 20, param1=250,
                                            param2=100, minRadius=1, maxRadius=400)

    # Малювання виявлених кіл
    if detected_circles is not None:
        # Перетворення параметрів кола a, b і r на цілі числа
        detected_circles = np.uint16(np.around(detected_circles))
        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]
            # Малювання окружності кола
            cv2.circle(image, (a, b), r, (0, 255, 0), 7)
            # Малювання маленького кола (радіусом 1), щоб показати центр
            cv2.circle(image, (a, b), 1, (0, 0, 255), 10)
        print("Знайдено {0} круглих об'єктів".format(len(detected_circles[0, :])))
        cv2.imwrite(file_name, image)
        plt.imshow(image)
        plt.show()

    return

if __name__ == '__main__':

    images = ['circles.jpg', 'jalynka.jpg', 'jalynka_2.jpg']
    descriptions = ['круги', 'ялинкові прикраси', 'ялинкові прикраси 2']
    processed_images = ['circles_filtred.jpg', 'jalynka_filtred.jpg', 'jalynka_2_filtred.jpg']
    results = ['circles_reconition.jpg', 'jalynka_reconition.jpg', 'jalynka_2_reconition.jpg']

    # Вибір зображення
    print('Оберіть зображення для image recognition:')
    for i in range(len(descriptions)):
        print(i + 1, '-', descriptions[i])
    data_mode = int(input('mode:'))
    # Якщо джерело даних існує
    if data_mode in range(1, len(images) + 1):

        image = image_read(images[data_mode - 1])
        processed_image = image_processing(processed_images[data_mode - 1], image)
        circle_recognition(image, processed_image, results[data_mode - 1], data_mode)