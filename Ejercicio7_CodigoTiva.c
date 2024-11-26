#include <stdint.h>
#include <stdbool.h>
#include "inc/hw_types.h"
#include "inc/hw_memmap.h"
#include "driverlib/sysctl.h"
#include "driverlib/gpio.h"
#include "driverlib/pin_map.h"
#include "driverlib/pwm.h"
#include "driverlib/uart.h"

// Motor control functions
void init_UART(void) {
    // UART initialization code for Tiva here
}

void init_motors(void) {
    // Motor initialization code (e.g., PWM, GPIO setup)
}

void move_forward(void) {
    // Code to move the motors forward
    // Set motor pins for forward direction
}

void move_left(void) {
    // Code to turn the robot left
    // Adjust motor pins for left turn
}

void move_right(void) {
    // Code to turn the robot right
    // Adjust motor pins for right turn
}

void turn_slowly(void) {
    // Code to make the robot turn slowly (rotate in place or move in a small circle)
}

void stop_movement(void) {
    // Code to stop the motors
    // Turn off motor PWM signals
}

void toggle_leds(void) {
    // Toggle two LEDs
    static bool led_state = false;
    led_state = !led_state;
    if (led_state) {
        // Turn on LEDs
    } else {
        // Turn off LEDs
    }
}

int main(void) {
    init_UART();  // Initialize UART communication
    init_motors(); // Initialize motor control

    while (1) {
        if (UARTCharsAvail(UART0_BASE)) {
            char command = UARTCharGet(UART0_BASE);  // Get the received command

            if (command == 'C') {  // 'C' for CENTER
                move_forward();  // Move forward if object is in the center
            } else if (command == 'L') {  // 'L' for LEFT
                move_left();  // Turn left if object is on the left
            } else if (command == 'R') {  // 'R' for RIGHT
                move_right();  // Turn right if object is on the right
            } else if (command == 'T') {  // 'T' for TOGGLE_LEDS
                toggle_leds();  // Toggle LEDs if two objects are detected
            } else if (command == 'S') {  // 'S' for TURN_SLOWLY
                turn_slowly();  // Turn around slowly if no object is detected
            } else {
                stop_movement();  // Stop if no recognized command
            }
        }
    }
}
