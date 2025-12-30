#include "perception_pipeline.hpp"
#include <iostream>

void PerceptionPipeline::process(const ImageFrame& frame) {
    std::cout << "Processing frame at timestamp\n";
    // Later: detection, tracking, etc.
}
