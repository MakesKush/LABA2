import os

import numpy as np
from PIL import Image

input_dir = 'input_images'
output_dir = 'output_images'
allowed = {'.bmp', '.png'}

alpha1 = 0.12
k1 = 0.20
k2 = 0.03
gamma = 2.0


def odd(x):
    return x if x % 2 == 1 else x + 1


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


def binarize(gray, w_local, w_range):
    w_local = odd(w_local)
    w_range = odd(w_range)

    if w_range < w_local:
        w_range = w_local

    h, w = gray.shape
    gray_f = gray.astype(np.float64)

    p1 = w_local // 2
    p2 = w_range // 2

    a = np.pad(gray_f, p1, mode='edge')
    b = np.pad(gray_f, p2, mode='edge')

    s1 = integral(a)
    s2 = integral(a * a)

    out = np.zeros((h, w), dtype=np.uint8)
    area = w_local * w_local

    for y in range(h):
        for x in range(w):
            t1 = y
            l1 = x
            b1 = y + w_local
            r1 = x + w_local

            sm = area_sum(s1, t1, l1, b1, r1)
            sq = area_sum(s2, t1, l1, b1, r1)

            m = sm / area
            var = sq / area - m * m
            if var < 0:
                var = 0
            s = np.sqrt(var)

            reg1 = a[t1:b1, l1:r1]
            m_min = float(reg1.min())

            t2 = y
            l2 = x
            b2 = y + w_range
            r2 = x + w_range
            reg2 = b[t2:b2, l2:r2]

            r_range = float(reg2.max()) - float(reg2.min())

            if r_range <= 1e-9:
                t = m
            else:
                ratio = s / r_range
                a2 = k1 * (ratio ** gamma)
                a3 = k2 * (ratio ** gamma)
                t = (1 - alpha1) * m + a2 * ratio * (m - m_min) + a3 * m_min

            out[y, x] = 255 if gray_f[y, x] > t else 0

    return out


def save_img(arr, path):
    Image.fromarray(arr).save(path)


def save_strip(rgb, gray, binary, path):
    gray_rgb = np.stack([gray, gray, gray], axis=2)
    binary_rgb = np.stack([binary, binary, binary], axis=2)
    strip = np.concatenate([rgb, gray_rgb, binary_rgb], axis=1)
    Image.fromarray(strip).save(path)


def main():
    os.makedirs(input_dir, exist_ok=True)
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

        binary_3 = binarize(gray, 3, 25)
        binary_25 = binarize(gray, 25, 25)

        base = os.path.splitext(os.path.basename(path))[0]

        save_img(gray, os.path.join(output_dir, base + '_gray.bmp'))
        save_img(binary_3, os.path.join(output_dir, base + '_binary_3x3.png'))
        save_img(binary_25, os.path.join(output_dir, base + '_binary_25x25.png'))

        save_strip(img, gray, binary_3, os.path.join(output_dir, base + '_result_3x3.png'))
        save_strip(img, gray, binary_25, os.path.join(output_dir, base + '_result_25x25.png'))

    print('done')


if __name__ == '__main__':
    main()