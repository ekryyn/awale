#ifndef RANDOM_STRATEGY_HPP
#define RANDOM_STRATEGY_HPP


#include "../game.hpp"
#include <random>

namespace strategies{


struct random_strategy{


    typedef std::minstd_rand RnG;

    random_strategy(const boost::program_options::variables_map& options) {}




    RnG g;


    size_t choose_move(const game& game_state){


        size_t n_valid_moves = game_state.valid_moves.size();


        typedef std::uniform_int_distribution<> D;
        D d(0, n_valid_moves - 1);

        return(d(g));

    }




};

} // ns strategies

#endif // RANDOM_STRATEGY_HPP
