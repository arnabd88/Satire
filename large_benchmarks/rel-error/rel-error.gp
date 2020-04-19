
set terminal postscript enhanced color font 'Helvetica, 11'

set output "rel-error-out.eps"
unset xlabel
unset ylabel

unset key


set multiplot layout 3,2 rowsfirst

POS = "at graph 0.12, 0.9 font ', 10'"
NOYTICS = "set format y ''; unset ylabel"
NOXTICS = "set format x ''; unset xlabel;" 
XTICS = "unset format x; set xlabel; set xtics 4000;"
YTICS = "unset format y; set ylabel; set ytics 10"
YTICS0 = "unset format y; set ylabel; set ytics 20"
YTICS1 = "unset format y; set ylabel; set ytics 5"
YTICS2 = "unset format y; set ylabel; set ytics 5"

noxlabel = "unset xlabel"
noylabel = "unset ylabel"
xlabel = "set xlabel '# of simulations'"
ylabel = "set ylabel '#bits diff using satire vs shadow value'"


TBMARGIN_0 = "set tmargin at screen 0.95; set bmargin at screen 0.50"
TBMARGIN_1 = "set tmargin at screen 0.50; set bmargin at screen 0.10"

LRMARGIN_0 = "set lmargin at screen 0.05; set rmargin at screen 0.27"
LRMARGIN_1 = "set lmargin at screen 0.28; set rmargin at screen 0.50"
LRMARGIN_2 = "set lmargin at screen 0.51; set rmargin at screen 0.73"
LRMARGIN_3 = "set lmargin at screen 0.74; set rmargin at screen 0.96"

set yrange[0:10]
set xrange[1:10000]
@NOXTICS; @YTICS1 ; @ylabel; @noxlabel
@TBMARGIN_0; @LRMARGIN_0
set label 1 'H0' @POS
	plot 'heat2d0_t32_error_profile.csv' using 1:4 pt 6 ps 0.2  


@NOXTICS; @NOYTICS ; @noylabel ; @noxlabel
@TBMARGIN_0; @LRMARGIN_1
set label 1 'C0' @POS
	plot 'convecdiff2d0_t32_error_profile.csv' using 1:4 pt 6 ps 0.2 
	#plot 'convecdiff2d0_t32_error_profile.csv' using 1:4 pt 6 ps 0.2 lc rgb "blue" 


@NOXTICS; @NOYTICS ; @noylabel ; @noxlabel
@TBMARGIN_0; @LRMARGIN_2
set label 1 'P0' @POS
	plot 'poisson2d0_t32_error_profile.csv' using 1:4 pt 6 ps 0.2 


@NOXTICS; @NOYTICS ; @noylabel ; @noxlabel
@TBMARGIN_0; @LRMARGIN_3
set label 1 'Prefix-sum' @POS
	plot 'Scan_1024_error_profile.csv' using 1:4 pt 6 ps 0.2


set yrange[0:30]
@XTICS; @YTICS1 ; @ylabel ; @xlabel
@TBMARGIN_1; @LRMARGIN_0
set label 1 'dqmom' @POS
	plot 'dqmom_error_profile.csv' using 1:4 pt 6 ps 0.2 

@XTICS; @NOYTICS ; @noylabel ; @xlabel
@TBMARGIN_1; @LRMARGIN_1
set label 1 'fdtd' @POS
	plot 'fdtd1d_t64_error_profile.csv' using 1:4 pt 6 ps 0.2 

@XTICS; @NOYTICS ; @noylabel ; @xlabel
@TBMARGIN_1; @LRMARGIN_2
set label 1 'fft' @POS
	plot 'fft_1024_error_profile.csv' using 1:4 pt 6 ps 0.2 


@XTICS; @NOYTICS ; @noylabel ; @xlabel
@TBMARGIN_1; @LRMARGIN_3
set label 1 'lorenz20' @POS
	plot 'lorentz20_error_profile.csv' using 1:4 pt 6 ps 0.2 


