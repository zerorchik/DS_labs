import numpy as np
import cv2 as cv

# Детектор кутів Харріса
def harris_corner_detector (filename, result_file):
    img = cv.imread(filename)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    dst = cv.cornerHarris(gray, 2, 3, 0.04)

    # Розширений результат для розмітки кутів
    dst = cv.dilate(dst, None)

    # Порогове значення для оптимального значення - може відрізнятися залежно від зображення
    img[dst > 0.01 * dst.max()] = [0, 0, 255]

    cv.imwrite(result_file, img)
    cv.imshow('Harris_Corner_Detector', img)
    if cv.waitKey(0) & 0xff == 27:
        cv.destroyAllWindows()

    return

# Дескриптор SIFT для заданих функцій на основі виявлення кутів Харріса
def sift_descriptors_on_harris (filename, result_file):

    def harris (img):
        gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        gray_img = np.float32(gray_img)
        dst = cv.cornerHarris(gray_img, 2, 3, 0.04)
        result_img = img.copy()  # Бекапна копія зображення

        # Порогове значення для оптимального значення - може відрізнятися залежно від зображення
        # Малює ключові точки кута Харріса на зображенні (RGB [0, 0, 255] -> синій)
        result_img[dst > 0.01 * dst.max()] = [0, 0, 255]
        # dst, більше за порогове значення = ключова точка
        keypoints = np.argwhere(dst > 0.01 * dst.max())
        keypoints = [cv.KeyPoint(float(x[1]), float(x[0]), 13) for x in keypoints]

        return (keypoints, result_img)

    img = cv.imread(filename)
    # Обчислюємо features кута Харріса та перетворюємо їх на ключові точки
    kp, img = harris(img)
    # Обчислюємо дескриптори SIFT з ключових точок Harris Corner
    sift = cv.SIFT_create()
    sift.compute(img, kp)
    img = cv.drawKeypoints(img, kp, img)

    cv.imwrite(result_file, img)
    cv.imshow('SIFT', img)
    if cv.waitKey(0) & 0xff == 27:
        cv.destroyAllWindows()

    return

# Порівняння двох зображень
def sift_feature_matching (filename_1, filename_2, result_file):

    img1 = cv.imread(filename_1, cv.IMREAD_GRAYSCALE)
    img2 = cv.imread(filename_2, cv.IMREAD_GRAYSCALE)

    # Запуск детектора SIFT
    sift = cv.SIFT_create()

    # Знаходження ключових точок та дескрипторів за допомогою SIFT
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    # Параметри FLANN
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)  # or pass empty dictionary
    flann = cv.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    # Створення маски
    matchesMask = [[0, 0] for i in range(len(matches))]

    # Тест співвідношення
    for i, (m, n) in enumerate(matches):
        if m.distance < 0.7 * n.distance:
            matchesMask[i] = [1, 0]

    draw_params = dict(matchColor=(0, 255, 0),
                       singlePointColor=(255, 0, 0),
                       matchesMask=matchesMask,
                       flags=cv.DrawMatchesFlags_DEFAULT)

    img3 = cv.drawMatchesKnn(img1, kp1, img2, kp2, matches, None, **draw_params)

    cv.imwrite(result_file, img3)
    cv.imshow('sift_feature_matching', img3)
    if cv.waitKey(0) & 0xff == 27:
        cv.destroyAllWindows()

    return

if __name__ == '__main__':

    descriptions = ['порівняння театра з зображенням на чашці', 'порівняння ракурса 1 театра зі шматком', 'порівняння ракурса 2 театра зі шматком']

    # Вибір режиму роботи програми
    print('Оберіть задачу для image descriptor:')
    for i in range(len(descriptions)):
        print(i + 1, '-', descriptions[i])
    data_mode = int(input('mode:'))
    # Якщо джерело даних існує
    if data_mode in range(1, len(descriptions) + 1):
        # Театр & чашка
        if (data_mode == 1):
            # Детектор кутів Харріса
            harris_corner_detector('theater_1.png', 'theater_1_harris.png')
            harris_corner_detector('cup.png', 'cup_harris.png')
            # Дескриптори SIFT для кутів Харріса
            sift_descriptors_on_harris('theater_1.png', 'theater_1_sift.png')
            sift_descriptors_on_harris('cup.png', 'cup_sift.png')
            # Співставлення ознак
            sift_feature_matching('theater_1.png', 'cup.png', 'theater_1_cup.png')
        # Театр & шматок
        elif (data_mode == 2):
            # Детектор кутів Харріса
            harris_corner_detector('theater_1.png', 'theater_1_harris.png')
            harris_corner_detector('theater_1_cut.png', 'theater_1_cut_harris.png')
            # Дескриптори SIFT для кутів Харріса
            sift_descriptors_on_harris('theater_1.png', 'theater_1_sift.png')
            sift_descriptors_on_harris('theater_1_cut.png', 'theater_1_cut_sift.png')
            # Співставлення ознак
            sift_feature_matching('theater_1.png', 'theater_1_cut.png', 'theater_1_theater_1_cut.png')
        # Театр 2 & шматок
        else:
            # Детектор кутів Харріса
            harris_corner_detector('theater_2.png', 'theater_2_harris.png')
            harris_corner_detector('theater_1_cut.png', 'theater_1_cut_harris.png')
            # Дескриптори SIFT для кутів Харріса
            sift_descriptors_on_harris('theater_2.png', 'theater_2_sift.png')
            sift_descriptors_on_harris('theater_1_cut.png', 'theater_1_cut_sift.png')
            # Співставлення ознак
            sift_feature_matching('theater_2.png', 'theater_1_cut.png', 'theater_2_theater_1_cut.png')