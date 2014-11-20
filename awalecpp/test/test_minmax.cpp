#define BOOST_TEST_MODULE test_minmax

#include <boost/test/unit_test.hpp>
#include <boost/test/test_tools.hpp>

#include "game.hpp"
#include "basic_minmax.hpp"
#include <sstream>



double heuristic(const game& game_state, const int& player_id){

    return (player_id == 0 ? 1 : -1 ) * (game_state.scores[0] - game_state.scores[1]);
}



BOOST_AUTO_TEST_CASE(test_constructor)
{


    std::stringstream s("1 2 0 1\n5 1\n0\n0 1\n");


    game game_state(s);



    int depth = 10;
    basic_minmax<game, decltype(heuristic)> strat(game_state, heuristic, depth);

    auto move_values = strat.compute_move_values();

    std::cout <<game_state << std::endl;

    for (int i = 0; i< move_values.size(); i++) {
        std::cout <<game_state.valid_moves[i] << "  " << move_values[i] <<std::endl;
    }

    BOOST_CHECK_EQUAL(move_values.size(), game_state.valid_moves.size());


}
