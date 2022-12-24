class Hogehoge:
    def __init__(self) -> None:
        pass

    def hogehoge(self, k: int) -> str:
        result = ""
        for idx in range(k):
            result += chr(ord("A") + idx)
        return result


if __name__ == "__main__":
    k = int(input())
    hogehoge_obj = Hogehoge()
    print(hogehoge_obj.hogehoge(k))
