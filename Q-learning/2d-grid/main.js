const ACTIONS = {
  UP: "UP",
  RIGHT: "RIGHT",
  DOWN: "DOWN",
  LEFT: "LEFT",
};

const ENV_CONFIG = {
  rows: 10,
  cols: 10,
  epsilon: 0.8,
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
};

function isRewarded(r, c) {
  return reward(r, c) !== undefined;
}

function reward(r, c) {
  return ENV_STATE.rewardedStates[s(r, c)];
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
                <td class="field state_${s(r, c)}">
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
            : actionSymbol(ACTIONS.RIGHT))
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
