from BST import BST


class FitnessGoal:
    def __init__(self, current_weight, goal_weight, gender):
        self.current_weight = current_weight
        self.goal_weight = goal_weight
        self.gender = gender

    def calculate_time_to_goal(self, weekly_goal):
        if weekly_goal == 0:
            return "Weekly goal cannot be zero."
        weight_difference = abs(self.goal_weight - self.current_weight)
        weeks = weight_difference / abs(weekly_goal)
        return f"With steady progress, you should reach your goal in approximately {weeks:.1f} weeks."


class WeightTracking(FitnessGoal):
    def __init__(self, current_weight, goal_weight, gender, calories_intake, calories_burned):
        super().__init__(current_weight, goal_weight, gender)
        self.weekly_goal = 2 if self.goal_weight > self.current_weight else -2
        self.calories_intake = calories_intake
        self.calories_burned = calories_burned

    def track_progress(self, actual_weight_change):
        if self.weekly_goal < 0 and actual_weight_change < 0:  # Weight loss
            if abs(actual_weight_change) >= abs(self.weekly_goal):
                return (
                    f"Great job! You've lost {abs(actual_weight_change):.1f} lbs this week, "
                    f"exceeding your goal of {abs(self.weekly_goal)} lbs!"
                )
            else:
                return (
                    f"You've lost {abs(actual_weight_change):.1f} lbs this week, but fell short of your goal of "
                    f"{abs(self.weekly_goal)} lbs. Keep pushing!"
                )
        elif self.weekly_goal > 0 and actual_weight_change > 0:  # Weight gain
            if abs(actual_weight_change) >= abs(self.weekly_goal):
                return (
                    f"Great job! You've gained {abs(actual_weight_change):.1f} lbs this week, "
                    f"exceeding your goal of {abs(self.weekly_goal)} lbs!"
                )
            else:
                return (
                    f"You've gained {abs(actual_weight_change):.1f} lbs this week, but fell short of your goal of "
                    f"{abs(self.weekly_goal)} lbs. Stay consistent!"
                )
        elif actual_weight_change == 0:
            return "No weight change this week. Let's refocus and try again!"
        else:
            if self.weekly_goal < 0 and actual_weight_change > 0:
                return "You gained weight this week, but your goal is to lose weight. Adjust your plan!"
            elif self.weekly_goal > 0 and actual_weight_change < 0:
                return "You lost weight this week, but your goal is to gain weight. Adjust your plan!"

    def calorie_feedback(self):
        if self.calories_intake > self.calories_burned:
            return "You are consuming more calories than you burn. This supports weight gain."
        elif self.calories_intake < self.calories_burned:
            return "You are burning more calories than you consume. This supports weight loss."
        else:
            return "Your calorie balance is neutral. Adjust intake or activity to match your goals."


class PerformanceTracking(FitnessGoal):
    def generate_workout_plan(self):
        if self.gender.lower() in ["male", "m"]:
            return self.men_workout_plan()
        elif self.gender.lower() in ["female", "f"]:
            return self.women_workout_plan()
        else:
            return "Invalid gender. Please specify 'male' or 'female'."

    def men_workout_plan(self):
        if self.current_weight > self.goal_weight:  # Overweight
            return (
                "4-Day Workout Plan for Men (Overweight):\n"
                "- Day 1: Back and biceps + 20 minutes HIIT cardio\n"
                "- Day 2: Chest and triceps + 30 minutes moderate cardio\n"
                "- Day 3: Full-body workout + 30 minutes boxing/kickboxing\n"
                "- Day 4: Shoulders and arms + 20 minutes low-intensity cardio\n"
            )
        else:  # Underweight
            return (
                "4-Day Workout Plan for Men (Underweight):\n"
                "- Day 1: Back and biceps (heavy lifting focus)\n"
                "- Day 2: Chest and triceps\n"
                "- Day 3: Shoulders and arms\n"
                "- Day 4: Full-body strength workout\n"
            )

    def women_workout_plan(self):
        if self.current_weight > self.goal_weight:  # Overweight
            return (
                "4-Day Workout Plan for Women (Overweight):\n"
                "- Day 1: Leg day + 30 minutes moderate cardio\n"
                "- Day 2: Glute and hamstrings + 20 minutes HIIT cardio\n"
                "- Day 3: Full-body workout + 30 minutes boxing\n"
                "- Day 4: Quads and calves + 20 minutes low-intensity cardio\n"
            )
        else:  # Underweight
            return (
                "4-Day Workout Plan for Women (Underweight):\n"
                "- Day 1: Leg day (heavy lifting focus)\n"
                "- Day 2: Glute and hamstrings\n"
                "- Day 3: Full-body workout\n"
                "- Day 4: Quad-focused workout\n"
            )


class NutritionGuidance(FitnessGoal):
    def get_nutrition_plan(self):
        if self.current_weight > self.goal_weight:  # Weight loss
            return (
                "Nutrition Plan for Weight Loss:\n"
                "- Avoid eating 2 hours before sleeping.\n"
                "- Consume a high-protein diet.\n"
                "- Focus on fiber-rich foods and avoid sugary drinks.\n"
                "- Drink plenty of water and practice portion control."
            )
        else:  # Weight gain
            return (
                "Nutrition Plan for Weight Gain:\n"
                "- Eat calorie-dense, nutrient-rich foods.\n"
                "- Include healthy oils, nuts, seeds, and whole grains.\n"
                "- Have a balanced intake of protein, carbs, and fats.\n"
                "- Drink protein shakes with calorie boosters like peanut butter."
            )


def main():
    print("Welcome to the Fitness Tracker!")

    # Create a BST instance for storing fitness records
    fitness_tree = BST()

    while True:
        # Gather user inputs
        current_weight = float(input("What is your current weight in pounds? "))
        goal_weight = float(input("What is your target weight in pounds? "))
        gender = input("Please specify your gender (male/female): ").strip().lower()
        calories_intake = float(input("How many calories do you consume daily? "))
        calories_burned = float(input("How many calories do you burn daily? "))

        # Initialize classes
        weight_tracker = WeightTracking(current_weight, goal_weight, gender, calories_intake, calories_burned)
        performance_tracker = PerformanceTracking(current_weight, goal_weight, gender)
        nutrition_guidance = NutritionGuidance(current_weight, goal_weight, gender)

        # Calculate time to goal
        print("\n--- Progress Tracker ---")
        print(weight_tracker.calculate_time_to_goal(weight_tracker.weekly_goal))

        actual_weight_change = float(input("\nHow much has your weight changed in the past week? "))
        print(weight_tracker.track_progress(actual_weight_change))
        print(weight_tracker.calorie_feedback())

        # Display workout and nutrition plans
        print("\n--- Workout Plan ---")
        print(performance_tracker.generate_workout_plan())
        print("\n--- Nutrition Plan ---")
        print(nutrition_guidance.get_nutrition_plan())

        # Insert record into the BST
        fitness_record = {
            "current_weight": current_weight,
            "goal_weight": goal_weight,
            "gender": gender,
            "calories_intake": calories_intake,
            "calories_burned": calories_burned,
            "weekly_change": actual_weight_change
        }
        fitness_tree.insert(fitness_record)

        # Ask if the user wants to view records
        view_records = input("\nDo you want to view all fitness records? (yes/no): ").strip().lower()
        if view_records == "yes":
            print("\n--- All Fitness Records (In-Order Traversal) ---")
            records = fitness_tree.inorder_traversal()
            for record in records:
                print(record)

        # Check if the user wants to continue
        continue_tracking = input("\nDo you want to add another record? (yes/no): ").strip().lower()
        if continue_tracking != "yes":
            print("\nThank you for using the Fitness Tracker. Good luck on your journey!")
            break




if __name__ == "__main__":
    main()
