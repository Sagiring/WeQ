from PIL import Image

class LSB:
    def __init__(self, raw_img, new_img):
        self.raw_img = raw_img
        self.new_img = new_img

    @staticmethod
    def mod(x, y):
        return x % y

    @staticmethod
    def plus(s):
        return s.zfill(8)

    @staticmethod
    def bin2str(info):
        string = ""
        for i in range(0, len(info), 8):
            string += chr(int(info[i: i+8], 2))
        return string

    def str2bin(self, info):
        string = ""
        for i in range(len(info)):
            string += "" + self.plus(bin(ord(info[i])).replace('0b', ''))
        return string

    def hide_data(self, info):
        img = Image.open(self.raw_img)
        width, height = img.size
        count = 0
        info = self.str2bin(info)
        info_length = len(info)

        for h in range(height):
            for w in range(width):
                pixel = img.getpixel((w, h))
                r, g, b = pixel[0], pixel[1], pixel[2]
                if count == info_length:
                    break

                r -= self.mod(r, 2) + int(info[count])
                count += 1
                if count == info_length:
                    img.putpixel((w, h), (r, g, b))
                    break

                g -= self.mod(g, 2) + int(info[count])
                count += 1
                if count == info_length:
                    img.putpixel((w, h), (r, g, b))
                    break

                b -= self.mod(b, 2) + int(info[count])
                count += 1
                if count == info_length:
                    img.putpixel((w, h), (r, g, b))
                    break

                if count % 3 == 0:
                    img.putpixel((w, h), (r, g, b))

        img.save(self.new_img)

    def get_data(self, new_img, length=255):
        img = Image.open(new_img)
        width, height = img.size
        length *= 8
        count = 0
        ret = ''

        for h in range(height):
            for w in range(width):
                pixel = img.getpixel((w, h))
                r, g, b = pixel[0], pixel[1], pixel[2]

                if count % 3 == 0:
                    count += 1
                    ret += str(self.mod(int(r), 2))
                    if count == length:
                        break

                if count % 3 == 1:
                    count += 1
                    ret += str(self.mod(int(g), 2))
                    if count == length:
                        break

                if count % 3 == 2:
                    count += 1
                    ret += str(self.mod(int(b), 2))
                    if count == length:
                        break

            if count == length:
                break

        ret = self.bin2str(ret)
        return ret