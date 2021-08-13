import re


def sumCheck(devID, func, devGM, data):
    intSum = int(devID) + int(func, 16) + int(devGM, 16)
    for i in data:
        intSum += int(i, 16)
    hexSum = hex(intSum)
    return str(hexSum)[-2:]


class CodeParser:

    shut_all_tunnel = "58 54 00 81 00 00 00 00 00 00 81"
    pw_shut_all_tunnel = "58 54 00 81 00 00 00 00 00 81"
    get_board_id = "58 54 00 83 00 00 00 00 00 00 83"
    pw_get_board_id = "58 54 00 83 00 00 00 00 00 83"

    def __init__(self, mode, id):
        self.mode = mode
        self.id = id

    def encode_81(self):
        return self.shut_all_tunnel

    def pw_encode_81(self):
        return self.pw_shut_all_tunnel

    def decode_81(self):
        pass

    def pw_decode_81(self):
        pass

    def encode_82(self, ls: list):
        tunnl = ""
        if self.mode.lower() == "e1":
            for i in ls:
                try:
                    tunnl += str(i.index(1) + 1)
                except ValueError:
                    tunnl += '0'
                except Exception as e:
                    print(e)
            tunnl += '0' * (10 - len(tunnl))
            tunnl_list = re.findall(".{2}", tunnl)
            check_sum = sumCheck(self.id, "82", "E1", tunnl_list)
            tunnl = " ".join(tunnl_list)
            return "58 54 {} 82 E1 {} {}".format(
                "%02x" % int(self.id),
                tunnl,
                check_sum
            )
        elif self.mode.lower() == "e2":
            for i in ls:
                try:
                    tunnl += str(i.index(1) + 1)
                except ValueError:
                    tunnl += '0'
                except Exception as e:
                    print(e)
            tunnl += '0' * (10 - len(tunnl))
            tunnl_list = re.findall(".{2}", tunnl)
            check_sum = sumCheck(self.id, "82", "E2", tunnl_list)
            tunnl = " ".join(tunnl_list)
            return "58 54 {} 82 E2 {} {}".format(
                "%02x" % int(self.id),
                tunnl,
                check_sum
            )
        elif self.mode.lower() == "e3":
            for i in ls:
                try:
                    tunnl += str((i.index(1) + 1) // 10)
                    tunnl += str((i.index(1) + 1) % 10)
                except ValueError:
                    tunnl += '00'
                except Exception as e:
                    print(e)
            tunnl += '0' * (10 - len(tunnl))
            tunnl_list = re.findall(".{2}", tunnl)
            check_sum = sumCheck(self.id, "82", "E3", tunnl_list)
            tunnl = " ".join(tunnl_list)
            return "58 54 {} 82 E3 {} {}".format(
                "%02x" % int(self.id),
                tunnl,
                check_sum
            )
        elif self.mode.lower() == "e4":
            for i in ls:
                try:
                    tunnl += str((i.index(1) + 1) // 10)
                    tunnl += str((i.index(1) + 1) % 10)
                except ValueError:
                    tunnl += '00'
                except Exception as e:
                    print(e)
            tunnl += '0' * (10 - len(tunnl))
            tunnl_list = re.findall(".{2}", tunnl)
            check_sum = sumCheck(self.id, "82", "E4", tunnl_list)
            tunnl = " ".join(tunnl_list)
            return "58 54 {} 82 E4 {} {}".format(
                "%02x" % int(self.id),
                tunnl,
                check_sum
            )

    def pw_encode_82(self, ls: list):
        tunnl = ''
        if self.mode.lower() == 'e1':
            for i in ls:
                try:
                    tunnl += str(i.index(1) + 1)
                except ValueError:
                    tunnl += '0'
                except Exception as e:
                    print(e)
            tunnl += '0' * (8 - len(tunnl))
            tunnl_list = re.findall(".{2}", tunnl)
            check_sum = sumCheck(self.id, "82", "E1", tunnl_list)
            tunnl = " ".join(tunnl_list)
            return "58 54 {} 82 E1 {} {}".format(
                "%02x" % int(self.id),
                tunnl,
                check_sum
            )
        elif self.mode.lower() == 'e2':
            for i in ls:
                try:
                    tunnl += str(i.index(1) + 1)
                except ValueError:
                    tunnl += '0'
                except Exception as e:
                    print(e)
            tunnl += '0' * (8 - len(tunnl))
            tunnl_list = re.findall(".{2}", tunnl)
            check_sum = sumCheck(self.id, "82", "E2", tunnl_list)
            tunnl = " ".join(tunnl_list)
            return "58 54 {} 82 E2 {} {}".format(
                "%02x" % int(self.id),
                tunnl,
                check_sum
            )
        elif self.mode.lower() == 'e3':
            for i in ls:
                try:
                    tunnl += str((i.index(1) + 1) // 10)
                    tunnl += str((i.index(1) + 1) % 10)
                except ValueError:
                    tunnl += '00'
                except Exception as e:
                    print(e)
            tunnl += '0' * (8 - len(tunnl))
            tunnl_list = re.findall(".{2}", tunnl)
            check_sum = sumCheck(self.id, "82", "E3", tunnl_list)
            tunnl = " ".join(tunnl_list)
            return "58 54 {} 82 E3 {} {}".format(
                "%02x" % int(self.id),
                tunnl,
                check_sum
            )

    '''
    def decode_82(self, code: str):
        res = []
        if self.cate.lower() == 'f2':
            if self.mode.lower() == "e1":
                status = code[15:30].replace(" ", "")
                for i in range(len(status)):
                    res.append([0] * 4)
                    if int(status[i]):
                        res[i].pop(int(status[i]) - 1)
                        res[i].insert(int(status[i]) - 1, 1)
                return res
            elif self.mode.lower() == "e2":
                status = code[15:22].replace(" ", "")
                for i in range(len(status)):
                    res.append([0] * 8)
                    if int(status[i]):
                        res[i].pop(int(status[i]) - 1)
                        res[i].insert(int(status[i]) - 1, 1)
                return res
            elif self.mode.lower() == "e3":
                status = code[15:21].replace(" ", "")
                counter = 0
                for i in range(0, len(status), 2):
                    res.append([0] * 16)
                    idx = int(status[i: i+2])
                    if idx:
                        res[counter].pop(idx - 1)
                        res[counter].insert(idx - 1, 1)
                    counter += 1
                return res
            elif self.mode.lower() == "e4":
                status = code[15:17]
                idx = int(status)
                res.append([0] * 32)
                if idx:
                    res[0].pop(idx - 1)
                    res[0].insert(idx - 1, 1)
                return res
    '''

    def encode_83(self):
        return self.get_board_id

    def pw_encode_83(self):
        return self.pw_get_board_id

    def decode_83(self, code: str):
        return self.decode_41(code)

    def pw_decode_83(self, code:str):
        return self.decode_41(code)

    def encode_84(self, *bid):
        try:
            return "58 54 {} 84 00 00 00 00 00 00 {}".format(
                "%02x" % bid[0],
                sumCheck(str(bid[0]), "84", "00", ["00"] * 5)
            )
        except IndexError:
            return "58 54 {} 84 00 00 00 00 00 00 {}".format(
                "%02x" % int(self.id),
                sumCheck(self.id, "84", "00", ["00"] * 5)
            )

    def pw_encode_84(self, *bid):
        try:
            return "58 54 {} 84 00 00 00 00 00 {}".format(
                "%02x" % bid[0],
                sumCheck(str(bid[0]), "84", "00", ["00"] * 4)
            )
        except IndexError:
            return "58 54 {} 84 00 00 00 00 00 {}".format(
                "%02x" % int(self.id),
                sumCheck(self.id, "84", "00", ["00"] * 4)
            )

    def decode_84(self, code: str):
        return self.decode_41(code)

    def pw_decode_84(self, code: str):
        return self.decode_41(code)

    def encode_85(self):
        return "58 54 {} 85 {} 00 00 00 00 00 {}".format(
            "%02x" % int(self.id),
            self.mode,
            sumCheck(self.id, "85", self.mode, ["00"] * 5)
        )

    def pw_encode_85(self):
        return "58 54 {} 85 {} 00 00 00 00 {}".format(
            "%02x" % int(self.id),
            self.mode,
            sumCheck(self.id, "85", self.mode, ["00"] * 4)
        )

    def decode_85(self, code: str):
        return self.decode_42(code)

    def pw_decode_85(self, code: str):
        return self.pw_decode_42(code)

    def encode_86(self, id):
        return "58 54 {} 86 00 {} 00 00 00 00 {}".format(
            "%02x" % int(self.id),
            "%02x" % int(id),
            sumCheck(self.id, "86", "00", [hex(int(id))] + ["00"] * 4)
        )

    def pw_encode_86(self, id):
        return "58 54 {} 86 00 {} 00 00 00 {}".format(
            "%02x" % int(self.id),
            "%02x" % int(id),
            sumCheck(self.id, "86", "00", [hex(int(id))] + ["00"] * 3)
        )

    def decode_86(self, code: str):
        return self.decode_41(code)

    def pw_decode_86(self, code: str):
        return self.decode_41(code)

    def encode_87(self, devGM):
        return "58 54 {} 87 {} 00 00 00 00 00 {}".format(
            "%02x" % int(self.id),
            devGM,
            sumCheck(self.id, "87", devGM, ["00"] * 5)
        )

    def pw_encode_87(self, devGM):
        return "58 54 {} 87 {} 00 00 00 00 {}".format(
            "%02x" % int(self.id),
            devGM,
            sumCheck(self.id, "87", devGM, ["00"] * 4)
        )

    def decode_87(self, code: str):
        return self.decode_41(code)

    def pw_decode_87(self, code: str):
        return self.decode_41(code)

    def encode_88(self):
        return "58 54 {} 88 00 00 00 00 00 00 {}".format(
            "%02x" % int(self.id),
            sumCheck(self.id, "88", "00", ["00"] * 5)
        )

    def pw_encode_88(self):
        return "58 54 {} 88 00 00 00 00 00 {}".format(
            "%02x" % int(self.id),
            sumCheck(self.id, "88", "00", ["00"] * 4)
        )

    def decode_88(self):
        pass

    def pw_decode_88(self):
        pass

    def decode_41(self, code):
        code = code.replace(" ", "")[4:]
        id = str(int(code[:2], 16))
        devGM = code[4:6]
        ver = "{}.{}".format(int(code[6:7], 16), int(code[7:8], 16))
        cate = code[8:10]
        return {"id": id, "devGM": devGM, "ver": ver, "cate": cate}

    def decode_42(self, code: str):
        code = code.replace(" ", "")[4:-2]
        id = code[:2]
        devGM = code[4:6]
        res = []
        if devGM == "e1":
            status = code[6:].replace(" ", "")
            for i in range(len(status)):
                res.append([0 for _ in range(4)])
                if int(status[i]):
                    res[i].pop(int(status[i]) - 1)
                    res[i].insert(int(status[i]) - 1, 1)
        elif devGM == "e2":
            status = code[6:11].replace(" ", "")
            for i in range(len(status)):
                res.append([0 for _ in range(8)])
                if int(status[i]):
                    res[i].pop(int(status[i]) - 1)
                    res[i].insert(int(status[i]) - 1, 1)
        elif devGM == "e3":
            status = code[6:10].replace(" ", "")
            counter = 0
            for i in range(0, len(status), 2):
                res.append([0 for _ in range(16)])
                idx = int(status[i: i + 2])
                if idx:
                    res[counter].pop(idx - 1)
                    res[counter].insert(idx - 1, 1)
                counter += 1
        elif devGM == "e4":
            status = code[6:8]
            idx = int(status)
            res.append([0 for _ in range(32)])
            if idx:
                res[0][idx - 1] = 1
        return {"id": id, "devGM": devGM, "tunnl_status": res}

    def pw_decode_42(self, code: str):
        code = code.replace(" ", "")[4:-2]
        id = code[:2]
        devGM = code[4:6]
        res = []
        if devGM == "e1":
            status = code[6:].replace(" ", "")
            for i in range(len(status)):
                res.append([0 for _ in range(4)])
                if int(status[i]):
                    res[i].pop(int(status[i]) - 1)
                    res[i].insert(int(status[i]) - 1, 1)
        elif devGM == "e2":
            status = code[6:8].replace(" ", "")
            for i in range(len(status)):
                res.append([0 for _ in range(8)])
                if int(status[i]):
                    res[i].pop(int(status[i]) - 1)
                    res[i].insert(int(status[i]) - 1, 1)
        elif devGM == "e3":
            status = code[6:8].replace(" ", "")
            counter = 0
            for i in range(0, len(status), 2):
                res.append([0 for _ in range(16)])
                idx = int(status[i: i + 2])
                if idx:
                    res[counter].pop(idx - 1)
                    res[counter].insert(idx - 1, 1)
                counter += 1
        return {"id": id, "devGM": devGM, "tunnl_status": res}






























