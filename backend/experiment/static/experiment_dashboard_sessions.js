// Show sessions for a specific block
const showBlockSessions = (id) => {
    document.getElementById(`show-sessions-${id}`).addEventListener("click", function () {
        document.querySelectorAll(`.block-${id}`).forEach(function (element) {
            element.classList.remove("hide");
        })
        document.getElementById("all-sessions").showModal();
    })
}

// Show sessions for a specific participant
const showParticipantSessions = (id) => {
    document.getElementById(`participant-sessions-${id}`).addEventListener("click", function () {
        document.querySelectorAll(`.participant-session-${id}`).forEach(function (element) {
            element.classList.remove("hide");
        })
        document.getElementById("all-participants").close();
        document.getElementById("all-sessions").showModal();
    })
}
