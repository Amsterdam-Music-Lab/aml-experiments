import { BrowserRouter as Router } from "react-router-dom";

import ScoreV2 from "../components/ExperimentCollection/Score/Score";

export default {
  title: "ExperimentCollection/Score",
  component: ScoreV2,
  parameters: {
    layout: "fullscreen",
  },
  argTypes: {
    "rank.class": {
      control: {
        type: "select",
      },
      options: ['diamond', 'platinum', 'gold', 'silver', 'bronze', 'plastic'],
    },
  }
};

function getScoreData(overrides = {}) {
  return {
    score: 100,
    label: "points",
    rank: {
      class: "gold",
      text: "Gold",
    },
    ...overrides,
  };
}

const getDecorator = (Story) => (
  <div
    style={{ width: "100%", height: "100%", backgroundColor: "#aaa", padding: "1rem" }}
  >
    <Router>
      <Story />
    </Router>
  </div>
);

export const Default = {
  args: getScoreData(),
  decorators: [getDecorator],
};

export const ZeroScore = {
  args: getScoreData({ score: 0, scoreClass: "scoreCircleZero" }),
  decorators: [getDecorator],
};

export const NegativeScore = {
  args: getScoreData({ score: -100, scoreClass: "scoreCircleNegative" }),
  decorators: [getDecorator],
};

export const ScoreWithoutLabel = {
  args: getScoreData({ label: "" }),
  decorators: [getDecorator],
};

export const CustomLabel = {
  args: getScoreData({ label: "points earned" }),
  decorators: [getDecorator],
};

export const CustomScoreClass = {
  args: getScoreData({ scoreClass: "silver" }),
  decorators: [getDecorator],
};

export const SelectableScoreClass = {
  args: getScoreData(),
  decorators: [getDecorator],
};
