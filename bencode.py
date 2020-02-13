# Author: Bilal Qandeel
# Date: 2020-02-07


class UnsupportedDataTypeException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self, *args):
        return "Unsupported data type " + self.message


class InvalidBencode(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        return "Unable to resolve invalid Bencode [" + self.message + "]"


def encode(element):
    """
    :param element: the element required to be bencoded
    :return: the bencoded string
    """
    return_code = ""
    if type(element) is int:
        return_code += "i" + str(int(element)) + "e"
    elif type(element) is str:
        return_code += str(len(element)) + ":" + str(element)
    elif type(element) is list:
        for value in element:
            return_code += encode(value)
        return "l" + return_code + "e"
    elif type(element) is dict:
        for key, value in element.items():
            return_code += encode(key)
            return_code += encode(value)
        return "d" + return_code + "e"
    else:
        raise UnsupportedDataTypeException(str(type(element)))
    return return_code


def process_dict(content):
    if content.strip() == "":
        return ""
    original_content = content
    exclusion_zone = []
    end = content.find("}")
    begin = content.rfind("{", 0, end)
    while end != -1:
        content = content[0:begin] + content[begin + 1: end].replace("{", "<").replace("}", ">") + content[end + 1:]
        exclusion_zone.extend(list(range(begin, end)))
        end = content.find("}")
        begin = content.find("{", 0, end)

    end = content.find("]")
    begin = content.rfind("[", 0, end)
    while end != -1:
        content = content[0:begin] + content[begin + 1: end].replace("[", "<").replace("]", ">") + content[end + 1:]
        exclusion_zone.extend(list(range(begin, end)))
        end = content.find("]")
        begin = content.find("[", 0, end)

    content = original_content
    at = 0
    token = content[at]
    token_order = 0
    while at < len(content)-1:
        if token == "," and at not in exclusion_zone:
            if (token_order % 2) == 0:
                content = content[0:at] + ":" + content[at + 1:]
            token_order += 1
            at += 1
            token = content[at]
        else:
            at += 1
            token = content[at]
    return content


def decode(code):
    try:
        if code.strip() == "":
            return ""
        result = code
        # # Process texts # #
        placeholder = []
        placeholder_counter = -1
        token = result.find(":")
        while token != -1:
            left_to_token = token-1
            while result[left_to_token:token].isdigit():
                left_to_token -= 1
            length = int(result[left_to_token + 1:token])
            text = result[token+1:token+1+length]

            # Encode texts so they won't interfere with `d`, `l`, or `i`
            placeholder.append(text)
            placeholder_counter += 1
            result =\
                result[0:left_to_token+1] + "\"" +\
                "TEXTPLACEHOLDER" + f"{placeholder_counter:04d}" +\
                "\"," + result[token+length+1:]
            token = result.find(":")

        # # Process integers # #
        begin = result.find("i")
        end = result.find("e", begin)
        while begin != -1:
            result = result[0:begin] + result[begin + 1:end] + "," + result[end + 1:]
            begin = result.find("i")
            end = result.find("e", begin)

        # # Process dicts and lists # #
        end = result.find("e")
        while end != -1:
            begin_l = result.rfind("l", 0, end)
            begin_d = result.rfind("d", 0, end)
            if begin_d > begin_l:
                result = result[0:begin_d] + "{" + process_dict(result[begin_d + 1:end]) + "}," + result[end + 1:]
            elif begin_l > begin_d:
                result = result[0:begin_l] + "[" + result[begin_l + 1:end] + "]," + result[end + 1:]
            else:
                raise InvalidBencode(result)
            end = result.find("e")

        # Cleanup for extraneous commas
        #  between square brackets
        fix = result.find(",]")
        while fix != -1:
            result = result.replace(",]", "]")
            fix = result.find(",]")

        #  between curly braces
        fix = result.find(",}")
        while fix != -1:
            result = result.replace(",}", "}")
            fix = result.find(",}")

        #  between braces
        fix = result.find(",)")
        while fix != -1:
            result = result.replace(",)", ")")
            fix = result.find(",)")

        #  and trailing ones
        if result[-1] == ",":
            result = result[0:-1]

        # Decode texts
        for text_id in range(0, len(placeholder)):
            result = result.replace("TEXTPLACEHOLDER" + f"{text_id:04d}", placeholder[text_id])

        return eval(result)

    except Exception:
        raise InvalidBencode
