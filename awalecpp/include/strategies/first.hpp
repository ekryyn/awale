#ifndef FIRST_HPP
#define FIRST_HPP


#include "../game.hpp"
#include <random>

namespace strategies{


struct first{

    first(const boost::program_options::variables_map& options) {}

    size_t choose_move(const game& game_state){


        return 0;

    }




};

} // ns strategies

#endif // FIRST_HPP
