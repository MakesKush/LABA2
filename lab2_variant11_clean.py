import os

import numpy as np
from PIL import Image

input_dir = 'input_images'
output_dir = 'output_images'
allowed = {'.bmp', '.png'}

w1 = 3
w2 = 15
alpha1 = 0.12
k1 = 0.20
k2 = 0.03
gamma = 2.0


def odd(x):
    return x if x % 2 == 1 else x + 1


w1 = odd(w1)
w2 = odd(w2)
if w2 < w1:
    w2 = odd(w1 + 2)


def load_image(path):
    return np.array(Image.open(path).convert('RGB'), dtype=np.uint8)


def to_gray(img):
    r = img[:, :, 0].astype(np.float64)
    g = img[:, :, 1].astype(np.float64)
    b = img[:, :, 2].astype(np.float64)
    y = 0.3 * r + 0.59 * g + 0.11 * b
    return np.clip(np.rint(y), 0, 255).astype(np.uint8)


def integral(img):
    s = np.zeros((img.shape[0] + 1, img.shape[1] + 1), dtype=np.float64)
    s[1:, 1:] = img.astype(np.float64).cumsum(axis=0).cumsum(axis=1)
    return s


def area_sum(s, top, left, bottom, right):
    return s[bottom, right] - s[top, right] - s[bottom, left] + s[top, left]


def binarize(gray):
    h, w = gray.shape
    gray_f = gray.astype(np.float64)

    p1 = w1 // 2
    p2 = w2 // 2

    a = np.pad(gray_f, p1, mode='edge')
    b = np.pad(gray_f, p2, mode='edge')

    s1 = integral(a)
    s2 = integral(a * a)

    out = np.zeros((h, w), dtype=np.uint8)
    area = w1 * w1

    for y in range(h):
        for x in range(w):
            t1 = y
            l1 = x
            b1 = y + w1
            r1 = x + w1

            sm = area_sum(s1, t1, l1, b1, r1)
            sq = area_sum(s2, t1, l1, b1, r1)

            m = sm / area
            var = sq / area - m * m
            if var < 0:
                var = 0
            s = np.sqrt(var)

            reg1 = a[t1:b1, l1:r1]
            M = float(reg1.min())

            t2 = y
            l2 = x
            b2 = y + w2
            r2 = x + w2
            reg2 = b[t2:b2, l2:r2]

            R = float(reg2.max()) - float(reg2.min())

            if R <= 1e-9:
                T = m
            else:
                ratio = s / R
                a2 = k1 * (ratio ** gamma)
                a3 = k2 * (ratio ** gamma)
                T = (1 - alpha1) * m + a2 * ratio * (m - M) + a3 * M

            out[y, x] = 255 if gray_f[y, x] > T else 0

    return out


def save_strip(rgb, gray, binary, path):
    gray_rgb = np.stack([gray, gray, gray], axis=2)
    binary_rgb = np.stack([binary, binary, binary], axis=2)
    strip = np.concatenate([rgb, gray_rgb, binary_rgb], axis=1)
    Image.fromarray(strip).save(path)


def save_img(arr, path):
    Image.fromarray(arr).save(path)


def main():
    if not os.path.exists(input_dir):
        os.makedirs(input_dir, exist_ok=True)
        return

    os.makedirs(output_dir, exist_ok=True)

    files = []
    for name in sorted(os.listdir(input_dir)):
        path = os.path.join(input_dir, name)
        ext = os.path.splitext(name)[1].lower()
        if os.path.isfile(path) and ext in allowed:
            files.append(path)

    for path in files:
        img = load_image(path)
        gray = to_gray(img)
        binary = binarize(gray)

        base = os.path.splitext(os.path.basename(path))[0]
        save_img(gray, os.path.join(output_dir, base + '_gray.bmp'))
        save_img(binary, os.path.join(output_dir, base + '_binary.png'))
        save_strip(img, gray, binary, os.path.join(output_dir, base + '_result.png'))

    print('done')


if __name__ == '__main__':
    main()
