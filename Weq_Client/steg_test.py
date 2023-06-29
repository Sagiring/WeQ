from steg import LSB
data = 'hello,world!'
lsb = LSB("raw.png", "new.png")
lsb.hide_data(data)
dec = lsb.get_data("new.png")
print(dec)