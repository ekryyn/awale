#ifndef BASIC_MINMAX_HPP
#define BASIC_MINMAX_HPP


#include <algorithm>
#include <limits>
#include <cstdlib>
#include "game.hpp"

/*

namespace checkers
{

int evaluatedStates = 0;

int evaluate(const GameState &state)
{
    // FIXME: Improve heuristics.
    int redScore = 0;
    int whiteScore = 0;
    int piece = 0;
    for (int i = 1; i <= 32; ++i)
    {
        piece = state.at(i);
        if (piece & CELL_RED) {
            ++redScore;
            if (piece & CELL_KING)
                redScore += 2;   // King bonus.
        } else if (piece & CELL_WHITE) {
            ++whiteScore;
            if (piece & CELL_KING)
                whiteScore += 2; // King bonus.
        }
    }
    return state.getNextPlayer() == CELL_RED ? whiteScore - redScore : redScore - whiteScore;
}

int minimax(const GameState &state, int depth, int a, int b, bool max)
{
    if (depth == 0 || state.isEOG()) {
        ++evaluatedStates;
        return evaluate(state);
    }
    std::vector<GameState> possibleMoves;
    state.findPossibleMoves(possibleMoves);
    if (max) {
        for (const GameState &move : possibleMoves) {
            a = std::max(a, minimax(move, depth - 1, a, b, false));
            if (b <= a)
                return b; // β cutoff.
        }
        return a;
    } else {
        for (const GameState &move : possibleMoves) {
            b = std::min(b, minimax(move, depth - 1, a, b, true));
            if (b <= a)
                return a; // α cutoff.
        }
        return b;
    }
}

int negamax(const GameState &state, int depth, int a, int b)
{
    if (depth == 0 || state.isEOG()) {
        ++evaluatedStates;
        return evaluate(state);
    }
    std::vector<GameState> possibleMoves;
    state.findPossibleMoves(possibleMoves);
    for (const GameState &move : possibleMoves) {
        a = std::max(a, -negamax(move, depth - 1, -b, -a));
        if (b <= a)
            return b; // β cutoff.
    }
    return a;
}

GameState Player::play(const GameState &pState, const Deadline &pDue)
{
    GameState bestMove(pState, Move());

    std::vector<GameState> possibleMoves;
    pState.findPossibleMoves(possibleMoves);

    int a = -std::numeric_limits<int>::max();
    int b = std::numeric_limits<int>::max();
    for (const GameState &move : possibleMoves) {
        int v = negamax(move, 10, a, b);
        //int v = minimax(move, 10, a, b, true);
        if (v > a) {
            a = v;
            bestMove = move;
        }
    }
    std::cerr << "Evaluated states: " << evaluatedStates << std::endl;
    return bestMove;
}

}

*/




//basic minmax templated on game class and heuristic function type F
template<typename Game, typename F>
struct basic_minmax{


    basic_minmax(const Game& game_state, F f, size_t search_depth):
        game_state(game_state),f(f),search_depth(search_depth){}



    std::vector<double> compute_move_values(){

        std::vector<double> move_values(game_state.valid_moves.size(),0.0);

        //loop on possible moves
        for (int i = 0; i < game_state.valid_moves.size(); i++){


            auto game_tmp = game_state;

            //compute minmax for this move

            game_tmp.play(i);
            game_tmp.update_after_play();

            move_values[i] = compute_minmax(game_tmp, search_depth - 1, game_state.next_player);


        }

        return move_values;
    }

    size_t get_best_move(std::vector<double> move_values){

        return std::distance(move_values.begin(), std::max_element(move_values.begin(), move_values.end()));

    }


    double compute_minmax(const Game& tmp_game_state, const int& search_depth_in, int player_id){

        
        int sign = (player_id == tmp_game_state.next_player)?1:-1;
        if (search_depth_in == 0 || tmp_game_state.game_over) {return sign * f(tmp_game_state);}


        double max_value = -10000000;


        for (int i = 0; i < tmp_game_state.valid_moves.size(); i++){

            //play this move
            auto game_tmp = tmp_game_state;
            //compute minmax after the move

            game_tmp.play(i);
            game_tmp.update_after_play();
            auto value = sign * compute_minmax(game_tmp, search_depth_in - 1 , player_id);
            //keep the best move
            if (value > max_value) {
                max_value = value ;
            }

        }


        return sign * max_value;
    }

    Game game_state;
    F* f;
    size_t search_depth;



};

#endif // BASIC_MINMAX_HPP
