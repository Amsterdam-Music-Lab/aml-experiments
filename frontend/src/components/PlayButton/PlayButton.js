import React from "react";
import classNames from "classnames";

const PlayButton = ({ playSection, className = ""}) => {
    return (
        <div
            className={classNames(
                "aha__play-button border-outside",
                "btn",
                className
            )}
            onClick={() => playSection(0)}
            tabIndex="0"
            onKeyPress={(e) => {
                playSection(0);
                finishedPlaying();
            }}
        ></div>
    );
};

export default PlayButton;
