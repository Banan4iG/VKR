import cv2
import numpy as np
from PIL import Image

img_1 = np.asarray(Image.open("E:/Никита/ИС-118/Диплом/VKR/123.jpg").convert('L'))
img_2 = np.asarray(Image.open("E:/Никита/ИС-118/Диплом/VKR/1231.jpg").convert('L'))

#img_1 = cv2.imread("E:/Никита/ИС-118/Диплом/VKR/rastr_admline200.png")
#img_2 = cv2.imread("rastr_admline1000.tif")

#Расчет функции SIFT
sift = cv2.xfeatures2d.SIFT_create()

psd_kp1, psd_des1 = sift.detectAndCompute(img_1, None)
psd_kp2, psd_des2 = sift.detectAndCompute(img_2, None)

# 4) Сопоставление признаков фланна
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)

flann = cv2.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(psd_des1, psd_des2, k=2)
goodMatch = []
for m, n in matches:
    # goodMatch - это отфильтрованная высококачественная пара. Если расстояние до первого совпадения в двух парах меньше 1/2 расстояния до второго совпадения, это может указывать на то, что первая пара является уникальной и неповторяющейся характерной точкой на двух изображениях. , Можно сохранить.
    if m.distance < 0.50*n.distance:
        goodMatch.append(m)
# Добавить измерение
goodMatch = np.expand_dims(goodMatch, 1)
print(goodMatch[:20])

img_out = cv2.drawMatchesKnn(img_1, psd_kp1, img_2, psd_kp2, goodMatch[:15], None, flags=2)

cv2.imshow('image', img_out)# Показать картинки
cv2.waitKey(0)# Дождитесь нажатия кнопки
cv2.destroyAllWindows()# Очистить все окна