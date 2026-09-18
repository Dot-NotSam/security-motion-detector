import cv2


def to_grayscale(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


def remove_noise(gray_frame, kernel_size=21):
    if kernel_size % 2 == 0:
        kernel_size += 1
    return cv2.GaussianBlur(gray_frame, (kernel_size, kernel_size), 0)


def preprocess_frame(frame, blur_kernel=21):
    gray = to_grayscale(frame)
    blurred = remove_noise(gray, blur_kernel)
    return blurred
