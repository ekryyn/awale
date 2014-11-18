#ifndef GAME_HPP
#define GAME_HPP

#include <iostream>
#include <string>


#include <sstream>
#include <vector>
#include <iterator>
#include "utils.hpp"



struct game{


    //explicit constructor
    game(std::vector<size_t> tab,
         size_t next_player,
         std::vector<size_t>  scores,
         std::vector<size_t> valid_moves):
        tab(tab),
        next_player(next_player),
        scores(scores),
        valid_moves(valid_moves)
    {}

    //from file reading
    game(std::istream& infile){

        std::string   line;
        // tab
        std::getline(infile, line);
        tab = read_int_line(line);
        // scores
        std::getline(infile, line);
        scores = read_int_line(line);
        // next_player
        std::getline(infile, line);
        next_player = read_int_line(line)[0];
        // valid_moves
        std::getline(infile, line);
        valid_moves = read_int_line(line);
    }

    //copy constructor
    game(const game& game_in):
        tab(game_in.tab),
        next_player(game_in.next_player),
        scores(game_in.scores),
        valid_moves(game_in.valid_moves)
    {}


    friend
    std::ostream& operator<< (std::ostream& out, const game& game_state)
    {
        out <<"tab " ;
        for (size_t i=0;i<game_state.tab.size();i++) {
            out << game_state.tab[i] << " ";
        }

        out <<"\nscores " ;
        for (size_t i=0;i<game_state.scores.size();i++) {
            out << game_state.scores[i] << " ";
        }

        out <<"\nnext_player " ;
        out << game_state.next_player << " ";

        out <<"\nvalid_moves " ;
        for (size_t i=0;i<game_state.valid_moves.size();i++) {
            out << game_state.valid_moves[i] << " ";
        }

        return out;

    }

    std::vector<size_t> tab;
    size_t next_player;
    std::vector<size_t>  scores;
    std::vector<size_t> valid_moves;

};


#endif // GAME_HPP
