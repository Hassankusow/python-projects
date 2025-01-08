# Base User class
class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role

    def login(self):
        return f"{self.username} has logged in."

    def logout(self):
        return f"{self.username} has logged out."


# Regular User class
class RegularUser(User):
    def __init__(self, username, current_weight, goal_weight, gender):
        super().__init__(username, "regular")
        self.current_weight = current_weight
        self.goal_weight = goal_weight
        self.gender = gender
        self.progress_log = []

    def log_progress(self, weight_change, calories):
        self.progress_log.append({"weight_change": weight_change, "calories": calories})
        return f"Progress logged for {self.username}."

    def view_report(self):
        return f"Progress Report for {self.username}: {self.progress_log}"


# Admin User class
class AdminUser(User):
    def __init__(self, username):
        super().__init__(username, "admin")
        self.managed_users = []

    def __add__(self, user):
        if isinstance(user, User):
            self.managed_users.append(user)
            return f"Added user {user.username}."
        return "Invalid user type."

    def __sub__(self, user):
        if isinstance(user, User) and user in self.managed_users:
            self.managed_users.remove(user)
            return f"Removed user {user.username}."
        return "User not found."

    def reset_user_data(self, user):
        if isinstance(user, RegularUser):
            user.progress_log = []
            return f"Reset progress data for {user.username}."


# Fitness Bot class
class FitnessBot(User):
    def __init__(self):
        super().__init__("FitnessBot", "bot")

    def check_inconsistencies(self, user):
        """
        Check if the user's logged data has inconsistencies.
        Example: High calorie intake with weight loss.
        """
        if isinstance(user, RegularUser):
            for log in user.progress_log:
                if log["calories"] > 2000 and log["weight_change"] < 0:
                    return f"Inconsistency found for {user.username}: Calorie surplus with weight loss."
                if abs(log["weight_change"]) > 10:
                    return f"Unrealistic progress for {user.username}: Weight change of {log['weight_change']} lbs in one week."
        return "No inconsistencies detected."

    def recommend_adjustments(self, user):
        """
        Provide personalized recommendations based on user's data.
        """
        if isinstance(user, RegularUser):
            if user.current_weight > user.goal_weight:
                return (
                    "Based on your progress, consider reducing calorie intake by 500-1000 calories/day "
                    "and incorporating moderate cardio exercises."
                )
            elif user.current_weight < user.goal_weight:
                return (
                    "To gain weight more effectively, aim to consume an additional 500 calories/day "
                    "and focus on strength training exercises."
                )
        return "Unable to provide recommendations for this user."

    def compare_users(self, user1, user2):
        """
        Compare the progress of two users for motivation or analysis.
        """
        if isinstance(user1, RegularUser) and isinstance(user2, RegularUser):
            progress1 = sum(log["weight_change"] for log in user1.progress_log)
            progress2 = sum(log["weight_change"] for log in user2.progress_log)
            return (
                f"{user1.username} has a total weight change of {progress1:.1f} lbs, "
                f"while {user2.username} has a total weight change of {progress2:.1f} lbs."
            )
        return "Comparison can only be made between regular users."



# FitnessGoal class
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


# WeightTracking class
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


# PerformanceTracking class
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


# NutritionGuidance class
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

    # Initialize users
    admin = AdminUser("Admin")
    bot = FitnessBot()

    print(admin.login())

    # Create a regular user
    username = input("Enter your username: ")
    current_weight = float(input("What is your current weight in pounds? "))
    goal_weight = float(input("What is your target weight in pounds? "))
    gender = input("Please specify your gender (male/female): ").strip().lower()
    regular_user = RegularUser(username, current_weight, goal_weight, gender)

    print(admin + regular_user)  # Add user to admin's managed users

    print(regular_user.login())

    # Initialize fitness-related features
    weight_tracker = WeightTracking(current_weight, goal_weight, gender, 0, 0)
    performance_tracker = PerformanceTracking(current_weight, goal_weight, gender)
    nutrition_guidance = NutritionGuidance(current_weight, goal_weight, gender)

    # Log progress
    weight_change = float(input("How much has your weight changed this week? "))
    calories = float(input("How many calories did you consume this week? "))
    print(regular_user.log_progress(weight_change, calories))

    # Display progress tracking
    print("\n--- Progress Tracker ---")
    print(weight_tracker.track_progress(weight_change))
    print(weight_tracker.calorie_feedback())

    # Generate workout plan
    print("\n--- Workout Plan ---")
    print(performance_tracker.generate_workout_plan())

    # Provide nutrition guidance
    print("\n--- Nutrition Plan ---")
    print(nutrition_guidance.get_nutrition_plan())

    # Bot checks for inconsistencies
    print("\n--- Bot Analysis ---")
    print(bot.check_inconsistencies(regular_user))

    # Bot provides recommendations
    print("\n--- Recommendations ---")
    print(bot.recommend_adjustments(regular_user))

    # Admin resets user data
    reset = input("Do you want to reset the user's data? (yes/no): ").strip().lower()
    if reset == "yes":
        print(admin.reset_user_data(regular_user))

    # Logout
    print(regular_user.logout())
    print(admin.logout())



if __name__ == "__main__":
    main()
