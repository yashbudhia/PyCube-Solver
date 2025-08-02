from flask import Flask, render_template, jsonify, request
from cube import Cube
from cube2x2 import Cube2x2
from cube4x4 import Cube4x4
from solver import Solver
from solver4x4 import Solver4x4
from solver2x2 import Solver2x2
from helper import getScramble
from helper2x2 import getScramble2x2
from helper4x4 import getScramble4x4
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
        cube_type = data.get('cube_type', '3x3')  # '2x2', '3x3', or '4x4'
        
        if cube_type == '2x2':
            # Create new 2x2 cube and scramble it
            cube = Cube2x2()
            scramble = getScramble2x2(min(scramble_length, 11)) # Ortega is better, can handle more
            cube.doMoves(scramble)
            # Create readable version for display by adding spaces
            import re
            scramble_display = re.sub(r"([RUFDLBrufxyz](?:'|2)?)", r"\1 ", scramble).strip()
        elif cube_type == '4x4':
            # Create new 4x4 cube and scramble it
            cube = Cube4x4()
            scramble = getScramble4x4(min(scramble_length, 40)) # 4x4 needs more moves
            cube.doMoves(scramble)
            # Create readable version for display by adding spaces
            import re
            scramble_display = re.sub(r"([RUFDLBrufxyz](?:'|2)?)", r"\1 ", scramble).strip()
        else:
            # Create new 3x3 cube and scramble it (default)
            cube = Cube()
            scramble = getScramble(scramble_length)
            cube.doMoves(scramble)
            scramble_display = scramble
        
        return jsonify({
            'success': True,
            'scramble': scramble_display,
            'cube_state': cube.getFaces(),
            'cube_display': str(cube),
            'cube_type': cube_type
        })
    except Exception as e:
        print(f"Error in /api/scramble: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/solve', methods=['POST'])
def solve_cube():
    """Solve the cube and return step-by-step solution"""
    try:
        data = request.get_json()
        cube_state = data.get('cube_state')
        cube_type = data.get('cube_type', '3x3')
        
        if not cube_state:
            return jsonify({'success': False, 'error': 'No cube state provided'})
        
        if cube_type == '2x2':
            cube = Cube2x2(faces=cube_state)
            solver = Solver2x2(cube)
            solver.solveCube(optimize=True)
            solution_plain = solver.getMoves(decorated=False)
            solution_decorated = solver.getMoves(decorated=True)
            
            # Since this uses the Ortega method, we don't have detailed steps like CFOP
            steps = [{"name": "2x2 Solution (Ortega Method)", "moves": solution_plain}]

            solved_cube = Cube2x2(faces=cube_state)
            if solution_plain and "Already solved" not in solution_plain and "Could not solve" not in solution_plain:
                solved_cube.doMoves(solution_plain)

        elif cube_type == '4x4':
            cube = Cube4x4(faces=cube_state)
            solver = Solver4x4(cube)
            solver.solveCube(optimize=True)
            solution_decorated = solver.getMoves(decorated=True)
            solution_plain = solver.getMoves(decorated=False)
            steps = [{"name": "4x4 Reduction Method", "moves": solution_plain}]
            
            solved_cube = Cube4x4(faces=cube_state)
            if solution_plain and "Already solved" not in solution_plain and "Could not solve" not in solution_plain:
                solved_cube.doMoves(solution_plain)

        else:
            # Create 3x3 cube with the given state (default)
            cube = Cube(faces=cube_state)
            solver = Solver(cube)
            solver.solveCube(optimize=True)
            solution_decorated = solver.getMoves(decorated=True)
            solution_plain = solver.getMoves(decorated=False)
            steps = parse_solution_steps(solution_decorated)
            solved_cube = Cube(faces=cube_state)
            if solution_plain and "Already solved" not in solution_plain:
                solved_cube.doMoves(solution_plain)
        
        return jsonify({
            'success': True,
            'solution': solution_decorated,
            'solution_plain': solution_plain,
            'steps': steps,
            'solved_state': solved_cube.getFaces(),
            'solved_display': str(solved_cube),
            'cube_type': cube_type
        })
    except Exception as e:
        print(f"Error in /api/solve: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/apply_moves', methods=['POST'])
def apply_moves():
    """Apply moves to a cube and return the new state"""
    try:
        data = request.get_json()
        cube_state = data.get('cube_state')
        moves = data.get('moves')
        cube_type = data.get('cube_type', '3x3')
        
        if not cube_state or not moves:
            return jsonify({'success': False, 'error': 'Missing cube state or moves'})
        
        # Create cube with the given state
        if cube_type == '2x2':
            cube = Cube2x2(faces=cube_state)
        elif cube_type == '4x4':
            cube = Cube4x4(faces=cube_state)
        else:
            cube = Cube(faces=cube_state)
            
        cube.doMoves(moves)
        
        return jsonify({
            'success': True,
            'cube_state': cube.getFaces(),
            'cube_display': str(cube),
            'cube_type': cube_type
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
        cube_type = data.get('cube_type', '3x3')
        
        if not cube_state:
            return jsonify({'success': False, 'error': 'No cube state provided'})
        
        animation_states = []
        if cube_type == '2x2':
            current_cube = Cube2x2(faces=cube_state)
        elif cube_type == '4x4':
            current_cube = Cube4x4(faces=cube_state)
        else:
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
            'animation_states': animation_states,
            'cube_type': cube_type
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/test4x4')
def test_4x4():
    """Test route to check 4x4 functionality"""
    try:
        cube = Cube4x4()
        faces = cube.getFaces()
        return jsonify({
            'success': True,
            'message': f'4x4 cube created successfully with {len(faces[0])}x{len(faces[0][0])} faces',
            'face_structure': [[len(row) for row in face] for face in faces]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/reset', methods=['POST'])
def reset_cube():
    """Reset cube to solved state"""
    try:
        data = request.get_json()
        cube_type = data.get('cube_type', '3x3')
        print(f"Reset cube called with cube_type: {cube_type}", flush=True)
        
        if cube_type == '2x2':
            cube = Cube2x2()
            print(f"Created 2x2 cube with face dimensions: {len(cube.getFaces()[0])}x{len(cube.getFaces()[0][0])}", flush=True)
        elif cube_type == '4x4':
            cube = Cube4x4()
            print(f"Created 4x4 cube with face dimensions: {len(cube.getFaces()[0])}x{len(cube.getFaces()[0][0])}", flush=True)
        else:
            cube = Cube()
            print(f"Created 3x3 cube with face dimensions: {len(cube.getFaces()[0])}x{len(cube.getFaces()[0][0])}", flush=True)
            
        faces = cube.getFaces()
        print(f"Returning cube with {len(faces)} faces, first face is {len(faces[0])}x{len(faces[0][0])}", flush=True)
        
        return jsonify({
            'success': True,
            'cube_state': faces,
            'cube_display': str(cube),
            'cube_type': cube_type
        })
    except Exception as e:
        print(f"Error in reset_cube: {e}", flush=True)
        return jsonify({'success': False, 'error': str(e)})

def parse_solution_steps(decorated_moves):
    """Parse the decorated solution string into individual steps"""
    if "Ortega" in decorated_moves:
        moves = decorated_moves.replace("Ortega Solution: ", "").strip()
        return [{"name": "Full Solve", "moves": moves}]
        
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
