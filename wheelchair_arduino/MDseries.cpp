#include "MDseries.h"
#include "Arduino.h"

void MD_Packet(char rmid, char tmid, char id, char pid, char num, int data)
{
   char md_protocol[7+num] = {0,};
   unsigned char data_1 = 0;
   unsigned char data_2 = 0;
   unsigned char chk = 0;
   int i = 0;

   if(num == 1)
   {
      data_1 = (0x00FF)&data;

      md_protocol[i++] = rmid;
      md_protocol[i++] = tmid;
      md_protocol[i++] = id;
      md_protocol[i++] = pid;
      md_protocol[i++] = num;
      md_protocol[i++] = data_1;
   }
   else if(num == 2)
   {
      data_1 = (0x00FF)&data;
      data_2 = ((0xFF00)&data)>>8;

      md_protocol[i++] = rmid;
      md_protocol[i++] = tmid;
      md_protocol[i++] = id;
      md_protocol[i++] = pid;
      md_protocol[i++] = num;
      md_protocol[i++] = data_1;
      md_protocol[i++] = data_2;  
   }

   chk = Checksum(i, md_protocol);

   md_protocol[i++] = chk;

   Serial1.write(md_protocol, i);
//   Serial.write(md_protocol, i);
}

char Checksum(short nPacketSize, char* byArray)
{
  char byTmp = 0;
  short i;

  for(i=0;i<nPacketSize;i++) byTmp += *(byArray+i);
  return (~byTmp + 1);
}
