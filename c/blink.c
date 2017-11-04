#include <wiringPi.h>

int main()
{
    wiringPiSetupGpio();
    pinMode(4, OUTPUT);
    for (;;) {
        digitalWrite(4, HIGH);
        delay(500);
        digitalWrite(4, LOW);
        delay(500);
    }
    return 0;
}
