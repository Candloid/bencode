import bencode as b


def main():
    print(" == Example == ")

    some_list = {"every": 1, "should": {"treat": "everyone", "else": "in respect"}}
    print("The element: " + str(some_list))
    print("of the type " + str(type(some_list)) + " can be encoded into a Bencode as:")
    result = b.encode(some_list)
    print(result)

    print()

    some_code = "l7:Januaryi2ed5:march5:APRILel3:May4:June4:Julyi-8eee"
    print("The Bencode: " + some_code)
    result = b.decode(some_code)
    print("would decode into the element of the type " + str(type(result)) + " of the following content:")
    print(result)


if __name__ == "__main__":
    main()