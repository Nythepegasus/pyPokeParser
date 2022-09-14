from .Pokemon import Gen3Pokemon

SECTION_NAMES = {
    "0000": "Trainer Info",
    "0100": "Team / Items",
    "0200": "Game State",
    "0300": "Misc Data",
    "0400": "Rival Info",
    "0500": "PC Buffer A",
    "0600": "PC Buffer B",
    "0700": "PC Buffer C",
    "0800": "PC Buffer D",
    "0900": "PC Buffer E",
    "0a00": "PC Buffer F",
    "0b00": "PC Buffer G",
    "0c00": "PC Buffer H",
    "0d00": "PC Buffer I"
}

SECTION_OFFSETS = {
    "0000": 0x0890,
    "0100": 0x0f80,
    "0200": 0x0f80,
    "0300": 0x0f80,
    "0400": 0x0c40,
    "0500": 0x0f80,
    "0600": 0x0f80,
    "0700": 0x0f80,
    "0800": 0x0f80,
    "0900": 0x0f80,
    "0a00": 0x0f80,
    "0b00": 0x0f80,
    "0c00": 0x0f80,
    "0d00": 0x07d0
}


class SaveSection:
    SIGNATURE = b'% \x01\x08'
    def __init__(self, data):
        self._data = bytearray(data)
        self._footer = self._data[0x0ff4:]
        self.section_id = self._data[0x0ff4:0x0ff6]
        try:
            self.title = SECTION_NAMES[self.section_id.hex()]
        except KeyError:
            print(f"{self.id.hex()} returned KeyError")
        self.signature = self._data[0x0ff8:0x0ffc]
        if self.signature != self.SIGNATURE:
            raise TypeError("Signature Mismatch!")
        self.save_index = self._data[0x0ffc:0x1000]
    
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
        if len(ret) != 7:
            ret[len(ret):7] = b"\xff" * (7 - len(ret))
        return ret

    @staticmethod
    def correct_overflow(value, bits, signed):
        """Allows us to simulate C-like overflows in Python"""
        base = 1 << bits
        value %= base
        return value - base if signed and value.bit_length() == bits else value

    @property
    def checksum(self):
        Chk = 0
        for i in range(0, SECTION_OFFSETS[self.section_id.hex()], 4):
            Chk += int.from_bytes(self._data[i:i+4], "little")
        Chk = self.correct_overflow(Chk, 32, False)
        Chk = ((Chk >> 16) + Chk) & 0xffff
        return Chk.to_bytes(2, "little")

    @property
    def footer(self):
        ftr = self.section_id + self.checksum + self.SIGNATURE + self.save_index
        self._data[0x0ff4:0x1000] = ftr
        return ftr

    @property
    def data(self):
        return self._data[:0x0ff4] + self.footer


class TrainerSection(SaveSection):
    def __init__(self, data):
        super().__init__(data)

    def __repr__(self):
        return f"TrainerSection('{self.name}', '{self.gender}')"

    @property
    def name(self):
        return self.decode_string(self._data[0x00:0x07]).strip()

    @name.setter
    def name(self, n):
        self._data[0x00:0x07] = self.encode_string(n)

    @property
    def gender(self):
        if int.from_bytes(self._data[0x08:0x09], "little") == 0:
            return "Male"
        elif int.from_bytes(self._data[0x08:0x09], "little") == 1:
            return "Female"
        else:
            raise ValueError(f"Unknown gender byte '{self._data[8:9]}'")

    @gender.setter
    def gender(self, g):
        if g in ["M", "m", 0]:
            self._data[0x08:0x09] = b"\x00"
        elif g in ["G", "g", 1]:
            self._data[0x08:0x09] = b"\x01"
        else:
            raise ValueError(f"Unknown value '{g}' when parsing gender.")

    @property
    def unused(self):
        return self._data[0x09:0x0a]

    @unused.setter
    def unused(self, _):
        raise ValueError("This is an unknown/unused value, it should not be edited.")

    @property
    def trainer_id(self):
        return (int.from_bytes(self._data[0x0a:0x0c], "little"), int.from_bytes(self._data[0x0c:0x0e], "little"))

    @trainer_id.setter
    def trainer_id(self, ids):
        if not isinstance(ids, tuple) or not all(isinstance(i, int) for i in ids) or len(ids) != 2:
            raise ValueError("Trainer ID setter only takes a tuple of 2 integers.")
        self._data[0x0a:0x0c] = ids[0].to_bytes(2, "little")
        self._data[0x0c:0x0e] = ids[1].to_bytes(2, "little")
        
    
    @property
    def time_played(self):
        hours = int.from_bytes(self._data[0x0e:0x10], "little")
        minutes = int.from_bytes(self._data[0x10:0x11], "little")
        seconds = int.from_bytes(self._data[0x11:0x12], "little")
        frames = int.from_bytes(self._data[0x12:0x13], "little")
        return (hours, minutes, seconds, frames)

    @time_played.setter
    def time_played(self, time):
        if not isinstance(time, tuple) or not all(isinstance(i, int) for i in time) or len(time) != 4:
            raise ValueError("Time value setter only takes a tuple of 4 integers.")
        self._data[0x0e:0x10] = time[0].to_bytes(2, "little")
        self._data[0x10:0x11] = time[1].to_bytes(1, "little")
        self._data[0x11:0x12] = time[2].to_bytes(1, "little")
        self._data[0x12:0x13] = time[3].to_bytes(1, "little")

    @property
    def options(self):
        return self._data[0x13:0x16]

    @property
    def button_mode(self):
        return self._data[0x13:0x14]

    @property
    def tspeed_frame(self):
        return self._data[0x14:0x15]

    @property
    def sound_battles(self):
        return self._data[0x15:0x16]


class TeamItemSection(SaveSection):
    def __init__(self, data):
        super().__init__(data)
        self._team_pokemon = self.data[0x238:0x238+600]
        self._pokemon = []
    
    @property
    def team_size(self):
        return int.from_bytes(self._data[0x0234:0x0238], "little")
    
    @team_size.setter
    def team_size(self, s):
        if not 1 <= s <= 6:
            raise ValueError("Team size must be between 1 and 6!")
        self._data[0x0234:0x0238] = int(s).to_bytes(4, "little")

    @property
    def team_pokemon(self):
        if len(self._pokemon) == 0:
            for i in range(0, self.team_size):
                self._pokemon.append(Gen3Pokemon(self.data[(0x0238+(i*100)):(0x0238+(i*100))+(100)]))
        
        return self._pokemon

    @property
    def money(self):
        pass

    @property
    def coins(self):
        pass

    @property
    def pc_items(self):
        pass

    @property
    def player_items(self):
        pass

    @property
    def key_items(self):
        pass

    @property
    def ball_items(self):
        pass

    @property
    def tm_case(self):
        pass

    @property
    def berry_items(self):
        pass


class GameStateSection(SaveSection):
    def __init__(self, data):
        super().__init__(data)


class MiscDataSection(SaveSection):
    def __init__(self, data):
        super().__init__(data)


class RivalInfoSection(SaveSection):
    def __init__(self, data):
        super().__init__(data)


class PCBufferSection(SaveSection):
    def __init__(self, data):
        super().__init__(data)

