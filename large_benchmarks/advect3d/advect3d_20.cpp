#include <cstdio>
#include <iostream>
#include <unistd.h>
#include <cstdlib>
#include<cmath>
#include <quadmath.h>
#include <time.h>
#include <cassert>

#define _low 1.0
#define _high 2.0

using namespace std ;
double _a_20_20_20	 	;
double _a_21_20_20	 	;
double _a_19_20_20	 	;
double _a_23_20_20	 	;
double _a_22_20_20	 	;
double _a_18_20_20	 	;
double _a_17_20_20	 	;
double _a_20_21_20	 	;
double _a_20_19_20	 	;
double _a_20_22_20	 	;
double _a_20_18_20	 	;
double _a_20_23_20	 	;
double _a_20_17_20	 	;
double _a_20_20_21	 	;
double _a_20_20_19	 	;
double _a_20_20_22	 	;
double _a_20_20_18	 	;
double _a_20_20_23	 	;
double _a_20_20_17	 	;
double _uyb_21_20_20	;
double _uyb_20_20_20	;
double _uxl_20_20_20	;
//double _uxl_20_20_20	;
double _uzf_20_20_21	;
double _uzf_20_20_20	;


template<class T>
void init() {

 _a_20_20_20	 	= _low + static_cast<T> (rand())/(static_cast<T>(RAND_MAX/(_high - _low)));
 _a_21_20_20	 	= _low + static_cast<T> (rand())/(static_cast<T>(RAND_MAX/(_high - _low)));
 _a_19_20_20	 	= _low + static_cast<T> (rand())/(static_cast<T>(RAND_MAX/(_high - _low)));
 _a_23_20_20	 	= _low + static_cast<T> (rand())/(static_cast<T>(RAND_MAX/(_high - _low)));
 _a_22_20_20	 	= _low + static_cast<T> (rand())/(static_cast<T>(RAND_MAX/(_high - _low)));
 _a_18_20_20	 	= _low + static_cast<T> (rand())/(static_cast<T>(RAND_MAX/(_high - _low)));
 _a_17_20_20	 	= _low + static_cast<T> (rand())/(static_cast<T>(RAND_MAX/(_high - _low)));
 _a_20_21_20	 	= _low + static_cast<T> (rand())/(static_cast<T>(RAND_MAX/(_high - _low)));
 _a_20_19_20	 	= _low + static_cast<T> (rand())/(static_cast<T>(RAND_MAX/(_high - _low)));
 _a_20_22_20	 	= _low + static_cast<T> (rand())/(static_cast<T>(RAND_MAX/(_high - _low)));
 _a_20_18_20	 	= _low + static_cast<T> (rand())/(static_cast<T>(RAND_MAX/(_high - _low)));
 _a_20_23_20	 	= _low + static_cast<T> (rand())/(static_cast<T>(RAND_MAX/(_high - _low)));
 _a_20_17_20	 	= _low + static_cast<T> (rand())/(static_cast<T>(RAND_MAX/(_high - _low)));
 _a_20_20_21	 	= _low + static_cast<T> (rand())/(static_cast<T>(RAND_MAX/(_high - _low)));
 _a_20_20_19	 	= _low + static_cast<T> (rand())/(static_cast<T>(RAND_MAX/(_high - _low)));
 _a_20_20_22	 	= _low + static_cast<T> (rand())/(static_cast<T>(RAND_MAX/(_high - _low)));
 _a_20_20_18	 	= _low + static_cast<T> (rand())/(static_cast<T>(RAND_MAX/(_high - _low)));
 _a_20_20_23	 	= _low + static_cast<T> (rand())/(static_cast<T>(RAND_MAX/(_high - _low)));
 _a_20_20_17	 	= _low + static_cast<T> (rand())/(static_cast<T>(RAND_MAX/(_high - _low)));
 _uyb_21_20_20		= _low + static_cast<T> (rand())/(static_cast<T>(RAND_MAX/(_high - _low)));
 _uyb_20_20_20		= _low + static_cast<T> (rand())/(static_cast<T>(RAND_MAX/(_high - _low)));
 _uxl_20_20_20		= _low + static_cast<T> (rand())/(static_cast<T>(RAND_MAX/(_high - _low)));
// _uxl_20_20_20		= _low + static_cast<T> (rand())/(static_cast<T>(RAND_MAX/(_high - _low)));
 _uzf_20_20_21		= _low + static_cast<T> (rand())/(static_cast<T>(RAND_MAX/(_high - _low)));
 _uzf_20_20_20		= _low + static_cast<T> (rand())/(static_cast<T>(RAND_MAX/(_high - _low)));
}

template<class T>
T execute_spec_precision()
{

	T	a_20_20_20	 	=	(T)	_a_20_20_20	 	;  
	T	a_21_20_20	 	=	(T)	_a_21_20_20	 	;  
	T	a_19_20_20	 	=	(T)	_a_19_20_20	 	;  
	T	a_23_20_20	 	=	(T)	_a_23_20_20	 	;  
	T	a_22_20_20	 	=	(T)	_a_22_20_20	 	;  
	T	a_18_20_20	 	=	(T)	_a_18_20_20	 	;  
	T	a_17_20_20	 	=	(T)	_a_17_20_20	 	;  
	T	a_20_21_20	 	=	(T)	_a_20_21_20	 	;  
	T	a_20_19_20	 	=	(T)	_a_20_19_20	 	;  
	T	a_20_22_20	 	=	(T)	_a_20_22_20	 	;  
	T	a_20_18_20	 	=	(T)	_a_20_18_20	 	;  
	T	a_20_23_20	 	=	(T)	_a_20_23_20	 	;  
	T	a_20_17_20	 	=	(T)	_a_20_17_20	 	;  
	T	a_20_20_21	 	=	(T)	_a_20_20_21	 	;  
	T	a_20_20_19	 	=	(T)	_a_20_20_19	 	;  
	T	a_20_20_22	 	=	(T)	_a_20_20_22	 	;  
	T	a_20_20_18	 	=	(T)	_a_20_20_18	 	;  
	T	a_20_20_23	 	=	(T)	_a_20_20_23	 	;  
	T	a_20_20_17	 	=	(T)	_a_20_20_17	 	;  
	T	uyb_21_20_20	=	(T)	_uyb_21_20_20		;  
	T	uyb_20_20_20	=	(T)	_uyb_20_20_20		;  
	T	uxl_20_20_20	=	(T)	_uxl_20_20_20		;  
//	T	uxl_20_20_20	=	(T)	_uxl_20_20_20		;  
	T	uzf_20_20_21	=	(T)	_uzf_20_20_21		;  
	T	uzf_20_20_20	=	(T)	_uzf_20_20_20		;  

	// begin exprs
	T ab_21_20_20 = (0.2 * (a_20_20_20 + a_21_20_20) + 0.5 
                        * (a_19_20_20 + a_22_20_20) + 0.3 * (a_18_20_20 
                            + a_23_20_20)) * 0.3 * uyb_21_20_20;

	T ab_20_20_20 = (0.2 * (a_19_20_20 + a_20_20_20) + 0.5 
                        * (a_18_20_20 + a_21_20_20) + 0.3 * (a_17_20_20 
                            + a_22_20_20)) * 0.3 * uyb_20_20_20;

	T al_20_21_20 = (0.2 * (a_20_20_20 + a_20_21_20) + 0.5 
                        * (a_20_19_20 + a_20_22_20) + 0.3 * (a_20_18_20 + a_20_23_20))
                    * 0.3 * uxl_20_20_20;

	T al_20_20_20 = (0.2 * (a_20_19_20 + a_20_20_20) + 0.5 
                        * (a_20_18_20 + a_20_21_20) + 0.3 * (a_20_17_20 + a_20_22_20))
                    * 0.3 * uxl_20_20_20;

	T af_20_20_21 = (0.2 * (a_20_20_20 + a_20_20_21) + 0.5 
                        * (a_20_20_19 + a_20_20_22) + 0.3 * (a_20_20_18 + a_20_20_23))
                    * 0.3 * uzf_20_20_21;

	T af_20_20_20 = (0.2 * (a_20_20_19 + a_20_20_20) + 0.5 
                        * (a_20_20_18 + a_20_20_21) + 0.3 * (a_20_20_17 + a_20_20_22))
                    * 0.3 * uzf_20_20_20;


	T ath_20_20_20 = a_20_20_20 +
                 (al_20_21_20 - al_20_20_20) +
				 (ab_21_20_20 - ab_20_20_20) +
				 (af_20_20_21 - af_20_20_20) ;

	return ath_20_20_20 ;

}

int main(int argc, char** argv)
{

	srand(time(0));
	FILE *fp ;
	int N;
	sscanf(argv[1], "%d", &N) ;
	fp = fopen("advect3d_error_profile.csv", "w+");

	__float80 val_dp = 0;
	__float80 val_sp = 0;
	__float80 val_qp = 0;
	__float80 err_dp_sp = 0;
	__float80 err_qp_dp = 0;

	//int N = 100000 ;
	__float80 maxsaterr = 2.22e-13 ;
	
	
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
		int emp_sat_lost_bits = ceil(log(fabs(maxsaterr/val_dp)*pow(2,53))/log(2));
		int emp_act_lost_bits = max((int)ceil(log(fabs((val_qp - val_dp)/val_qp)*pow(2,53))/log(2)), 0);
		int diff = emp_sat_lost_bits - emp_act_lost_bits ;
		fprintf(fp, "%d, %d, %d, %d\n",i+1,  emp_sat_lost_bits, emp_act_lost_bits, diff);
		assert(diff > 0);
	//	fprintf(fp, "%0.50llf, %0.50llf\n",  fabs(val_dp - val_sp), fabs(val_qp - val_dp));

	}
	fclose(fp);

	cout << "Avg Error in DP -> " << err_qp_dp/N << endl ;
	cout << "Avg Error in SP -> " << err_dp_sp/N << endl ;
	cout << "Max Error in DP -> " << maxerrdp << endl ;
	cout << "Max Error in SP -> " << maxerrsp << endl ;

	return 1;


}
