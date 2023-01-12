from statistics import mean
import matplotlib.pyplot as plt
import numpy as np


stream = open(".\\BenjaminPodlogar_NatezniTest_FTPO_CSV.csv", "r")

stream_without_header = stream.readlines()[3:]

s1 = []
s2 = []
s3 = []
s4 = []
s5 = []

thick = 2.0300
width = 5.0000
gauge_len = 50.0000

Sizh = [[thick, width, gauge_len]] * 5
Sntrd = []
Sraz = []

def castToFloat(value):
    if value == "":
        return 0

    return float(value)

def parse_line(line):
    time = line[0]
    force = line[1]
    stroke = line[2]
    ext = line[3]

    if time == "" and force == "" and stroke == "" and ext == "":
        return None

    return [castToFloat(time), castToFloat(force), castToFloat(stroke), castToFloat(ext)]

def calculate_surface(width, thickness):
    return width * thickness

def calculate_tensile_strength(force, a):
    return force/a

def prepare_Sntrd(beaker_data, entry_data):
    list = []
    a = calculate_surface(beaker_data[1], beaker_data[0])

    for [time, force, stroke, ext] in entry_data:
        tensile_strength = calculate_tensile_strength(force, a)
        list.append(tensile_strength)

    return list


def prepare_Sraz(entry_data):
    list = []

    for [time, force, stroke, ext] in entry_data:
        raztezek = (((stroke + gauge_len)/gauge_len) - 1) * 100
        list.append(raztezek)

    return list

def pripravi_seznam_povprecji(seznam):
    seznam_povprecji = []
    stevec = 0

    velikost_najmanjsega = 100000000
    for epruveta in seznam:
        if len(epruveta) <= velikost_najmanjsega:
            velikost_najmanjsega = len(epruveta)

    while stevec < velikost_najmanjsega:
        povprecje = mean([seznam[0][stevec], seznam[1][stevec], seznam[2][stevec], seznam[3][stevec], seznam[4][stevec]])
        seznam_povprecji.append(povprecje)
        stevec += 1

    return seznam_povprecji

for line in stream_without_header:
    line = line.replace("\n", "")
    line = line.replace(",", ".")
    exploded_data = line.split(";")

    line_s1 = exploded_data[0:4]
    line_s2 = exploded_data[4:8]
    line_s3 = exploded_data[8:12]
    line_s4 = exploded_data[12:16]
    line_s5 = exploded_data[16:20]

    parsed_line1 = parse_line(line_s1)
    parsed_line2 = parse_line(line_s2)
    parsed_line3 = parse_line(line_s3)
    parsed_line4 = parse_line(line_s4)
    parsed_line5 = parse_line(line_s5)

    if parsed_line1 is not None:
        s1.append(parse_line(line_s1))

    if parsed_line2 is not None:
        s2.append(parse_line(line_s2))

    if parsed_line3 is not None:
        s3.append(parse_line(line_s3))

    if parsed_line4 is not None:
        s4.append(parse_line(line_s4))

    if parsed_line5 is not None:
        s5.append(parse_line(line_s5))


parsed_data = [s1, s2, s3, s4, s5]

for index in range(0, 5):
    # 2.3
    list = prepare_Sntrd(Sizh[index], parsed_data[index])
    Sntrd.append(list)

    # 2.4
    list2 = prepare_Sraz(parsed_data[index])
    Sraz.append(list)

# 2.5
Sntrd_povp = pripravi_seznam_povprecji(Sntrd)

# 2.6
Sraz_povp = pripravi_seznam_povprecji(Sraz)

plt.plot(Sraz_povp, Sntrd_povp, label = "Average Tensile Test", c = "#C71585")
plt.title("Relationship between Stress and Strain (Tensile Test) - Average")
plt.xlabel("Strain (%) - Average")
plt.ylabel("Stress (MPa) - Average")
plt.legend()
plt.grid(linestyle = "dotted")
plt.show()