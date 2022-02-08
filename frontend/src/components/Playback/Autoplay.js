import React, { useState, useEffect, useRef } from "react";

import * as audio from "../../util/audio";
import { getCurrentTime } from "../../util/time";
import { MEDIA_ROOT } from "../../config";

import Circle from "../Circle/Circle";
import ListenCircle from "../ListenCircle/ListenCircle";
import Preload from "../Preload/Preload";

const PRELOAD = "PRELOAD";
const RECOGNIZE = "RECOGNIZE";
const SILENCE = "SILENCE";
const SYNC = "SYNC";


const AutoPlay = ({instructions, config, sections, finishedPlaying, submitResult, className=''}) => {
    // player state
    const [state, setState] = useState({ view: PRELOAD });
    const [running, setRunning] = useState(config.auto_play);
    const setView = (view, data = {}) => {
        setState({ view, ...data });
    }

    const section = sections[0];

    const startTime = useRef(getCurrentTime());

    // Time ref, stores the time without updating the view
    const time = useRef(0);

    const onCircleTimerTick = (t) => {
        time.current = t;
    };
    

    // Handle view logic
    useEffect(() => {
        switch (state.view) {
            case RECOGNIZE:
                // Play audio at start time
                audio.playFrom(0);
                startTime.current = getCurrentTime();
                break;
            case SYNC:
                // Play audio from sync start time
                const syncStart = Math.max(
                    0,
                    state.result.recognition_time +
                        config.silence_time +
                        config.continuation_offset
                );
                audio.playFrom(syncStart);
                startTime.current = getCurrentTime();
                break;
            default:
            // nothing
        }

        // Clean up
        return () => {
            audio.pause();
        };
    }, [state, config]);


    // Render component based on view
    switch (state.view) {
        case PRELOAD:
            return (
                <Preload
                    instruction={instructions.preload}
                    duration={config.ready_time}
                    url={MEDIA_ROOT + section.url}
                    onNext={() => {
                        setView(RECOGNIZE);
                    }}
                />
            );
        case RECOGNIZE:
            return (
                <div>
                    <div className="circle">
                        <Circle
                            key={instructions.during_presentation + config.decision_time}
                            running={running}
                            duration={config.decision_time}
                            color="white"
                            animateCircle={config.show_animation}
                            onTick={onCircleTimerTick}
                            onFinish={() => {
                                // Stop audio
                                audio.pause();
                                setRunning(false);
                                finishedPlaying(true);
                                if (config.auto_advance) {
                                    // Create a time_passed result
                                    submitResult({
                                        type: "time_passed",
                                        decision_time: config.decision_time,
                                    });
                                }
                            }}
                        />
                        <div className="circle-content">
                            {config.show_animation 
                                ? <ListenCircle
                                    duration={config.decision_time}
                                    histogramRunning={running}
                                    countDownRunning={running}
                                />
                                : <div className="stationary">
                                    <span className="ti-headphone"></span>
                                </div>
                            }
                        </div>
                    </div>
                    <div className={
                        "aha__listen d-flex flex-column justify-content-center align-items-center " +
                        className
                    }
                    >
                    {/* Instruction */}
                    <div className="instruction d-flex justify-content-center align-items-center">
                        <h3 className="text-center">{instructions.during_presentation}</h3>
                    </div>
                </div>
            </div>
            )
            default:
                return <div>Unknown view: {state.view}</div>;
        }
}   
export default AutoPlay;
