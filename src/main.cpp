#include "image_frame.hpp"
#include <iostream>

int main() {
    ImageFrame frame(640, 480, 0.016);
    std::cout << frame.getInfo() << std::endl;
    return 0;
}
