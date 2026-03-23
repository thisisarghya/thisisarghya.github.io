# \<ranges\> in C++20

## \<ranges\> is a new library extension introduced in C++20 that abstracts away from explicit begin/end iterator pairs, allowing algorithms to operate directly on whole containers with a functional-style programming through lazy-evaluated views.

Date: Aug 15, 2025

**Let’s understand with an example.**  
Use case: Given an array of integers, filter even numbers, square them, and print the first three results.

## The pre-cpp20 way

```c
#include <vector>
#include <algorithm>
#include <iostream>

int main() {
    std::vector<int> numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    
    // 1. Filter even numbers into a temporary vector
    std::vector<int> evens;
    for (int n : numbers) {
        if (n % 2 == 0) evens.push_back(n);
    }

    // 2. Square them
    std::vector<int> squared;
    for (int n : evens) {
        squared.push_back(n * n);
    }

    // 3. Take the first three and print
    for (int i = 0; i < 3 && i < squared.size(); ++i) {
        std::cout << squared[i] << " ";
    }
}
```

Quick compiler check

```shell
### For Mac
arghyabh-mac:~ arghyabh$ clang++ --version
Apple clang version 17.0.0 (clang-1700.6.4.2)
Target: arm64-apple-darwin25.3.0
Thread model: posix
InstalledDir: /Library/Developer/CommandLineTools/usr/bin

### For Linux
arghyabh@arghya:~$ g++ --version
g++ (Debian 15.2.0-4) 15.2.0
Copyright (C) 2025 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

```

Apple clang version 13.0.0 or higher indicates C++20 support. Almost every version since 2012 has C++11 support. GCC 10 or higher is needed for C++20 ranges. Use GCC 13 or 14 for best experience (standard on modern Ubuntu 24.04+).

How to compile?

```shell
clang++ -std=c++11 test_ranges_old.cpp -o test_ranges_old  ## For Mac
g++ -std=c++11 test_ranges_old.cpp -o test_ranges_old  ## For linux
```

## The post-cpp20 way

```c
#include <vector>
#include <iostream>
#include <ranges> // New in C++20

int main() {
    std::vector<int> numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

    // Use the pipe operator | to chain operations
    auto result = numbers 
                | std::views::filter([](int n) { return n % 2 == 0; })
                | std::views::transform([](int n) { return n * n; })
                | std::views::take(3);

    for (int n : result) {
        std::cout << n << " "; // Output: 4 16 36
    }
}
```

How to compile?

```shell
clang++ -std=c++11 test_ranges.cpp -o test_ranges  ## For Mac
g++ -std=c++20 test_ranges.cpp -o test_ranges  ## For linux
```

## Advantages

1. The trivial one: cleaner and more readable code.  
2. Iterators not needed anymore: the whole container numbers is passed, not numbers.begin(), numbers.end()  
3. Lazy Evaluation: The squaring and filtering only happen when you iterate through the result variable. If you never use the result variable, the computer does zero work.  
4. Temporary vectors are not created.

Ranges also provide **some algorithm functionalities** where we will not need to pass the iterators but just pass the whole container.

1. std::sort(v.begin(), v.end()) \-\> std::ranges::sort(v)  
2. std::find(v.begin(), v.end(), q) \-\> std::ranges::find(v, q)  
3. std::binary\_search(v.begin(), v.end(), q) \-\> std::ranges::binary\_search(v, q)  
4. std::reverse(v.begin(), v.end()) \-\> std::ranges::reverse(v)

