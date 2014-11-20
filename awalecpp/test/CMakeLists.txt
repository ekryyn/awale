set(TESTS test_game test_minmax)

foreach(test ${TESTS})
    add_executable(${test} ${test}.cpp)
    target_link_libraries(${test} ${Boost_TEST_EXEC_MONITOR_LIBRARY})
    add_test(${test} ${EXECUTABLE_OUTPUT_PATH}/${test})
endforeach(test)
