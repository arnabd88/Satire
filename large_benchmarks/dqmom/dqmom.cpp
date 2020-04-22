

#include <cstdio>
#include <iostream>
#include <unistd.h>
#include <cstdlib>
#include<cmath>
#include <quadmath.h>
#include <time.h>

#define _a0_low 0.00001
#define _a0_high 1.0
#define _a1_low 0.00001
#define _a1_high 1.0
#define _a2_low 0.00001
#define _a2_high 1.0

#define _w0_low 0.00001
#define _w0_high 1.0
#define _w1_low 0.00001
#define _w1_high 1.0
#define _w2_low 0.00001
#define _w2_high 1.0

#define _m0_low -1.0
#define _m0_high 1.0
#define _m1_low -1.0
#define _m1_high 1.0
#define _m2_low -1.0
#define _m2_high 1.0


using namespace std;

double _a0 ;
double _a1 ;
double _a2 ;

double _m0;
double _m1;
double _m2;

double _w0;
double _w1;
double _w2;


template<class T>
void init() {

	 _a0 = _a0_low + static_cast <T> (rand()) /( static_cast <T> (RAND_MAX/(_a0_high-_a0_low)));
	 _a1 = _a1_low + static_cast <T> (rand()) /( static_cast <T> (RAND_MAX/(_a1_high-_a1_low)));
	 _a2 = _a2_low + static_cast <T> (rand()) /( static_cast <T> (RAND_MAX/(_a2_high-_a2_low)));

	 //cout << _a0 << " , " << _a1 << " , " << _a2 << endl ;

	 _w0 = _w0_low + static_cast <T> (rand()) /( static_cast <T> (RAND_MAX/(_w0_high-_w0_low)));
	 _w1 = _w1_low + static_cast <T> (rand()) /( static_cast <T> (RAND_MAX/(_w1_high-_w1_low)));
	 _w2 = _w2_low + static_cast <T> (rand()) /( static_cast <T> (RAND_MAX/(_w2_high-_w2_low)));

	 _m0 = _m0_low + static_cast <T> (rand()) /( static_cast <T> (RAND_MAX/(_m0_high-_m0_low)));
	 _m1 = _m1_low + static_cast <T> (rand()) /( static_cast <T> (RAND_MAX/(_m1_high-_m1_low)));
	 _m2 = _m2_low + static_cast <T> (rand()) /( static_cast <T> (RAND_MAX/(_m2_high-_m2_low)));

}


template<class T>
T execute_spec_precision()
{

	T a0 = (T) _a0 ;
	T a1 = (T) _a1 ;
	T a2 = (T) _a2 ;

	T m0 = (T) _m0 ;
	T m1 = (T) _m1 ;
	T m2 = (T) _m2 ;

	T w0 = (T) _w0 ;
	T w1 = (T) _w1 ;
	T w2 = (T) _w2 ;

	T e1 = (((w2 * (0.0 - m2)) * (-3.0 * ((1.0 * (a2/w2)) * (a2/w2)))) * 1.0) ;
	T e2 = (((w1 * (0.0 - m1)) * (-3.0 *((1.0 * (a1/w1)) * (a1/w1)))) * 1.0) ;
	T e3 = (((w0 * (0.0 - m0)) * (-3.0 * ((1.0 * (a0/w0)) * (a0/w0)))) * 1.0) ;
	T r = (0.0 + (e1 + (e2 + (e3 + 0.0)))) ;

	//cout << r << endl;

	return r ;
	
}


int main(int argc, char** argv)
{

	srand(time(0));
	FILE *fp ;
	int N;
	sscanf(argv[1], "%d", &N);
	fp = fopen("dqmom_error_profile.csv", "w+");

	__float80 val_dp = 0;
	__float80 val_sp = 0;
	__float80 val_qp = 0;
	__float80 err_dp_sp = 0;
	__float80 err_qp_dp = 0;

	//int N = 1000000 ;
	
	__float80 maxerrdp = 0.0 ;
	__float80 maxerrsp = 0.0 ;

	__float80 maxsaterr = 9.992007221626417e-10 ;
	

	fprintf(fp, "%s, %s, %s, %s\n", "iter", "sat-rel-lost-bits", "emp-lost-bits", "difference");
	for (int i=0; i<N; i++) {

		init<double>();
		__float80 val_sp = (__float80) execute_spec_precision<float>();
		__float80 val_dp = (__float80) execute_spec_precision<double>();
		__float80 val_qp   = (__float80) execute_spec_precision<__float128>();

		err_dp_sp += fabs(val_dp - val_sp);
		err_qp_dp += fabs(val_qp - val_dp);
		if( maxerrdp < fabs(val_qp - val_dp)) maxerrdp = fabs(val_qp - val_dp) ;
		if( maxerrsp < fabs(val_dp - val_sp)) maxerrsp = fabs(val_dp - val_sp) ;		
		int emp_sat_lost_bits = ceil(log(fabs(maxsaterr/val_dp)*pow(2,53))/log(2));
		int emp_act_lost_bits = max((int)ceil(log(fabs((val_qp - val_dp)/val_qp)*pow(2,53))/log(2)), 0);
		fprintf(fp, "%d, %d, %d, %d\n",i+1,  emp_sat_lost_bits, emp_act_lost_bits, emp_sat_lost_bits-emp_act_lost_bits);
		//fprintf(fp, "%d, %0.50llf, %0.50llf, %d, %d, %d\n",i+1,  fabs(val_dp - val_sp), fabs(val_qp - val_dp), emp_sat_lost_bits, emp_act_lost_bits, emp_sat_lost_bits-emp_act_lost_bits);
		//cout << fabs(val_dp - val_sp) << " , " <<  fabs(val_qp - val_dp) << endl ;

		//cout << fabs(val_double - val_quad) << endl ;
		//printf("Err = %0.50llf\n", fabs(val_quad - val_double)) ;
		//cout << val_double - val_quad << endl ;
		//printf("Err = %0.50llf\n", fabs(val_quad - val_double)) ;

	}
	fclose(fp);

	cout << "Avg Error in DP -> " << err_qp_dp/N << endl ;
	cout << "Avg Error in SP -> " << err_dp_sp/N << endl ;
	cout << "Max Error in DP -> " << maxerrdp << endl ;
	cout << "Max Error in SP -> " << maxerrsp << endl ;	

	return 1;


}
