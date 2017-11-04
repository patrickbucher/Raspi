#include <wiringPi.h>

#define START_BLINK 3

void blink_green(int millis)
{
    digitalWrite(17, HIGH);
    delay(millis);
    digitalWrite(17, LOW);
}

void blink_red(int millis)
{
    digitalWrite(4, HIGH);
    delay(millis);
    digitalWrite(4, LOW);
}
void blink(int millis)
{
    digitalWrite(4, HIGH);
    digitalWrite(17, HIGH);
    delay(millis);
    digitalWrite(4, LOW);
    digitalWrite(17, LOW);
}

int main()
{
    wiringPiSetupGpio();
    pinMode(4, OUTPUT);
    pinMode(17, OUTPUT);
    pinMode(27, INPUT);

    for (int i = 0; i < START_BLINK; i++) {
        blink(200);
        if (i < START_BLINK - 1) {
            delay(200);
        }
    }

    for (;;) {
        while (digitalRead(27) == LOW);
        blink_red(100);
        while (digitalRead(27) == HIGH);
        blink_green(100);
    }

    return 0;
}
