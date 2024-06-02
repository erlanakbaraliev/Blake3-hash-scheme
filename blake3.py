def quarter_round(a, b, c, d):
    a = (a + b) & 0xFFFFFFFF
    d ^= a
    d = ((d << 16) | (d >> 16)) & 0xFFFFFFFF

    c = (c + d) & 0xFFFFFFFF
    b ^= c
    b = ((b << 12) | (b >> 20)) & 0xFFFFFFFF

    a = (a + b) & 0xFFFFFFFF
    d ^= a
    d = ((d << 8) | (d >> 24)) & 0xFFFFFFFF

    c = (c + d) & 0xFFFFFFFF
    b ^= c
    b = ((b << 7) | (b >> 25)) & 0xFFFFFFFF

    return a, b, c, d

def blake3_compress(state):
    for _ in range(12):
        state[0], state[4], state[8], state[12] = quarter_round(state[0], state[4], state[8], state[12]) 
        state[1], state[5], state[9], state[13] = quarter_round(state[1], state[5], state[9], state[13]) 
        state[2], state[6], state[10], state[14] = quarter_round(state[2], state[6], state[10], state[14]) 
        state[3], state[7], state[11], state[15] = quarter_round(state[3], state[7], state[11], state[15]) 

    for i in range(16):
        state[i] = (state[i] + state[i % 16]) & 0xFFFFFFFF

    return state

def blake3_hash(key, counter, message):
    state = [0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A]
    key_words = [int.from_bytes(key[i:i+4], 'little') for i in range(0, len(key), 4)]

    state += key_words + [counter] + [0] * (15 - len(state) - len(key_words))

    state = blake3_compress(state)

    result = b''.join(word.to_bytes(4, 'little') for word in state[:8]) 
    return result

key_bytes = b"erlan"
counter = 0
message = b"crypto is fun"
hash_result = blake3_hash(key_bytes, counter, message)
print(f"Hash result: {hash_result.hex()}")