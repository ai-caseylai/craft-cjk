import sys
# Big5 level 1: the standard 常用字 (0xA440-0xC67E)
l1 = set()
for hi in range(0xA4, 0xC7):
    for lo in range(0x40, 0xFF):
        try:
            c = bytes([hi, lo]).decode("big5")
            if c:
                l1.add(c)
        except Exception:
            pass
# Everything Big5-HKSCS can decode: Big5 plus the Hong Kong Supplementary set
hkscs = set()
for hi in range(0x81, 0xFF):
    for lo in range(0x40, 0xFF):
        try:
            c = bytes([hi, lo]).decode("big5hkscs")
            if c:
                hkscs.add(c)
        except Exception:
            pass
hk_only = hkscs - l1
extra = set(chr(c) for c in range(0x20, 0x7F))
extra |= set("\u3000\u3001\u3002\u3008\u3009\u300a\u300b\u300c\u300d\u300e\u300f\u3010\u3011\u3014\u3015\u30fb\u30fc\u2026\u2014\uff5e\uff0d\uff08\uff09\uff1d\uff0b\uff05\uff03\uff20\uff06\uff0a\uff1b\uff1a\uff1f\uff01\uff0c\uff0e\uff0f\uff3c\uff5c\uff04\u2018\u2019\u201c\u201d\u00b7")
final = l1 | hk_only | extra
open(sys.argv[1], "w", encoding="utf-8").write("".join(sorted(final)))
print("Big5 level 1      :", len(l1))
print("Big5-HKSCS total  :", len(hkscs))
print("HK-only additions :", len(hk_only))
print("FINAL list        :", len(final))
# a few Hong Kong Cantonese characters people actually type
probe = "\u5605\u54d7\u554f\u5617\u4f62\u5514\u5497\u558e\u55ce\u5636\u5617\u5565\u55ce\u54cb\u5427\u55da\u54ea\u5617\u55b3"
print("HK probe present  :", sum(1 for c in probe if c in final), "/", len(probe))
