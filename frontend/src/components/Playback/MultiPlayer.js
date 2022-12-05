import React from "react";
import PlayerSmall from "../PlayButton/PlayerSmall";
import PlayCard from "../PlayButton/PlayCard";
import classNames from "classnames";

import { getPlayerLabel } from "../../util/label";

const MultiPlayer = ({
    playSection,
    sections,
    playerIndex,
    playConfig,
    disabledPlayers,
    extraContent,
}) => {
    return (
        <div
            className={classNames(
                "aha__multiplayer d-flex justify-content-around",
                "player-count-" + sections.length
            )}
        >
            {Object.keys(sections).map((index) => (
            //     <PlayCard 
            //     key={index}
            //     onClick={()=> playSection(index)}
            //     registerUserClicks={registerUserClicks}
            //     playing={playerIndex === index}
            //     inactive={sections[index].inactive}
            //     turned={sections[index].turned}
            // />
                <div className="player-wrapper" key={index}>
                    <PlayerSmall
                        onClick={() => {
                            playSection(index);
                        }}
                        disabled={
                            Array.isArray(disabledPlayers) &&
                            disabledPlayers.includes(parseInt(index))
                        }
                        label={
                            playConfig.label_style
                                ? getPlayerLabel(
                                      index,
                                      playConfig.label_style,
                                      playConfig.labels || []
                                  )
                                : ""
                        }
                        playing={playerIndex === index}
                    />
                    {extraContent && extraContent(index)}
                </div>
            ))}
        </div>
    );
};

export default MultiPlayer;
