import os

class Subsection:
    def __init__(self, data) -> None:
        if len(data) != 12:
            raise ValueError(f"Expected 12 bytes, got {len(data)}!")
        self.data = data

class Growth(Subsection):
    SPECIES = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "pokemon.txt")).read().split("\n")
    def __init__(self, data) -> None:
        super().__init__(data)
        self._species = data[0x00:0x02]
        self._item = data[0x02:0x04]
        self._experience = data[0x04:0x08]
        self._pp = data[0x08:0x09]
        self._friendship = data[0x09:0x0a]
        self._unknown = data[0x0a:0x0c]
    
    @property
    def species(self):
        species_index = int.from_bytes(self._species, "little")
        name = SPECIES[species_index]
        return name

    @species.setter
    def species(self, sp: [str, int]):
        if isinstance(sp, str):
            sp = SPECIES.index(sp)
        elif isinstance(species, int):
            sp = sp
        else:
            raise ValueError("Expected type 'str' or 'int' got ", type(sp))

        self._species = sp.to_bytes(2, "little")
    
    @property
    def item(self):
        it = ITEMS[int.from_bytes(self._item, "little")]
        return it

    @item.setter
    def item(self, it: [str, int]):
        if isinstance(sp, str):
            sp = ITEMS.index(sp)
        elif isinstance(species, int):
            sp = sp
        else:
            raise ValueError("Expected type 'str' or 'int' got ", type(sp))

        self._species = sp.to_bytes(2, "little")
    
    @property
    def experience(self):
        return int.from_bytes(self._experience, "little")
    
    @property
    def pp(self):
        return self._pp
    
    @property
    def friendship(self):
        return int.from_bytes(self._friendship, "little")

    @friendship.setter
    def friendship(self, fr: int):
        if not 0 <= fr <= 255:
            raise ValueError("Expected a value between 0 and 255, got ", fr, " instead.")

        self._friendship = fr.to_bytes(1, "little")
    
    @property
    def unknown(self):
        return self._unknown

    @unknown.setter
    def unknown(self, _):
        raise ValueError("This is unknown/unused, setting it is unrecommended.")


class Attack(Subsection):
    MOVES = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "moves.txt")).read().split("\n")
    def __init__(self, data) -> None:
        super().__init__(data)
        self._move_one = self.data[0x00:0x02]
        self._move_two = self.data[0x02:0x04]
        self._move_three = self.data[0x04:0x06]
        self._move_four = self.data[0x06:0x08]
        self._pp_one = self.data[0x08:0x09]
        self._pp_two = self.data[0x09:0x0a]
        self._pp_three = self.data[0x0a:0x0b]
        self._pp_four = self.data[0x0b:0x0c]

    @property
    def move_one(self):
        mv = self.MOVES[int.from_bytes(self._move_one, "little") - 1]
        return mv

    @move_one.setter
    def move_one(self, move: [str, int]):
        if isinstance(move, str):
            move = self.MOVES.index(move) - 1
        elif isinstance(move, int):
            move = move - 1
        else:
            raise ValueError("Expected 'str' or 'int' got ", type(move))

        self._move_one = move.to_bytes(2, "little")

    @property
    def move_two(self):
        mv = self.MOVES[int.from_bytes(self._move_two, "little") - 1]
        return mv

    @move_two.setter
    def move_two(self, move: [str, int]):
        if isinstance(move, str):
            move = self.MOVES.index(move) - 1
        elif isinstance(move, int):
            move = move - 1
        else:
            raise ValueError("Expected 'str' or 'int' got ", type(move))

        self._move_two = move.to_bytes(2, "little")

    @property
    def move_three(self):
        mv = self.MOVES[int.from_bytes(self._move_three, "little") - 1]
        return mv

    @move_three.setter
    def move_three(self, move: [str, int]):
        if isinstance(move, str):
            move = self.MOVES.index(move) - 1
        elif isinstance(move, int):
            move = move - 1
        else:
            raise ValueError("Expected 'str' or 'int' got ", type(move))

        self._move_three = move.to_bytes(2, "little")

    @property
    def move_four(self):
        mv = self.MOVES[int.from_bytes(self._move_four, "little") - 1]
        return mv

    @move_four.setter
    def move_four(self, move: [str, int]):
        if isinstance(move, str):
            move = self.MOVES.index(move) - 1
        elif isinstance(move, int):
            move = move - 1
        else:
            raise ValueError("Expected 'str' or 'int' got ", type(move))

        self._move_four = move.to_bytes(2, "little")

    @property
    def pp_one(self):
        return int.from_bytes(self._pp_one, "little")

    @property
    def pp_two(self):
        return int.from_bytes(self._pp_two, "little")

    @property
    def pp_three(self):
        return int.from_bytes(self._pp_three, "little")

    @property
    def pp_four(self):
        return int.from_bytes(self._pp_four, "little")

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
    
    SUBORDERS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "suborders.txt")).read().split("\n")
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

