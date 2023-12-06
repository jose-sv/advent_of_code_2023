/*
 * This was a fun chance to learn a bit about, and play around with, AVX512!
 */

#include<iostream>
#include<fstream>
#include<string>
#include<stdint.h>
#include<immintrin.h>

int atoi(char* value) {
    int val = 0;
    int mult = 1;  // which digits place?

    for (char* c = value+2; c>=value; c--) {
        if (*c != '-') {
            val += (*c - '0') * mult;
            mult *= 10;
        }
    }

    value[0] = '-';
    value[1] = '-';
    value[2] = '-';

    return val;
}

inline void init_values(uint32_t* winning, uint32_t* exist, int* card_id, char* curr_val, int* curr_val_idx, int* processing) {
    *processing = 0;
    *curr_val_idx = 0;
    curr_val[0] = '-';
    curr_val[1] = '-';
    curr_val[2] = '-';

    // TODO memset
    for (uint32_t* b=winning; b<winning+16; b+=8) {
        b[0] &= 0x00000000;
        b[1] &= 0x00000000;
        b[2] &= 0x00000000;
        b[3] &= 0x00000000;
        b[4] &= 0x00000000;
        b[5] &= 0x00000000;
        b[6] &= 0x00000000;
        b[7] &= 0x00000000;
    }

    // TODO memset
    for (uint32_t* b=exist; b<exist+16; b+=8) {
        b[0] &= 0x00000000;
        b[1] &= 0x00000000;
        b[2] &= 0x00000000;
        b[3] &= 0x00000000;
        b[4] &= 0x00000000;
        b[5] &= 0x00000000;
        b[6] &= 0x00000000;
        b[7] &= 0x00000000;
    }
}

inline int get_addr_by_idx(int idx) {
    return idx / 32;
}

static const uint32_t masks[32] = {
    0x80000000, 0x40000000, 0x20000000, 0x10000000,
    0x08000000, 0x04000000, 0x02000000, 0x01000000,
    0x00800000, 0x00400000, 0x00200000, 0x00100000,
    0x00080000, 0x00040000, 0x00020000, 0x00010000,
    0x00008000, 0x00004000, 0x00002000, 0x00001000,
    0x00000800, 0x00000400, 0x00000200, 0x00000100,
    0x00000080, 0x00000040, 0x00000020, 0x00000010,
    0x00000008, 0x00000004, 0x00000002, 0x00000001
};
// masks= [ 0x80000000, 0x40000000, 0x20000000, 0x10000000, 0x08000000, 0x04000000, 0x02000000, 0x01000000, 0x00800000, 0x00400000, 0x00200000, 0x00100000, 0x00080000, 0x00040000, 0x00020000, 0x00010000, 0x00008000, 0x00004000, 0x00002000, 0x00001000, 0x00000800, 0x00000400, 0x00000200, 0x00000100, 0x00000080, 0x00000040, 0x00000020, 0x00000010, 0x00000008, 0x00000004, 0x00000002, 0x00000001 ]

int count_wins(uint32_t* winning, uint32_t* exist) {
    __m512i win_vec = _mm512_load_epi32(winning);
    __m512i exi_vec = _mm512_load_epi32(exist);

    __m512i matches = _mm512_and_epi32(win_vec, exi_vec);

    __m512i counts  = _mm512_popcnt_epi32(matches);

    int f_count = _mm512_reduce_add_epi32(counts);
    return f_count;
}

inline uint32_t get_bitmask_by_idx(int idx) {
    return masks[idx % 32];
}

void parse_file() {
    char n_char;
    char curr_val[3];  // support vals < 999
    int curr_val_idx = 0;
    int card_id;

    int bit_to_set;
    alignas(64) uint32_t winning[16];  // TODO leverage extra space
    alignas(64) uint32_t exist[16];    // TODO leverage extra space

    uint32_t* lists[2];
    lists[0] = winning;
    lists[1] = exist;
    int processing = 0;

    std::ifstream in_f("input.txt");

    // skip first four chars ("Card")
    in_f.get(); in_f.get(); in_f.get(); in_f.get();

    init_values(winning, exist, &card_id, curr_val, &curr_val_idx, &processing);
    while(in_f) {
        n_char = in_f.get();

        switch(n_char) {
            case '\n':
                curr_val_idx = 0;
                if (curr_val[0] != '-') {
                    bit_to_set = atoi(curr_val);
                    lists[processing][get_addr_by_idx(bit_to_set)] |= get_bitmask_by_idx(bit_to_set);
                }

                // TODO compute SCORES using count
                std::cout << "Card " << card_id << " has " << count_wins(winning, exist) << " wins!\n";

                init_values(winning, exist, &card_id, curr_val, &curr_val_idx, &processing);
                break;

            case ':':  // end of name
                card_id = atoi(curr_val);
                break;

            case ' ':  // terminate and skip
                curr_val_idx = 0;
                if (curr_val[0] != '-') {
                    // convert from "index" (loaded value) to bit number
                    bit_to_set = atoi(curr_val);
                    lists[processing][get_addr_by_idx(bit_to_set)] |= get_bitmask_by_idx(bit_to_set);
                }
                break;

            case '|':  // switch to existing
                processing = processing ^ 0x1;
                break;

            default:
                // being lazy and processing later
                // TODO compute and scale directly
                // int:curr_val = int:curr_val * 10 + atoi(n_char)
                curr_val[curr_val_idx++] = n_char;
                break;
        }
    }
}

int main() {
    parse_file();

    return 0;
}
