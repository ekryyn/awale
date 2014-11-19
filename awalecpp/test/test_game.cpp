#define BOOST_TEST_MODULE test_game

#include <boost/test/unit_test.hpp>
#include <boost/test/test_tools.hpp>

#include "game.hpp"
#include <sstream>

BOOST_AUTO_TEST_CASE(test_constructor)
{

    std::stringstream s("1 2 3 4\n1 2\n0\n0 1\n");


    game game_state(s);


    BOOST_CHECK_EQUAL(game_state.size_, 2);

    BOOST_CHECK_EQUAL(game_state.tab.size(), 4);
    BOOST_CHECK_EQUAL(game_state.tab[0], 1);
    BOOST_CHECK_EQUAL(game_state.tab[1], 2);
    BOOST_CHECK_EQUAL(game_state.tab[2], 3);
    BOOST_CHECK_EQUAL(game_state.tab[3], 4);

    BOOST_CHECK_EQUAL(game_state.valid_moves.size(), 2);
    BOOST_CHECK_EQUAL(game_state.valid_moves[0], 0);
    BOOST_CHECK_EQUAL(game_state.valid_moves[1], 1);

    BOOST_CHECK_EQUAL(game_state.scores.size(), 2);
    BOOST_CHECK_EQUAL(game_state.scores[0], 1);
    BOOST_CHECK_EQUAL(game_state.scores[1], 2);

    BOOST_CHECK_EQUAL(game_state.next_player, 0);

}


BOOST_AUTO_TEST_CASE(test_game_play)
{

    std::stringstream s("1 2 3 1\n1 2\n0\n0 1\n");


    game game_state(s);

    std::cout <<game_state <<std::endl;

    game_state.play(1);
    game_state.update_after_play();
    std::cout <<game_state <<std::endl;

    //new tab should be "1 0 4 0\n3 2\n1\n0\n"

    BOOST_CHECK_EQUAL(game_state.size_, 2);

    BOOST_CHECK_EQUAL(game_state.tab.size(), 4);
    BOOST_CHECK_EQUAL(game_state.tab[0], 1);
    BOOST_CHECK_EQUAL(game_state.tab[1], 0);
    BOOST_CHECK_EQUAL(game_state.tab[2], 4);
    BOOST_CHECK_EQUAL(game_state.tab[3], 0);


    BOOST_CHECK_EQUAL(game_state.scores.size(), 2);
    BOOST_CHECK_EQUAL(game_state.scores[0], 3);
    BOOST_CHECK_EQUAL(game_state.scores[1], 2);


    BOOST_CHECK_EQUAL(game_state.valid_moves.size(), 1);
    BOOST_CHECK_EQUAL(game_state.valid_moves[0], 0);



    BOOST_CHECK_EQUAL(game_state.next_player, 1);


}
