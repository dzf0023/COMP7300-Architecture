/********************************************************************\
 * Laboratory Exercise COMP 7300/06                                   *
 * Author: Saad Biaz                                                  *
 * Date  : October 25, 2017                                           *
 * File  : myInitializeMatrix.c  for Lab3                             *
 \*******************************************************************/


/********************************************************************\
 *                    Global system headers                           *
 \********************************************************************/
#include <stdio.h>
#include <stdlib.h>
#include <sys/select.h>
#include <sys/time.h>
#include <string.h>
#include <pthread.h>
#include <unistd.h>

/******************************************************************\
 *                  Global data types                               *
 \******************************************************************/
typedef double          Timestamp;
typedef double          Period;

/**********************************************************************\
 *                      Global definitions                              *
 \**********************************************************************/
#define DIMENSION       40000
#define BLOCKSIZE       125
#define PRINTDIM        7 // Dimension of matrix to display
#define NUMBER_TESTS    7
#define ROWWISE         0
#define COLUMNWISE      1
/**********************************************************************\
 *                      Global data                              *
 \**********************************************************************/
Timestamp StartTime;
double    Matrix[DIMENSION][DIMENSION];
Period    Max[2],Min[2],Avg[2];
unsigned int MaxIndex[2],MinIndex[2];
/**********************************************************************\
 *                        Function prototypes                           *
 \**********************************************************************/
Timestamp   Now();
void        InitializeMatrixRowwise();
//void        InitializeMatrixColumnwise();
void        DisplayUpperQuandrant(unsigned dimension);
void        TransposeMatrixRowwise(void *Nrow);

int main(){
    int choice;
    Timestamp StartInitialize;
    Period    testTime;
    unsigned int i,j,nbreTests;
    
    // Global Initialization
    StartTime       = Now();
    nbreTests       = NUMBER_TESTS;
    Max[ROWWISE]    = 0.00;
    //    Max[COLUMNWISE] = 0.00;
    
    Min[ROWWISE]    = 10000.00;
    //    Min[COLUMNWISE] = 10000.00;
    
    Avg[ROWWISE]    = 0.00;
    //    Avg[COLUMNWISE] = 0.00;
    
    pthread_t t1,t2,t3,t4,t5,t6,t7,t8;
    int Nrow1 = 0;
    int Nrow2 = DIMENSION >> 3; //5000
    int Nrow3 = DIMENSION >> 2; //10000
    int Nrow4 = Nrow2 + Nrow3;  //15000
    int Nrow5 = DIMENSION >> 1; //20000
    int Nrow6 = Nrow5 + Nrow2;  //25000
    int Nrow7 = Nrow5 + Nrow3;  //30000
    int Nrow8 = Nrow7 + Nrow2;  //35000
    
    // Matrix Initialization
    printf("Be patient! Initializing............\n\n");
    for (j = 1; j <= nbreTests; j++){
        //        for (i = ROWWISE; i <= COLUMNWISE; i++){
        StartInitialize = Now();
        //            if (i == ROWWISE){
        InitializeMatrixRowwise();
        pthread_create(&t1, NULL, (void *)TransposeMatrixRowwise, (void*)Nrow1);
        pthread_create(&t2, NULL, (void *)TransposeMatrixRowwise, (void*)Nrow2);
        pthread_create(&t3, NULL, (void *)TransposeMatrixRowwise, (void*)Nrow3);
        pthread_create(&t4, NULL, (void *)TransposeMatrixRowwise, (void*)Nrow4);
        pthread_create(&t5, NULL, (void *)TransposeMatrixRowwise, (void*)Nrow5);
        pthread_create(&t6, NULL, (void *)TransposeMatrixRowwise, (void*)Nrow6);
        pthread_create(&t7, NULL, (void *)TransposeMatrixRowwise, (void*)Nrow7);
        pthread_create(&t8, NULL, (void *)TransposeMatrixRowwise, (void*)Nrow8);
        //                TransposeMatrixRowwise();
        //            }
        //            else
        //                InitializeMatrixColumnwise();
        testTime = Now() - StartInitialize;
        if (testTime > Max[i])
        {
            Max[i] = testTime;
            MaxIndex[i] = j;
        }
        if (testTime < Min[i])
        {
            Min[i] = testTime;
            MinIndex[i] = j;
        }
        Avg[i] += testTime;
    printf("%3d: Init&transpose Rowwise     Max[%2d]=%7.3f Min[%2d]=%7.3f Avg=%7.3f\n",
           j,MaxIndex[ROWWISE],Max[ROWWISE],MinIndex[ROWWISE],
           Min[ROWWISE],Avg[ROWWISE]/j);
    //        printf("     TransposeRowwise Max[%2d]=%7.3f Min[%2d]=%7.3f Avg=%7.3f\n",
    //               MaxIndex[COLUMNWISE],Max[COLUMNWISE],MinIndex[COLUMNWISE],
    //               Min[COLUMNWISE],Avg[COLUMNWISE]/j);
    //        printf("     Total            Avg=%7.3f\n",Avg[ROWWISE]/j+Avg[COLUMNWISE]/j);
    DisplayUpperQuandrant(PRINTDIM);
    }
}



/*********************************************************************\
 * Input    : None                                                    *
 * Output   : Returns the current system time                         *
 \*********************************************************************/
Timestamp Now()
{
    struct timeval tv_CurrentTime;
    gettimeofday(&tv_CurrentTime,NULL);
    return( (Timestamp) tv_CurrentTime.tv_sec + (Timestamp) tv_CurrentTime.tv_usec / 1000000.0-StartTime);
}


/*********************************************************************\                   
 * Input    : None                                                     *
 * Output   : None                                                     *
 * Function : Initialize a matrix rowwise                              *
 \*********************************************************************/
void      InitializeMatrixRowwise()
{
    int i,j;
    Matrix[0][0] = 0;
    for (j = 1; j < DIMENSION; j++)
        Matrix[0][j] = 1;
    for (i = 1;i < DIMENSION; i++)
    {
        memcpy(Matrix[i],Matrix[i - 1],sizeof(Matrix[i - 1]));
        for (j = 0; j < i; j++)
            Matrix[i][j] = Matrix[i][j] + i;
        Matrix[i][j] = Matrix[i][j - 1] + 1;
    }
}

void        TransposeMatrixRowwise(void*Nrow)
{
    int column,row,i,j,Upbound,Lobound;
    Lobound = (int)Nrow;
    Upbound = Lobound + DIMENSION>>3;
    
    double temp;
    for (row = Lobound; row < Upbound; row += BLOCKSIZE)
    {
        for (column = 0; column <= row; column += BLOCKSIZE)
        {
            for (i = row; i < (row + BLOCKSIZE) && i < DIMENSION; i++)
            {
                for (j = column; j < (column + BLOCKSIZE) && j < DIMENSION; j++)
                {
                    if (i > j)
                    {
                        temp = Matrix[i][j];
                        Matrix[i][j] = Matrix[j][i];
                        Matrix[j][i] = temp;
                       
                    }
                    else break;
                }
            }
        }
    }
}

    
    
    /*********************************************************************\
     * Input    : None                                                     *
     * Output   : None                                                     *
     * Function : Initialize a matrix columnwise                           *
     \*********************************************************************/
//    void      InitializeMatrixColumnwise(){
//            int i,j;
//            double x;
//
//            x = 0.0;
//            for (j = 0; j < DIMENSION; j++){
//                for (i = 0; i < DIMENSION; i++){
//                    if (i >= j){
//                        Matrix[i][j] = x;
//                        x += 1.0;
//                    } else
//                        Matrix[i][j] = 1.0;
//                }
//            }
//    }
    /*********************************************************************\
     * Input    : dimension (first n lines/columns)                        *
     * Output   : None                                                     *
     * Function : Initialize a matrix columnwise                           *
     \*********************************************************************/
    void      DisplayUpperQuandrant(unsigned dimension){
        int i,j;
        
        printf("\n\n********************************************************\n");
        for (i = 0; i < dimension; i++){
            printf("[");
            for (j = 0; j < dimension; j++){
                printf("%8.1f ",Matrix[i][j]);
            }
            printf("]\n");
        }
        printf("***************************************************************\n\n");
    }
