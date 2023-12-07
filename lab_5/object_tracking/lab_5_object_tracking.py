import cv2

videos = ['V_1', 'V_2', 'V_3', 'V_4', 'V_5', 'V_6', 'V_7']
descriptions = ['чоловік', 'поїздка в транспорті', 'віддалення', 'команда', 'автомагістраль', 'пішохідний перехід', 'собака']
algs = ['MOSSE', 'KCF', 'CSRT']

# Вибір відео
print('Оберіть відео для object tracking:')
for i in range(len(descriptions)):
    print(i + 1, '-', descriptions[i])
data_mode = int(input('mode:'))
# Якщо джерело даних існує
if data_mode in range(1, len(videos) + 1):

    # Вибір алгоритму
    print('Оберіть алгоритм для object tracking:')
    for i in range(len(algs)):
        print(i + 1, '-', algs[i])
    alg_mode = int(input('mode:'))
    # Якщо джерело даних існує
    if alg_mode in range(1, len(algs) + 1):

        # Зчитування відео
        cap = cv2.VideoCapture('{0}.mp4'.format(videos[data_mode - 1]))
        # Визначення параметрів запису відео
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Використовуйте 'mp4v', або 'XVID' для кодування у mp4
        output_video = cv2.VideoWriter('{0}_{1}.mp4'.format(videos[data_mode - 1], algs[alg_mode - 1]), fourcc, 60, (int(cap.get(3)), int(cap.get(4))))

        # Зчитування першого кадру
        ret, frame = cap.read()
        # Встановлення ROI (Region of Interest) - об'єкт, який відслідковуємо
        x, y, w, h = cv2.selectROI(frame)

        # MOSSE
        if (alg_mode == 1):
            tracker = cv2.legacy.TrackerMOSSE_create()
        # KCF
        elif (alg_mode == 2):
            tracker = cv2.TrackerKCF_create()
        # CSRT
        elif (alg_mode == 3):
            tracker = cv2.TrackerCSRT_create()

        # Ініціалізація трекера
        tracker.init(frame, (x, y, w, h))

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Оновлення трекера
            ret, track_window = tracker.update(frame)
            # Малювання рамки відстежуваного об'єкту на кадрі
            x, y, w, h = int(track_window[0]), int(track_window[1]), int(track_window[2]), int(track_window[3])
            img2 = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # Запис кадра до вихідного відеофайлу
            output_video.write(frame)
            # Відображення результуючої рамки
            cv2.imshow('frame', img2)
            # Вихід з відео якщо натиснути 'q'
            if cv2.waitKey(1) == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()