# bencode
A Python library to encode and decode `b-encode` codes. Is it me or did it just rhythm like a rap?

## How to use
### Importing
The user can load the library normally as:
```python
import bencode as b
```

### Encoding
You can use the function `encode` that will detect the used data types and processes it accordingly. Even with complex `list` or `dict` elements.
```python
b.encode(5)
# Returns bencode string: `i5e`

b.encode("xyz")
# Returns bencode string: `3:xyz`

b.encode(['January', 2, {"march": "APRIL"}, ["May", "June", "July", -8]])
# Returns bencode string: `l7:Januaryi2ed5:march5:APRILel3:May4:June4:Julyi-8eee`

b.encode({11: "x", 22: "y", 33: "z", 44: {0: [-1, 2, -3]}})
# Returns bencode string: `di11e1:xi22e1:yi33e1:zi44edi0eli-1ei2ei-3eeee`
```

### Decoding
On the other hand, if you wish to decode:
 ```python
b.decode("i5e")
# Returns the integer: 5

b.decode("3:xyz")
# Returns the string: "xyz"

b.encode("l7:Januaryi2ed5:march5:APRILel3:May4:June4:Julyi-8eee")
# Returns the list: ['January', 2, {"march": "APRIL"}, ["May", "June", "July", -8]]

b.encode("di11e1:xi22e1:yi33e1:zi44edi0eli-1ei2ei-3eeee")
# Returns the dictionary: {11: "x", 22: "y", 33: "z", 44: {0: [-1, 2, -3]}}
```
