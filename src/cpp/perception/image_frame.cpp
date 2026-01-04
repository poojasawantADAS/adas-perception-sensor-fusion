#include "image_frame.hpp"

ImageFrame::ImageFrame(TimePoint timestamp)
    : timestamp_(timestamp)
{
}

ImageFrame::TimePoint ImageFrame::timestamp() const
{
    return timestamp_;
}
