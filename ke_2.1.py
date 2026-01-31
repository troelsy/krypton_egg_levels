
level_sets = {
    1:{
        0: 0xAB99,
        1: 0xEB89,
        2: 0xBB9,
        3: 0x4BA9,
        4: 0xABD8,
        5: 0xEBC8,
        6: 0xBF8,
        7: 0x4BE8,
        9: 0xCB0B,
        11: 0x6B2B,
        12: 0x8B5A,
        13: 0xCB4A,
        15: 0x6B6A,
        16: 0xAA9D,
        17: 0xEA8D,
        18: 0xABD,
        32: 0xA991,
    },
    2:{
        3: 0x47AE,
        4: 0xA7DF,
        5: 0xE7CF,
        7: 0x47EF,
        16: 0xA69A,
        17: 0xE68A,
        18: 0x6BA,
        32: 0xA596,
    },
    3: {
        0: 0x839F,
        1: 0xC38F,
        2: 0x23BF,
        3: 0x63AF,
        4: 0x83DE,
        5: 0xC3CE,
        6: 0x23FE,
        8: 0xA31D,
        9: 0xE30D,
        10: 0x33D,
        12: 0xA35C,
        14: 0x37C,
        32: 0x8197,
    },
    4: {
        0: 0x9F9C,
        1: 0xDF8C,
        12: 0xBF5F,
        32: 0x9D94,
    },
    5: {
        0: 0xBB9D,
        6: 0x1BFC,
        7: 0x5BEC,
        10: 0x3B3F,
        16: 0xBA99,
        18: 0x1AB9,
        22: 0x1AF8,
        32: 0xB995,
        48: 0xB891,
    }
}


def encode(level, lives):
    life_checksum_lut = {
        1: 0b100100,
        2: 0b111000,
        3: 0b111100,
        4: 0b110000,
        5: 0b110100,
    }

    encoded_level = 0b011 ^ level
    encoded_lives = 0b111001 ^ lives
    life_checksum3 = (life_checksum_lut[level] ^ lives) >> 2

    # Extract bits from lives
    life_b8 = (encoded_lives >> 3) & 0b1
    life_b2 = (encoded_lives >> 1) & 0b1
    life_b1 = encoded_lives & 0b1

    life_checksum2 = life_b8 ^ life_b2
    if ((level - 1) // 2) & 0b1 == 1:  # 1, 1, 0, 0, 1, ...
        life_checksum2 = not life_checksum2

    life_checksum1 = ~((life_b2 << 1) + life_b1) & 0b11

    package = (
        (life_checksum1 << 14) +
        (life_checksum2 << 13) +
        (encoded_level << 10) +
        (encoded_lives << 4) +
        life_checksum3
    )

    return package


# Test the encoder
for level, level_set in level_sets.items():
    for lives, code in level_set.items():
        encoded_code = encode(level, lives)
        if encoded_code != code:
            print(level, lives, hex(code), hex(encoded_code), encoded_code == code)


# Print a markdown table with levels as columns and lives as rows
print("| Lives |", " | ".join(f"Level {i}" for i in range(1, 6)), "|")
print("|-------|" + "|".join(["-------"] * 5) + "|")

for lives in range(0, 64):
    row = f"| {lives} |"
    for level in range(1, 6):
        row += f" {hex(encode(level, lives))[2:].upper()} |"
    print(row)
