import pandas as pd


def main():
    df = pd.read_csv("Daghregisters - Inventories.csv")

    urls = []
    for d in df.to_dict(orient="records"):
        for i in range(1, d["Pages"] + 1):
            url = d["URL"] + str(i)
            urls.append(url)

    with open("urls.txt", "w") as f:
        f.write("\n".join(urls))


if __name__ == "__main__":
    main()
