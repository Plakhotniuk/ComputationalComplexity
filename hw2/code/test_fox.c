#include <mpi.h>
#include <assert.h>
#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#define N 1200
#define TIME 1

int ind(int i, int j, int row_size) {
	return i * row_size + j;
}

void copy_arr(int *from, int *to, int size) {
	int i;
	for (i = 0; i < size; ++i) {
		to[i] = from[i];
	}
}

void matrix_mult(int *m1, int *m2, int* res, int size) {
	int i, j, k;
	for (i = 0; i < size; ++i)
		for (k = 0; k < size; ++k) {
			for (j = 0; j < size; ++j)
				res[ind(i, j, size)] += m1[ind(i, k, size)] * m2[ind(k, j, size)];
		}
}

void matrix_add(int *from, int* to, int size) {
	int i, j;
	for (i = 0; i < size; ++i) {
		for (j = 0; j < size; ++j) {
			to[ind(i, j, size)] += from[ind(i, j, size)];
		}
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

int main() {
	MPI_Init(NULL, NULL);
	
	int rank, row_rank, send_rank, recv_rank, numtasks, npsqrt, reorder, dims[2], periods[2], coords[2];
	int l, i, j, block_size, block_size2;
	int * A; int * B; int * AA; int * BB; int* C; int* CC;
	 	
	MPI_Comm_size(MPI_COMM_WORLD, &numtasks);
	MPI_Comm_rank(MPI_COMM_WORLD, &rank);

	npsqrt = (unsigned int)sqrt(numtasks);
	assert(npsqrt * npsqrt == numtasks);
	assert(N % npsqrt == 0);
	block_size = N / npsqrt;
	block_size2 = block_size * block_size;
	
	A = (int *)malloc(sizeof(int) * block_size2);
	B = (int *)malloc(sizeof(int) * block_size2);
	AA = (int *)malloc(sizeof(int) * block_size2);
	BB = (int *)malloc(sizeof(int) * block_size2);
	C = (int *)calloc(block_size2, sizeof(int));
	CC = (int *)calloc(block_size2, sizeof(int));
	
	for (i = 0; i < block_size; ++i)
		for (j = 0; j < block_size; ++j) {
			A[ind(i, j, block_size)] = rank;
			B[ind(i, j, block_size)] = rank;
		} 
	/*printf("Rank %d\n", rank);
	print_matrix(A, block_size);
	printf("\n");
	print_matrix(B, block_size);
	printf("\n");*/

#if TIME
    double time;
    if(rank == 0) time = MPI_Wtime();
#endif

    MPI_Comm comm_cart, comm_row;
    dims[0] = npsqrt;
    dims[1] = npsqrt;
    periods[0] = 1;
    periods[1] = 1;
    reorder = 0;
    MPI_Cart_create(MPI_COMM_WORLD, 2, dims, periods, reorder, &comm_cart);
    MPI_Cart_coords(comm_cart, rank, 2, coords);

    MPI_Comm_split(comm_cart, coords[0], coords[1], &comm_row);
    MPI_Comm_rank(comm_row, &row_rank);

    //printf("Rank: %d Cart_coords: %d %d Row rank: %d\n", rank, coords[0], coords[1], row_rank);
    for (l = 0; l < npsqrt; ++l) {
        j = (coords[0] + l) % npsqrt;
        if (coords[1] == j) copy_arr(A, AA, block_size2);
        MPI_Bcast(AA, block_size2, MPI_INT, j, comm_row);
        matrix_mult(AA, B, CC, block_size);
        matrix_add(CC, C, block_size);
        if (l != (npsqrt - 1)) {
            send_rank = (rank - npsqrt + numtasks) % numtasks;
            recv_rank = (rank + npsqrt) % numtasks;
            //if (rank == 0) printf("Send rank: %d Receive rank: %d\n", send_rank, recv_rank);
            if (coords[0] % 2 == 0) {
                MPI_Send(B, block_size2, MPI_INT, send_rank, 1, MPI_COMM_WORLD);
                MPI_Recv(BB, block_size2, MPI_INT, recv_rank, MPI_ANY_TAG, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
                copy_arr(BB, B, block_size2);
            } else {
                MPI_Recv(BB, block_size2, MPI_INT, recv_rank, MPI_ANY_TAG, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
                MPI_Send(B, block_size2, MPI_INT, send_rank, 1, MPI_COMM_WORLD);
                copy_arr(BB, B, block_size2);
            }
        }
    }

#if TIME
    if (rank == 0) {
		time = MPI_Wtime() - time;
		FILE *f;
		f = fopen("../data/time_fox.txt", "a");
		assert(f);
        fprintf(f, "%d %f %d\n", numtasks, time, N);
		fclose(f);
	}
#endif

//	printf("Rank %d\n", rank);
//	print_matrix(C, block_size);

	free(A);
	free(B);
	free(AA);
	free(BB);
	free(C);
	free(CC);

	MPI_Finalize();
}
