const int red_pin = 9;
const int green_pin = 10;
const int blue_pin = 11;

const int relay_pin = 2;
const int button_pin = 3;

int red_value = 0;
int green_value = 0;
int blue_value = 0;

volatile byte state = LOW;

void setup()
{
    Serial.begin(9600);

    pinMode(red_pin, OUTPUT);
    pinMode(green_pin, OUTPUT);
    pinMode(blue_pin, OUTPUT);

    pinMode(relay_pin, OUTPUT);
    pinMode(button_pin, INPUT_PULLUP);
    attachInterrupt(digitalPinToInterrupt(button_pin), change_state, RISING);
}

void change_state() {
    state = !state;
}

String message = "";

void loop()
{
    analogWrite(red_pin, red_value);
    analogWrite(green_pin, green_value);
    analogWrite(blue_pin, blue_value);

    digitalWrite(relay_pin, state);

    if (Serial.available())
    {
        message = Serial.readStringUntil('\n');

        String s = message.substring(0, 3);
        red_value = s.toInt();
        s = message.substring(4, 7);
        green_value = s.toInt();
        s = message.substring(8, 11);
        blue_value = s.toInt();
    }

    Serial.println(message);
    delay(100);
}
