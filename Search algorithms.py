import timeit
import os

# ---------------- KMP ----------------
def kmp_search(text, pattern):
    if not pattern:
        return True

    lps = [0] * len(pattern)
    j = 0

    for i in range(1, len(pattern)):
        while j > 0 and pattern[i] != pattern[j]:
            j = lps[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
            lps[i] = j

    i = j = 0
    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1

        if j == len(pattern):
            return True

        elif i < len(text) and text[i] != pattern[j]:
            if j:
                j = lps[j - 1]
            else:
                i += 1

    return False


# ---------------- Boyer-Moore ----------------
def boyer_moore_search(text, pattern):
    m = len(pattern)
    n = len(text)

    if m == 0:
        return True

    bad_char = {}

    for i in range(m):
        bad_char[pattern[i]] = i

    shift = 0

    while shift <= n - m:
        j = m - 1

        while j >= 0 and pattern[j] == text[shift + j]:
            j -= 1

        if j < 0:
            return True

        shift += max(1, j - bad_char.get(text[shift + j], -1))

    return False


# ---------------- Rabin-Karp ----------------
def rabin_karp_search(text, pattern):
    d = 256
    q = 101

    m = len(pattern)
    n = len(text)

    if m == 0 or m > n:
        return False

    h = pow(d, m - 1) % q

    p = 0
    t = 0

    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    for i in range(n - m + 1):

        if p == t:
            if text[i:i + m] == pattern:
                return True

        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
            t %= q

    return False


# ---------- читання файлів ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def read_text(filename):
    encodings = [
        "utf-8",
        "utf-8-sig",
        "cp1251",
        "windows-1251",
        "cp1252",
        "latin1"
    ]

    for enc in encodings:
        try:
            with open(os.path.join(BASE_DIR, filename), "r", encoding=enc) as f:
                text = f.read()
            print(f"{filename} відкрито ({enc})")
            return text
        except UnicodeDecodeError:
            continue

    raise Exception(f"Could not open the file. {filename}")


text1 = read_text("article1.txt")
text2 = read_text("article2.txt")


# ---------- підрядки ----------
existing1 = text1[:20]
existing2 = text2[:20]

fake = "qwertyuiopasdfgh"


# ---------- вимір часу ----------
def measure(func, text, pattern):
    return timeit.timeit(lambda: func(text, pattern), number=100)


algorithms = {
    "KMP": kmp_search,
    "Boyer-Moore": boyer_moore_search,
    "Rabin-Karp": rabin_karp_search
}

results1 = {}
results2 = {}

print("\n================ Article 1 ================\n")

for name, algo in algorithms.items():
    t_exist = measure(algo, text1, existing1)
    t_fake = measure(algo, text1, fake)

    results1[name] = t_exist + t_fake

    print(f"{name}")
    print(f"  existing : {t_exist:.6f}")
    print(f"  fake: {t_fake:.6f}")
    print()

print("The fastest:", min(results1, key=results1.get))

print("\n================ Article 2 ================\n")

for name, algo in algorithms.items():
    t_exist = measure(algo, text2, existing2)
    t_fake = measure(algo, text2, fake)

    results2[name] = t_exist + t_fake

    print(f"{name}")
    print(f"  existing : {t_exist:.6f}")
    print(f"  fake: {t_fake:.6f}")
    print()

print("The fastest:", min(results2, key=results2.get))

overall = {}

for name in algorithms:
    overall[name] = results1[name] + results2[name]

print("\n================ Overall Result ================\n")

for name in overall:
    print(f"{name}: {overall[name]:.6f}")

print("\nThe fastest algorithm:", min(overall, key=overall.get))