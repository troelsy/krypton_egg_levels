
level_sets = {
    1: {
        0:  0xEDB0,
        1:  0x6DA0,
        2:  0xAD91,
        3:  0x2D81,
        4:  0xEDF2,
        5:  0x6DE2,
        6:  0xADD3,
        7:  0x2DC3,
        8:  0xAD34,
        10: 0xED15,
        14: 0xED57,
        22: 0xACDB,
        28: 0xAC7E,
        31: 0x6C4F,
        39: 0x2FC3
    },
    2: {
        56: 0xA232,
    },
    3: {
        49: 0x26A4,
    },
    4: {
        21: 0x38E0,
        22: 0xF8D1,
        23: 0x78C1,
        25: 0x7826,
        26: 0xB817,
        27: 0x3807,
        28: 0xF874,
        29: 0x7864,
        30: 0xB855,
        31: 0x3845,
        32: 0xBBBA,
        45: 0x7B6C,
        46: 0xBB5D,
        47: 0x3B4D,
        53: 0x3AE0,
    },
    5: {
        24: 0xBC34
    },
    6: {
        17: 0x70AE
    },
    7: {
        57: 0x7628
    },
    8: {
        38: 0xCBD1
    },
    9: {
        29: 0x0C6E
    },
}


def encode(level, lives):
    life_checksum_lut = {
        1: 0b0000,
        2: 0b1110,
        3: 0b1100,
        4: 0b1010,
        5: 0b1000,
        6: 0b0110,
        7: 0b0100,
        8: 0b0010,
        9: 0b0000,
    }

    encoded_life = lives ^ 0b011011
    encoded_level = level ^ 0b1010
    life_checksum1 = life_checksum_lut[level] ^ ((lives & 0b011110) >> 1)

    # Extract bits from lives
    life_b8 = (lives >> 3) & 0b1
    life_b2 = (lives >> 1) & 0b1
    life_b1 = lives & 0b1 == 0

    life_checksum2 = life_b8 ^ life_b2
    if ((level - 1) // 2) & 0b1 == 0:  # 1, 1, 0, 0, 1, ...
        life_checksum2 = not life_checksum2

    package = (
        (life_b1 << 15) +
        (life_checksum2 << 14) +
        (encoded_level << 10) +
        (encoded_life << 4) +
        life_checksum1
    )

    return package


# Test the encoder
for level, level_set in level_sets.items():
    for lives, code in level_set.items():
        encoded_code = encode(level, lives)
        if encoded_code != code:
            print(level, lives, hex(code), hex(encoded_code), encoded_code == code)


# Print a markdown table with levels as columns and lives as rows
print("| Lives |", " | ".join(f"Level {i}" for i in range(1, 10)), "|")
print("|-------|" + "|".join(["-------"] * 9) + "|")

for lives in range(0, 64):
    row = f"| {lives} |"
    for level in range(1, 10):
        row += f" {hex(encode(level, lives))[2:].upper()} |"
    print(row)
