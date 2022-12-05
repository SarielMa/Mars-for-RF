#include<iostream>
#include<pthread.h>
#include"my_q.h"
#include"help.h"
using namespace std;
Queue var0 = Queue();

void *thrd1(void* arg)
{
    //Queue * var0=(Queue*)arg;
    int var1 = var0.getlength();
    var0.enqueue(var1);
    int var2 = var0.dequeue();
    var0.enqueue(28);

    pthread_exit((void*)1);
}
void *thrd2(void* arg)
{
    //Queue * var0=(Queue*)arg;
    int var3 = var0.dequeue();
    var0.enqueue(var3);
    int var4 = var0.dequeue();
    var0.enqueue(var4);

    pthread_exit((void*)2);
}
int main()
{
   int err=0;
   pthread_t tid1,tid2;
   void* res;
   pthread_create(&tid1,NULL,thrd1,NULL); 
   pthread_create(&tid2,NULL,thrd2,NULL);
   pthread_join(tid1,&res); 
   pthread_join(tid2,&res); 
   return 0;
}
