const ACTIONS = {
  UP: "UP",
  RIGHT: "RIGHT",
  DOWN: "DOWN",
  LEFT: "LEFT",
};

const ENV_CONFIG = {
  rows: 10,
  cols: 10,
  learningRate: 0.8,
  discountFactor: 0.99,
  epsilon: 0.2,
  maxMoves: 50,
  nextMoveDelayMs: 0,
};

const ENV_STATE = {
  rewardedStates: {
    [s(0, 0)]: 0.5,
    [s(0, 9)]: 1,
  },
  absorbingStates: [s(0, 0), s(0, 9)],
  obstacles: [
    s(0, 2),
    s(1, 2),
    s(2, 2),
    s(3, 2),
    s(5, 3),
    s(5, 4),
    s(5, 5),
    s(3, 4),
    s(3, 5),
    s(3, 6),
    s(3, 7),
    s(3, 8),
    s(3, 9),
    s(6, 4),
    s(7, 4),
    s(8, 4),
    s(9, 4),
    s(6, 2),
    s(7, 1),
    s(6, 6),
    s(7, 7),
  ],
  currentState: s(8, 6),
  qValues: {},
  moves: 0,
  nextMoveDelayMs: ENV_CONFIG.nextMoveDelayMs,
};

function chooseInitialState() {
  while (1) {
    const r = Math.floor(ENV_CONFIG.rows * Math.random());
    const c = Math.floor(ENV_CONFIG.cols * Math.random());
    const state = s(r, c);
    if (
      !ENV_STATE.obstacles.includes(state) &&
      !ENV_STATE.absorbingStates.includes(state)
    ) {
      return state;
    }
  }
}

function startLoop() {
  (function loop() {
    if (ENV_STATE.absorbingStates.includes(ENV_STATE.currentState)) {
      console.log("Reached absorbing state, restarting");
      resetState();
    } else if (ENV_STATE.moves >= ENV_CONFIG.maxMoves) {
      console.log(`Exceeded allowed ${ENV_CONFIG.maxMoves} moves, restarting`);
      resetState();
    } else {
      performMove();
    }
    updateGrid();
    setTimeout(loop, ENV_STATE.nextMoveDelayMs);
  })();
}

function resetState() {
  ENV_STATE.currentState = chooseInitialState();
  ENV_STATE.moves = 0;
}

function performMove() {
  const { currentState } = ENV_STATE;

  const action = chooseAction(currentState);
  const nextState = stateAfterAction(currentState, action);
  if (nextState != currentState) {
    const reward = rewardInState(nextState);
    updateQValue(currentState, action, nextState, reward);
  }
  ENV_STATE.currentState = nextState;
  updateGrid();

  ENV_STATE.moves++;
}

function getQValue(state, a) {
  return ENV_STATE.qValues[q(state, a)] || 0;
}

function updateQValue(state, action, nextState, reward) {
  const { learningRate, discountFactor } = ENV_CONFIG;
  const [_, bestNextActionValue] = bestActionWithValue(nextState);
  const currentValue = getQValue(state, action);
  ENV_STATE.qValues[q(state, action)] =
    currentValue +
    learningRate *
      (reward + discountFactor * bestNextActionValue - currentValue);
}

function stateAfterAction(state, action) {
  const [r, c] = getRowCol(state);
  let newRow = r;
  let newCol = c;
  switch (action) {
    case ACTIONS.UP:
      newRow -= 1;
      break;
    case ACTIONS.RIGHT:
      newCol += 1;
      break;
    case ACTIONS.DOWN:
      newRow += 1;
      break;
    case ACTIONS.LEFT:
      newCol -= 1;
      break;
  }
  const newState = s(newRow, newCol);
  if (
    newRow < 0 ||
    newRow >= ENV_CONFIG.rows ||
    newCol < 0 ||
    newCol >= ENV_CONFIG.cols ||
    ENV_STATE.obstacles.includes(newState)
  ) {
    return state;
  }
  return newState;
}

function rewardInState(state) {
  return ENV_STATE.rewardedStates[state] || 0;
}

function bestActionWithValue(state) {
  return Object.values(ACTIONS)
    .map((a) => [a, getQValue(state, a)])
    .sort((x, y) => y[1] - x[1])[0];
}

function bestAction(state) {
  const [bestNextAction, _] = bestActionWithValue(state);
  return bestNextAction;
}

function chooseAction(state) {
  if (Math.random() < ENV_CONFIG.epsilon) {
    const actions = Object.values(ACTIONS);
    return actions[Math.floor(Math.random() * actions.length)];
  }
  return bestAction(state);
}

function renderGrid(parent) {
  const table = document.createElement("table");
  table.className = "grid";
  for (let r = 0; r < ENV_CONFIG.rows; ++r) {
    const tr = document.createElement("tr");
    tr.insertAdjacentHTML("beforeend", `<th>${r}</th>`);
    for (let c = 0; c < ENV_CONFIG.cols; ++c) {
      tr.insertAdjacentHTML(
        "beforeend",
        `
                <td data-state="${s(r, c)}" class="field state_${s(r, c)}">
                    <div class="reward"></div>
                    <div class="best-action"></div>
                </td>`
      );
    }
    table.appendChild(tr);
  }
  const tr = document.createElement("tr");
  tr.insertAdjacentHTML("beforeend", `<th></th>`);
  for (let c = 0; c < ENV_CONFIG.cols; ++c) {
    tr.insertAdjacentHTML("beforeend", `<th>${c}</th>`);
  }
  table.appendChild(tr);
  parent.appendChild(table);

  updateGrid();
}

function updateGrid() {
  for (const [state, reward] of Object.entries(ENV_STATE.rewardedStates)) {
    document.querySelector(`.grid .state_${state} .reward`).innerText = reward;
  }

  document.querySelectorAll(`.grid .field`).forEach((field) => {
    field.classList.remove("absorbing");
    field.classList.remove("obstacle");
    field.classList.remove("current");
  });

  const { absorbingStates, obstacles, currentState } = ENV_STATE;

  absorbingStates.forEach((state) =>
    document.querySelector(`.grid .state_${state}`).classList.add("absorbing")
  );

  obstacles.forEach((state) =>
    document.querySelector(`.grid .state_${state}`).classList.add("obstacle")
  );

  document
    .querySelector(`.grid .state_${currentState}`)
    .classList.add("current");

  document
    .querySelectorAll(`.grid .field`)
    .forEach(
      (field) =>
        (field.querySelector(".best-action").innerText =
          field.classList.contains("absorbing") ||
          field.classList.contains("obstacle")
            ? ""
            : actionSymbol(bestAction(field.dataset.state)))
    );
}

function actionSymbol(action) {
  if (action == ACTIONS.UP) {
    return "↑";
  }
  if (action == ACTIONS.RIGHT) {
    return "→";
  }
  if (action == ACTIONS.DOWN) {
    return "↓";
  }
  if (action == ACTIONS.LEFT) {
    return "←";
  }
}

function s(r, c) {
  return `${r}_${c}`;
}

function q(state, a) {
  return `${state}_${a}`;
}

function getRowCol(state) {
  return state.split("_").map((x) => parseInt(x));
}
