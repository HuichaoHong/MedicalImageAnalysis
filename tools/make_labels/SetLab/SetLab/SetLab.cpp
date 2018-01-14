/*
Author     :    honghuichao
Data       :    2017-08-22
修改日志   ：   空
功能       ：   输入目录，为相应的目录做标签

例子       ：   调用TraverseFiles函数，TraverseFiles("c:/", 1);
                会在c:/目录生成  1.txt文件
                1.txt的格式为:
                文件路径1 1
                文件路径2 1
                文件路径3 1
                ....
				文件路径n 1
*/
#include <iostream>
#include<fstream>
#include <string>  
#include <io.h>  
using namespace std;

//遍历当前目录下的文件夹和文件,默认是按字母顺序遍历  
bool TraverseFiles(string path, char* lab, ofstream& out)
{
	
	_finddata_t file_info;
	string current_path = path + "/*.*"; //可以定义后面的后缀为*.exe，*.txt等来查找特定后缀的文件，*.*是通配符，匹配所有类型,路径连接符最好是左斜杠/，可跨平台  
	//打开文件查找句柄  
	int handle = _findfirst(current_path.c_str(), &file_info);
	//返回值为-1则查找失败  
	if (-1 == handle)
		return false;
	do
	{
		//判断是否子目录  
		string attribute;
		if (file_info.attrib == _A_SUBDIR) //是目录  
			attribute = "dir";
		else
			attribute = "file";
		//输出文件信息并计数,文件名(带后缀)、文件最后修改时间、文件字节数(文件夹显示0)、文件是否目录  
		out << path << file_info.name << ' ' <<lab<< endl; //获得的最后修改时间是time_t格式的长整型，需要用其他方法转成正常时间显示  
		
	} while (!_findnext(handle, &file_info));  //返回0则遍历完  
	//关闭文件句柄  
	_findclose(handle);
	return true;
}

int main(int argc, char *argv[])
{
	if (argc==1)
	{
		cout << endl;
		
		cout << "usage:  SetLab.exe dir_1, it's labels | dir_2 ,it's labels| ....|saved path" << endl;
		return 0;

	}
	string path(argv[argc - 1]);
	ofstream out(path + ".txt",ios::app);
	for (size_t i = 1; i < argc-1; i++)
	{
		TraverseFiles(argv[i],argv[++i],out);
		
	}
	return 0;
}