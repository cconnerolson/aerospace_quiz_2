# Aerospace Propulsion Quiz 2

1) For combustion chamber stagnation temperature of 2000K, and inlet temperature of 223 K for a ramjet flying at altitude where the atmospheric pressure is 16.5 kPa, conduct an ideal analysis with perfect gas assumption and plot specific thrust variation with inlet flight Mach number for the regime M<sub>0</sub> = 1.5\-4.0.  Identify where max specific thrust occurs.  __**Don’t neglect fuel air ratio in your computations.**__  Assume calorific value of fuel as 43,000 KJ/kg.    \(2\)

2) Starting with perfect gas assumption, relax the condition P<sub>0</sub> = P<sub>4</sub> and design an optimal nozzle by selecting an area ratio A<sub>4</sub>/A<sup>\*</sup>, such that there is no normal shock at the exit and the optimal nozzle closely approximates the specific thrust of part (1). This requires starting with an M<sub>4</sub> = M0<sup>\*</sup>, where M0<sup>\*</sup> is given by equation (A) and then plugging into equation (B) to get the nozzle shape, and then computing the specific thrust for Mach numbers M<sub>0</sub> 1.5 – 4, with both momentum and pressure thrust components. Note P<sub>4</sub> varies for each M<sub>0</sub> and is given by the equation (C). Optimization requires rerunning the code for slightly different area ratios (two higher and two lower) and checking the specific thrust outcome. Don’t neglect air fuel ratio.    \(4\)

3) Introduce a diffuser efficiency of &Pi;<sub>d</sub> = 1 − 0.08  (M<sub>0</sub> − 1)<sup>1.1</sup> and assume that the combustor and the nozzle are 100\% efficient and modify design \(2\) to get the most optimal performance and plot specific thrust as a function of flight Mach number in the same 1.5\-4.0 regime.  __**Again don’t neglect fuel air ratio.**__    \(2\)

4) For the chosen design of problem \(3\), i.e, fixed nozzle shape, redo the specific thrust calculations using real properties of the working fluid for computation of fuel air ratio, and exit temperature and Mach Number in the same inlet Mach number regime of 1.5\-4.0.    \(2\)



### Design Considerations

1. Ideal (dont neglect *f*).
    * air is a perfect gas
    * Pressure:
      * diffuser is idea; &Pi;<sub>d</sub> = (P<sub>at</sub> / P<sub>0t</sub>) = 1
      * ideal combustion chamber; &Pi;<sub>b</sub> = (P<sub>3t</sub> / P<sub>2t</sub>) = 1
      * ideal nozzle; &Pi;<sub>n</sub> = (P<sub>4t</sub> / P<sub>3t</sub>) = 1
      * P<sub>4</sub> = P<sub>0</sub>
    * Temperature:
      * &Pi;<sub>a</sub> = (T<sub>2t</sub> / T<sub>0t</sub>) = 1
      * &Pi;<sub>c</sub> = (T<sub>3t</sub> / T<sub>2t</sub>) = heat work
      * &Pi;<sub>n</sub> = (T<sub>4t</sub> / T<sub>3t</sub>) = 1
2. Fit realistic nozzle.
3. Relax Perfect Gas Assumptions.
4. Bring in inefficiencies.
    * tolerable stagnation pressure loss = 10\%


## Running The Code

Run any problem in the terminal as shown below:

`~$ python3 /path/problem_{}.py`

Data will be saved to /data/, plots will be saved to /plots/ and opened in their own window.


### License

[MIT](https://choosealicense.com/licenses/mit/)
