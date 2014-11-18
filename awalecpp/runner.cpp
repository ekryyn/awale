#include <iostream>
#include <string>


#include <sstream>
#include <vector>
#include <iterator>

#include "utils.hpp"
#include "game.hpp"
#include "random_strategy.hpp"


int main(){


    random_strategy strategy;
    while(true) {

        game game_state(std::cin);

        //pick best move

        size_t best_move = strategy.choose_move(game_state);


        //return best move

        //send move
        std::cout << game_state.valid_moves[best_move] << std::endl;

    }

    return 0;
}
