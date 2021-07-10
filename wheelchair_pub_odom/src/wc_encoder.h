#include <iostream>

#define WHEEL_RADIUS 0.17
#define PI 3.1415927
#define lengthBetweenWheels 0.52

using namespace std;

typedef struct
{
    double l_heel_vel;
    double r_heel_vel;
    
}HEELVEL;

class ENCODER
{
    public:
            ENCODER();
            void UpdateEncoder(int l_pulse, int r_pulse, double Tc, double PPR);
            void ThicktoRPM();
            void TimetoRPM();
            void RPMtoVelocity();
            HEELVEL SubVelocity();
            HEELVEL SubTmethod();
    private:
            double _Tc;
            double _PPR;
            int _lpulse, _rpulse;
            double lheel_tk_to_rpm, rheel_tk_to_rpm;
            double lheel_rpm_to_vel, rheel_rpm_to_vel;
            double lheel_time_to_rpm, rheel_time_to_rpm;  
    
            
};