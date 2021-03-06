#include <iostream>
#include <string>


#include <sstream>
#include <vector>
#include <iterator>

#include "process_args.hpp"
#include "utils.hpp"
#include "game.hpp"
#include "strategies/random_strategy.hpp"
#include "strategies/first.hpp"

template<typename Strategy>
void run_bot(const boost::program_options::variables_map& options, std::istream& infile = std::cin, std::ostream& outfile = std::cout)
{

    Strategy strategy(options);

    while(true) {

        game game_state(infile);

        //pick best move

        size_t best_move = strategy.choose_move(game_state);


        //send best move

        outfile << game_state.valid_moves[best_move] << std::endl;

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
