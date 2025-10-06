// Gestion du jeu côté client
const socket = io();
let timer = 20;
let timerInterval;
let gameData = {};

// Éléments DOM
const timerDisplay = document.getElementById('timer');
const timerProgress = document.getElementById('timer-progress');
const questionNumber = document.getElementById('question-number');
const questionText = document.getElementById('question-text');
const buzzerAlert = document.getElementById('buzzer-alert');
const playersList = document.getElementById('players-list');
const startBtn = document.getElementById('start-btn');
const correctBtn = document.getElementById('correct-btn');
const wrongBtn = document.getElementById('wrong-btn');
const buzzerSound = document.getElementById('buzzer-sound');

// Démarrer le jeu
function startGame() {
    socket.emit('start_game');
    startBtn.style.display = 'none';
}

// Réponse correcte
function correctAnswer() {
    socket.emit('correct_answer');
    hideAnswerButtons();
}

// Réponse incorrecte
function wrongAnswer() {
    socket.emit('wrong_answer');
    hideAnswerButtons();
}

function hideAnswerButtons() {
    correctBtn.style.display = 'none';
    wrongBtn.style.display = 'none';
    buzzerAlert.textContent = '';
}

function showAnswerButtons() {
    correctBtn.style.display = 'inline-block';
    wrongBtn.style.display = 'inline-block';
}

// Gestion du chrono
function startTimer() {
    timer = 20;
    updateTimerDisplay();
    
    // Jouer le son du timer au début
    socket.emit('timer_start');
    
    timerInterval = setInterval(() => {
        timer--;
        updateTimerDisplay();
        
        if (timer <= 0) {
            clearInterval(timerInterval);
            socket.emit('time_up');
        }
    }, 1000);
}

function pauseTimer() {
    clearInterval(timerInterval);
}

function resumeTimer() {
    if (timer > 0) {
        timerInterval = setInterval(() => {
            timer--;
            updateTimerDisplay();
            
            if (timer <= 0) {
                clearInterval(timerInterval);
                socket.emit('time_up');
            }
        }, 1000);
    }
}

function updateTimerDisplay() {
    timerDisplay.textContent = timer;
    const percentage = (timer / 20) * 100;
    timerProgress.style.width = percentage + '%';
    
    // Changer la couleur selon le temps restant
    if (timer <= 10) {
        timerProgress.style.background = 'linear-gradient(90deg, #ff4444, #cc0000)';
    } else if (timer <= 20) {
        timerProgress.style.background = 'linear-gradient(90deg, #FFA500, #FF8C00)';
    } else {
        timerProgress.style.background = 'linear-gradient(90deg, #FFD700, #FFA500)';
    }
}

// Mise à jour de l'affichage des joueurs
function updatePlayersDisplay() {
    const sortedPlayers = Object.entries(gameData.players || {})
        .sort(([,a], [,b]) => b.score - a.score);
    
    playersList.innerHTML = '';
    
    sortedPlayers.forEach(([name, data], index) => {
        const playerDiv = document.createElement('div');
        playerDiv.className = 'player-score';
        playerDiv.innerHTML = `
            <span class="player-name">${index + 1}. ${name}</span>
            <span class="score">${data.score}</span>
        `;
        playersList.appendChild(playerDiv);
    });
}

// Événements Socket.IO
socket.on('game_update', function(data) {
    gameData = data;
    
    if (data.current_question) {
        questionNumber.textContent = `Question ${data.question_number}/${data.total_questions}`;
        questionText.textContent = data.current_question.question;
        
        // Démarrer le chrono si ce n'est pas en pause
        if (!data.timer_paused && !data.buzzer_pressed) {
            startTimer();
        } else if (data.timer_paused) {
            pauseTimer();
        }
    }
    
    updatePlayersDisplay();
    
    // Gérer l'état du buzzer
    if (!data.buzzer_pressed) {
        hideAnswerButtons();
        buzzerAlert.textContent = '';
        if (!data.timer_paused) {
            resumeTimer();
        }
    }
});

socket.on('buzzer_activated', function(data) {
    if (data.play_sound) {
        buzzerSound.play().catch(e => console.log('Erreur son:', e));
    }
    
    buzzerAlert.textContent = `${data.player} a buzzé !`;
    pauseTimer();
    showAnswerButtons();
});

socket.on('game_finished', function() {
    clearInterval(timerInterval);
    setTimeout(() => {
        window.location.href = '/winner';
    }, 2000);
});

// Initialisation
socket.on('connect', function() {
    console.log('Connecté au serveur');
});