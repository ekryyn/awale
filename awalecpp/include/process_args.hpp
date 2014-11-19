#ifndef PROCESS_ARGS_HPP
#define PROCESS_ARGS_HPP

#include <boost/program_options.hpp>
#include <iostream>
#include <fstream>

boost::program_options::variables_map
process_arguments(int argc, char** argv)
{
    const char* help = "Allowed options:";
    namespace po = boost::program_options;

    po::options_description desc("Model options");
    desc.add_options()
            ("help", help)
            ("config", po::value<std::string>()->default_value(std::string("")),
             "path to configuration file.")
            /// Typical command line arguments.
            ("strategy", po::value<std::string>()->default_value(std::string("random")),
             "name of the strategy to use: currently only random or first.")

            /// Typical config file arguments.

            ("search_depth", po::value<int>(),
             "depth of the tree to search in.");


    po::variables_map options;
    po::store(po::parse_command_line(argc, argv, desc), options);
    po::notify(options);

    if (options.count("help")){
        std::cout << desc << "\n";
        exit(1);
    }


    if (options["config"].as<std::string>() != "") {
        std::ifstream config(options["config"].as<std::string>());

        if (!config)
            throw std::runtime_error("Can't open config file\n"
                                     + options["config"].as<std::string>());

        po::store(po::parse_config_file(config, desc), options);
        po::notify(options);
    }
    return options;
}


#endif // PROCESS_ARGS_HPP
