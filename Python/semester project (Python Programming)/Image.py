from PIL import Image
import numpy as np
import sys
import os.path
import itertools


def read_args(arguments, parameters):
    param_needs_arg = False
    for arg in sys.argv[1:]:
        if arg.startswith('--'):
            if param_needs_arg:  # expecting a number
                print('I THINK THERE SHOULD BE A NUMBER BUT THERE IS A STRING')
                raise ValueError
            if arg == '--lighten' or arg == '--darken':
                param_needs_arg = True
            parameters.append(arg)
        else:
            if param_needs_arg:
                if arg.isdigit():
                    param_needs_arg = False
                else:
                    print('I THINK THERE SHOULD BE A NUMBER BUT THERE IS A STRING')
                    raise ValueError
            arguments.append(arg)


def rotate(img):
    return np.rot90(img, 3)


def mirror(img):
    return np.fliplr(img)


def negative(img):
    return 255 - img


def gray(img):
    if img.ndim == 2:  # it's already gray
        return img
    return np.average(img.astype(np.float), weights=[0.299, 0.587, 0.114], axis=2).astype(np.uint8)


def lighten(img, percent):
    percent = (int(percent) + 100) / 100
    light = img.copy()
    height = range(light.shape[0])
    width = range(light.shape[1])

    for i in itertools.product(width, height):
        if img.ndim == 3:
            r = light[i[1]][i[0]][0]
            g = light[i[1]][i[0]][1]
            b = light[i[1]][i[0]][2]
            light[i[1]][i[0]] = [(r * percent if r * percent < 255 else 255),
                                 (g * percent if g * percent < 255 else 255),
                                 (b * percent if b * percent < 255 else 255)]
        else:
            light[i[1]][i[0]] = light[i[1]][i[0]] * percent if light[i[1]][i[0]] * percent <= 255 else 255
    return light


def darken(img, percent):
    percent = int(percent) / 100
    dark = img.copy()
    height = range(dark.shape[0])
    width = range(dark.shape[1])
    for i in itertools.product(width, height):
        dark[i[1]][i[0]] = dark[i[1]][i[0]] * percent
    return dark


def convolve(channel, kernel):
    padded = np.zeros((channel.shape[0] + 2, channel.shape[1] + 2))
    padded[1:-1, 1:-1] = channel
    output = np.zeros_like(channel)
    w = range(channel.shape[1])
    h = range(channel.shape[0])
    for i in itertools.product(w, h):
        s = (kernel * padded[i[1]:i[1] + 3, i[0]:i[0] + 3]).sum()
        if s > 255:
            s = 255
        if s < 0:
            s = 0
        output[i[1], i[0]] = s
    return output


def sharpening(img):
    sharpening_kernel = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0],
    ])
    if img.ndim == 3:
        result = np.copy(img)
        for i in range(img.shape[2]):
            result[:, :, i] = convolve(img[:, :, i], sharpening_kernel)
        return result
    else:
        return convolve(img, sharpening_kernel)


def main():
    arguments = []
    parameters = []
    read_args(arguments, parameters)

    if len(arguments) >= 2:
        input = arguments[-2].lower()
        if not os.path.isfile(input):
            print(input, " IS A WRONG NAME FOR INPUT FILE")
            raise FileNotFoundError
        output = arguments[-1].lower()
        if not output.endswith('png') and not output.endswith('jpg') and not output.endswith('jpeg'):
            print(output, " HAS A WRONG FILE EXTENSION")
            raise TypeError
    else:
        print("SOMETHING IS WRONG. TOO LITTLE PARAMETERS")
        raise BufferError

    img = np.array(Image.open(input))
    if img.ndim == 2:
        mode = 'L'
    else:
        mode = 'RGB'

    for i in parameters:
        if i == '--rotate':
            img = rotate(img)
        elif i == '--mirror':
            img = mirror(img)
        elif i == '--inverse':
            img = negative(img)
        elif i == '--bw':
            mode = 'L'
            img = gray(img)
        elif i == '--lighten':
            if len(arguments):
                percent = arguments[0]
                arguments.pop(0)
                if not percent.isdigit() or int(percent) < 0 or int(percent) > 100:
                    print('ARGUMENT IS WRONG')
                    raise TypeError
                img = lighten(img, percent)
        elif i == '--darken':
            if len(arguments):
                percent = arguments[0]
                arguments.pop(0)
                if not percent.isdigit() or int(percent) < 0 or int(percent) > 100:
                    print('ARGUMENT IS WRONG')
                    raise TypeError
                img = darken(img, percent)
        elif i == '--sharpen':
            img = sharpening(img)

    Image.fromarray(img, mode=mode).save(output)


if __name__ == '__main__':
    main()
