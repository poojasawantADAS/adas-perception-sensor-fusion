#pragma once

#include "image_frame.hpp"

class PerceptionPipeline {
public:
    void process(const ImageFrame& frame);
};
