export enum QuestionViews {
    AUTOCOMPLETE = "AUTOCOMPLETE",
    BUTTON_ARRAY = "BUTTON_ARRAY",
    CHECKBOXES = "CHECKBOXES",
    DROPDOWN = "DROPDOWN",
    RADIOS = "RADIOS",
    RANGE = "RANGE",
    TEXT_RANGE = "TEXT_RANGE",
    ICON_RANGE = "ICON_RANGE",
    STRING = "STRING",
}

export default interface Question {
    question: string;
    view: QuestionViews;
    value?: any;
    style?: any;
    explainer?: string;
    expected_response?: string;
    choices?: { [key: string]: string };
}
