/*
Author     :    honghuichao
Data       :    2017-08-22
�޸���־   ��   ��
����       ��   ����Ŀ¼��Ϊ��Ӧ��Ŀ¼����ǩ

����       ��   ����TraverseFiles������TraverseFiles("c:/", 1);
                ����c:/Ŀ¼����  1.txt�ļ�
                1.txt�ĸ�ʽΪ:
                �ļ�·��1 1
                �ļ�·��2 1
                �ļ�·��3 1
                ....
				�ļ�·��n 1
*/
#include <iostream>
#include<fstream>
#include <string>  
#include <io.h>  
using namespace std;

//������ǰĿ¼�µ��ļ��к��ļ�,Ĭ���ǰ���ĸ˳�����  
bool TraverseFiles(string path, char* lab, ofstream& out)
{
	
	_finddata_t file_info;
	string current_path = path + "/*.*"; //���Զ������ĺ�׺Ϊ*.exe��*.txt���������ض���׺���ļ���*.*��ͨ�����ƥ����������,·�����ӷ��������б��/���ɿ�ƽ̨  
	//���ļ����Ҿ��  
	int handle = _findfirst(current_path.c_str(), &file_info);
	//����ֵΪ-1�����ʧ��  
	if (-1 == handle)
		return false;
	do
	{
		//�ж��Ƿ���Ŀ¼  
		string attribute;
		if (file_info.attrib == _A_SUBDIR) //��Ŀ¼  
			attribute = "dir";
		else
			attribute = "file";
		//����ļ���Ϣ������,�ļ���(����׺)���ļ�����޸�ʱ�䡢�ļ��ֽ���(�ļ�����ʾ0)���ļ��Ƿ�Ŀ¼  
		out << path << file_info.name << ' ' <<lab<< endl; //��õ�����޸�ʱ����time_t��ʽ�ĳ����ͣ���Ҫ����������ת������ʱ����ʾ  
		
	} while (!_findnext(handle, &file_info));  //����0�������  
	//�ر��ļ����  
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