#define BOOST_TEST_MODULE test_minmax

#include <boost/test/unit_test.hpp>
#include <boost/test/test_tools.hpp>

#include "game.hpp"
#include "basic_minmax.hpp"
#include <sstream>



double heuristic(const game& game_state){

    return (game_state.next_player == 0 ? 1 : -1 ) * (game_state.scores[0] - game_state.scores[1]);
}



BOOST_AUTO_TEST_CASE(test_constructor)
{


    //std::stringstream s("1 2 0 1\n5 1\n0\n0 1\n");

	std::stringstream s("0 2 0 1\n5 1\n0\n1\n");

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


BOOST_AUTO_TEST_CASE(test_constructor1)
{


    //std::stringstream s("1 2 0 1\n5 1\n0\n0 1\n");

	std::stringstream s("1 1 0 1\n5 1\n0\n0 1\n");

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


BOOST_AUTO_TEST_CASE(test_constructor2)
{


    //std::stringstream s("1 2 0 1\n5 1\n0\n0 1\n");

	//std::stringstream s("4 4 4 4 4 4 4 4 4 4 4 4\n0 0\n0\n0 1 2 3 4 5\n");
    std::stringstream s("0 0 2 2 2 2 2 2 2 2 2 2\n0 0\n0\n2 3 4 5\n");

    game game_state(s);



    for (int depth = 1;depth <8;depth++){
		std::cout << "depth " << depth << std::endl;
		basic_minmax<game, decltype(heuristic)> strat(game_state, heuristic, depth);

		auto move_values = strat.compute_move_values();

		std::cout <<game_state << std::endl;

		for (int i = 0; i< move_values.size(); i++) {
			std::cout <<game_state.valid_moves[i] << "  " << move_values[i] <<std::endl;
		}

		BOOST_CHECK_EQUAL(move_values.size(), game_state.valid_moves.size());
    }
}

BOOST_AUTO_TEST_CASE(test_constructor3)
{


    //std::stringstream s("1 2 0 1\n5 1\n0\n0 1\n");

	//std::stringstream s("4 4 4 4 4 4 4 4 4 4 4 4\n0 0\n0\n0 1 2 3 4 5\n");
    std::stringstream s("0 0 2 2 2 2 2 2 2 2 2 2\n0 0\n1\n6 7 8 9 10 11\n");

    game game_state(s);



    for (int depth = 1;depth <8;depth++){
		std::cout << "depth " << depth << std::endl;
		basic_minmax<game, decltype(heuristic)> strat(game_state, heuristic, depth);

		auto move_values = strat.compute_move_values();

		std::cout <<game_state << std::endl;

		for (int i = 0; i< move_values.size(); i++) {
			std::cout <<game_state.valid_moves[i] << "  " << move_values[i] <<std::endl;
		}

		BOOST_CHECK_EQUAL(move_values.size(), game_state.valid_moves.size());
	}	

}

