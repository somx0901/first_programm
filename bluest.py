import serial

# функция проверки наличия COM-портов
def test_com():
    print("Программа проверяет доступные COM-порты")
    found = False
    for i in range(128):
        try:
            port = "COM" + str(i)
            ser = serial.Serial(port)
            ser.close()
            print("Найден последовательный порт: ", port)
            found = True
        except serial.serialutil.SerialException:
            pass
    if not found:
        print("Последовательных портов не обнаружено")


def obrabot(s):
    a = len(s)
    i = 0
    while i < (a):
        print(chr(s[i]), sep='', end='')
        i = i + 1
    print()


def mund_mode(line):
    ##    print("pfilb в мундштук моде")
    s = len(line)
    stroka = ''
    for i in range(s):
        if (line[i] > 0x26 and line[i] <= 0x3f) or (line[i] > 0x40 and line[i] < 0x5b):
            print(chr(line[i]), sep='', end='')
            stroka += chr(line[i])
        if line[i] == 0x0d:
            print()
        if line[i] == 0x20:
            print(' ', sep='', end='')
        if line[i] > 0x7f and line[i] <= 0x9f:
            print(chr(line[i] + 912), sep='', end='')
            stroka += chr(line[i] + 912)
        if line[i] > 0xa1 and line[i] <= 0xc1:
            print(chr(line[i] + 910), sep='', end='')
            stroka += chr(line[i] + 910)
        if line[i] == 0xc4:  # замена знака градуса
            print('\u00b0', sep='', end='')

            ##    print(stroka)
    return stroka


def screening_mode(line):
    print('\n' + '\t' * 3 + "Screening mode")
    s = line[7:13]
    print("Номер прибора:" + '\t' * 3, sep='', end='')
    obrabot(s)
    s = line[15:25]
    print("Дата выполнения измерения:" + '\t', sep='', end='')
    obrabot(s)
    s = line[27:32]
    print("Время теста:" + '\t' * 3, sep='', end='')
    obrabot(s)
    s = line[34:44]
    print("Дата корректирова показаний:" + '\t', sep='', end='')
    obrabot(s)
    s = line[46:56]
    print("Дата поверки:" + '\t' * 3, sep='', end='')
    obrabot(s)
    s = line[58]
    if s == 0x90:
        print("Режим:" + '\t' * 4 + "Ручной забор")
    if s == 0x80:
        print("Режим:" + '\t' * 4 + "Автоматический забор")
    s = line[61]
    if s == 0xa7:
        print("Результат:" + '\t' * 3 + "Алкоголь обнаружен")
        print()
    if s == 0xaf:
        print("Результат:" + '\t' * 3 + "Алкоголь не обнаружен")
        print()


test_com()
com_number = input("Введите номер COM порта для связи с ЮПИТЕРОМ: ")
com = "COM" + com_number
print(com)
print('A' + "\n" + 'B')
ser = serial.Serial(com, 4800, timeout=1)
global tester  # переменная для хранения суммы длины посылки
tester = 0
while True:
    line = ser.readline()
    s = len(line)
    ##  tester+=s
    ##  print(tester)
    if s > 0:
        print()
        ##    print("Длина посылки" + str(s))
        ##    print(line)
        #    print(line[0:3])

        # Скрининг режим
        if line[0] == 0x11 and line[1] == 0x12 and line[2] == 0x13 and line[63] == 0x17 and line[64] == 0x18 and line[
            65] == 0x19:
            screening_mode(line)
        # Прибор выключен
        elif line[0] == 0x1b and line[1] == 0xbb and line[2] == 0xbb:
            print('\t' * 3 + "Прибор выключили")
        elif line[0] == 0x1b and line[1] == 0xbb and line[2] == 0x1b and line[3] == 0xbb and line[4] == 0xbb:
            print('\t' * 3 + "Прибор выключили")



        # Режим с мундштуком
        elif line[0] == 0x1b and line[1] == 0x10 and line[2] == 0x01:
            tester = line[3] - len(line) + 4
            print("осталось принять символов-" + str(tester))
            mund_mode(line)
        else:
            tester -= len(line)
            art = mund_mode(line)  # по надписи подпись проверяю конец ли енто посылки без ввода данных
            art1 = 'Подпись:'
            if tester == 0:
                print('Вся первая посылка принята')
                if art1 in art:
                    print('конец найден')
                    ser.write(b'\x1b')
                    ser.write(b'\xAA')
                    # ПОТОМ СЮДА ДОБАВЬ !!!!!!!!!!!!!!! что если подписи нет то 1и 10 нужно послать





##    elif line[0]==0x1b and line[1]==0x10 and line[2]==0x1b:
##       line=line[2:]
##       mund_mode(line)

##попробуй проверять чтовся посылка первая пришла через окнчание с подписью!!!!!!!!!!!!!!!!!!
