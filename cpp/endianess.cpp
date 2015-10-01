#include <iostream>
#include <cstdint>

int main()
{
    // determine machine endianess
    //                +------+------+------+------+
    // Big Endian:    | 0x42 | 0x03 | 0x30 | 0x24 |
    //                +------+------+------+------+
    // Byte Address:  | 0x00 | 0x01 | 0x02 | 0x03 |
    //                +------+------+------+------+
    // Little Endian: | 0x24 | 0x30 | 0x03 | 0x42 |
    //                +------+------+------+------+
    std::uint32_t x = 0x42033024;
    char *y = reinterpret_cast<char*>(&x);
    
    if (y[0] == 0x24)
        std::cout << "Little Endian" << std::endl;

    if (y[0] == 0x42)
        std::cout << "Big Endian" << std::endl;

    return 0;
}
