#include <iostream>
#include <vector>

using namespace std;

void gaussianElimination(vector<vector<double>> &matrix, int n)
{
    for (int i = 0; i < n; ++i)
    {
        // Partial pivoting
        int maxRow = i;
        for (int k = i + 1; k < n; ++k)
        {
            if (abs(matrix[k][i]) > abs(matrix[maxRow][i]))
            {
                maxRow = k;
            }
        }
        swap(matrix[i], matrix[maxRow]);

        double pivot = matrix[i][i];
        for (int j = 0; j < n; ++j)
        {
            matrix[i][j] /= pivot;
        }

        // Make the rest of the elements in the column zero
        for (int k = 0; k < n; ++k)
        {
            if (k != i)
            {
                double factor = matrix[k][i];
                for (int j = 0; j < n; ++j)
                {
                    matrix[k][j] -= factor * matrix[i][j];
                }
            }
        }
    }
}

// Function to calculate the matrix inverse
vector<vector<double>> MatrixInversion(vector<vector<double>> M)
{
    int n = M.size();

    // Create an identity M of the same size as the input M
    vector<vector<double>> identity(n, vector<double>(n, 0));
    for (int i = 0; i < n; ++i)
    {
        identity[i][i] = 1.0;
    }

    // Augment the input M with the identity M
    for (int i = 0; i < n; ++i)
    {
        M[i].insert(M[i].end(), identity[i].begin(), identity[i].end());
    }

    // Perform Gaussian elimination with partial pivoting
    gaussianElimination(M, n);

    // Extract the inverse M from the augmented M
    vector<vector<double>> inverse(n, vector<double>(n));
    for (int i = 0; i < n; ++i)
    {
        for (int j = 0; j < n; ++j)
        {
            inverse[i][j] = M[i][j + n];
        }
    }

    return inverse;
}

int main()
{
    // Define the matrix
    vector<vector<double>> matrix = {
        {1, 2, 3},
        {4, 5, 6},
        {7, 8, 9}};

    // Calculate the matrix inverse
    vector<vector<double>> matrixInverse = MatrixInversion(matrix);

    // Output the original matrix and its inverse
    cout << "Original Matrix:\n";
    for (const auto &row : matrix)
    {
        for (const auto &val : row)
        {
            cout << val << " ";
        }
        cout << endl;
    }

    cout << "Inverse Matrix:\n";
    for (const auto &row : matrixInverse)
    {
        for (const auto &val : row)
        {
            cout << val << " ";
        }
        cout << endl;
    }

    return 0;
}
