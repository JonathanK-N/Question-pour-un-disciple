from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'quiz_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading', ping_timeout=120, ping_interval=60, max_http_buffer_size=1000000)

# États des jeux par salle
game_rooms = {}

def get_or_create_room(room_id):
    """Obtenir ou créer une salle de jeu"""
    if room_id not in game_rooms:
        game_rooms[room_id] = {
            'current_question': 0,
            'questions': [],
            'players': {},
            'buzzer_pressed': False,
            'buzzer_player': None,
            'timer_paused': False,
            'game_finished': False
        }
    return game_rooms[room_id]

def load_questions(room_id):
    """Charge les questions depuis le fichier JSON"""
    game_state = get_or_create_room(room_id)
    try:
        with open('data/questions.json', 'r', encoding='utf-8') as f:
            game_state['questions'] = json.load(f)
    except FileNotFoundError:
        game_state['questions'] = []

@app.route('/')
def index():
    """Page de sélection de salle"""
    return render_template('room_selector.html')

@app.route('/room/<room_id>')
def room_home(room_id):
    """Page d'accueil pour une salle spécifique"""
    return render_template('home.html', room_id=room_id)

@app.route('/display')
@app.route('/room/<room_id>/display')
def display(room_id='default'):
    """Écran de projection"""
    return render_template('display.html', room_id=room_id)

@app.route('/admin')
@app.route('/room/<room_id>/admin')
def admin(room_id='default'):
    """Interface animateur"""
    return render_template('admin.html', room_id=room_id)

@app.route('/player')
@app.route('/room/<room_id>/player')
def player(room_id='default'):
    """Interface joueur"""
    return render_template('player.html', room_id=room_id)

@app.route('/test')
def test_display():
    """Page de test pour diagnostiquer SocketIO"""
    return render_template('../test_display.html')

@socketio.on('join_player')
def handle_join_player(data):
    """Joueur rejoint la partie"""
    room_id = data.get('room_id', 'default')
    player_name = data.get('name', '').strip()
    
    # Rejoindre la salle
    join_room(room_id)
    game_state = get_or_create_room(room_id)
    
    # Vérifications
    if not player_name or len(player_name) > 20 or game_state['game_finished']:
        emit('join_error', {'message': 'Nom invalide ou jeu en cours'})
        return
    
    # Empêcher les doublons pendant le jeu
    if player_name in game_state['players'] and game_state['current_question'] > 0:
        emit('join_error', {'message': 'Joueur déjà connecté'})
        return
    
    if player_name not in game_state['players']:
        game_state['players'][player_name] = {'score': 0}
    
    emit('join_success', {'name': player_name})
    socketio.emit('game_update', get_game_data(room_id), room=room_id)

@app.route('/winner')
def winner():
    """Page des résultats finaux"""
    room_id = request.args.get('room_id', 'default')
    game_state = get_or_create_room(room_id)
    sorted_players = sorted(
        game_state['players'].items(),
        key=lambda x: x[1]['score'],
        reverse=True
    )
    return render_template('winner.html', players=sorted_players, room_id=room_id)

@socketio.on('join_room')
def handle_join_room(data):
    """Rejoindre une salle spécifique"""
    room_id = data.get('room_id', 'default')
    join_room(room_id)
    game_state = get_or_create_room(room_id)
    emit('game_update', get_game_data(room_id))

@socketio.on('connect')
def handle_connect(auth):
    """Connexion d'un client"""
    # Rejoindre la salle par défaut
    join_room('default')
    emit('game_update', get_game_data('default'))

@socketio.on('buzzer_press')
def handle_buzzer(data):
    """Gestion du buzzer"""
    room_id = data.get('room_id', 'default')
    player_name = data.get('player', '').strip()
    game_state = get_or_create_room(room_id)
    
    # Vérifications de sécurité
    if (not player_name or 
        game_state['buzzer_pressed'] or 
        game_state['game_finished'] or 
        game_state['current_question'] >= len(game_state['questions']) or
        player_name not in game_state['players']):
        return
    
    game_state['buzzer_pressed'] = True
    game_state['buzzer_player'] = player_name
    game_state['timer_paused'] = True
    
    socketio.emit('buzzer_activated', {
        'player': player_name,
        'play_sound': True
    }, room=room_id)
    socketio.emit('game_update', get_game_data(room_id), room=room_id)

@socketio.on('correct_answer')
def handle_correct_answer(data):
    """Réponse correcte"""
    room_id = data.get('room_id', 'default') if data else 'default'
    game_state = get_or_create_room(room_id)
    
    if game_state['buzzer_player']:
        game_state['players'][game_state['buzzer_player']]['score'] += 20
    
    socketio.emit('play_sound', {'sound': 'correct'}, room=room_id)
    socketio.emit('pause_timer', room=room_id)
    
    # Attendre 3 secondes avant la question suivante
    socketio.start_background_task(delayed_next_question, room_id, 3)

@socketio.on('wrong_answer')
def handle_wrong_answer(data):
    """Réponse incorrecte - reprendre le chrono"""
    room_id = data.get('room_id', 'default') if data else 'default'
    game_state = get_or_create_room(room_id)
    
    socketio.emit('play_sound', {'sound': 'wrong'}, room=room_id)
    socketio.emit('resume_timer', room=room_id)
    game_state['buzzer_pressed'] = False
    game_state['buzzer_player'] = None
    game_state['timer_paused'] = False
    socketio.emit('game_update', get_game_data(room_id), room=room_id)

@socketio.on('time_up')
def handle_time_up(data):
    """Temps écoulé"""
    room_id = data.get('room_id', 'default') if data else 'default'
    
    # Jouer le son timeout et attendre 6 secondes
    socketio.emit('play_sound', {'sound': 'timeout'}, room=room_id)
    socketio.start_background_task(delayed_next_question, room_id, 6)

@socketio.on('get_final_results')
def handle_get_final_results(data):
    """Envoyer les résultats finaux"""
    room_id = data.get('room_id', 'default') if data else 'default'
    game_state = get_or_create_room(room_id)
    emit('final_results', game_state['players'])

@socketio.on('next_question')
def handle_next_question(data):
    """Passer à la question suivante manuellement"""
    room_id = data.get('room_id', 'default') if data else 'default'
    next_question(room_id)

@socketio.on('time_warning')
def handle_time_warning():
    """Diffuser l'alerte temps"""
    socketio.emit('time_warning')

@socketio.on('timer_start')
def handle_timer_start():
    """Démarrage du timer"""
    socketio.emit('timer_start')

@socketio.on('get_questions')
def handle_get_questions(data):
    """Envoyer la liste des questions"""
    room_id = data.get('room_id', 'default') if data else 'default'
    game_state = get_or_create_room(room_id)
    emit('questions_list', game_state['questions'])

@socketio.on('add_question')
def handle_add_question(data):
    """Ajouter une nouvelle question"""
    room_id = data.get('room_id', 'default')
    game_state = get_or_create_room(room_id)
    
    new_question = {
        'question': data['question'],
        'answer': data['answer']
    }
    game_state['questions'].append(new_question)
    save_questions(room_id)
    emit('questions_list', game_state['questions'])

@socketio.on('delete_question')
def handle_delete_question(data):
    """Supprimer une question"""
    room_id = data.get('room_id', 'default')
    game_state = get_or_create_room(room_id)
    
    index = data['index']
    if 0 <= index < len(game_state['questions']):
        game_state['questions'].pop(index)
        save_questions(room_id)
        emit('questions_list', game_state['questions'])

def save_questions(room_id):
    """Sauvegarder les questions dans le fichier JSON"""
    game_state = get_or_create_room(room_id)
    try:
        with open('data/questions.json', 'w', encoding='utf-8') as f:
            json.dump(game_state['questions'], f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f'Erreur sauvegarde: {e}')

@socketio.on('start_game')
def handle_start_game(data):
    """Démarrer le jeu"""
    room_id = data.get('room_id', 'default') if data else 'default'
    game_state = get_or_create_room(room_id)
    
    # Vérifications avant de démarrer
    if game_state['game_finished'] == False and game_state['current_question'] > 0:
        return  # Jeu déjà en cours
    
    if len(game_state['players']) == 0:
        return  # Aucun joueur
    
    load_questions(room_id)
    if len(game_state['questions']) == 0:
        return  # Aucune question
    
    game_state['current_question'] = 0
    game_state['game_finished'] = False
    game_state['buzzer_pressed'] = False
    game_state['buzzer_player'] = None
    game_state['timer_paused'] = False
    
    socketio.emit('game_started', room=room_id)
    socketio.emit('game_update', get_game_data(room_id), room=room_id)

def next_question(room_id):
    """Passer à la question suivante"""
    game_state = get_or_create_room(room_id)
    
    game_state['buzzer_pressed'] = False
    game_state['buzzer_player'] = None
    game_state['timer_paused'] = False
    game_state['current_question'] += 1
    
    if game_state['current_question'] >= len(game_state['questions']):
        game_state['game_finished'] = True
        socketio.emit('game_finished', room=room_id)
        socketio.emit('show_final_results', room=room_id)
    
    socketio.emit('game_update', get_game_data(room_id), room=room_id)

def reset_game_after_delay(room_id):
    """Réinitialiser le jeu après un délai"""
    import time
    time.sleep(30)
    reset_game(room_id)

def delayed_next_question(room_id, delay):
    """Passer à la question suivante après un délai"""
    import time
    time.sleep(delay)
    next_question(room_id)

def reset_game(room_id):
    """Réinitialiser complètement le jeu"""
    game_state = get_or_create_room(room_id)
    
    game_state['current_question'] = 0
    game_state['players'] = {}
    game_state['buzzer_pressed'] = False
    game_state['buzzer_player'] = None
    game_state['timer_paused'] = False
    game_state['game_finished'] = False
    socketio.emit('game_reset', room=room_id)
    socketio.emit('game_update', get_game_data(room_id), room=room_id)

def get_game_data(room_id):
    """Récupère les données actuelles du jeu pour une salle"""
    game_state = get_or_create_room(room_id)
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
