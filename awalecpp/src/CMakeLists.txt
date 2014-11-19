set(LIBS )

foreach(lib ${LIBS})
    add_library(${lib} ${lib}.cpp process_args)
    target_link_libraries(${lib} ${Boost_PROGRAM_OPTIONS_LIBRARY} )
endforeach(lib)

set(PROGRAMS runner)
set(LINK_LIBS ${MYSQLCONN_LIBRARY}
              ${BLAS_LIBRARIES}
              ${Boost_PROGRAM_OPTIONS_LIBRARY}
              ${Boost_LOG_LIBRARY}
              ${Boost_LOG_SETUP_LIBRARY}
              ${CMAKE_THREAD_LIBS_INIT}
              )

foreach(prog ${PROGRAMS})
    add_executable(${prog} ${prog}.cpp)
    target_link_libraries(${prog} ${LINK_LIBS})
    #add_dependencies(${prog} )
endforeach(prog)
