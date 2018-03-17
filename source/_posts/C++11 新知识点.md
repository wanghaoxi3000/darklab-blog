---
title: C++11 新知识点
date: 2017/9/25 23:51:00
categories:
- cpp
toc: true
---

翻了下新版的C++ Primer，新的C++ 11真是变化很大，新增了很多语法特性。虽然已经很久没在写C++了，但一直对这门经典语言很感兴趣的，大致看了看前几章基础部分，总结下新特性备个忘，总结下新特性备个忘吧。估计也很难有机会用上了... ╮(─▽─)╭

## 基本语法
### 类型别名
C++11新规定了一种使用using的别名声明的方法
```
typedef double wages;
using wages = double;
```

### decltype类型指示符
通过decltype选安置并返回操作数的数据类型
```
//sum的类型是f()的返回值
decltype(f()) sum = x;

//错误示例, cj是z的一个引用, 必须初始化
const int &cj = ci;
decltype(cj) z;
```
变量名加上一层或多层括号时, 编译器会把它当成是一个表达式, 此时decltype会得到一个引用类型.
```
decltype((i)) d; //错误示例, d是int&, 必须初始化
```

### 迭代语句
#### for循环
```
for (declaration : expression)
    statemet
```

例子:
```
//将vector对象中每个元素都翻倍
vector<int> v = {0, 1, 2, 3, 5}

for (auto &r : v)
    r *= 2;
```

## 基本类型
### string类型
#### string:: size_type
size_type是string中一种与机器无关的类型, 一个无符号类型的值而且能够存放下任何string对象的大小,所有用于存放string类的size函数返回值的变量, 都应该是string:: size_type类型的.

## 函数
### 可变形参函数
#### initializer_list
适用于全部类型都一样的可变形参, 定义在同名头文件中, 同vector一样, 也是种模板类型. 拷贝或赋值一个initializer_list对象不会拷贝列表中的元素, 拷贝后原始列表和副本共享元素

例子:
```
void error_msg(initializer_list<string> il)
{
	for (auto beg = il.begin(); beg != il.end(); ++beg)
	{
		cout << *beg << " ";
		cout << endl;
	}
}
```

### 函数重载
#### const_cast强转重载函数
```
//比较两个string的长度, 返回较短的那一个
const string &shorterString(const string &s1, const string &s2)
{
    return s1.size() <= s2.size() ? s1 : s2;
}

//使用const_cast改造成比较非常量时返回普通引用
string &shorterString(string &s1, string &s2)
{
    auto &r = shorterString(const_cast<const string&>(s1),
                const_cast<const string&>(s2));
    return const_cast<string&>(r);
}
```

### constexpr函数
能用于常量表达式的函数, 函数返回类型及所有形参类型都得是字面类型, 且函数体重有且只有一条return语句
```
constexpr int new_sz() { return 42; }
constexpr int foo = new_sz();
```

### 函数指针
#### typedef和decltype定义函数类型及指针
```
//Func和Func2是函数类型
typedef bool Func(const string&, const string&);
tyedef decltype(lengthCompare) Func2;   //等价类型

//Func和Func2是指向函数的指针
typedef bool (*Func)(const string&, const string&);
typedef decltype(lengthCompare) *Func2; //等价类型
```

## 类
### 成员函数
- 定义在类内部的函数是隐式的inline函数
- 参数列表后加const, 用于修改隐式this指针类型, 便于指向常量, 限制this修改所指对象\
- C++11中可以通过在参数列表后面写上= default来要求编译器生成默认构造函数
- 通过mutable关键字来声明一个可变成员函数, 可在const成员函数中改变
- 通过explicit限制一个实参的构造函数进行隐式转换

### 委托构造函数
C++11中可使用委托构造函数来使用它所属类的其它构造函数来执行自己的初始化过程
```
class Sales_data {
    Sales_data(std::string s, unsigned cnt, double price):
    bookNo(s), units_sold(cnt), revenu(cnt*price) {}
    Sales_data(): Sales_data("", 0, 0) {}
    Sales_data(std::string s): Sales_data(s, 0, 0) {}
    Sales_data(std::istream &is): Sales_data() {
        read(is, *this)
    }
}
```