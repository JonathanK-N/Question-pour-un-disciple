from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'quiz_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

# État du jeu
game_state = {
    'current_question': 0,
    'questions': [],
    'players': {},
    'buzzer_pressed': False,
    'buzzer_player': None,
    'timer_paused': False,
    'game_finished': False
}

def load_questions():
    """Charge les questions depuis le fichier JSON"""
    try:
        with open('data/questions.json', 'r', encoding='utf-8') as f:
            game_state['questions'] = json.load(f)
    except FileNotFoundError:
        game_state['questions'] = []

@app.route('/')
def index():
    """Page principale - écran de jeu"""
    return render_template('index.html')

@app.route('/buzzer_page/<player_name>')
def buzzer_page(player_name):
    """Page buzzer pour les joueurs"""
    if player_name not in game_state['players']:
        game_state['players'][player_name] = {'score': 0}
    return render_template('buzzer.html', player_name=player_name)

@app.route('/winner')
def winner():
    """Page des résultats finaux"""
    sorted_players = sorted(game_state['players'].items(), key=lambda x: x[1]['score'], reverse=True)
    return render_template('winner.html', players=sorted_players)

@socketio.on('connect')
def handle_connect():
    """Connexion d'un client"""
    emit('game_update', get_game_data())

@socketio.on('buzzer_press')
def handle_buzzer(data):
    """Gestion du buzzer"""
    if not game_state['buzzer_pressed'] and not game_state['game_finished']:
        game_state['buzzer_pressed'] = True
        game_state['buzzer_player'] = data['player']
        game_state['timer_paused'] = True
        
        socketio.emit('buzzer_activated', {
            'player': data['player'],
            'play_sound': True
        })
        socketio.emit('game_update', get_game_data())

@socketio.on('correct_answer')
def handle_correct_answer():
    """Réponse correcte"""
    if game_state['buzzer_player']:
        game_state['players'][game_state['buzzer_player']]['score'] += 1
    next_question()

@socketio.on('wrong_answer')
def handle_wrong_answer():
    """Réponse incorrecte - reprendre le chrono"""
    game_state['buzzer_pressed'] = False
    game_state['buzzer_player'] = None
    game_state['timer_paused'] = False
    socketio.emit('game_update', get_game_data())

@socketio.on('time_up')
def handle_time_up():
    """Temps écoulé"""
    next_question()

@socketio.on('start_game')
def handle_start_game():
    """Démarrer le jeu"""
    load_questions()
    game_state['current_question'] = 0
    game_state['game_finished'] = False
    socketio.emit('game_update', get_game_data())

def next_question():
    """Passer à la question suivante"""
    game_state['buzzer_pressed'] = False
    game_state['buzzer_player'] = None
    game_state['timer_paused'] = False
    game_state['current_question'] += 1
    
    if game_state['current_question'] >= len(game_state['questions']):
        game_state['game_finished'] = True
        socketio.emit('game_finished')
    
    socketio.emit('game_update', get_game_data())

def get_game_data():
    """Récupère les données actuelles du jeu"""
    current_q = None
    if (game_state['current_question'] < len(game_state['questions']) and 
        not game_state['game_finished']):
        current_q = game_state['questions'][game_state['current_question']]
    
    return {
        'current_question': current_q,
        'question_number': game_state['current_question'] + 1,
        'total_questions': len(game_state['questions']),
        'players': game_state['players'],
        'buzzer_pressed': game_state['buzzer_pressed'],
        'buzzer_player': game_state['buzzer_player'],
        'timer_paused': game_state['timer_paused'],
        'game_finished': game_state['game_finished']
    }

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)