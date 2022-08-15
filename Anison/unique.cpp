#include <fstream>
#include <iostream>
#include <string>
#include <cstring>
#include <ctime>
#include <unordered_map>

#define PREFIX 33
#define DEF_FILE "Music.sav"

bool is_number(const std::string& s)
{
    std::string::const_iterator it = s.begin();
    while (it != s.end() && std::isdigit(*it)) ++it;
    return !s.empty() && it == s.end();
}

int main(int argc, const char **argv)
{
    std::string fn = DEF_FILE;
    std::string ofn = DEF_FILE;
    bool DEBUG = false;
    size_t prefix = PREFIX;

    if(argc == 2) fn = argv[1];
    else
    {
        for(int i = 1; i < argc-1; i++)
        {
            if(strcmp("-f",argv[i]) == 0) fn = argv[++i];
            else if(strcmp("-o",argv[i]) == 0) ofn = argv[++i];
            else if(strcmp("-d",argv[i]) == 0) DEBUG = true;
            else if(strcmp("-p",argv[i]) == 0)
            {
                if(is_number(argv[++i]))
                {
                    prefix = atoi(argv[i]);
                }
                else
                {
                    std::cout << "Invalid parameter value int required.\nValue: " << argv[i] << '\n';
                    return 1;
                }
            }
        }
    }

    int line_count = 0;
    std::unordered_map<std::string,std::string> lines;
    std::ifstream is(fn);

    if(!is.is_open()) return 1;

    while(!is.eof())
    {
        std::string buff;
        std::getline(is,buff,'\n');
        if(buff.size())
        {
            line_count++;
            lines.insert(std::make_pair(buff.substr(prefix),buff.substr(0,prefix)));
            if(DEBUG)
                std::cout << "Key: " << buff.substr(prefix) << "\nValue: " << buff.substr(0,prefix) << '\n';
        }
    }

    is.close();



    std::ofstream os(ofn, std::ios_base::trunc);
    for(auto it = lines.begin(); it != lines.end(); it++)
    {
        os << it->second << it->first << '\n';
    }
    os.close();

    std::cout << "Deleted: " << line_count - lines.size() << '\n';

    if(DEBUG)
        std::cout << "Total: " << lines.size() << '\n';

    return 0;
}