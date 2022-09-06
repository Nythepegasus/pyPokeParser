
class Subsection:
    def __init__(self, data) -> None:
        if len(data) != 12:
            raise ValueError(f"Expected 12 bytes, got {len(data)}!")
        self.data = data

class Growth(Subsection):
    def __init__(self, data) -> None:
        super().__init__(data)
    
    @property
    def species(self):
        return self.data[0x00:0x02]
    
    @property
    def item(self):
        return self.data[0x02:0x04]
    
    @property
    def experience(self):
        return self.data[0x04:0x08]
    
    @property
    def pp_bonus(self):
        return self.data[0x08:0x09]
    
    @property
    def friendship(self):
        return self.data[0x09:0x10]
    
    @property
    def unknown(self):
        return self.data[0x10:0x12]


class Attack(Subsection):
    def __init__(self, data) -> None:
        super().__init__(data)

    @property
    def move_one(self):
        return self.data[0x00:0x02]

    @property
    def move_two(self):
        return self.data[0x02:0x04]

    @property
    def move_three(self):
        return self.data[0x04:0x06]

    @property
    def move_four(self):
        return self.data[0x06:0x08]

    @property
    def pp_one(self):
        return self.data[0x08:0x09]

    @property
    def pp_two(self):
        return self.data[0x09:0x10]

    @property
    def pp_three(self):
        return self.data[0x10:0x11]

    @property
    def pp_four(self):
        return self.data[0x11:0x12]

class EVCondition(Subsection):
    def __init__(self, data) -> None:
        super().__init__(data)

    @property
    def hp(self):
        return self.data[0x00:0x01]

    @property
    def attack(self):
        return self.data[0x01:0x02]

    @property
    def defense(self):
        return self.data[0x02:0x03]

    @property
    def speed(self):
        return self.data[0x03:0x04]

    @property
    def sp_attack(self):
        return self.data[0x04:0x05]

    @property
    def sp_defense(self):
        return self.data[0x05:0x06]

    @property
    def coolness(self):
        return self.data[0x06:0x07]

    @property
    def beauty(self):
        return self.data[0x07:0x08]

    @property
    def cuteness(self):
        return self.data[0x08:0x09]

    @property
    def smartness(self):
        return self.data[0x09:0x10]

    @property
    def toughness(self):
        return self.data[0x10:0x11]

    @property
    def feel(self):
        return self.data[0x11:0x12]

class Misc(Subsection):
    def __init__(self, data) -> None:
        super().__init__(data)
    
    @property
    def pokerus(self):
        return self.data[0x00:0x01]

    @property
    def met_location(self):
        return self.data[0x01:0x02]

    @property
    def origins(self):
        return self.data[0x02:0x04]

    @property
    def ivs_egg_ability(self):
        # TODO: Split data
        return self.data[0x04:0x08]

    @property
    def ribbons_obedience(self):
        return self.data[0x08:0x12]


class Gen3Pokemon:
    SUBORDERS = open("suborders.txt").read().split("\n")
    def __init__(self, data):
        self.data = bytearray(data)
        self._encrypted_data = self.encrypted_data
        if len(self.data) != 100:
            raise ValueError(f"Expected 100 bytes, got {len(self.data)}")

    @classmethod
    def from_data(cls, data):
        return cls(data)
    
    # TODO: Create classmethod to create custom Pokemon
    
    @staticmethod
    def decode_string(s):
        chars = "0123456789!?.-         ,  ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        return "".join([chars[int(i)-161] if 0 < (int(i) - 161) < len(chars) else " " for i in s])

    @staticmethod
    def encode_string(s):
        chars = "0123456789!?.-         ,  ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        ret = bytearray()
        for i in s:
            try:
                ret += int(chars.index(i) + 161).to_bytes(1, "little")
            except ValueError:
                ret += int(0).to_bytes(1, "little")
        if len(ret) != 10:
            ret[len(ret):10] = b"\xff" * (10 - len(ret))
        return ret

    @staticmethod
    def correct_overflow(value, bits, signed):
        """Allows us to simulate C-like overflows in Python"""
        base = 1 << bits
        value %= base
        return value - base if signed and value.bit_length() == bits else value

    @property
    def pvalue(self):
        return int.from_bytes(self.data[0x00:0x04], "little")

    @property
    def otid(self):
        return int.from_bytes(self.data[0x04:0x08], "little")

    @property
    def nickname(self):
        return self.decode_string(self.data[0x08:0x12]).strip()
    
    @nickname.setter
    def nickname(self, s):
        self.data[0x08:0x12] = self.encode_string(s)

    @property
    def language(self):
        lang = self.data[0x12:0x13]
        if lang == b"\x01":
            return "Japanese"
        elif lang == b"\x02":
            return "English"
        elif lang == b"\x03":
            return "French"
        elif lang == b"\x04":
            return "Italian"
        elif lang == b"\x05":
            return "German"
        elif lang == b"\x06":
            return "Korean"
        elif lang == b"\x07":
            return "Spanish"
        else:
            return self.data[0x12:0x13]

    @property
    def egg_name(self):
        return self.data[0x13:0x14]
    
    @property
    def ot_name(self):
        return self.decode_string(self.data[0x14:0x1b]).strip()
    
    @property
    def marking(self):
        return self.data[0x1b:0x1c]
    
    @property
    def encryption_key(self):
        return self.otid ^ self.pvalue
    
    @property
    def encrypted_data(self):
        return self.data[0x20:0x50]
    
    @property
    def decrypted_data(self):
        ret = bytearray()
        for i in range(0, 4):
            data = self.encrypted_data[i*12:(i*12)+12]
            for i in range(0, 3):
                ret += (int.from_bytes(data[i*4:(i*4)+4], "little") ^ self.encryption_key).to_bytes(4, "little")
        return ret
    
    @property
    def checksum(self):
        Chk = 0
        for i in range(0, 48, 2):
            Chk += int.from_bytes(self.decrypted_data[i:i+2], "little")
        Chk = self.correct_overflow(Chk, 16, False)
        return bytearray(Chk.to_bytes(2, "little"))
    
    @property
    def suborder(self):
        return list(self.SUBORDERS[self.pvalue % 24])
    
    def encrypt(self):
        ret = bytearray()
        for i in range(0, 4):
            data = self.decrypted_data[i*12:(i*12)+12]
            for i in range(0, 3):
                ret += (self.encryption_key ^ int.from_bytes(data[i*4:(i*4)+4], "little")).to_bytes(4, "little")
        self._encrypted_data = ret

