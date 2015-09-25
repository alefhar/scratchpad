// compile with: g++ -std=c++14 -O3 -o bit_add bit_add.cpp
#include <iostream>

template <size_t N>
int add(int a, int b)
{
  int c = 0u;
  
  bool carry = false;
  for (size_t i = 0; i < N; ++i)
  {
    bool a_i = a & (1 << i);
    bool b_i = b & (1 << i);
    bool c_i = a_i ^ b_i ^ carry;

    c = c | (c_i << i);
    carry = (a_i & b_i) ^ ((a_i ^ b_i) & carry);
  }

  c = c | (carry << N);
  return c;
}

int main()
{
  bool error = false;
  const size_t size = 14;

  for (auto a = 0u; a < 1u << size; ++a) 
  { 
    for (auto b = 0u; b < 1u << size; ++b) 
    { 
      auto c = add<size>(a, b); 
      bool local_error = (a + b != c); 
      error |= local_error; 
      if (local_error) 
        std::cout << a << " + " << b << " = " << c << std::endl; 
    } 
  } 

  std::cout << (error ? "fail" : "pass") << std::endl; 

  return 0;
}
