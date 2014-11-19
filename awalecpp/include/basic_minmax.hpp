#ifndef BASIC_MINMAX_HPP
#define BASIC_MINMAX_HPP


//basic minmax templated on game class and heuristic function type F
template<typename Game, typename F>
struct basic_minmax{


    basic_minmax(const Game& game_state, const F& f, size_t depth_search):
        game_state(game_state),f(f),depth_search(depth_search){}



    std::vector<double> compute_move_values(){

        std::vector<double> move_values(game_state.valid_moves.size(),0.0);

        //loop on possible moves
        for (int i = 0; i < game_state.valid_moves.size(); i++){


            auto game_tmp = tmp_game_state;

            //compute minmax for this move

            game_tmp.play(valid_moves[i]);

            move_values[i] = compute_minmax(game_tmp, depth, game_state.next_player);


        }

        return move_values;
    }

    size_t get_best_move(std::vector<double> move_values){

        return std::distance(move_values.begin(), std::max_element(move_values.begin(), move_values.end()));

    }


    double compute_minmax(const Game& tmp_game_state, const int& depth, int player_id){

        if (depth == 0 || tmp_game_state.game_over) {return f(game_state, player);}

        int sign = (player_id == tmp_game_state.next_player)?1:-1;


        double max_value = -Inf;


        for (const auto& move : tmp_game_state.valid_moves){

            //play this move
            auto game_tmp = tmp_game_state;
            //compute minmax after the move

            game_tmp.play(move);
            auto value = sign * compute_minmax(game_tmp, depth - 1 , 1 - player);
            //keep the best move
            if (value > max_value) {
                max_value = value ;
            }

        }


    }

    Game game_state;
    F f;
    size_t depth_search;



}












#endif // BASIC_MINMAX_HPP
