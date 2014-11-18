#include <iostream>
#include <string>


#include <sstream>
#include <vector>
#include <iterator>

#include "include/process_args.hpp"
#include "include/utils.hpp"
#include "include/game.hpp"
#include "include/strategies/random_strategy.hpp"
#include "include/strategies/first.hpp"

template<typename Strategy>
void run_bot(const boost::program_options::variables_map& options)
{

    Strategy strategy(options);

    while(true) {

        game game_state(std::cin);

        //pick best move

        size_t best_move = strategy.choose_move(game_state);


        //send best move

        std::cout << game_state.valid_moves[best_move] << std::endl;

    }


    return;

}

int main(int argc, char** argv)
{
    auto options = process_arguments(argc, argv);
    const std::string strategy = options["strategy"].as<std::string>();

    if (strategy == "random")
    {
        run_bot<strategies::random_strategy>(options);
    }
    else if (strategy == "first")
    {
        run_bot<strategies::first>(options);
    }

    return 0;
}
