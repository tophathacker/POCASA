// Build command:  gcc IOToggle_Clib.c -o IOToggle_Clib -I/usr/local/include -L/usr/local/lib -lwiringPi
#define DEBUG

//#include <python.h>
#include <wiringPi.h>
#include <unistd.h>
//#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <ncurses.h>
#include <time.h>

int main (int argc, char **argv)
{

  if (wiringPiSetup () == -1)
    exit (1) ;
  int ClockPin = 0;
  int DataPin = 1;
  int DumpPin = 2;
  int buttonPin1 = 7;
  int buttonPin2 = 3;
  unsigned char dataAr[] = "UU";
  setupShift(ClockPin,DataPin,DumpPin);
  setupButton(buttonPin1);
  setupButton(buttonPin2);

  int currentString = 0;

  for (;;)
  {
    shiftOut(ClockPin,DataPin,DumpPin,"UU");
  }
  for (;;)
  {
    if(digitalRead(buttonPin1) == 0)
    {
      currentString = (currentString + 1) % 3;
      while(digitalRead(buttonPin1) == 0)
        pauseMe(100);
    }
    if(digitalRead(buttonPin2) == 0)
    {
      currentString = 3;
      while(digitalRead(buttonPin2) == 0)
        pauseMe(100);
    }
    switch(currentString)
    {
      case 0:
        shiftOut(ClockPin,DataPin,DumpPin,"UU");
        break;
      case 1:
        shiftOut(ClockPin,DataPin,DumpPin,"RU");
        break;
      case 2:
        shiftOut(ClockPin,DataPin,DumpPin,"00");
        break;
      case 3:
        shiftOut(ClockPin,DataPin,DumpPin,"\0\0");
        break;
    }

  }

  return 0 ;
}

int setupButton(int button)
{
  pinMode(button,INPUT);
}

int setupShift(int clock, int data, int dump)
{
  //setup pins
  pinMode(clock,OUTPUT);
  digitalWrite(clock,0);
  pinMode(data,OUTPUT);
  digitalWrite(data,0);
  pinMode(dump,OUTPUT);
  digitalWrite(dump,0);
  return 0;
}

int pauseMe(int time)
{
  int i;
  for(i=0; i<time; i++);
}


int shiftOut(int clock, int data, int dump, char input[])
{

  int counter = 0;
  int i,j,k;

  for(j=0; j<2; j++)
  {
    char current = input[j];
    for(i=0; i < 8; i++)
    {
      digitalWrite(data,current & 1);
      current >>= 1;
      digitalWrite(clock,1);
      //pauseMe(10);
      digitalWrite(clock,0);
      //pauseMe(10);
    }
  }

  digitalWrite(dump,1);
  //pauseMe(10);
  digitalWrite(dump,0);
  pauseMe(200);
  return 0;
}
