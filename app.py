from flask import Flask, render_template, jsonify, request
from cube import Cube
from solver import Solver
from helper import getScramble
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/scramble', methods=['POST'])
def scramble_cube():
    """Generate a scrambled cube and return its state"""
    try:
        data = request.get_json()
        scramble_length = data.get('length', 20)
        
        # Create new cube and scramble it
        cube = Cube()
        scramble = getScramble(scramble_length)
        cube.doMoves(scramble)
        
        return jsonify({
            'success': True,
            'scramble': scramble,
            'cube_state': cube.getFaces(),
            'cube_display': str(cube)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/solve', methods=['POST'])
def solve_cube():
    """Solve the cube and return step-by-step solution"""
    try:
        data = request.get_json()
        cube_state = data.get('cube_state')
        
        if not cube_state:
            return jsonify({'success': False, 'error': 'No cube state provided'})
        
        # Create cube with the given state
        cube = Cube(faces=cube_state)
        solver = Solver(cube)
        
        # Solve the cube
        solver.solveCube(optimize=True)
        
        # Get the moves with decoration to show steps
        moves = solver.getMoves(decorated=True)
        moves_plain = solver.getMoves(decorated=False)
        
        # Parse the decorated moves to extract individual steps
        steps = parse_solution_steps(moves)
        
        # Apply the complete solution to get final state
        solved_cube = Cube(faces=cube_state)
        if moves_plain.strip():  # Only apply if there are moves
            solved_cube.doMoves(moves_plain)
        
        return jsonify({
            'success': True,
            'solution': moves,
            'solution_plain': moves_plain,
            'steps': steps,
            'solved_state': solved_cube.getFaces(),
            'solved_display': str(solved_cube)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/apply_moves', methods=['POST'])
def apply_moves():
    """Apply moves to a cube and return the new state"""
    try:
        data = request.get_json()
        cube_state = data.get('cube_state')
        moves = data.get('moves')
        
        if not cube_state or not moves:
            return jsonify({'success': False, 'error': 'Missing cube state or moves'})
        
        # Create cube with the given state
        cube = Cube(faces=cube_state)
        cube.doMoves(moves)
        
        return jsonify({
            'success': True,
            'cube_state': cube.getFaces(),
            'cube_display': str(cube)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/animate_solution', methods=['POST'])
def animate_solution():
    """Get step-by-step cube states for solution animation"""
    try:
        data = request.get_json()
        cube_state = data.get('cube_state')
        steps = data.get('steps', [])
        
        if not cube_state:
            return jsonify({'success': False, 'error': 'No cube state provided'})
        
        animation_states = []
        current_cube = Cube(faces=cube_state)
        
        # Add initial state
        animation_states.append({
            'step_name': 'Initial State',
            'moves': '',
            'cube_state': current_cube.getFaces(),
            'cube_display': str(current_cube)
        })
        
        # Apply each step and capture states
        for step in steps:
            if step.get('moves'):
                current_cube.doMoves(step['moves'])
                animation_states.append({
                    'step_name': step['name'],
                    'moves': step['moves'],
                    'cube_state': current_cube.getFaces(),
                    'cube_display': str(current_cube)
                })
        
        return jsonify({
            'success': True,
            'animation_states': animation_states
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/reset', methods=['POST'])
def reset_cube():
    """Reset cube to solved state"""
    try:
        cube = Cube()
        return jsonify({
            'success': True,
            'cube_state': cube.getFaces(),
            'cube_display': str(cube)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def parse_solution_steps(decorated_moves):
    """Parse the decorated solution string into individual steps"""
    steps = []
    lines = decorated_moves.strip().split('\n')
    
    for line in lines:
        if line.startswith('For '):
            # Extract step name and moves
            parts = line.split(': ')
            if len(parts) == 2:
                step_name = parts[0].replace('For ', '')
                moves = parts[1].strip()
                if moves:  # Only add non-empty move sequences
                    steps.append({
                        'name': step_name,
                        'moves': moves
                    })
    
    return steps

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port)
