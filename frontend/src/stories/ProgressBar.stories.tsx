import ProgressBar from "../components/ProgressBar/ProgressBar";

export default {
    title: "ProgressBar",
    component: ProgressBar,
    parameters: {
        layout: "fullscreen",
    },
};

export const Default = {
    args: {
        value: 50,
        max: 100,
        showPercentage: false,
        label: "3 / 20",
    },
    decorators: [
        (Story) => (
            <div
                style={{ width: "100%", height: "100%", backgroundColor: "#666", padding: "1rem" }}
            >
                <Story />
            </div>
        ),
    ],
};

export const WithPercentage = {
    args: {
        value: 50,
        max: 100,
        showPercentage: true,
        label: "3 / 20",
    },
    decorators: [
        (Story) => (
            <div
                style={{ width: "100%", height: "100%", backgroundColor: "#666", padding: "1rem" }}
            >
                <Story />
            </div>
        ),
    ],
};
