# Auto Driving Car Simulation

A command-line simulation where multiple cars move on a 2D field according to simple commands. The simulation runs step-by-step and reports final positions or any collisions when two or more cars end up at the same cell.

## About the Project

- **Field**: A rectangular grid defined by width and height. Cars move within these bounds.
- **Cars**: Each car has a unique name, starting position (x, y), facing direction (N/E/S/W), and a sequence of commands.
- **Commands**:
  - **L** — turn left (N→W→S→E→N)
  - **R** — turn right (N→E→S→W→N)
  - **F** — move forward one cell in the current direction (only if the new cell is inside the field)
- **Simulation**: Runs one step at a time. If two or more cars would occupy the same cell, that counts as a collision and the simulation stops. Results show either final positions or collision details.

The app is interactive: you define the field, add one or more cars, then run the simulation and optionally start over or exit.

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) for dependency and environment management

## Commands

### Install dependencies

```bash
uv sync
```

### Run the simulation

```bash
uv run python src/main.py
```

### Run tests

```bash
uv run pytest
```

Run tests with verbose output:

```bash
uv run pytest -v
```

## Usage flow

1. **Enter field size**: Two integers, e.g. `10 10` for a 10×10 grid.
2. **Add cars** (option 1): For each car you’ll be asked for:
   - Name (must be unique)
   - Initial position and direction, e.g. `1 2 N` (x, y, direction)
   - Command string, e.g. `FFRFFL` (forward, forward, right, forward, forward, left)
3. **Run simulation** (option 2): Executes the commands step-by-step and prints either final positions or collision information.
4. After the run, choose to **Start over** or **Exit**.

## Example

```
Please enter the width and height of the simulation field in x y format:
10 10

You have created a field of 10 x 10.

Please choose from the following options:
[1] Add a car to field
[2] Run simulation
1
Please enter the name of the car:
Car1
Please enter initial position of car Car1 in x y Direction format:
0 0 N
Please enter the commands for car Car1:
FFRFF

...
[2] Run simulation
```

After simulation, the result is either a list of final positions per car or collision lines such as:
`Car1, collides with Car2 at (3,2) at step 5`.
