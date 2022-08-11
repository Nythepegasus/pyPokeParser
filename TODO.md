# Section Format
* `0x0000 - 0x0f80`: Data
* `0x0ff4 - 0x0ff6`: Section ID
* `0x0ff6 - 0x0ff8`: Checksum
* `0x0ff8 - 0x0ffc`: Signature
* `0x0ffc - 0x1000`: Save Index

## Section ID
* `0x00`: Trainer Info
* `0x01`: Team / Items
* `0x02`: Game State
* `0x03`: Misc Data
* `0x04`: Rival Info
* `0x05`: PC Buffer A
* `0x06`: PC Buffer B
* `0x07`: PC Buffer C
* `0x08`: PC Buffer D
* `0x09`: PC Buffer E
* `0x0a`: PC Buffer F
* `0x0b`: PC Buffer G
* `0x0c`: PC Buffer H
* `0x0d`: PC Buffer I

## Trainer Info
* `0x0000 - 0x0007`: Player 

	Player name, 1 - 7 characters proprietary encoding

* `0x0008 - 0x0009`: Player gender

	Player gender, `\x00` is male, `\x01` is female.

* `0x0009 - 0x000a`: Unused/Unknown

	Unknown value, is usually `\x00`

* `0x000a - 0x000e`: Trainer ID

	

* `0x000e - 0x0013`: Time Played
* `0x0013 - 0x0016`: Options
* `0x00ac - 0x00b0`: Game Code / Security Key (Emerald)
* `0x0af8 - 0x0afc`: Security Key (FR/LG)

## Team / Items
```
* Team size
    * R/S/E: 0x0234 - 0x0238 (4 bytes)
    * FR/LG: 0x0034 - 0x0038 (4 bytes)
Number of Pokemon in the team currently.
```

```
* Team Pokemon list
    * R/S/E: 0x0238 - 0x0490 (600 bytes)
    * FR/LG: 0x0038 - 0x0290 (600 bytes)
Data of each Pokemon, each Pokemon being 100 bytes long. Extra Pokemon are '\xff'
```

```
* Money
    * R/S/E: 0x0490 - 0x0494 (4 bytes)
    * FR/LG: 0x0290 - 0x0294 (4 bytes)
R/S money is plain, FR/LG/E is XOR'd with the security key
```

```
* Coins
    * R/S/E: 0x0494 - 0x0496 (2 bytes)
    * FR/LG: 0x0294 - 0x0296 (2 bytes)
```

```
* PC items
    * R/S/E: 0x0498 - 0x0560 (200 bytes)
    * FR/LG: 0x0298 - 0x0310 (120 bytes)
```

```
* Item Pocket
    * R/S  : 0x0560 - 0x05b0 (80 bytes)
    * E    : 0x0560 - 0x05d8 (120 bytes)
    * FR/LG: 0x0310 - 0x03b8 (168 bytes)
```

```
* Key Item Pocket
    * R/S  : 0x05b0 - 0x0600 (80 bytes)
    * E    : 0x05d8 - 0x0650 (120 bytes)
    * FR/LG: 0x03b8 - 0x0430 (120 bytes)
```

```
* Ball Item Pocket
    * R/S  : 0x0600 - 0x0640 (64 bytes)
    * E    : 0x0650 - 0x0690 (64 bytes)
    * FR/LG: 0x0430 - 0x0464 (52 bytes)
```

```
*  TM Case
    * R/S  : 0x0640 - 0x0740 (256 bytes)
    * E    : 0x0690 - 0x0790 (256 bytes)
    * FR/LG: 0x0464 - 0x054c (232 bytes)
```

```
*  Berry Pocket
    * R/S  : 0x0740 - 0x07f8 (184 bytes)
    * E    : 0x0790 - 0x0848 (184 bytes)
    * FR/LG: 0x054c - 0x05f8 (172 bytes)
```

