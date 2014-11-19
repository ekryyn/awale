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


}
