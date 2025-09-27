from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'quiz_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)

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
    """Page d'accueil - sélection du rôle"""
    return render_template('home.html')

@app.route('/display')
def display():
    """Écran de projection"""
    return render_template('display.html')

@app.route('/admin')
def admin():
    """Interface animateur"""
    return render_template('admin.html')

@app.route('/player')
def player():
    """Interface joueur"""
    return render_template('player.html')

@socketio.on('join_player')
def handle_join_player(data):
    """Joueur rejoint la partie"""
    player_name = data['name']
    if player_name not in game_state['players']:
        game_state['players'][player_name] = {'score': 0}
    socketio.emit('game_update', get_game_data())

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
        game_state['players'][game_state['buzzer_player']]['score'] += 20
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

@socketio.on('get_final_results')
def handle_get_final_results():
    """Envoyer les résultats finaux"""
    emit('final_results', game_state['players'])

@socketio.on('next_question')
def handle_next_question():
    """Passer à la question suivante manuellement"""
    next_question()

@socketio.on('time_warning')
def handle_time_warning():
    """Diffuser l'alerte temps"""
    socketio.emit('time_warning')

@socketio.on('timer_start')
def handle_timer_start():
    """Démarrage du timer"""
    socketio.emit('timer_start')

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
    import os
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=False, allow_unsafe_werkzeug=True)