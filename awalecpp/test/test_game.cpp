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

    std::cout <<"lala" <<std::endl;

    game_state.play(1);
    std::cout <<game_state <<std::endl;
    std::cout <<"lala" <<std::endl;

    game_state.update_after_play();
    std::cout <<game_state <<std::endl;
    std::cout <<"lala" <<std::endl;

    std::cout << std::endl <<game_state.valid_moves.size() << std::endl;
     std::cout <<std::endl;
    std::cout <<game_state <<std::endl;
 std::cout <<std::endl;
    //new tab should be "1 0 4 0\n3 2\n1\n2\n"

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
    BOOST_CHECK_EQUAL(game_state.valid_moves[0], 2);



    BOOST_CHECK_EQUAL(game_state.next_player, 1);


    std::cout << std::endl <<game_state.valid_moves.size() << std::endl;
    game_state.play(0);
    game_state.update_after_play();
    std::cout <<game_state <<std::endl;

    //new tab should be "2 1 0 2\n3 2\n0\n0 1\n"

    BOOST_CHECK_EQUAL(game_state.size_, 2);

    BOOST_CHECK_EQUAL(game_state.tab.size(), 4);
    BOOST_CHECK_EQUAL(game_state.tab[0], 2);
    BOOST_CHECK_EQUAL(game_state.tab[1], 1);
    BOOST_CHECK_EQUAL(game_state.tab[2], 0);
    BOOST_CHECK_EQUAL(game_state.tab[3], 2);


    BOOST_CHECK_EQUAL(game_state.scores.size(), 2);
    BOOST_CHECK_EQUAL(game_state.scores[0], 3);
    BOOST_CHECK_EQUAL(game_state.scores[1], 2);


    BOOST_CHECK_EQUAL(game_state.valid_moves.size(), 2);
    BOOST_CHECK_EQUAL(game_state.valid_moves[0], 0);
    BOOST_CHECK_EQUAL(game_state.valid_moves[1], 1);



    BOOST_CHECK_EQUAL(game_state.next_player, 0);

    game_state.play(0);
    game_state.update_after_play();
    std::cout <<game_state <<std::endl;

    //new tab should be "0 2 1 2\n3 2\n1\n2 3\n"

    BOOST_CHECK_EQUAL(game_state.size_, 2);

    BOOST_CHECK_EQUAL(game_state.tab.size(), 4);
    BOOST_CHECK_EQUAL(game_state.tab[0], 0);
    BOOST_CHECK_EQUAL(game_state.tab[1], 2);
    BOOST_CHECK_EQUAL(game_state.tab[2], 1);
    BOOST_CHECK_EQUAL(game_state.tab[3], 2);


    BOOST_CHECK_EQUAL(game_state.scores.size(), 2);
    BOOST_CHECK_EQUAL(game_state.scores[0], 3);
    BOOST_CHECK_EQUAL(game_state.scores[1], 2);


    BOOST_CHECK_EQUAL(game_state.valid_moves.size(), 2);
    BOOST_CHECK_EQUAL(game_state.valid_moves[0], 2);
    BOOST_CHECK_EQUAL(game_state.valid_moves[1], 3);



    BOOST_CHECK_EQUAL(game_state.next_player, 1);

    game_state.play(1);
    game_state.update_after_play();
    std::cout <<game_state <<std::endl;

    //new tab should be "1 0 1 0\n3 5\n0\n0\n"

    BOOST_CHECK_EQUAL(game_state.size_, 2);

    BOOST_CHECK_EQUAL(game_state.tab.size(), 4);
    BOOST_CHECK_EQUAL(game_state.tab[0], 1);
    BOOST_CHECK_EQUAL(game_state.tab[1], 0);
    BOOST_CHECK_EQUAL(game_state.tab[2], 1);
    BOOST_CHECK_EQUAL(game_state.tab[3], 0);


    BOOST_CHECK_EQUAL(game_state.scores.size(), 2);
    BOOST_CHECK_EQUAL(game_state.scores[0], 3);
    BOOST_CHECK_EQUAL(game_state.scores[1], 5);


    BOOST_CHECK_EQUAL(game_state.valid_moves.size(), 1);
    BOOST_CHECK_EQUAL(game_state.valid_moves[0], 0);



    BOOST_CHECK_EQUAL(game_state.next_player, 0);

}


BOOST_AUTO_TEST_CASE(test_game_over)
{

    std::stringstream s("1 2 3 1\n7 2\n0\n0 1\n");


    game game_state(s);

    std::cout <<game_state <<std::endl;



    game_state.play(1);
    std::cout <<game_state <<std::endl;

    game_state.update_after_play();
    std::cout <<game_state <<std::endl;

    std::cout << std::endl <<game_state.valid_moves.size() << std::endl;


    std::cout <<std::endl;
    //new tab should be "1 0 4 0\n9 2\n1\n2\n"

    //player 0 wins as score > 8
    BOOST_CHECK_EQUAL(game_state.size_, 2);

    BOOST_CHECK_EQUAL(game_state.tab.size(), 4);
    BOOST_CHECK_EQUAL(game_state.tab[0], 0);
    BOOST_CHECK_EQUAL(game_state.tab[1], 0);
    BOOST_CHECK_EQUAL(game_state.tab[2], 0);
    BOOST_CHECK_EQUAL(game_state.tab[3], 0);


    BOOST_CHECK_EQUAL(game_state.scores.size(), 2);
    BOOST_CHECK_EQUAL(game_state.scores[0], 10);
    BOOST_CHECK_EQUAL(game_state.scores[1], 6);


    BOOST_CHECK_EQUAL(game_state.valid_moves.size(), 0);




    BOOST_CHECK_EQUAL(game_state.next_player, 1);


}
