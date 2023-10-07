import React, { useState, useRef } from "react";
import Question from "../Question/Question";
import Button from "../Button/Button";

// FeedbackForm
const FeedbackForm = ({
    formActive,
    form,
    buttonLabel,
    skipLabel,
    isSkippable,
    onResult,
    emphasizeTitle = false,
}) => {
    const isSubmitted = useRef(false);
    const showSubmitButtons =
        form.filter((formElement) => formElement.submits).length === 0;

    const [formValid, setFormValid] = useState(false);

    const onSubmit = () => {
        // Prevent double submit
        if (isSubmitted.current){
            console.error("Multiple submits detected");
            return;
        }
        isSubmitted.current = true;

        // Callback onResult with question data
        onResult({
            form,
        });
    };

    const onChange = (value, question_key) => {
        form[question_key].value = value;
        if (form[question_key].submits) {
            onSubmit(form);
        }
        // for every non-skippable question, check that we have a value
        const validFormElements = form.filter( formElement => {
            if (formElement.is_skippable) return true;
            else if (formElement.value && validateFormElement(formElement)) return true;
        });
        if (validFormElements.length === form.length) setFormValid(true);
        else setFormValid(false);
    };

    function validateFormElement(formElement) {
        // For multiple choices in CHECKBOXES view, formElement.value is a string of comma-separated values
        if (formElement.view == "CHECKBOXES" && formElement.min_values && (formElement.value.split(",").length < formElement.min_values)) {
            return false;
        }
        return true;
    };

    return (
        <div className="aha__feedback justify-content-center">
            <form>
                {Object.keys(form).map((index) => (
                    <Question
                        key={index}
                        id={index}
                        active={formActive}
                        question={form[index]}
                        onChange={onChange}
                        emphasizeTitle={emphasizeTitle}
                    />
                ))}
                {/* Continue button */}
                {showSubmitButtons && formValid && (
                    <div className="center">
                        <Button
                            onClick={() => {
                                onSubmit();
                            }}
                            className={
                                "btn-primary submit anim anim-fade-in anim-speed-500"
                            }
                            title={buttonLabel}
                        />
                    </div>
                )}

                {/* Skip button */}
                {/* Only show skip-button when there is no value */}
                {isSkippable && showSubmitButtons && (
                    <div className="center">
                        <Button
                            onClick={() => {
                                onSubmit();
                            }}
                            className={
                                "btn-gray anim anim-fade-in anim-speed-500"
                            }
                            title={skipLabel}
                        />
                    </div>
                )}
            </form>
        </div>
    );
};

export default FeedbackForm;
