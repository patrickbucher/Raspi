all: blink push_button

blink: blink.c
	gcc -Wall -o blink blink.c -lwiringPi

push_button: push_button.c
	gcc -Wall -o push_button push_button.c -lwiringPi

clean:
	rm -f blink push_button
