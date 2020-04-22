
#include <cstdio>
#include <iostream>
#include <unistd.h>
#include <cstdlib>
#include<cmath>
#include <quadmath.h>
#include <time.h>

#define _low 1.0
#define _high 2.0

using namespace std;


double _x ;
double _y ;
double _z ;

template<class T>
void init() {

	_x = _low + static_cast<T> (rand())/(static_cast<T>(RAND_MAX/(_high - _low))) ;
	_y = _low + static_cast<T> (rand())/(static_cast<T>(RAND_MAX/(_high - _low))) ;
	_z = _low + static_cast<T> (rand())/(static_cast<T>(RAND_MAX/(_high - _low))) ;
}

template<class T>
T execute_spec_precision()
{
  T x = (T) _x ;
  T y = (T) _y ;
  T z = (T) _z ;

  // begin EXPRS
	T x_1_0  = (x + 10.0*(y - x)*0.005);
	T x_1_1  = (y + (28.0*x - y - x*z)*0.005);
	T x_1_2  = (z + (x*y - 2.666667*z)*0.005);
	T x_2_0  = (x_1_0 + 10.0*(x_1_1 - x_1_0)*0.005);
	T x_2_1  = (x_1_1 + (28.0*x_1_0 - x_1_1 - x_1_0*x_1_2)*0.005);
	T x_2_2  = (x_1_2 + (x_1_0*x_1_1 - 2.666667*x_1_2)*0.005);
	T x_3_0  = (x_2_0 + 10.0*(x_2_1 - x_2_0)*0.005);
	T x_3_1  = (x_2_1 + (28.0*x_2_0 - x_2_1 - x_2_0*x_2_2)*0.005);
	T x_3_2  = (x_2_2 + (x_2_0*x_2_1 - 2.666667*x_2_2)*0.005);
	T x_4_0  = (x_3_0 + 10.0*(x_3_1 - x_3_0)*0.005);
	T x_4_1  = (x_3_1 + (28.0*x_3_0 - x_3_1 - x_3_0*x_3_2)*0.005);
	T x_4_2  = (x_3_2 + (x_3_0*x_3_1 - 2.666667*x_3_2)*0.005);
	T x_5_0  = (x_4_0 + 10.0*(x_4_1 - x_4_0)*0.005);
	T x_5_1  = (x_4_1 + (28.0*x_4_0 - x_4_1 - x_4_0*x_4_2)*0.005);
	T x_5_2  = (x_4_2 + (x_4_0*x_4_1 - 2.666667*x_4_2)*0.005);
	T x_6_0  = (x_5_0 + 10.0*(x_5_1 - x_5_0)*0.005);
	T x_6_1  = (x_5_1 + (28.0*x_5_0 - x_5_1 - x_5_0*x_5_2)*0.005);
	T x_6_2  = (x_5_2 + (x_5_0*x_5_1 - 2.666667*x_5_2)*0.005);
	T x_7_0  = (x_6_0 + 10.0*(x_6_1 - x_6_0)*0.005);
	T x_7_1  = (x_6_1 + (28.0*x_6_0 - x_6_1 - x_6_0*x_6_2)*0.005);
	T x_7_2  = (x_6_2 + (x_6_0*x_6_1 - 2.666667*x_6_2)*0.005);
	T x_8_0  = (x_7_0 + 10.0*(x_7_1 - x_7_0)*0.005);
	T x_8_1  = (x_7_1 + (28.0*x_7_0 - x_7_1 - x_7_0*x_7_2)*0.005);
	T x_8_2  = (x_7_2 + (x_7_0*x_7_1 - 2.666667*x_7_2)*0.005);
	T x_9_0  = (x_8_0 + 10.0*(x_8_1 - x_8_0)*0.005);
	T x_9_1  = (x_8_1 + (28.0*x_8_0 - x_8_1 - x_8_0*x_8_2)*0.005);
	T x_9_2  = (x_8_2 + (x_8_0*x_8_1 - 2.666667*x_8_2)*0.005);
	T x_10_0  = (x_9_0 + 10.0*(x_9_1 - x_9_0)*0.005);
	T x_10_1  = (x_9_1 + (28.0*x_9_0 - x_9_1 - x_9_0*x_9_2)*0.005);
	T x_10_2  = (x_9_2 + (x_9_0*x_9_1 - 2.666667*x_9_2)*0.005);
	T x_11_0  = (x_10_0 + 10.0*(x_10_1 - x_10_0)*0.005);
	T x_11_1  = (x_10_1 + (28.0*x_10_0 - x_10_1 - x_10_0*x_10_2)*0.005);
	T x_11_2  = (x_10_2 + (x_10_0*x_10_1 - 2.666667*x_10_2)*0.005);
	T x_12_0  = (x_11_0 + 10.0*(x_11_1 - x_11_0)*0.005);
	T x_12_1  = (x_11_1 + (28.0*x_11_0 - x_11_1 - x_11_0*x_11_2)*0.005);
	T x_12_2  = (x_11_2 + (x_11_0*x_11_1 - 2.666667*x_11_2)*0.005);
	T x_13_0  = (x_12_0 + 10.0*(x_12_1 - x_12_0)*0.005);
	T x_13_1  = (x_12_1 + (28.0*x_12_0 - x_12_1 - x_12_0*x_12_2)*0.005);
	T x_13_2  = (x_12_2 + (x_12_0*x_12_1 - 2.666667*x_12_2)*0.005);
	T x_14_0  = (x_13_0 + 10.0*(x_13_1 - x_13_0)*0.005);
	T x_14_1  = (x_13_1 + (28.0*x_13_0 - x_13_1 - x_13_0*x_13_2)*0.005);
	T x_14_2  = (x_13_2 + (x_13_0*x_13_1 - 2.666667*x_13_2)*0.005);
	T x_15_0  = (x_14_0 + 10.0*(x_14_1 - x_14_0)*0.005);
	T x_15_1  = (x_14_1 + (28.0*x_14_0 - x_14_1 - x_14_0*x_14_2)*0.005);
	T x_15_2  = (x_14_2 + (x_14_0*x_14_1 - 2.666667*x_14_2)*0.005);
	T x_16_0  = (x_15_0 + 10.0*(x_15_1 - x_15_0)*0.005);
	T x_16_1  = (x_15_1 + (28.0*x_15_0 - x_15_1 - x_15_0*x_15_2)*0.005);
	T x_16_2  = (x_15_2 + (x_15_0*x_15_1 - 2.666667*x_15_2)*0.005);
	T x_17_0  = (x_16_0 + 10.0*(x_16_1 - x_16_0)*0.005);
	T x_17_1  = (x_16_1 + (28.0*x_16_0 - x_16_1 - x_16_0*x_16_2)*0.005);
	T x_17_2  = (x_16_2 + (x_16_0*x_16_1 - 2.666667*x_16_2)*0.005);
	T x_18_0  = (x_17_0 + 10.0*(x_17_1 - x_17_0)*0.005);
	T x_18_1  = (x_17_1 + (28.0*x_17_0 - x_17_1 - x_17_0*x_17_2)*0.005);
	T x_18_2  = (x_17_2 + (x_17_0*x_17_1 - 2.666667*x_17_2)*0.005);
	T x_19_0  = (x_18_0 + 10.0*(x_18_1 - x_18_0)*0.005);
	T x_19_1  = (x_18_1 + (28.0*x_18_0 - x_18_1 - x_18_0*x_18_2)*0.005);
	T x_19_2  = (x_18_2 + (x_18_0*x_18_1 - 2.666667*x_18_2)*0.005);
	T x_20_0  = (x_19_0 + 10.0*(x_19_1 - x_19_0)*0.005);
	T x_20_1  = (x_19_1 + (28.0*x_19_0 - x_19_1 - x_19_0*x_19_2)*0.005);
	T x_20_2  = (x_19_2 + (x_19_0*x_19_1 - 2.666667*x_19_2)*0.005);

	return x_20_1 ;
}


int main(int argc, char** argv)
{

	srand(time(0));
	FILE *fp ;
	int N;
	sscanf(argv[1], "%d", &N) ;
	fp = fopen("lorentz20_error_profile.csv", "w+");

	__float80 val_dp = 0;
	__float80 val_sp = 0;
	__float80 val_qp = 0;
	__float80 err_dp_sp = 0;
	__float80 err_qp_dp = 0;

	//int N = 100000 ;
	
	__float80 maxerrdp = 0.0 ;
	__float80 maxerrsp = 0.0 ;


	for (int i=0; i<N; i++) {

		init<double>();
		__float80 val_sp = (__float80) execute_spec_precision<float>();
		__float80 val_dp = (__float80) execute_spec_precision<double>();
		__float80 val_qp   = (__float80) execute_spec_precision<__float128>();

		err_dp_sp += fabs(val_dp - val_sp);
		err_qp_dp += fabs(val_qp - val_dp);
			if( maxerrdp < fabs(val_qp - val_dp)) maxerrdp = fabs(val_qp - val_dp) ;
		if( maxerrsp < fabs(val_dp - val_sp)) maxerrsp = fabs(val_dp - val_sp) ;
	fprintf(fp, "%0.50llf, %0.50llf\n",  fabs(val_dp - val_sp), fabs(val_qp - val_dp));

	}
	fclose(fp);

	cout << "Avg Error in DP -> " << err_qp_dp/N << endl ;
	cout << "Avg Error in SP -> " << err_dp_sp/N << endl ;
	cout << "Max Error in DP -> " << maxerrdp << endl ;
	cout << "Max Error in SP -> " << maxerrsp << endl ;

	return 1;


}
