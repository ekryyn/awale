set(TIMERS )

foreach(timer ${TIMERS})
    add_executable(${timer} ${timer}.cpp)
    target_link_libraries(${timer} soprofiling
                                   ${Boost_PROGRAM_OPTIONS_LIBRARY})
endforeach(timer)
