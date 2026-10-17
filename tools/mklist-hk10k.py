import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
def scan(codec):
    out = set()
    for hi in range(0x81, 0xFF):
        for lo in range(0x40, 0xFF):
            try:
                c = bytes([hi, lo]).decode(codec)
                if c: out.add(c)
            except Exception: pass
    return out
std = scan("big5")
hk  = scan("big5hkscs")
l1 = set()
for hi in range(0xA4, 0xC7):
    for lo in range(0x40, 0xFF):
        try:
            c = bytes([hi, lo]).decode("big5")
            if c: l1.add(c)
        except Exception: pass
hkscs_only = hk - std                      # the genuine Hong Kong supplementary set
extra = set(chr(c) for c in range(0x20, 0x7F))
extra |= set("\u3000\u3001\u3002\u3008\u3009\u300a\u300b\u300c\u300d\u300e\u300f\u3010\u3011\u3014\u3015\u30fb\u30fc\u2026\u2014\uff5e\uff0d\uff08\uff09\uff1d\uff0b\uff05\uff03\uff20\uff06\uff0a\uff1b\uff1a\uff1f\uff01\uff0c\uff0e\uff0f\uff3c\uff5c\uff04\u2018\u2019\u201c\u201d\u00b7")
final = l1 | hkscs_only | extra
open(sys.argv[1], "w", encoding="utf-8").write("".join(sorted(final)))
print("Big5 level 1        :", len(l1))
print("true HKSCS additions:", len(hkscs_only))
print("FINAL list          :", len(final))
probe = "\u5605\u54d7\u5617\u4f62\u5514\u5497\u558e\u55ce\u5565\u54cb\u55da\u5617\u55b3\u5427\u54ea"
print("HK Cantonese probe  :", sum(1 for c in probe if c in final), "/", len(probe))
