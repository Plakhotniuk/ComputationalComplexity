#include <mpi.h>
#include <assert.h>
#include <math.h>
#include <stdlib.h>
#include <stdio.h>

#define N 1200 // размер матрицы
#define TIME 1

int ind(int i, int j, int row_size) {
    return i * row_size + j;
}

void matrix_mult(int *m1, int *m2, int* res, int size) {
    int i, j, k;
    for (i = 0; i < size; ++i)
        for (k = 0; k < size; ++k) {
            for (j = 0; j < size; ++j)
                res[ind(i, j, size)] += m1[ind(i, k, size)] * m2[ind(k, j, size)];
        }
}

void print_matrix(int *m, int size) {
    int i, j;
    for (i = 0; i < size; ++i) {
        for (j = 0; j < size; ++j)
            printf("%d ", m[ind(i, j, size)]);
        printf("\n");
    }
}

int main(int argc, char **argv) {

    int num_tasks, rank;
    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &num_tasks);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    int i, j;
    int iterations = 1000000;
    int *A, *B, *CC;

    A = (int *)calloc(N*N, sizeof(int));
    B = (int *)calloc(N*N, sizeof(int));
    CC = (int *)calloc(N*N, sizeof(int));


#if TIME
    double time;
    if(rank == 0) time = MPI_Wtime();
#endif

    matrix_mult(A, B, CC, N);

#if TIME
    if (rank == 0) {
		time = MPI_Wtime() - time;
		FILE *f;
		f = fopen("../data/time_common.txt", "a");
		assert(f);
		fprintf(f, "%d %f\n", num_tasks, time);
		fclose(f);
	}
#endif

    free(A);
    free(B);
    MPI_Finalize();
}

