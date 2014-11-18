#ifndef RANDOM_STRATEGY_HPP
#define RANDOM_STRATEGY_HPP


#include "game.hpp"
#include <random>

struct random_strategy{


    typedef std::minstd_rand G;

    G g;


    size_t choose_move(const game& game_state){


        size_t n_valid_moves = game_state.valid_moves.size();


        typedef std::uniform_int_distribution<> D;
        D d(0, n_valid_moves - 1);

        return(d(g));

    }




};



#endif // RANDOM_STRATEGY_HPP
