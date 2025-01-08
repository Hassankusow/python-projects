import pytest
from fitness import FitnessGoal, WeightLossTracking, PerformanceTracking, WeightGoalTracking

def test_fitness_goal():
    # Create an instance of FitnessGoal
    goal = FitnessGoal(current_weight=200, goal_weight=180, gender="male")

    # Test calculate_time_to_goal
    assert goal.calculate_time_to_goal() == 10  

    # Test generate_instructions
    assert goal.generate_instructions() == "Focus on a calorie deficit and consistent workouts to lose weight."

    # Test at goal weight
    goal.current_weight = 180
    assert goal.generate_instructions() == "You are at your goal weight. Maintain a balanced diet and regular exercise."

    # Test weight gain
    goal.current_weight = 170
    assert goal.generate_instructions() == "Focus on a calorie surplus and strength training to gain weight."


def test_weight_loss_tracking():
    # Create an instance of WeightLossTracking
    tracker = WeightLossTracking(current_weight=200, goal_weight=180, gender="female", calories_intake=2000, calories_burned=2500)

    # Test track_progress
    assert tracker.track_progress() == pytest.approx(0.142857, rel=1e-3) 

    # Test generate_instructions
    assert tracker.generate_instructions() == "Focus on a calorie deficit and consistent workouts to lose weight."

    # Test calculate_time_to_goal
    assert tracker.calculate_time_to_goal() == 10


def test_performance_tracking():
    # Create an instance of PerformanceTracking
    tracker = PerformanceTracking(current_weight=200, goal_weight=180, gender="male", workout_sessions=5, strength_gain=20)

    # Test analyze_performance
    assert tracker.analyze_performance() == "You have completed 5 sessions and improved strength by 20 units."

    # Test generate_instructions
    assert tracker.generate_instructions() == "Focus on a calorie deficit and consistent workouts to lose weight."


def test_weight_goal_tracking():
    # Create an instance of WeightGoalTracking
    tracker = WeightGoalTracking(current_weight=200, goal_weight=180, gender="male", calories_intake=2000, calories_burned=2500, workout_sessions=5, strength_gain=15)

    # Test combined instructions
    assert tracker.generate_instructions() == (
        "Focus on a calorie deficit and consistent workouts to lose weight. "
        "Make sure to track both calorie intake and workout performance."
    )

    # Test calculate_time_to_goal
    assert tracker.calculate_time_to_goal() == 10

    # Test track_progress
    assert tracker.track_progress() == pytest.approx(0.142857, rel=1e-3) 

    # Test analyze_performance
    assert tracker.analyze_performance() == "You have completed 5 sessions and improved strength by 15 units."
