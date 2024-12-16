import cv2
import numpy as np

def decode_image(file):
    img_bytes = np.frombuffer(file.read(), np.uint8)       
    result = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)     
    if result is None:
        return "Error: Unable to decode image", 400
    return result


def check_brightness(img, lower_threshold, upper_threshold):
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    avg_brightness = img.mean()
    
    if avg_brightness > upper_threshold:
        return (f"Фото слишком яркое (Средняя яркость: {avg_brightness:.2f})")
    elif avg_brightness < lower_threshold:
        return (f"Фото слишком тёмное (Средняя яркость: {avg_brightness:.2f})")
    else:
        return (f"Освещённость в норме (Средняя яркость: {avg_brightness:.2f})")
    

def check_blurriness(img, slightly_blur_value=50, strong_blur_value=150):
    if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(img, cv2.CV_64F).var()

    if laplacian_var < strong_blur_value:
        return (f"Картинка сильно размыта (Резкость: {laplacian_var:.2f})")
    elif laplacian_var < slightly_blur_value:
        return (f"Картинка слегка размыта (Резкость: {laplacian_var:.2f})")
    else:
        return (f"Картинка чёткая (Резкость: {laplacian_var:.2f})")
    

def check_vibrancy(img, low_saturation_value=30, high_saturation_value=150):
    if len(img.shape) == 3:
        # Преобразовать в HSV
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    else:
        return "Изображение в оттенках серого, не может быть оценено по красочности."

    # Извлечь канал насыщенности (S)
    saturation = hsv[:, :, 1]

    # Среднее и стандартное отклонение по насыщенности
    mean_saturation = np.mean(saturation)
    std_saturation = np.std(saturation)

    if std_saturation > high_saturation_value:
        return f"Картинка очень красочная (Насыщенность: {mean_saturation:.2f}, Отклонение: {std_saturation:.2f})"
    elif std_saturation > low_saturation_value:
        return f"Картинка достаточно красочная (Насыщенность: {mean_saturation:.2f}, Отклонение: {std_saturation:.2f})"
    else:
        return f"Картинка тусклая (Насыщенность: {mean_saturation:.2f}, Отклонение: {std_saturation:.2f})"
    

def check_resolution(img):
    height, width = img.shape[:2]
    ratio = width / height
    return (f"Разрешение: {height} x {width} (Соотношение: {ratio})")