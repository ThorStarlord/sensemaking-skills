import secrets

def main() -> None:
    for name in ("seed_pilot_dispatch", "seed_tranche1_dispatch", "seed_tranche2_dispatch"):
        print(f"{name}={secrets.token_hex(16)}")

if __name__ == "__main__":
    main()
