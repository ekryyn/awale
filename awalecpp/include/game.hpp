#ifndef GAME_HPP
#define GAME_HPP

#include <iostream>
#include <string>
#include <algorithm>

#include <sstream>
#include <vector>
#include <iterator>
#include "utils.hpp"



struct game{


    //explicit constructor
    game(std::vector<int> tab,
         int next_player,
         std::vector<int>  scores,
         std::vector<int> valid_moves):
        tab(tab),
        size_(tab.size()/2),
        next_player(next_player),
        scores(scores),
        valid_moves(valid_moves)
    {}

    //from file reading
    game(std::istream& infile){

        std::string line;
        // tab
        std::getline(infile, line);
        tab = read_int_line(line);
        //size
        size_ =  tab.size()/2;
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
        size_(game_in.size_),
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

    std::vector<int> get_valid_moves(){

        std::vector<int> non_empty_holes;

        for (int i=0; i<size_; i++){

            if (tab[i + size_ * next_player] >0) {
                non_empty_holes.push_back(i);
            }
        }

        //quick sufficient condition
        if ((*std::max_element(tab.begin() + size_ * (1 - next_player),
                              tab.begin() + size_ * (2 - next_player) )) > 2) {
            return non_empty_holes;
        } else {
            //test every move to see if opponent got empty side
            std::vector<int> new_valid_moves;
            for (size_t i=0; i<non_empty_holes.size();i++){

                auto game_tmp = *this;

                game_tmp.play(non_empty_holes[i]);
                if ((*std::max_element(game_tmp.tab.begin() + size_ * (1 - next_player),
                                      game_tmp.tab.begin() + size_ * (1 - next_player) + size_)) >0) {

                    new_valid_moves.push_back(non_empty_holes[i]);
                }


            }
            return new_valid_moves;

        }

    }

    void play(int move){

        if (move >= (int)valid_moves.size()) throw std::runtime_error("invalid move");


        //distribute seeds into holes

        int start_idx = valid_moves[move] + size_ * next_player;
        auto n_seeds = tab[start_idx];

        int n_laps = n_seeds /(2 * size_ -1);

        //distribute laps seeds
        if (n_laps >0) {
            n_seeds -= n_laps * (2 * size_ -1);
            std::transform(tab.begin(),
                           tab.end(),
                           tab.begin(),
                           [n_laps](int n){return  n + n_laps;}
                          );
        }



        //distribute remaining seeds
        tab[start_idx] = 0;
        for (int i=1; i<=n_seeds; i++) {

            tab[(start_idx + i) % (2*size_)]+=1;

        }

        //capture seeds
        int last_hole_idx = start_idx + n_seeds;
        if (last_hole_idx >= size_ && next_player == 0){

            while(last_hole_idx>=size_){

                if (tab[last_hole_idx]==2 || tab[last_hole_idx]==3) {
                    scores[next_player] += tab[last_hole_idx];
                    tab[last_hole_idx]= 0;
                    last_hole_idx--;
                } else {
                    break;
                }
            }

        } else if (last_hole_idx < size_ && next_player == 1){

            while(last_hole_idx>=0){

                if (tab[last_hole_idx]==2 || tab[last_hole_idx]==3) {
                    scores[next_player] += tab[last_hole_idx];
                    tab[last_hole_idx]= 0;
                    last_hole_idx--;
                } else {
                    break;
                }
            }


        }


    }

    void update_after_play(){

    //update next_player
    next_player = 1 - next_player;
    //compute next valid moves
    valid_moves = get_valid_moves();




    }

//




std::vector<int> tab;
int size_;
int next_player;
std::vector<int>  scores;
std::vector<int> valid_moves;

};


#endif // GAME_HPP
