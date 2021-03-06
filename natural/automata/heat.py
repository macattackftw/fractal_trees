import numba
import numpy as np


@numba.njit(cache=True)
def step(grid, temp):
    """Perform one time step of a 2D diffusion CA."""
    rows, cols = grid.shape
    # Do not update any of the four boundaries.
    for row in range(1, rows - 1):
        for col in range(1, cols - 1):
            left, right = col - 1, col + 1
            top, bottom = row - 1, row + 1
            # Perform a four neighbor average.
            temp[row, col] = (
                grid[top, right] + grid[top, left] + grid[bottom, right] + grid[bottom, left]
            ) / 4
    # Update the values of the top and bottom rows to have no flux boundary conditions.
    temp[0, :] = temp[1, :]
    temp[-1, :] = temp[-2, :]
    grid[:, :] = temp[:, :]


def istep(rows, cols, ymin, ymax):
    domain = np.zeros((rows, cols))
    domain[:, 0] = np.linspace(ymin, ymax, cols) * (10 - np.linspace(ymin, ymax, rows))
    temporary = domain.copy()
    while True:
        step(domain, temporary)
        yield domain
