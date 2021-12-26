#include <iostream>
#include<fstream> 			//File output
#include<math.h> 			//The main production waveform uses the SIN function, so I got this header

using namespace std;
float dou = 256; 			//The frequency of the sound dou is 264, here is 256 HZ for rounding up  

struct WavHead{
 char RIFF[4];    			//The RIFF in the first part
 long int size0;			//Save the size of all files behind
 char WAVE[4];
 char FMT[4];
 long int size1;			//Stored is the size saved by fmt, after including this, the first few data, a total of 16
 short int fmttag;
 short int channel;
 long int samplespersec;	//The number of samples per second, using 11025
 long int bytepersec;
 short int blockalign;
 short int bitpersamples;
 char DATA[4];
 long int size2;			//The remaining file size, that is, the size of the sound sample, because it is one second of content, then it is 11025.

};

int main() {

    WavHead head={{'R','I','F','F'},0,{'W','A','V','E'},{'f','m','t',' '},16,
            1,1,11025,11025,1,8,{'d','a','t','a'},
		0};					//Initialization, did not assign the size of the sound sample file, modify it later
    head.size0=11025+16+8;
    head.size2=11025;
    char body[head.size2];	//Intend to put the sampled data in this
    int i,i2;				//In order that the sound is not very monotonous, two loops are used. The inner layer i generates sound functions, and the outer layer i2 generates different frequencies.
    float a=(head.samplespersec/dou);//It is the dou duration (1/dou) divided by the number of samples (1/head.samplespersec), that is, there are a sampling points in a dou waveform, here it is 43.
    for (i2=1;i2<=2;i2++){	//There are two sounds here, one is 256HZ and the other is 512HZ

        for(i=0+head.size2/2*(i2-1);i<head.size2/2*i2;i++){

                body[i]=(int)(64*sin(6.28/a*i*i2)+128);//This wave uses the sine function, a sine wave centered on 128 (ox80). In fact, when the sampling point is 0x80, it is muted. If the sampling point is 0x80, it is positive, and if it is less than 0x80, it is negative. The first 64 is the sound level, which is equal to At 128, the generated sound is the loudest
        }

    }
    ofstream ocout;
    ocout.open("123.wav",ios::out|ios::binary);//Open (generated if it does not exist) 123.wav

    ocout.write((char*)&head,sizeof head);//Write the header part of the file into the file
    ocout.write((char*)&body,sizeof body);//Write data file to program

    ocout.close();//Close file
    cout <<head.samplespersec <<" "<<dou<< endl; //  Check if the file size is wrong when debugging
    return 0;

	//next steps: either understanding how we go about writing these wav files or I look into realtime audio implementation in c++
}