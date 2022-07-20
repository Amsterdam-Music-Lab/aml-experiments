import React from "react";
import classNames from "classnames";

// Radios is a question view for selecting a single option from a list
const Radios = ({ question, value, onChange, emphasizeTitle = false }) => {
    return (
        <div className="aha__radios">
            {question.explainer && (
                <p className="explainer">{question.explainer}</p>
            )}
            <h3 className={classNames({title: emphasizeTitle})}>{question.question}</h3>
            {Object.keys(question.choices).sort((a,b) => a-b).map((val, index) => (
                <Radio
                    key={index}
                    name={question.key}
                    label={question.choices[val]}
                    value={val}
                    checked={value === val}
                    onChange={onChange}
                />
            ))}
        </div>
    );
};

const Radio = ({ label, value, checked, onChange }) => {
    return (
        <div
            className={classNames("radio", { checked })}
            onClick={() => {
                onChange(value);
            }}
            tabIndex="0"
            onKeyPress={() => {
                onChange(value);
            }}
        >
            <i></i>
            <span>{label}</span>
        </div>
    );
};

export default Radios;
