import py_poke_parser.gen3.Sections as Sections


class Gen3Save:
    def __init__(self, filename):
        self.sections = []
        with open(filename, "rb") as f:
            f.seek(0x0ffc)
            fsindex = f.read(4)
            f.seek(0xe000-4)
            ssindex = f.read(4)
            f.seek(0, 0)
            SEEKED = False
            if ssindex > fsindex:
                SEEKED = True
                f.seek(0xe000)
            for i in range(0, 14):
                f.seek(i*4096)
                d = f.read(4096)
                if d[0x0ff4:0x0ff6] == b"\x00\x00":
                    s = Sections.TrainerSection(d)
                elif d[0x0ff4:0x0ff6] == b"\x01\x00":
                    s = Sections.TeamItemSection(d)
                elif d[0x0ff4:0x0ff6] == b"\x02\x00":
                    s = Sections.GameStateSection(d)
                elif d[0x0ff4:0x0ff6] == b"\x03\x00":
                    s = Sections.MiscDataSection(d)
                elif d[0x0ff4:0x0ff6] == b"\x04\x00":
                    s = Sections.RivalInfoSection(d)
                elif b"\x05\x00" <= d[0x0ff4:0x0ff6] <= b"\x13\x00":
                    s = Sections.PCBufferSection(d)
                else:
                    s = Sections.SaveSection(d)
                self.sections.append(s)
            if not SEEKED:
                f.seek(14*4096)
            self.ext = f.read(16384)
        self.sections.sort(key=lambda x: x.section_id.hex())

    def save(self, filename):
        with open(filename, "wb") as f:
            for sect in self.sections:
                sect.footer
                f.write(sect._data)
            for sect in self.sections:
                sect.footer
                f.write(sect._data)
            f.write(self.ext)

data = Gen3Save("Ruby_1_Test.sav")
pk = data.sections[1].team_pokemon[1]
