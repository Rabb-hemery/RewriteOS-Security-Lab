from collections import Counter
from pathlib import Path
import re
import sys

THRESHOLD = 5
IP_PATTERN = re.compile(r"\bip=(\d{1,3}(?:\.\d{1,3}){3})\b")


def analyze_log(log_path: Path) -> int:
    failures = Counter()

    if not log_path.is_file():
        print(f"[ERROR] Fichier introuvable : {log_path}")
        return 2

    with log_path.open("r", encoding="utf-8") as log_file:
        for line_number, line in enumerate(log_file, start=1):
            if "LOGIN_FAILED" not in line:
                continue

            match = IP_PATTERN.search(line)
            if match:
                failures[match.group(1)] += 1
            else:
                print(f"[WARN] Ligne {line_number} : IP absente ou invalide")

    print("=== RewriteOS Security Lab ===")
    print(f"Échecs analysés : {sum(failures.values())}")
    print(f"Seuil d'alerte : {THRESHOLD}")

    alerts = 0

    for ip, count in sorted(failures.items()):
        if count >= THRESHOLD:
            print(f"[ALERTE] {ip} : {count} échecs de connexion")
            alerts += 1

    if alerts == 0:
        print("[OK] Aucune adresse n'a atteint le seuil d'alerte.")

    return 0


if __name__ == "__main__":
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("logs/sample.log")
    raise SystemExit(analyze_log(path))
