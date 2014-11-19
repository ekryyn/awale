#ifndef UTILS_HPP
#define UTILS_HPP

#include <iostream>
#include <string>


#include <sstream>
#include <vector>
#include <iterator>

//put line into vector of ints
std::vector<int> read_int_line(const std::string& line){

    std::vector<int>   line_data;
    std::stringstream  line_stream(line);

    int value;
    // Read an integer at a time from the line
    while(line_stream >> value)
    {
        // Add the integers from a line to a 1D array (vector)
        line_data.push_back(value);
    }

    return line_data;

}




#endif // UTILS_HPP
