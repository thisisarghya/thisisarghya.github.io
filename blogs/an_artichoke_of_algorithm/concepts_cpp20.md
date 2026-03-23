# \<concepts\> in C++20

## \<concepts\> provides compile-time predicates with the primary advantage of much more readable error messages, early catching of errors during compilation of programs, and improved overloading.

Date: Aug 22, 2025

**Let’s understand with an example.**  
Use case: We wrote a function to add 2 integers but mistakenly passed two vectors of integers in the function.

## Pre-C++20 way

```c
#include <vector>
#include <iostream>

template <typename T>
T add(T a, T b) {
    return a + b;
}

int main() {
  std::vector<int> x = {4, 5, 6};
  std::vector<int> y = {1, 2, 3};
  auto z = add(x, y);
  std::cout << z << std::endl;
}
```

We call it \`add(5, 10)\`. However, if we mistakenly call this function with two std::vector objects. A vector does not have a \+ operator. Well, the compiler will generate a super-long error message of no help instead of prompting “"Vectors can't be added.” Error message:

```shell
arghyabh@arghya:~$ g++ -std=c++11 test_concepts_old.cpp -o a.out
test_concepts_old.cpp: In function ‘int main()’:
test_concepts_old.cpp:13:13: error: no match for ‘operator<<’ (operand types are ‘std::ostream’ {aka ‘std::basic_ostream<char>’} and ‘std::vector<int>’)
   13 |   std::cout << z << std::endl;
      |   ~~~~~~~~~ ^~ ~
      |        |       |
      |        |       std::vector<int>
      |        std::ostream {aka std::basic_ostream<char>}
test_concepts_old.cpp:13:13: note: there are 30 candidates
   13 |   std::cout << z << std::endl;
      |   ~~~~~~~~~~^~~~
In file included from /usr/include/c++/15/ostream:42,
                 from /usr/include/c++/15/iostream:43,
                 from test_concepts_old.cpp:2:
/usr/include/c++/15/bits/ostream.h:116:7: note: candidate 1: ‘std::basic_ostream<_CharT, _Traits>::__ostream_type& std::basic_ostream<_CharT, _Traits>::operator<<(__ostream_type& (*)(__ostream_type&)) [with _CharT = char; _Traits = std::char_traits<char>; __ostream_type = std::basic_ostream<char>]’
  116 |       operator<<(__ostream_type& (*__pf)(__ostream_type&))
      |       ^~~~~~~~
/usr/include/c++/15/bits/ostream.h:116:36: note: no known conversion for argument 1 from ‘std::vector<int>’ to ‘std::basic_ostream<char>::__ostream_type& (*)(std::basic_ostream<char>::__ostream_type&)’ {aka ‘std::basic_ostream<char>& (*)(std::basic_ostream<char>&)’}
  116 |       operator<<(__ostream_type& (*__pf)(__ostream_type&))
      |                  ~~~~~~~~~~~~~~~~~~^~~~~~~~~~~~~~~~~~~~~~
/usr/include/c++/15/bits/ostream.h:125:7: note: candidate 2: ‘std::basic_ostream<_CharT, _Traits>::__ostream_type& std::basic_ostream<_CharT, _Traits>::operator<<(__ios_type& (*)(__ios_type&)) [with _CharT = char; _Traits = std::char_traits<char>; __ostream_type = std::basic_ostream<char>; __ios_type = std::basic_ios<char>]’
  125 |       operator<<(__ios_type& (*__pf)(__ios_type&))
      |       ^~~~~~~~
/usr/include/c++/15/bits/ostream.h:125:32: note: no known conversion for argument 1 from ‘std::vector<int>’ to ‘std::basic_ostream<char>::__ios_type& (*)(std::basic_ostream<char>::__ios_type&)’ {aka ‘std::basic_ios<char>& (*)(std::basic_ios<char>&)’}
  125 |       operator<<(__ios_type& (*__pf)(__ios_type&))
      |                  ~~~~~~~~~~~~~~^~~~~~~~~~~~~~~~~~
/usr/include/c++/15/bits/ostream.h:135:7: note: candidate 3: ‘std::basic_ostream<_CharT, _Traits>::__ostream_type& std::basic_ostream<_CharT, _Traits>::operator<<(std::ios_base& (*)(std::ios_base&)) [with _CharT = char; _Traits = std::char_traits<char>; __ostream_type = std::basic_ostream<char>]’
  135 |       operator<<(ios_base& (*__pf) (ios_base&))
      |       ^~~~~~~~
/usr/include/c++/15/bits/ostream.h:135:30: note: no known conversion for argument 1 from ‘std::vector<int>’ to ‘std::ios_base& (*)(std::ios_base&)’
  135 |       operator<<(ios_base& (*__pf) (ios_base&))
      |                  ~~~~~~~~~~~~^~~~~~~~~~~~~~~~~
/usr/include/c++/15/bits/ostream.h:174:7: note: candidate 4: ‘std::basic_ostream<_CharT, _Traits>::__ostream_type& std::basic_ostream<_CharT, _Traits>::operator<<(long int) [with _CharT = char; _Traits = std::char_traits<char>; __ostream_type = std::basic_ostream<char>]’
  174 |       operator<<(long __n)
      |       ^~~~~~~~
/usr/include/c++/15/bits/ostream.h:174:23: note: no known conversion for argument 1 from ‘std::vector<int>’ to ‘long int’
  174 |       operator<<(long __n)
      |                  ~~~~~^~~
/usr/include/c++/15/bits/ostream.h:178:7: note: candidate 5: ‘std::basic_ostream<_CharT, _Traits>::__ostream_type& std::basic_ostream<_CharT, _Traits>::operator<<(long unsigned int) [with _CharT = char; _Traits = std::char_traits<char>; __ostream_type = std::basic_ostream<char>]’
  178 |       operator<<(unsigned long __n)
      |       ^~~~~~~~
/usr/include/c++/15/bits/ostream.h:178:32: note: no known conversion for argument 1 from ‘std::vector<int>’ to ‘long unsigned int’
  178 |       operator<<(unsigned long __n)
      |                  ~~~~~~~~~~~~~~^~~
/usr/include/c++/15/bits/ostream.h:182:7: note: candidate 6: ‘std::basic_ostream<_CharT, _Traits>::__ostream_type& std::basic_ostream<_CharT, _Traits>::operator<<(bool) [with _CharT = char; _Traits = std::char_traits<char>; __ostream_type = std::basic_ostream<char>]’
  182 |       operator<<(bool __n)
      |       ^~~~~~~~
/usr/include/c++/15/bits/ostream.h:182:23: note: no known conversion for argument 1 from ‘std::vector<int>’ to ‘bool’
  182 |       operator<<(bool __n)
      |                  ~~~~~^~~
In file included from /usr/include/c++/15/ostream:294:
/usr/include/c++/15/bits/ostream.tcc:100:5: note: candidate 7: ‘std::basic_ostream<_CharT, _Traits>& std::basic_ostream<_CharT, _Traits>::operator<<(short int) [with _CharT = char; _Traits = std::char_traits<char>]’
  100 |     basic_ostream<_CharT, _Traits>::
      |     ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
/usr/include/c++/15/bits/ostream.tcc:101:22: note: no known conversion for argument 1 from ‘std::vector<int>’ to ‘short int’
  101 |     operator<<(short __n)
      |                ~~~~~~^~~
/usr/include/c++/15/bits/ostream.h:189:7: note: candidate 8: ‘std::basic_ostream<_CharT, _Traits>::__ostream_type& std::basic_ostream<_CharT, _Traits>::operator<<(short unsigned int) [with _CharT = char; _Traits = std::char_traits<char>; __ostream_type = std::basic_ostream<char>]’
  189 |       operator<<(unsigned short __n)
      |       ^~~~~~~~
/usr/include/c++/15/bits/ostream.h:189:33: note: no known conversion for argument 1 from ‘std::vector<int>’ to ‘short unsigned int’
  189 |       operator<<(unsigned short __n)
      |                  ~~~~~~~~~~~~~~~^~~
/usr/include/c++/15/bits/ostream.tcc:114:5: note: candidate 9: ‘std::basic_ostream<_CharT, _Traits>& std::basic_ostream<_CharT, _Traits>::operator<<(int) [with _CharT = char; _Traits = std::char_traits<char>]’
  114 |     basic_ostream<_CharT, _Traits>::
      |     ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
/usr/include/c++/15/bits/ostream.tcc:115:20: note: no known conversion for argument 1 from ‘std::vector<int>’ to ‘int’
  115 |     operator<<(int __n)
      |                ~~~~^~~
/usr/include/c++/15/bits/ostream.h:200:7: note: candidate 10: ‘std::basic_ostream<_CharT, _Traits>::__ostream_type& std::basic_ostream<_CharT, _Traits>::operator<<(unsigned int) [with _CharT = char; _Traits = std::char_traits<char>; __ostream_type = std::basic_ostream<char>]’
  200 |       operator<<(unsigned int __n)
      |       ^~~~~~~~
/usr/include/c++/15/bits/ostream.h:200:31: note: no known conversion for argument 1 from ‘std::vector<int>’ to ‘unsigned int’
  200 |       operator<<(unsigned int __n)
      |                  ~~~~~~~~~~~~~^~~
/usr/include/c++/15/bits/ostream.h:211:7: note: candidate 11: ‘std::basic_ostream<_CharT, _Traits>::__ostream_type& std::basic_ostream<_CharT, _Traits>::operator<<(long long int) [with _CharT = char; _Traits = std::char_traits<char>; __ostream_type = std::basic_ostream<char>]’
  211 |       operator<<(long long __n)
      |       ^~~~~~~~
/usr/include/c++/15/bits/ostream.h:211:28: note: no known conversion for argument 1 from ‘std::vector<int>’ to ‘long long int’
  211 |       operator<<(long long __n)
      |                  ~~~~~~~~~~^~~
/usr/include/c++/15/bits/ostream.h:215:7: note: candidate 12: ‘std::basic_ostream<_CharT, _Traits>::__ostream_type& std::basic_ostream<_CharT, _Traits>::operator<<(long long unsigned int) [with _CharT = char; _Traits = std::char_traits<char>; __ostream_type = std::basic_ostream<char>]’
  215 |       operator<<(unsigned long long __n)
      |       ^~~~~~~~
/usr/include/c++/15/bits/ostream.h:215:37: note: no known conversion for argument 1 from ‘std::vector<int>’ to ‘long long unsigned int’
  215 |       operator<<(unsigned long long __n)
      |                  ~~~~~~~~~~~~~~~~~~~^~~
/usr/include/c++/15/bits/ostream.h:231:7: note: candidate 13: ‘std::basic_ostream<_CharT, _Traits>::__ostream_type& std::basic_ostream<_CharT, _Traits>::operator<<(double) [with _CharT = char; _Traits = std::char_traits<char>; __ostream_type = std::basic_ostream<char>]’
  231 |       operator<<(double __f)
      |       ^~~~~~~~
/usr/include/c++/15/bits/ostream.h:231:25: note: no known conversion for argument 1 from ‘std::vector<int>’ to ‘double’
  231 |       operator<<(double __f)
      |                  ~~~~~~~^~~
/usr/include/c++/15/bits/ostream.h:235:7: note: candidate 14: ‘std::basic_ostream<_CharT, _Traits>::__ostream_type& std::basic_ostream<_CharT, _Traits>::operator<<(float) [with _CharT = char; _Traits = std::char_traits<char>; __ostream_type = std::basic_ostream<char>]’
  235 |       operator<<(float __f)
      |       ^~~~~~~~
/usr/include/c++/15/bits/ostream.h:235:24: note: no known conversion for argument 1 from ‘std::vector<int>’ to ‘float’
  235 |       operator<<(float __f)
      |                  ~~~~~~^~~
/usr/include/c++/15/bits/ostream.h:243:7: note: candidate 15: ‘std::basic_ostream<_CharT, _Traits>::__ostream_type& std::basic_ostream<_CharT, _Traits>::operator<<(long double) [with _CharT = char; _Traits = std::char_traits<char>; __ostream_type = std::basic_ostream<char>]’
  243 |       operator<<(long double __f)
      |       ^~~~~~~~
/usr/include/c++/15/bits/ostream.h:243:30: note: no known conversion for argument 1 from ‘std::vector<int>’ to ‘long double’
  243 |       operator<<(long double __f)
      |                  ~~~~~~~~~~~~^~~
/usr/include/c++/15/bits/ostream.h:301:7: note: candidate 16: ‘std::basic_ostream<_CharT, _Traits>::__ostream_type& std::basic_ostream<_CharT, _Traits>::operator<<(const void*) [with _CharT = char; _Traits = std::char_traits<char>; __ostream_type = std::basic_ostream<char>]’
  301 |       operator<<(const void* __p)
      |       ^~~~~~~~
/usr/include/c++/15/bits/ostream.h:301:30: note: no known conversion for argument 1 from ‘std::vector<int>’ to ‘const void*’
  301 |       operator<<(const void* __p)
      |                  ~~~~~~~~~~~~^~~
/usr/include/c++/15/bits/ostream.tcc:128:5: note: candidate 17: ‘std::basic_ostream<_CharT, _Traits>& std::basic_ostream<_CharT, _Traits>::operator<<(__streambuf_type*) [with _CharT = char; _Traits = std::char_traits<char>; __streambuf_type = std::basic_streambuf<char>]’
  128 |     basic_ostream<_CharT, _Traits>::
      |     ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
/usr/include/c++/15/bits/ostream.tcc:129:34: note: no known conversion for argument 1 from ‘std::vector<int>’ to ‘std::basic_ostream<char>::__streambuf_type*’ {aka ‘std::basic_streambuf<char>*’}
  129 |     operator<<(__streambuf_type* __sbin)
      |                ~~~~~~~~~~~~~~~~~~^~~~~~
In file included from /usr/include/c++/15/string:56,
                 from /usr/include/c++/15/bits/locale_classes.h:42,
                 from /usr/include/c++/15/bits/ios_base.h:43,
                 from /usr/include/c++/15/ios:46,
                 from /usr/include/c++/15/bits/ostream.h:43:
/usr/include/c++/15/bits/basic_string.h:4367:5: note: candidate 18: ‘template<class _CharT, class _Traits, class _Alloc> std::basic_ostream<_CharT, _Traits>& std::operator<<(basic_ostream<_CharT, _Traits>&, const __cxx11::basic_string<_CharT, _Traits, _Alloc>&)’
 4367 |     operator<<(basic_ostream<_CharT, _Traits>& __os,
      |     ^~~~~~~~
/usr/include/c++/15/bits/basic_string.h:4367:5: note: template argument deduction/substitution failed:
test_concepts_old.cpp:13:16: note:   ‘std::vector<int>’ is not derived from ‘const std::__cxx11::basic_string<_CharT, _Traits, _Alloc>’
   13 |   std::cout << z << std::endl;
      |                ^
In file included from /usr/include/c++/15/bits/ios_base.h:48:
/usr/include/c++/15/system_error:341:5: note: candidate 19: ‘template<class _CharT, class _Traits> std::basic_ostream<_CharT, _Traits>& std::operator<<(basic_ostream<_CharT, _Traits>&, const error_code&)’
  341 |     operator<<(basic_ostream<_CharT, _Traits>& __os, const error_code& __e)
      |     ^~~~~~~~
/usr/include/c++/15/system_error:341:5: note: template argument deduction/substitution failed:
test_concepts_old.cpp:13:16: note:   cannot convert ‘z’ (type ‘std::vector<int>’) to type ‘const std::error_code&’
   13 |   std::cout << z << std::endl;
      |                ^
/usr/include/c++/15/bits/ostream.h:626:5: note: candidate 20: ‘template<class _CharT, class _Traits> std::basic_ostream<_CharT, _Traits>& std::operator<<(basic_ostream<_CharT, _Traits>&, _CharT)’
  626 |     operator<<(basic_ostream<_CharT, _Traits>& __out, _CharT __c)
      |     ^~~~~~~~
/usr/include/c++/15/bits/ostream.h:626:5: note: template argument deduction/substitution failed:
test_concepts_old.cpp:13:16: note:   deduced conflicting types for parameter ‘_CharT’ (‘char’ and ‘std::vector<int>’)
   13 |   std::cout << z << std::endl;
      |                ^
/usr/include/c++/15/bits/ostream.h:636:5: note: candidate 21: ‘template<class _CharT, class _Traits> std::basic_ostream<_CharT, _Traits>& std::operator<<(basic_ostream<_CharT, _Traits>&, char)’
  636 |     operator<<(basic_ostream<_CharT, _Traits>& __out, char __c)
      |     ^~~~~~~~
/usr/include/c++/15/bits/ostream.h:636:5: note: template argument deduction/substitution failed:
test_concepts_old.cpp:13:16: note:   cannot convert ‘z’ (type ‘std::vector<int>’) to type ‘char’
   13 |   std::cout << z << std::endl;
      |                ^
/usr/include/c++/15/bits/ostream.h:642:5: note: candidate 22: ‘template<class _Traits> std::basic_ostream<char, _Traits>& std::operator<<(basic_ostream<char, _Traits>&, char)’
  642 |     operator<<(basic_ostream<char, _Traits>& __out, char __c)
      |     ^~~~~~~~
/usr/include/c++/15/bits/ostream.h:642:5: note: template argument deduction/substitution failed:
test_concepts_old.cpp:13:16: note:   cannot convert ‘z’ (type ‘std::vector<int>’) to type ‘char’
   13 |   std::cout << z << std::endl;
      |                ^
/usr/include/c++/15/bits/ostream.h:653:5: note: candidate 23: ‘template<class _Traits> std::basic_ostream<char, _Traits>& std::operator<<(basic_ostream<char, _Traits>&, signed char)’
  653 |     operator<<(basic_ostream<char, _Traits>& __out, signed char __c)
      |     ^~~~~~~~
/usr/include/c++/15/bits/ostream.h:653:5: note: template argument deduction/substitution failed:
test_concepts_old.cpp:13:16: note:   cannot convert ‘z’ (type ‘std::vector<int>’) to type ‘signed char’
   13 |   std::cout << z << std::endl;
      |                ^
/usr/include/c++/15/bits/ostream.h:658:5: note: candidate 24: ‘template<class _Traits> std::basic_ostream<char, _Traits>& std::operator<<(basic_ostream<char, _Traits>&, unsigned char)’
  658 |     operator<<(basic_ostream<char, _Traits>& __out, unsigned char __c)
      |     ^~~~~~~~
/usr/include/c++/15/bits/ostream.h:658:5: note: template argument deduction/substitution failed:
test_concepts_old.cpp:13:16: note:   cannot convert ‘z’ (type ‘std::vector<int>’) to type ‘unsigned char’
   13 |   std::cout << z << std::endl;
      |                ^
/usr/include/c++/15/bits/ostream.h:717:5: note: candidate 25: ‘template<class _CharT, class _Traits> std::basic_ostream<_CharT, _Traits>& std::operator<<(basic_ostream<_CharT, _Traits>&, const _CharT*)’
  717 |     operator<<(basic_ostream<_CharT, _Traits>& __out, const _CharT* __s)
      |     ^~~~~~~~
/usr/include/c++/15/bits/ostream.h:717:5: note: template argument deduction/substitution failed:
test_concepts_old.cpp:13:16: note:   mismatched types ‘const _CharT*’ and ‘std::vector<int>’
   13 |   std::cout << z << std::endl;
      |                ^
/usr/include/c++/15/bits/ostream.tcc:311:5: note: candidate 26: ‘template<class _CharT, class _Traits> std::basic_ostream<_CharT, _Traits>& std::operator<<(basic_ostream<_CharT, _Traits>&, const char*)’
  311 |     operator<<(basic_ostream<_CharT, _Traits>& __out, const char* __s)
      |     ^~~~~~~~
/usr/include/c++/15/bits/ostream.tcc:311:5: note: template argument deduction/substitution failed:
test_concepts_old.cpp:13:16: note:   cannot convert ‘z’ (type ‘std::vector<int>’) to type ‘const char*’
   13 |   std::cout << z << std::endl;
      |                ^
/usr/include/c++/15/bits/ostream.h:734:5: note: candidate 27: ‘template<class _Traits> std::basic_ostream<char, _Traits>& std::operator<<(basic_ostream<char, _Traits>&, const char*)’
  734 |     operator<<(basic_ostream<char, _Traits>& __out, const char* __s)
      |     ^~~~~~~~
/usr/include/c++/15/bits/ostream.h:734:5: note: template argument deduction/substitution failed:
test_concepts_old.cpp:13:16: note:   cannot convert ‘z’ (type ‘std::vector<int>’) to type ‘const char*’
   13 |   std::cout << z << std::endl;
      |                ^
/usr/include/c++/15/bits/ostream.h:747:5: note: candidate 28: ‘template<class _Traits> std::basic_ostream<char, _Traits>& std::operator<<(basic_ostream<char, _Traits>&, const signed char*)’
  747 |     operator<<(basic_ostream<char, _Traits>& __out, const signed char* __s)
      |     ^~~~~~~~
/usr/include/c++/15/bits/ostream.h:747:5: note: template argument deduction/substitution failed:
test_concepts_old.cpp:13:16: note:   cannot convert ‘z’ (type ‘std::vector<int>’) to type ‘const signed char*’
   13 |   std::cout << z << std::endl;
      |                ^
/usr/include/c++/15/bits/ostream.h:752:5: note: candidate 29: ‘template<class _Traits> std::basic_ostream<char, _Traits>& std::operator<<(basic_ostream<char, _Traits>&, const unsigned char*)’
  752 |     operator<<(basic_ostream<char, _Traits>& __out, const unsigned char* __s)
      |     ^~~~~~~~
/usr/include/c++/15/bits/ostream.h:752:5: note: template argument deduction/substitution failed:
test_concepts_old.cpp:13:16: note:   cannot convert ‘z’ (type ‘std::vector<int>’) to type ‘const unsigned char*’
   13 |   std::cout << z << std::endl;
      |                ^
/usr/include/c++/15/bits/ostream.h:836:5: note: candidate 30: ‘template<class _Ostream, class _Tp> _Ostream&& std::operator<<(_Ostream&&, const _Tp&)’
  836 |     operator<<(_Ostream&& __os, const _Tp& __x)
      |     ^~~~~~~~
/usr/include/c++/15/bits/ostream.h:836:5: note: template argument deduction/substitution failed:
/usr/include/c++/15/bits/ostream.h: In substitution of ‘template<class _Ostream, class _Tp> _Ostream&& std::operator<<(_Ostream&&, const _Tp&) [with _Ostream = std::basic_ostream<char>&; _Tp = std::vector<int>]’:
test_concepts_old.cpp:13:16:   required from here
   13 |   std::cout << z << std::endl;
      |                ^
/usr/include/c++/15/bits/ostream.h:836:5: error: no type named ‘type’ in ‘struct std::enable_if<false, void>’
  836 |     operator<<(_Ostream&& __os, const _Tp& __x)
      |     ^~~~~~~~
test_concepts_old.cpp: In instantiation of ‘T add(T, T) [with T = std::vector<int>]’:
test_concepts_old.cpp:12:15:   required from here
   12 |   auto z = add(x, y);
      |            ~~~^~~~~~
test_concepts_old.cpp:6:14: error: no match for ‘operator+’ (operand types are ‘std::vector<int>’ and ‘std::vector<int>’)
    6 |     return a + b;
      |            ~~^~~
test_concepts_old.cpp:6:14: note: there are 14 candidates
In file included from /usr/include/c++/15/bits/stl_algobase.h:67,
                 from /usr/include/c++/15/vector:64,
                 from test_concepts_old.cpp:1:
/usr/include/c++/15/bits/stl_iterator.h:629:5: note: candidate 1: ‘template<class _Iterator> std::reverse_iterator<_Iterator> std::operator+(typename reverse_iterator<_Iterator>::difference_type, const reverse_iterator<_Iterator>&)’
  629 |     operator+(typename reverse_iterator<_Iterator>::difference_type __n,
      |     ^~~~~~~~
/usr/include/c++/15/bits/stl_iterator.h:629:5: note: template argument deduction/substitution failed:
test_concepts_old.cpp:6:14: note:   ‘std::vector<int>’ is not derived from ‘const std::reverse_iterator<_Iterator>’
    6 |     return a + b;
      |            ~~^~~
/usr/include/c++/15/bits/stl_iterator.h:1793:5: note: candidate 2: ‘template<class _Iterator> std::move_iterator<_IteratorL> std::operator+(typename move_iterator<_IteratorL>::difference_type, const move_iterator<_IteratorL>&)’
 1793 |     operator+(typename move_iterator<_Iterator>::difference_type __n,
      |     ^~~~~~~~
/usr/include/c++/15/bits/stl_iterator.h:1793:5: note: template argument deduction/substitution failed:
test_concepts_old.cpp:6:14: note:   ‘std::vector<int>’ is not derived from ‘const std::move_iterator<_IteratorL>’
    6 |     return a + b;
      |            ~~^~~
/usr/include/c++/15/bits/basic_string.h:3840:5: note: candidate 3: ‘template<class _CharT, class _Traits, class _Alloc> std::__cxx11::basic_string<_CharT, _Traits, _Alloc> std::operator+(const __cxx11::basic_string<_CharT, _Traits, _Alloc>&, const __cxx11::basic_string<_CharT, _Traits, _Alloc>&)’
 3840 |     operator+(const basic_string<_CharT, _Traits, _Alloc>& __lhs,
      |     ^~~~~~~~
/usr/include/c++/15/bits/basic_string.h:3840:5: note: template argument deduction/substitution failed:
test_concepts_old.cpp:6:14: note:   ‘std::vector<int>’ is not derived from ‘const std::__cxx11::basic_string<_CharT, _Traits, _Alloc>’
    6 |     return a + b;
      |            ~~^~~
/usr/include/c++/15/bits/basic_string.h:3858:5: note: candidate 4: ‘template<class _CharT, class _Traits, class _Alloc> std::__cxx11::basic_string<_CharT, _Traits, _Alloc> std::operator+(const _CharT*, const __cxx11::basic_string<_CharT, _Traits, _Alloc>&)’
 3858 |     operator+(const _CharT* __lhs,
      |     ^~~~~~~~
/usr/include/c++/15/bits/basic_string.h:3858:5: note: template argument deduction/substitution failed:
test_concepts_old.cpp:6:14: note:   mismatched types ‘const _CharT*’ and ‘std::vector<int>’
    6 |     return a + b;
      |            ~~^~~
/usr/include/c++/15/bits/basic_string.h:3877:5: note: candidate 5: ‘template<class _CharT, class _Traits, class _Alloc> std::__cxx11::basic_string<_CharT, _Traits, _Alloc> std::operator+(_CharT, const __cxx11::basic_string<_CharT, _Traits, _Alloc>&)’
 3877 |     operator+(_CharT __lhs, const basic_string<_CharT,_Traits,_Alloc>& __rhs)
      |     ^~~~~~~~
/usr/include/c++/15/bits/basic_string.h:3877:5: note: template argument deduction/substitution failed:
test_concepts_old.cpp:6:14: note:   ‘std::vector<int>’ is not derived from ‘const std::__cxx11::basic_string<_CharT, _Traits, _Alloc>’
    6 |     return a + b;
      |            ~~^~~
/usr/include/c++/15/bits/basic_string.h:3894:5: note: candidate 6: ‘template<class _CharT, class _Traits, class _Alloc> std::__cxx11::basic_string<_CharT, _Traits, _Alloc> std::operator+(const __cxx11::basic_string<_CharT, _Traits, _Alloc>&, const _CharT*)’
 3894 |     operator+(const basic_string<_CharT, _Traits, _Alloc>& __lhs,
      |     ^~~~~~~~
/usr/include/c++/15/bits/basic_string.h:3894:5: note: template argument deduction/substitution failed:
test_concepts_old.cpp:6:14: note:   ‘std::vector<int>’ is not derived from ‘const std::__cxx11::basic_string<_CharT, _Traits, _Alloc>’
    6 |     return a + b;
      |            ~~^~~
/usr/include/c++/15/bits/basic_string.h:3912:5: note: candidate 7: ‘template<class _CharT, class _Traits, class _Alloc> std::__cxx11::basic_string<_CharT, _Traits, _Alloc> std::operator+(const __cxx11::basic_string<_CharT, _Traits, _Alloc>&, _CharT)’
 3912 |     operator+(const basic_string<_CharT, _Traits, _Alloc>& __lhs, _CharT __rhs)
      |     ^~~~~~~~
/usr/include/c++/15/bits/basic_string.h:3912:5: note: template argument deduction/substitution failed:
test_concepts_old.cpp:6:14: note:   ‘std::vector<int>’ is not derived from ‘const std::__cxx11::basic_string<_CharT, _Traits, _Alloc>’
    6 |     return a + b;
      |            ~~^~~
/usr/include/c++/15/bits/basic_string.h:3924:5: note: candidate 8: ‘template<class _CharT, class _Traits, class _Alloc> std::__cxx11::basic_string<_CharT, _Traits, _Alloc> std::operator+(__cxx11::basic_string<_CharT, _Traits, _Alloc>&&, const __cxx11::basic_string<_CharT, _Traits, _Alloc>&)’
 3924 |     operator+(basic_string<_CharT, _Traits, _Alloc>&& __lhs,
      |     ^~~~~~~~
/usr/include/c++/15/bits/basic_string.h:3924:5: note: template argument deduction/substitution failed:
test_concepts_old.cpp:6:14: note:   ‘std::vector<int>’ is not derived from ‘std::__cxx11::basic_string<_CharT, _Traits, _Alloc>’
    6 |     return a + b;
      |            ~~^~~
/usr/include/c++/15/bits/basic_string.h:3931:5: note: candidate 9: ‘template<class _CharT, class _Traits, class _Alloc> std::__cxx11::basic_string<_CharT, _Traits, _Alloc> std::operator+(const __cxx11::basic_string<_CharT, _Traits, _Alloc>&, __cxx11::basic_string<_CharT, _Traits, _Alloc>&&)’
 3931 |     operator+(const basic_string<_CharT, _Traits, _Alloc>& __lhs,
      |     ^~~~~~~~
/usr/include/c++/15/bits/basic_string.h:3931:5: note: template argument deduction/substitution failed:
test_concepts_old.cpp:6:14: note:   ‘std::vector<int>’ is not derived from ‘const std::__cxx11::basic_string<_CharT, _Traits, _Alloc>’
    6 |     return a + b;
      |            ~~^~~
/usr/include/c++/15/bits/basic_string.h:3938:5: note: candidate 10: ‘template<class _CharT, class _Traits, class _Alloc> std::__cxx11::basic_string<_CharT, _Traits, _Alloc> std::operator+(__cxx11::basic_string<_CharT, _Traits, _Alloc>&&, __cxx11::basic_string<_CharT, _Traits, _Alloc>&&)’
 3938 |     operator+(basic_string<_CharT, _Traits, _Alloc>&& __lhs,
      |     ^~~~~~~~
/usr/include/c++/15/bits/basic_string.h:3938:5: note: template argument deduction/substitution failed:
test_concepts_old.cpp:6:14: note:   ‘std::vector<int>’ is not derived from ‘std::__cxx11::basic_string<_CharT, _Traits, _Alloc>’
    6 |     return a + b;
      |            ~~^~~
/usr/include/c++/15/bits/basic_string.h:3961:5: note: candidate 11: ‘template<class _CharT, class _Traits, class _Alloc> std::__cxx11::basic_string<_CharT, _Traits, _Alloc> std::operator+(const _CharT*, __cxx11::basic_string<_CharT, _Traits, _Alloc>&&)’
 3961 |     operator+(const _CharT* __lhs,
      |     ^~~~~~~~
/usr/include/c++/15/bits/basic_string.h:3961:5: note: template argument deduction/substitution failed:
test_concepts_old.cpp:6:14: note:   mismatched types ‘const _CharT*’ and ‘std::vector<int>’
    6 |     return a + b;
      |            ~~^~~
/usr/include/c++/15/bits/basic_string.h:3968:5: note: candidate 12: ‘template<class _CharT, class _Traits, class _Alloc> std::__cxx11::basic_string<_CharT, _Traits, _Alloc> std::operator+(_CharT, __cxx11::basic_string<_CharT, _Traits, _Alloc>&&)’
 3968 |     operator+(_CharT __lhs,
      |     ^~~~~~~~
/usr/include/c++/15/bits/basic_string.h:3968:5: note: template argument deduction/substitution failed:
test_concepts_old.cpp:6:14: note:   ‘std::vector<int>’ is not derived from ‘std::__cxx11::basic_string<_CharT, _Traits, _Alloc>’
    6 |     return a + b;
      |            ~~^~~
/usr/include/c++/15/bits/basic_string.h:3975:5: note: candidate 13: ‘template<class _CharT, class _Traits, class _Alloc> std::__cxx11::basic_string<_CharT, _Traits, _Alloc> std::operator+(__cxx11::basic_string<_CharT, _Traits, _Alloc>&&, const _CharT*)’
 3975 |     operator+(basic_string<_CharT, _Traits, _Alloc>&& __lhs,
      |     ^~~~~~~~
/usr/include/c++/15/bits/basic_string.h:3975:5: note: template argument deduction/substitution failed:
test_concepts_old.cpp:6:14: note:   ‘std::vector<int>’ is not derived from ‘std::__cxx11::basic_string<_CharT, _Traits, _Alloc>’
    6 |     return a + b;
      |            ~~^~~
/usr/include/c++/15/bits/basic_string.h:3982:5: note: candidate 14: ‘template<class _CharT, class _Traits, class _Alloc> std::__cxx11::basic_string<_CharT, _Traits, _Alloc> std::operator+(__cxx11::basic_string<_CharT, _Traits, _Alloc>&&, _CharT)’
 3982 |     operator+(basic_string<_CharT, _Traits, _Alloc>&& __lhs,
      |     ^~~~~~~~
/usr/include/c++/15/bits/basic_string.h:3982:5: note: template argument deduction/substitution failed:
test_concepts_old.cpp:6:14: note:   ‘std::vector<int>’ is not derived from ‘std::__cxx11::basic_string<_CharT, _Traits, _Alloc>’
    6 |     return a + b;
      |            ~~^~~
```

How did we improve? \`std::enable\_if\`

```c
#include <vector>
#include <iostream>

template <typename T,
          typename = typename std::enable_if<std::is_arithmetic<T>::value>::type>
T add(T a, T b) {
    return a + b;
}

int main() {
  std::vector<int> x = {4, 5, 6};
  std::vector<int> y = {1, 2, 3};
  auto z = add(x, y);
  std::cout << z << std::endl;
}
```

Hard to read, hard to write, and even harder to debug. Error message:

```shell
arghyabh@arghya:~$ g++ -std=c++11 test_concepts_old.cpp -o a.out
test_concepts_old.cpp: In function ‘int main()’:
test_concepts_old.cpp:13:15: error: no matching function for call to ‘add(std::vector<int>&, std::vector<int>&)’
   13 |   auto z = add(x, y);
      |            ~~~^~~~~~
test_concepts_old.cpp:13:15: note: there is 1 candidate
test_concepts_old.cpp:6:3: note: candidate 1: ‘template<class T, class> T add(T, T)’
    6 | T add(T a, T b) {
      |   ^~~
test_concepts_old.cpp:6:3: note: template argument deduction/substitution failed:
test_concepts_old.cpp:5:11: error: no type named ‘type’ in ‘struct std::enable_if<false, void>’
    5 |           typename = typename std::enable_if<std::is_arithmetic<T>::value>::type>
      |           ^~~~~~~~
```

## Post-C++20 way

```c
#include <vector>
#include <iostream>
#include <concepts>

template <typename T>
concept Addable = requires(T a, T b) {
    { a + b } -> std::convertible_to<T>; // It must support + and return T
};

template <Addable T>
T add(T a, T b) {
    return a + b;
}

// shorter and elegant
auto add(Addable auto a, Addable auto b) {
    return a + b;
}

int main() {
  std::vector<int> x = {4, 5, 6};
  std::vector<int> y = {1, 2, 3};
  auto z = add(x, y);
  std::cout << z << std::endl;
}
```

Error message:

```shell
arghyabh@arghya:~$ g++ -std=c++20 test_concepts.cpp -o a.out
test_concepts.cpp: In function ‘int main()’:
test_concepts.cpp:18:15: error: no matching function for call to ‘add(std::vector<int>&, std::vector<int>&)’
   18 |   auto z = add(x, y);
      |            ~~~^~~~~~
test_concepts.cpp:18:15: note: there is 1 candidate
test_concepts.cpp:11:3: note: candidate 1: ‘template<class T>  requires  Addable<T> T add(T, T)’
   11 | T add(T a, T b) {
      |   ^~~
test_concepts.cpp:11:3: note: template argument deduction/substitution failed:
test_concepts.cpp:11:3: note: constraints not satisfied
test_concepts.cpp: In substitution of ‘template<class T>  requires  Addable<T> T add(T, T) [with T = std::vector<int>]’:
test_concepts.cpp:18:15:   required from here
   18 |   auto z = add(x, y);
      |            ~~~^~~~~~
test_concepts.cpp:6:9:   required for the satisfaction of ‘Addable<T>’ [with T = std::vector<int, std::allocator<int> >]
test_concepts.cpp:6:19:   in requirements with ‘T a’, ‘T b’ [with T = std::vector<int, std::allocator<int> >]
test_concepts.cpp:7:9: note: the required expression ‘(a + b)’ is invalid
    7 |     { a + b } -> std::convertible_to<T>; // It must support + and return T
      |       ~~^~~
cc1plus: note: set ‘-fconcepts-diagnostics-depth=’ to at least 2 for more detail
```

## Advantage: avoid tag dispatching and allow overloading

```c
// Tag Dispatching
// You had to write a helper function
template <typename Iterator>
void process_impl(Iterator it, std::random_access_iterator_tag) {
    std::cout << "Fast version";
}

template <typename Iterator>
void process_impl(Iterator it, std::input_iterator_tag) {
    std::cout << "Slow version";
}

// And then a wrapper to "extract" the tag
template <typename Iterator>
void process(Iterator it) {
    process_impl(it, typename std::iterator_traits<Iterator>::iterator_category());
}

```

```c
template <typename T>
typename std::enable_if<std::is_same<decltype(std::declval<T>().size()), size_t>::value>::type
print_size(T const& container) {
    std::cout << container.size() << std::endl;
}

```

As we call \`process(v.begin())\`, the compiler picks the most specific match.  
The double \`requires requires\` looks weird, but it simply means: "This function requires that the type T satisfies the requirement of having a \`.size()\` method."

```c
#include <iostream>
#include <concepts>
#include <vector>
#include <list>

// Advantage 1: Ad-hoc Constraints
template <typename T>
void print_size(T const& container)
    requires requires(T t) { t.size(); } // Check if .size() exists
{
    std::cout << container.size() << std::endl;
}

// Advantage 2: Concept-based Overloading
// Fast version for vectors (Random Access)
void process(std::random_access_iterator auto it) {
    std::cout << "Using fast jump-to-index processing" << std::endl;
}

// Slower version for lists (Step-by-step)
void process(std::input_iterator auto it) {
    std::cout << "Using step-by-step processing" << std::endl;
}

int main() {
    std::vector<int> v = {1, 2, 3};
    std::list<int> l = {1, 2, 3};

    process(v.begin()); // Calls the Random Access version
    process(l.begin()); // Calls the Input Iterator version
}

```

In our main() function, when we pass \`v.begin() (Vector)\` and \`l.begin() (List)\`, the compiler generates two different versions of the code at compile-time. There is zero performance hit at runtime.

Before C++20, you might pass a std::list to a function that needs to jump to the middle of a collection. The code would compile, but it would be extremely slow because std::list has to step through every element.

With Concepts, you can force the user to provide a container that supports "Random Access" (like std::vector or an array). Otherwise, we do not want the code to compile.

```c
#include <iterator>
#include <vector>
#include <list>

// This function REFUSES to compile if the container is slow (like a list)
// std::random_access_iterator is the concept
void fast_process(std::random_access_iterator auto it) {
    auto middle = it + 10; // This is only O(1) for random access!
}

int main() {
    std::vector<int> v(100);
    std::list<int> l(100);

    fast_process(v.begin()); // OK: Vector is fast
    // fast_process(l.begin()); // ERROR: List is slow. Compiler catches this logic fail!
}

```

## Advantage: Static Polymorphism

**Pre-C++20 way: Dynamic Polymorphism / Inheritance**

```c
#include <iostream>

// The Interface (Base Class)
class Shape {
public:
    virtual void draw() = 0;           // Pure virtual
    virtual double area() = 0;         // Pure virtual
    virtual ~Shape() {}                // Necessary for cleanup
};

struct Circle : public Shape {         // Explicitly "is-a" Shape
    double radius;
    void draw() override { std::cout << "Drawing Circle\n"; }
    double area() override { return 3.14 * radius * radius; }
};

// The function now takes a Pointer or Reference
void render(Shape& s) {
    s.draw();
    std::cout << "Area: " << s.area() << "\n";
}
```

This has a performance cost.

1. When we use virtual functions, the compiler doesn't know which draw() to call at compile-time. It has to wait until the program is running to see if the object is a Circle or a Square.  
2. The vtable (Virtual Method Table): Every class with virtual functions has a hidden table created by the compiler. It’s basically a list of memory addresses for its functions.  
3. The vptr (Virtual Pointer): Every object (such as, Circle) gets a hidden pointer that points to that table.  
4. The Lookup: As we call s.draw(), the CPU has to:  
   1. Follow the vptr to find the vtable.  
   2. Look up the address for draw() in that table.  
   3. Jump to that address.

**Post-C++20 way:** 

```c
#include <concepts>
#include <iostream>

// 1. Define the "Interface" via a Concept
template <typename T>
concept Shape = requires(T s) {
    { s.draw() } -> std::same_as<void>;
    { s.area() } -> std::convertible_to<double>;
};

// 2. Create unrelated structs (No "public Shape" inheritance needed!)
struct Circle {
    double radius;
    void draw() { std::cout << "Drawing Circle\n"; }
    double area() { return 3.14 * radius * radius; }
};

struct Square {
    double side;
    void draw() { std::cout << "Drawing Square\n"; }
    double area() { return side * side; }
};

// 3. A generic function that works with ANY Shape
void render(Shape auto s) {
    s.draw();
    std::cout << "Area: " << s.area() << "\n";
}

int main() {
    render(Circle{5.0}); // Works!
    render(Square{4.0}); // Works!
}
```

