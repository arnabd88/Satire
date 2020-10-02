#include <cstdio>
#include <iostream>
#include <unistd.h>
#include <cstdlib>
#include<cmath>
#include <cassert>
#include <quadmath.h>
#include <time.h>

#define _low_x1  -5.0
#define _high_x1 5.0
#define _low_x2  -20.0
#define _high_x2 5.0

using namespace std;


double _x1 ;
double _x2 ;

template<class T>
void init() {

	_x1 = _low_x1 + static_cast<T> (rand())/(static_cast<T>(RAND_MAX/(_high_x1 - _low_x1))) ;
	_x2 = _low_x2 + static_cast<T> (rand())/(static_cast<T>(RAND_MAX/(_high_x2 - _low_x2))) ;

}


template<class T>
T execute_spec_precision()
{
	T x1 = (T) _x1 ;
	T x2 = (T) _x2 ;

	T t = ((((3 * x1) * x1) + (2 * x2)) - x1);
	T t_42_ = ((((3 * x1) * x1) - (2 * x2)) - x1);
	T d = ((x1 * x1) + 1);
	T s = (t / d);
	T s_42_ = (t_42_ / d);
	T jetEngine = (x1 + (((((((((2 * x1) * s) * (s - 3)) + ((x1 * x1) * ((4 * s) - 6))) * d) + (((3 * x1) * x1) * s)) + ((x1 * x1) * x1)) + x1) + (3 * s_42_)));

	return jetEngine ;

}

template<class T>
T execute_error_expression()
{
	T x1 = (T) _x1 ;
	T x2 = (T) _x2 ;

	T err = 2*fabs(0.5*pow(x1,3)) + fabs(0.5*(-3.0*pow(x1,3)/(1.0 + pow(x1,2)) + 9.0*pow(x1,4)/(1.0 + pow(x1,2)) + 6.0*x2*pow(x1,2)/(1.0 + pow(x1,2)))) + fabs(0.5*(0.0 - 3.0*x1/(1.0 + pow(x1,2)) + 9.0*pow(x1,2)/(1.0 + pow(x1,2)) - 6.0*x2/(1.0 + pow(x1,2)))) + fabs(0.5*(0.0 + 6.0*pow(x1,2)/(1.0 + pow(x1,2)) - 25.0*pow(x1,3)/(1.0 + pow(x1,2)) + 2.0*pow(x1,3)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 27.0*pow(x1,4)/(1.0 + pow(x1,2)) - 12.0*pow(x1,4)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) - 22.0*pow(x1,5)/(1.0 + pow(x1,2)) + 20.0*pow(x1,5)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 12.0*pow(x1,6)/(1.0 + pow(x1,2)) - 12.0*pow(x1,6)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 18.0*pow(x1,7)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) - 12.0*x2*x1/(1.0 + pow(x1,2)) + 14.0*x2*pow(x1,2)/(1.0 + pow(x1,2)) - 8.0*x2*pow(x1,2)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) - 12.0*x2*pow(x1,3)/(1.0 + pow(x1,2)) + 24.0*x2*pow(x1,3)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 8.0*x2*pow(x1,4)/(1.0 + pow(x1,2)) - 8.0*x2*pow(x1,4)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 24.0*x2*pow(x1,5)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 8.0*pow(x2,2)*x1/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 8.0*pow(x2,2)*pow(x1,3)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) - 6.0*pow(x1,2) - 6.0*pow(x1,4))) + fabs(0.5*(0.0 + 6.0*pow(x1,2)/(1.0 + pow(x1,2)) - 22.0*pow(x1,3)/(1.0 + pow(x1,2)) + 2.0*pow(x1,3)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 18.0*pow(x1,4)/(1.0 + pow(x1,2)) - 12.0*pow(x1,4)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) - 22.0*pow(x1,5)/(1.0 + pow(x1,2)) + 20.0*pow(x1,5)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 12.0*pow(x1,6)/(1.0 + pow(x1,2)) - 12.0*pow(x1,6)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 18.0*pow(x1,7)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) - 12.0*x2*x1/(1.0 + pow(x1,2)) + 8.0*x2*pow(x1,2)/(1.0 + pow(x1,2)) - 8.0*x2*pow(x1,2)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) - 12.0*x2*pow(x1,3)/(1.0 + pow(x1,2)) + 24.0*x2*pow(x1,3)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 8.0*x2*pow(x1,4)/(1.0 + pow(x1,2)) - 8.0*x2*pow(x1,4)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 24.0*x2*pow(x1,5)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 8.0*pow(x2,2)*x1/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 8.0*pow(x2,2)*pow(x1,3)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) - 6.0*pow(x1,2) - 6.0*pow(x1,4))) + fabs(0.5*(0.0 + 6.0*pow(x1,2)/(1.0 + pow(x1,2)) - 25.0*pow(x1,3)/(1.0 + pow(x1,2)) + 2.0*pow(x1,3)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 27.0*pow(x1,4)/(1.0 + pow(x1,2)) - 12.0*pow(x1,4)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) - 22.0*pow(x1,5)/(1.0 + pow(x1,2)) + 20.0*pow(x1,5)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 12.0*pow(x1,6)/(1.0 + pow(x1,2)) - 12.0*pow(x1,6)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 18.0*pow(x1,7)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) - 12.0*x2*x1/(1.0 + pow(x1,2)) + 14.0*x2*pow(x1,2)/(1.0 + pow(x1,2)) - 8.0*x2*pow(x1,2)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) - 12.0*x2*pow(x1,3)/(1.0 + pow(x1,2)) + 24.0*x2*pow(x1,3)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 8.0*x2*pow(x1,4)/(1.0 + pow(x1,2)) - 8.0*x2*pow(x1,4)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 24.0*x2*pow(x1,5)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 8.0*pow(x2,2)*x1/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 8.0*pow(x2,2)*pow(x1,3)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) - 6.0*pow(x1,2) + pow(x1,3) - 6.0*pow(x1,4))) + fabs(0.5*(0.0 + x1 + 6.0*pow(x1,2)/(1.0 + pow(x1,2)) - 25.0*pow(x1,3)/(1.0 + pow(x1,2)) + 2.0*pow(x1,3)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 27.0*pow(x1,4)/(1.0 + pow(x1,2)) - 12.0*pow(x1,4)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) - 22.0*pow(x1,5)/(1.0 + pow(x1,2)) + 20.0*pow(x1,5)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 12.0*pow(x1,6)/(1.0 + pow(x1,2)) - 12.0*pow(x1,6)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 18.0*pow(x1,7)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) - 12.0*x2*x1/(1.0 + pow(x1,2)) + 14.0*x2*pow(x1,2)/(1.0 + pow(x1,2)) - 8.0*x2*pow(x1,2)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) - 12.0*x2*pow(x1,3)/(1.0 + pow(x1,2)) + 24.0*x2*pow(x1,3)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 8.0*x2*pow(x1,4)/(1.0 + pow(x1,2)) - 8.0*x2*pow(x1,4)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 24.0*x2*pow(x1,5)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 8.0*pow(x2,2)*x1/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 8.0*pow(x2,2)*pow(x1,3)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) - 6.0*pow(x1,2) + pow(x1,3) - 6.0*pow(x1,4))) + fabs(0.5*(0.0 + x1 - 3.0*x1/(1.0 + pow(x1,2)) + 15.0*pow(x1,2)/(1.0 + pow(x1,2)) - 25.0*pow(x1,3)/(1.0 + pow(x1,2)) + 2.0*pow(x1,3)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 27.0*pow(x1,4)/(1.0 + pow(x1,2)) - 12.0*pow(x1,4)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) - 22.0*pow(x1,5)/(1.0 + pow(x1,2)) + 20.0*pow(x1,5)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 12.0*pow(x1,6)/(1.0 + pow(x1,2)) - 12.0*pow(x1,6)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 18.0*pow(x1,7)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) - 6.0*x2/(1.0 + pow(x1,2)) - 12.0*x2*x1/(1.0 + pow(x1,2)) + 14.0*x2*pow(x1,2)/(1.0 + pow(x1,2)) - 8.0*x2*pow(x1,2)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) - 12.0*x2*pow(x1,3)/(1.0 + pow(x1,2)) + 24.0*x2*pow(x1,3)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 8.0*x2*pow(x1,4)/(1.0 + pow(x1,2)) - 8.0*x2*pow(x1,4)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 24.0*x2*pow(x1,5)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 8.0*pow(x2,2)*x1/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 8.0*pow(x2,2)*pow(x1,3)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) - 6.0*pow(x1,2) + pow(x1,3) - 6.0*pow(x1,4))) + fabs(0.5*(0.0 + 2*x1 - 3.0*x1/(1.0 + pow(x1,2)) + 15.0*pow(x1,2)/(1.0 + pow(x1,2)) - 25.0*pow(x1,3)/(1.0 + pow(x1,2)) + 2.0*pow(x1,3)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 27.0*pow(x1,4)/(1.0 + pow(x1,2)) - 12.0*pow(x1,4)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) - 22.0*pow(x1,5)/(1.0 + pow(x1,2)) + 20.0*pow(x1,5)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 12.0*pow(x1,6)/(1.0 + pow(x1,2)) - 12.0*pow(x1,6)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 18.0*pow(x1,7)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) - 6.0*x2/(1.0 + pow(x1,2)) - 12.0*x2*x1/(1.0 + pow(x1,2)) + 14.0*x2*pow(x1,2)/(1.0 + pow(x1,2)) - 8.0*x2*pow(x1,2)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) - 12.0*x2*pow(x1,3)/(1.0 + pow(x1,2)) + 24.0*x2*pow(x1,3)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 8.0*x2*pow(x1,4)/(1.0 + pow(x1,2)) - 8.0*x2*pow(x1,4)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 24.0*x2*pow(x1,5)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 8.0*pow(x2,2)*x1/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 8.0*pow(x2,2)*pow(x1,3)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) - 6.0*pow(x1,2) + pow(x1,3) - 6.0*pow(x1,4))) + fabs(1.5*(-x1/(1.0 + pow(x1,2)) + 3.0*pow(x1,2)/(1.0 + pow(x1,2)) - 2.0*x2/(1.0 + pow(x1,2)))) + fabs(0.5*pow(x1,2)*(0.0 + 6.0*pow(x1,2)/(1.0 + pow(x1,2)) - 22.0*pow(x1,3)/(1.0 + pow(x1,2)) + 2.0*pow(x1,3)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 12.0*pow(x1,4)/(1.0 + pow(x1,2)) - 12.0*pow(x1,4)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 18.0*pow(x1,5)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) - 3.0*(-x1 - 2.0*x2 + 3.0*pow(x1,2))/pow((1.0 + pow(x1,2)),2) + (1.0 + pow(x1,2))*(-6.0 - 4.0*x1/(1.0 + pow(x1,2)) + 12.0*pow(x1,2)/(1.0 + pow(x1,2)) + 8.0*x2/(1.0 + pow(x1,2))) - 12.0*x2*x1/(1.0 + pow(x1,2)) + 8.0*x2*pow(x1,2)/(1.0 + pow(x1,2)) - 8.0*x2*pow(x1,2)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 24.0*x2*pow(x1,3)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 8.0*pow(x2,2)*x1/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) - (-x1 + 2.0*x2 + 3.0*pow(x1,2))*(4.0*pow(x1,2)*(1.0 + pow(x1,2)) + (1.0 + pow(x1,2))*(-2.0*pow(x1,2)/(1.0 + pow(x1,2)) + 6.0*pow(x1,3)/(1.0 + pow(x1,2)) + 4.0*x2*x1/(1.0 + pow(x1,2))) + 2.0*x1*(1.0 + pow(x1,2))*(-3.0 - x1/(1.0 + pow(x1,2)) + 3.0*pow(x1,2)/(1.0 + pow(x1,2)) + 2.0*x2/(1.0 + pow(x1,2))) + 3.0*pow(x1,2))/pow((1.0 + pow(x1,2)),2) - 6.0*pow(x1,2))) + fabs(0.5*(1.0 + pow(x1,2))*(-4.0*pow(x1,3)/(1.0 + pow(x1,2)) + 12.0*pow(x1,4)/(1.0 + pow(x1,2)) + 8.0*x2*pow(x1,2)/(1.0 + pow(x1,2)) - 6.0*pow(x1,2))) + fabs(0.5*(1.0 + pow(x1,2))*(0.0 + 6.0*pow(x1,2)/(1.0 + pow(x1,2)) - 22.0*pow(x1,3)/(1.0 + pow(x1,2)) + 2.0*pow(x1,3)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 12.0*pow(x1,4)/(1.0 + pow(x1,2)) - 12.0*pow(x1,4)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 18.0*pow(x1,5)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) - 12.0*x2*x1/(1.0 + pow(x1,2)) + 8.0*x2*pow(x1,2)/(1.0 + pow(x1,2)) - 8.0*x2*pow(x1,2)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 24.0*x2*pow(x1,3)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 8.0*pow(x2,2)*x1/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) - 6.0*pow(x1,2))) + fabs(0.5*(4.0*pow(x1,2)*(1.0 + pow(x1,2)) + (1.0 + pow(x1,2))*(-2.0*pow(x1,2)/(1.0 + pow(x1,2)) + 6.0*pow(x1,3)/(1.0 + pow(x1,2)) + 4.0*x2*x1/(1.0 + pow(x1,2))) + 2.0*x1*(1.0 + pow(x1,2))*(-3.0 - x1/(1.0 + pow(x1,2)) + 3.0*pow(x1,2)/(1.0 + pow(x1,2)) + 2.0*x2/(1.0 + pow(x1,2))) + 3.0*pow(x1,2))*(-x1/(1.0 + pow(x1,2)) + 3.0*pow(x1,2)/(1.0 + pow(x1,2)) + 2.0*x2/(1.0 + pow(x1,2)))) + fabs(0.5*(0.0 + 6.0*pow(x1,2)/(1.0 + pow(x1,2)) - 18.0*pow(x1,3)/(1.0 + pow(x1,2)) + 2.0*pow(x1,3)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) - 12.0*pow(x1,4)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 18.0*pow(x1,5)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) - 12.0*x2*x1/(1.0 + pow(x1,2)) - 8.0*x2*pow(x1,2)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 24.0*x2*pow(x1,3)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 8.0*pow(x2,2)*x1/(1.0 + 2.0*pow(x1,2) + pow(x1,4)))*(1.0 + pow(x1,2))) + fabs(0.5*(0.0 + 6.0*pow(x1,2)/(1.0 + pow(x1,2)) - 22.0*pow(x1,3)/(1.0 + pow(x1,2)) + 2.0*pow(x1,3)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 12.0*pow(x1,4)/(1.0 + pow(x1,2)) - 12.0*pow(x1,4)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 18.0*pow(x1,5)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) - 3.0*(-x1 - 2.0*x2 + 3.0*pow(x1,2))/pow((1.0 + pow(x1,2)),2) - 12.0*x2*x1/(1.0 + pow(x1,2)) + 8.0*x2*pow(x1,2)/(1.0 + pow(x1,2)) - 8.0*x2*pow(x1,2)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 24.0*x2*pow(x1,3)/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) + 8.0*pow(x2,2)*x1/(1.0 + 2.0*pow(x1,2) + pow(x1,4)) - (-x1 + 2.0*x2 + 3.0*pow(x1,2))*(4.0*pow(x1,2)*(1.0 + pow(x1,2)) + (1.0 + pow(x1,2))*(-2.0*pow(x1,2)/(1.0 + pow(x1,2)) + 6.0*pow(x1,3)/(1.0 + pow(x1,2)) + 4.0*x2*x1/(1.0 + pow(x1,2))) + 2.0*x1*(1.0 + pow(x1,2))*(-3.0 - x1/(1.0 + pow(x1,2)) + 3.0*pow(x1,2)/(1.0 + pow(x1,2)) + 2.0*x2/(1.0 + pow(x1,2))) + 3.0*pow(x1,2))/pow((1.0 + pow(x1,2)),2) - 6.0*pow(x1,2))*(1.0 + pow(x1,2))) + 2*fabs(1.5*pow(x1,2)*(-x1/(1.0 + pow(x1,2)) + 3.0*pow(x1,2)/(1.0 + pow(x1,2)) + 2.0*x2/(1.0 + pow(x1,2)))) + fabs(1.5*(-2.0*x2 + 3.0*pow(x1,2))/(1.0 + pow(x1,2))) + fabs(1.5*(-x1 - 2.0*x2 + 3.0*pow(x1,2))/(1.0 + pow(x1,2))) + fabs(3.0*x2/(1.0 + pow(x1,2))) + 2*fabs(4.5*pow(x1,2)/(1.0 + pow(x1,2))) + fabs(0.5*pow(x1,2)*(1.0 + pow(x1,2))*(-6.0 - 4.0*x1/(1.0 + pow(x1,2)) + 12.0*pow(x1,2)/(1.0 + pow(x1,2)) + 8.0*x2/(1.0 + pow(x1,2)))) + fabs(0.5*pow(x1,2)*(1.0 + pow(x1,2))*(0.0 - 4.0*x1/(1.0 + pow(x1,2)) + 12.0*pow(x1,2)/(1.0 + pow(x1,2)) + 8.0*x2/(1.0 + pow(x1,2)))) + 2*fabs(0.5*(1.0 + pow(x1,2))*(-2.0*pow(x1,2)/(1.0 + pow(x1,2)) + 6.0*pow(x1,3)/(1.0 + pow(x1,2)) + 4.0*x2*x1/(1.0 + pow(x1,2)))*(-3.0 - x1/(1.0 + pow(x1,2)) + 3.0*pow(x1,2)/(1.0 + pow(x1,2)) + 2.0*x2/(1.0 + pow(x1,2)))) + fabs(0.5*(2.0*x2 + 3.0*pow(x1,2))*(4.0*pow(x1,2)*(1.0 + pow(x1,2)) + (1.0 + pow(x1,2))*(-2.0*pow(x1,2)/(1.0 + pow(x1,2)) + 6.0*pow(x1,3)/(1.0 + pow(x1,2)) + 4.0*x2*x1/(1.0 + pow(x1,2))) + 2.0*x1*(1.0 + pow(x1,2))*(-3.0 - x1/(1.0 + pow(x1,2)) + 3.0*pow(x1,2)/(1.0 + pow(x1,2)) + 2.0*x2/(1.0 + pow(x1,2))) + 3.0*pow(x1,2))/(1.0 + pow(x1,2))) + fabs(0.5*(-x1 + 2.0*x2 + 3.0*pow(x1,2))*(4.0*pow(x1,2)*(1.0 + pow(x1,2)) + (1.0 + pow(x1,2))*(-2.0*pow(x1,2)/(1.0 + pow(x1,2)) + 6.0*pow(x1,3)/(1.0 + pow(x1,2)) + 4.0*x2*x1/(1.0 + pow(x1,2))) + 2.0*x1*(1.0 + pow(x1,2))*(-3.0 - x1/(1.0 + pow(x1,2)) + 3.0*pow(x1,2)/(1.0 + pow(x1,2)) + 2.0*x2/(1.0 + pow(x1,2))) + 3.0*pow(x1,2))/(1.0 + pow(x1,2))) + fabs(1.0*x2*(4.0*pow(x1,2)*(1.0 + pow(x1,2)) + (1.0 + pow(x1,2))*(-2.0*pow(x1,2)/(1.0 + pow(x1,2)) + 6.0*pow(x1,3)/(1.0 + pow(x1,2)) + 4.0*x2*x1/(1.0 + pow(x1,2))) + 2.0*x1*(1.0 + pow(x1,2))*(-3.0 - x1/(1.0 + pow(x1,2)) + 3.0*pow(x1,2)/(1.0 + pow(x1,2)) + 2.0*x2/(1.0 + pow(x1,2))) + 3.0*pow(x1,2))/(1.0 + pow(x1,2))) + 2*fabs(1.5*pow(x1,2)*(4.0*pow(x1,2)*(1.0 + pow(x1,2)) + (1.0 + pow(x1,2))*(-2.0*pow(x1,2)/(1.0 + pow(x1,2)) + 6.0*pow(x1,3)/(1.0 + pow(x1,2)) + 4.0*x2*x1/(1.0 + pow(x1,2))) + 2.0*x1*(1.0 + pow(x1,2))*(-3.0 - x1/(1.0 + pow(x1,2)) + 3.0*pow(x1,2)/(1.0 + pow(x1,2)) + 2.0*x2/(1.0 + pow(x1,2))) + 3.0*pow(x1,2))/(1.0 + pow(x1,2))) + fabs(1.0*x1*(1.0 + pow(x1,2))*(-3.0 - x1/(1.0 + pow(x1,2)) + 3.0*pow(x1,2)/(1.0 + pow(x1,2)) + 2.0*x2/(1.0 + pow(x1,2)))*(-x1/(1.0 + pow(x1,2)) + 3.0*pow(x1,2)/(1.0 + pow(x1,2)) + 2.0*x2/(1.0 + pow(x1,2))));

	return err ;

	
}




int main(int argc, char** argv)
{

	srand(time(0));
	FILE *fp;
	int N;
	sscanf(argv[1], "%d", &N);
	fp = fopen("jetEngine_error_profile.csv", "w+");

	__float80 val_dp = 0;
	__float80 val_sp = 0;
	__float80 val_qp = 0;
	__float80 err_dp_sp = 0;
	__float80 err_qp_dp = 0;

	__float80 maxerrdp = 0.0;
	__float80 maxerrsp = 0.0;

	__float80 maxerrstat = 0.0;


	for (int i=0; i<N; i++) {
		
		init<double>();
		__float80 val_sp = (__float80) execute_spec_precision<float>();
		__float80 val_dp = (__float80) execute_spec_precision<double>();
		__float80 val_qp = (__float80) execute_spec_precision<__float128>();

		__float80 errstat = ((__float80) execute_error_expression<double>())*pow(2,-53);

		__float80 local_err_sp = fabs(val_dp - val_sp);
		__float80 local_err_dp = fabs(val_qp - val_dp);
		err_dp_sp += local_err_sp;
		err_qp_dp += local_err_dp;

		if(maxerrsp < local_err_sp) maxerrsp = local_err_sp ;
		if(maxerrdp < local_err_dp) maxerrdp = local_err_dp ;
		if(maxerrstat < errstat) maxerrstat = errstat ;

		//fprintf(fp, "%0.50f, %0.50f, %0.50llf, %0.50llf\n", _x1, _x2, local_err_sp, local_err_dp);
		fprintf(fp, "%0.50f, %0.50f, %0.50llf, %0.50llf\n", _x1, _x2, local_err_dp, errstat);

		assert(maxerrstat >= maxerrdp);
	}

	fclose(fp);

	cout << "Avg Error in DP -> " << err_qp_dp/N << endl ;
	cout << "Avg Error in SP -> " << err_dp_sp/N << endl ;
	cout << "Max Error in DP -> " << maxerrdp << endl ;
	cout << "Max Error in SP -> " << maxerrsp << endl ;
	cout << "Max Error STAT  -> " << maxerrstat << endl ;

	return 1;


}
