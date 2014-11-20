#ifndef GAME_HPP
#define GAME_HPP

#include <iostream>
#include <string>
#include <algorithm>

#include <sstream>
#include <vector>
#include <iterator>
#include "utils.hpp"

int compute_decisive_score(const std::vector<int>& tab_in,
                           const std::vector<int>&  scores_in){


return((std::accumulate(tab_in.begin(),tab_in.end(),0) + std::accumulate(scores_in.begin(),scores_in.end(),0))/2);

}

bool compute_game_over(const std::vector<int>& scores_in, const int& decisive_score_in){


return ((scores_in[0] > decisive_score_in) ||
    (scores_in[1] > decisive_score_in) ||
    ((scores_in[0] == decisive_score_in) && (scores_in[1] == decisive_score_in))
       );

}

template<typename Game>
std::vector<int> get_valid_moves(const Game& game_state){

    std::vector<int> non_empty_holes;

    for (int i=0; i<game_state.size_; i++){

        if (game_state.tab[i + game_state.size_ * game_state.next_player] >0) {
            non_empty_holes.push_back(i + game_state.size_ * game_state.next_player);
        }
    }

    //quick sufficient condition
    if ((*std::max_element(game_state.tab.begin() + game_state.size_ * (1 - game_state.next_player),
                          game_state.tab.begin() + game_state.size_ * (2 - game_state.next_player) )) > 2) {
        return non_empty_holes;
    } else {
        //test every move to see if opponent got empty side
        std::vector<int> new_valid_moves;
        for (size_t i=0; i<non_empty_holes.size();i++){

            auto game_tmp = game_state;

            game_tmp.play(i, non_empty_holes);
            if ((*std::max_element(game_tmp.tab.begin() + game_state.size_ * (1 - game_state.next_player),
                                  game_tmp.tab.begin() + game_state.size_ * (1 - game_state.next_player) + game_state.size_)) >0) {

                new_valid_moves.push_back(non_empty_holes[i]);
            }


        }
        return new_valid_moves;

    }

}




struct game{


    //explicit constructor
    game(std::vector<int> tab,
         int next_player,
         std::vector<int>  scores,
         std::vector<int> valid_moves,
         bool game_over):
        tab(tab),
        size_(tab.size()/2),
        next_player(next_player),
        scores(scores),
        valid_moves(valid_moves),
        game_over(game_over)
        {}

    //build from file reading
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

        decisive_score = compute_decisive_score(tab, scores);

        //game_over
        game_over = compute_game_over(scores, decisive_score);
    }

    //update from file reading
    void update_from_file(std::istream& infile){

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

        //game_over
        game_over = is_game_over();
        return;
    }

    //copy constructor
    game(const game& game_in):
        tab(game_in.tab),
        size_(game_in.size_),
        next_player(game_in.next_player),
        scores(game_in.scores),
        valid_moves(game_in.valid_moves),
        game_over(game_in.game_over),
        decisive_score(game_in.decisive_score)
    {}


    friend
    std::ostream& operator<< (std::ostream& out, const game& game_state)
    {
        out << "*********************\n";
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

        out << "\n*********************\n";
        return out;

    }




    void play(int move, std::vector<int> moves){


        if (move >= moves.size()) {std::cout << move << "  >=   " << valid_moves.size() <<std::endl;
                                         throw std::runtime_error("invalid move");
        }


        //distribute seeds into holes

        int start_idx = moves[move];
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
        int last_hole_idx = (start_idx + n_seeds) % (2* size_);
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

    void play(int move){


        play(move, valid_moves);

    }




    void update_after_play(){

    //update next_player
    next_player = 1 - next_player;
    //compute next valid moves
    valid_moves = get_valid_moves(*this);
    //game_over?
    game_over = is_game_over();



    }

    void empty_tab_and_update_scores(){

        //empty tab and update scores
            for (int i=0;i<size_;i++){

                scores[0] += tab[i];
                scores[1] += tab[i + size_];
                tab[i] = 0;
                tab[i + size_] = 0;

            }
            valid_moves = std::vector<int>(0);
            game_over = true;

    }


    bool is_game_over(){


        if ((valid_moves.size()==0) ||
            (scores[0] > decisive_score) ||
            (scores[1] > decisive_score) ||
            ((scores[0] == decisive_score) && (scores[1] == decisive_score))
            ) {


            empty_tab_and_update_scores();
            return true;
        } else {
            return false;
        }
    }




    std::vector<int> tab;
    int size_;
    int next_player;
    std::vector<int>  scores;
    std::vector<int> valid_moves;
    bool game_over;
    int decisive_score;


};



#endif // GAME_HPP
