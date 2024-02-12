import React, { useEffect, useState } from "react";
import classNames from "classnames";

import PlayCard from "../PlayButton/PlayCard";

const VisualMatchingPairs = (props) => {

    const {
        sections,
        playerIndex,
        finishedPlaying,
        setPlayerIndex,
        submitResult,
        view,
    } = props;

    const [gameState, setGameState] = useState(sections);
    const [inBetweenTurns, setInBetweenTurns] = useState(false);
    const [score, setScore] = useState(null);
    const [firstCard, setFirstCard] = useState(-1);
    const [secondCard, setSecondCard] = useState(-1);
    const [total, setTotal] = useState(100);
    const [message, setMessage] = useState('Pick a card')
    const [end, setEnd] = useState(false);
    const columnCount = gameState.length > 6 ? 4 : 3;

    const [resultBuffer, setResultBuffer] = useState([]);

    const [startTime] = useState(Date.now());

    const getScoreMessage = (score) => {
        switch (score) {
            case -10: return '-10 <br />Misremembered';
            case 0: return '0 <br />No match';
            case 10: return '+10 <br />Lucky match';
            case 20: return '+20 <br />Good job!';
            default: return '';
        }
    }

    const formatTime = (time) => {
        return time / 1000;
    }

    // Show (animated) feedback after second click on second card or finished playing
    const showFeedback = (firstCard, secondCard, score) => {

        // update total score & display current score
        setTotal(total + score);
        setMessage(getScoreMessage(score));

        // show end of turn animations
        switch (score) {
            case 10:
                setGameState(prev => prev.map((section, i) => {
                    if (i === firstCard || i === secondCard) {
                        return { ...section, lucky: true };
                    }
                    return section;
                }));

                break;
            case 20:
                setGameState(prev => prev.map((section, i) => {
                    if (i === firstCard || i === secondCard) {
                        return { ...section, memory: true };
                    }
                    return section;
                }));
                break;
            default:
                setGameState(prev => prev.map((section, i) => {
                    if (i === firstCard || i === secondCard) {
                        return { ...section, nomatch: true };
                    }
                    return section;
                }));

                // reset nomatch cards for coming turns
                setTimeout(() => {
                    setGameState(prev => prev.map((section, i) => {
                        if (i === firstCard || i === secondCard) {
                            return { ...section, nomatch: false };
                        }
                        return section;
                    }));
                }, 700);
                break;
        }

        // add third click event to finish the turn
        setInBetweenTurns(true);

        return;
    }

    const checkMatchingPairs = (index) => {
        let gameStateCopy = gameState.map(s => ({ ...s }));
        const currentCard = gameStateCopy[index];
        const turnedCardsCount = gameStateCopy.filter(s => s.turned).length;
        let newScore = 0;

        if (turnedCardsCount === 1) {
            // We have two turned cards
            gameStateCopy[index].turned = true;
            setSecondCard(index);

            // set no mouse events for all but current
            gameStateCopy = gameStateCopy.map((section, i) => {
                if (i === index) {
                    return { ...currentCard, noevents: true };
                }
                return { ...section, noevents: true };
            });

            // check for match
            const lastCard = gameStateCopy[firstCard];
            if (lastCard.group === currentCard.group) {
                // match
                if (currentCard.seen) {
                    newScore = 20;
                } else {
                    newScore = 10;
                }
            } else {
                if (currentCard.seen) {
                    newScore = -10;
                } else {
                    newScore = 0;
                }
            };
            gameStateCopy[index].seen = true;
            gameStateCopy[firstCard].seen = true;

            setScore(newScore);
            setGameState([...gameStateCopy]);
            showFeedback(firstCard, index, newScore);
        }

        if (turnedCardsCount === 0) {
            // first click of the turn
            setFirstCard(index);
            // turn first card, disable events
            gameStateCopy[index] = {
                ...currentCard,
                turned: true,
                noevents: true,
            }

            setGameState(gameStateCopy);

            // clear message
            setMessage('');
        }

        console.log('start time', startTime)

        const newResult = {
            selectedSection: currentCard.id,
            cardIndex: index,
            score: newScore,
            timestamp: formatTime(Date.now() - startTime)
        }

        setResultBuffer([...resultBuffer, newResult]);

        return;
    };

    const finishTurn = () => {
        finishedPlaying();
        // remove matched cards from the board
        if (score === 10 || score === 20) {
            setGameState(prev => prev.map((section, i) => {
                if (i === firstCard || i === secondCard) {
                    return { ...section, inactive: true };
                }

                return section;
            }))
        }
        setFirstCard(-1);
        setSecondCard(-1);
        // remove third click event
        setScore(null);
        // Turn all cards back and enable events
        setGameState(prev => prev.map((section, i) => {
            return { ...section, turned: false, noevents: false };
        }));

        setMessage('');

        setInBetweenTurns(false);
    }

    useEffect(() => {
        const noMoreActiveCards = !gameState.some(s => !s.inactive);

        if (noMoreActiveCards) {
            setEnd(true);
        }
    }, [gameState, setEnd]);

    const registerUserClicks = () => void 0;
    const stopAudioAfter = () => void 0;

    const onPlayCardClick = (index) => {
        setPlayerIndex(-1);
        checkMatchingPairs(index);
    }

    useEffect(() => {
        if (end) {
            submitResult({ score: total, moves: resultBuffer });
        }
    }, [end, submitResult, total, resultBuffer]);

    const getScoreClasses = (score) => {
        switch (score) {
            case -10: return 'fbmisremembered';
            case 0: return 'fbnomatch';
            case 10: return 'fblucky';
            case 20: return 'fbmemory';
            default: return '';
        }
    }

    return (
        <div className="aha__visual-matching-pairs">

            <div className="row justify-content-between">
                <div className="col-6 align-self-start">
                    <div dangerouslySetInnerHTML={{ __html: message }}
                        className={classNames("visual-matching-pairs__feedback", getScoreClasses(score))}
                    />
                </div>
                <div className="col-6 align-self-end">
                    <div className="visual-matching-pairs__score" data-testid="score">
                        Score: <br />{total}
                    </div>
                </div>
            </div>

            <div className={classNames("playing-board", columnCount === 3 && "playing-board--three-columns")}>
                {(gameState).map((section, index) => (
                    <PlayCard
                        key={index}
                        onClick={() => onPlayCardClick(index)}
                        playing={playerIndex === index}
                        onFinish={showFeedback}
                        registerUserClicks={registerUserClicks}
                        section={section}
                        stopAudioAfter={stopAudioAfter}
                        view={view}
                    />
                )
                )}
            </div>
            <div
                className="visual-matching-pairs__overlay"
                onClick={finishTurn}
                style={{ display: inBetweenTurns ? 'block' : 'none' }}
                data-testid="overlay"
            ></div>
        </div>
    )
}

export default VisualMatchingPairs;
