import re


def sumCheck(devID, func, devGM, data):
    intSum = int(devID) + int(func, 16) + int(devGM, 16)
    for i in data:
        intSum += int(i, 16)
    hexSum = hex(intSum)
    return str(hexSum)[-2:]


def mode_to_tunnl(mode):
    if "E1".lower() in mode.lower():
        return "4*1"
    if "E2".lower() in mode.lower():
        return "8*1"
    if "E3".lower() in mode.lower():
        return "16*1"
    if "E4".lower() in mode.lower():
        return "32*1"


def tunnl_to_mode(tunnl):
    if tunnl == "4*1":
        return "E1"
    if tunnl == "8*1":
        return "E2"
    if tunnl == "16*1":
        return "E3"
    if tunnl == "32*1":
        return "E4"


class CodeParser:

    shut_all_tunnel = "58 54 00 81 00 00 00 00 00 00 81"
    get_board_id = "58 54 00 83 00 00 00 00 00 00 83"

    def __init__(self, mode, id):
        self.mode = mode
        self.id = id

    def encode_81(self):
        return self.shut_all_tunnel

    def decode_81(self):
        pass

    def encode_82(self, ls: list):
        tunnl = ""
        if self.mode == "4*1":
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
        elif self.mode == "8*1":
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
        elif self.mode == "16*1":
            for i in ls:
                try:
                    tunnl += str(i.index(1) + 1)
                except ValueError:
                    tunnl += '0'
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
        elif self.mode == "32*1":
            for i in ls:
                try:
                    tunnl += str(i.index(1) + 1)
                except ValueError:
                    tunnl += '0'
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

    def decode_82(self, code: str):
        res = []
        if self.mode == "4*1":
            status = code[15:30].replace(" ", "")
            for i in range(len(status)):
                res.append([0] * 4)
                if int(status[i]):
                    res[i].pop(int(status[i]) - 1)
                    res[i].insert(int(status[i]) - 1, 1)
            return res
        elif self.mode == "8*1":
            status = code[15:22].replace(" ", "")
            for i in range(len(status)):
                res.append([0] * 8)
                if int(status[i]):
                    res[i].pop(int(status[i]) - 1)
                    res[i].insert(int(status[i]) - 1, 1)
            return res
        elif self.mode == "16*1":
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
        elif self.mode == "32*1":
            status = code[15:17]
            idx = int(status)
            res.append([0] * 32)
            if idx:
                res[0].pop(idx - 1)
                res[0].insert(idx - 1, 1)
            return res

    def encode_83(self):
        return self.get_board_id

    def decode_83(self, code: str):
        return self.decode_41(code)

    def encode_84(self):
        return "58 54 {} 84 00 00 00 00 00 00 {}".format(
            "%02x" % int(self.id),
            sumCheck(self.id, "84", "00", ["00"] * 5)
        )

    def decode_84(self, code: str):
        return self.decode_41(code)

    def encode_85(self):
        print("encode_85 is executed")
        return "58 54 {} 85 {} 00 00 00 00 00 {}".format(
            "%02x" % int(self.id),
            tunnl_to_mode(self.mode),
            sumCheck(self.id, "85", tunnl_to_mode(self.mode), ["00"] * 5)
        )

    def decode_85(self, code: str):
        return self.decode_42(code)

    def encode_86(self, id):
        return "58 54 {} 86 00 {} 00 00 00 00 {}".format(
            "%02x" % int(self.id),
            hex(id),
            sumCheck(self.id, "86", "00", ["23"] + ["00"] * 4)
        )

    def decode_86(self, code: str):
        return self.decode_41(code)

    def encode_87(self, devGM):
        if "*" in devGM:
            devGM = tunnl_to_mode(devGM)
        return "58 54 {} 87 {} 00 00 00 00 00 {}".format(
            "%02x" % int(self.id),
            devGM,
            sumCheck(self.id, "87", devGM, ["00"] * 5)
        )

    def decode_87(self, code: str):
        return self.decode_41(code)

    def encode_88(self):
        return "58 54 {} 88 00 00 00 00 00 00 {}".format(
            "%02x" % int(self.id),
            sumCheck(self.id, "88", "00", ["00"] * 5)
        )

    def decode_88(self):
        pass

    def decode_41(self, code: str):
        code = code.replace(" ", "")[4:]
        id = code[:2]
        devGM = code[4:6]
        ver = "{}.{}".format(int(code[6:7], 16), int(code[7:8], 16))
        cate = code[8:10]
        return {"id": id, "devGM": devGM, "ver": ver, "cate": cate}

    def decode_42(self, code: str):
        print("decode_42 is executed")
        code = code.replace(" ", "")[4:-2]
        id = code[:2]
        devGM = code[4:6]
        res = []
        mode = mode_to_tunnl(devGM)
        if mode == "4*1":
            status = code[6:].replace(" ", "")
            for i in range(len(status)):
                res.append([0] * 4)
                if int(status[i]):
                    res[i].pop(int(status[i]) - 1)
                    res[i].insert(int(status[i]) - 1, 1)
        elif mode == "8*1":
            status = code[6:11].replace(" ", "")
            for i in range(len(status)):
                res.append([0] * 8)
                if int(status[i]):
                    res[i].pop(int(status[i]) - 1)
                    res[i].insert(int(status[i]) - 1, 1)
        elif mode == "16*1":
            status = code[6:10].replace(" ", "")
            counter = 0
            for i in range(0, len(status), 2):
                res.append([0] * 16)
                idx = int(status[i: i + 2])
                if idx:
                    res[counter].pop(idx - 1)
                    res[counter].insert(idx - 1, 1)
                counter += 1
        elif mode == "32*1":
            status = code[6:8]
            idx = int(status)
            res.append([0] * 32)
            if idx:
                res[0].pop(idx - 1)
                res[0].insert(idx - 1, 1)
        return {"id": id, "devGM": devGM, "tunnl_status": res}




































