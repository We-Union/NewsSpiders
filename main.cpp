#include <iostream>
#include <fstream>
using namespace std;
int main()
{
    ifstream file("events.txt");
    ofstream outfile("events_out.txt");
    string str;
    file >> str;
    while(!file.eof())
    {
        file >> str;
        str += " ";
        outfile << str<<endl;
        for(int i=1;i<=13;i++)
        {
            file >>str;
        }
       
    }
    return 0;
}