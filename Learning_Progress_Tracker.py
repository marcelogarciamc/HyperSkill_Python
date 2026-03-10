from string import ascii_letters
import re

print("Learning progress tracker")
pattern_1 = r"^[A-Za-z]+('|-)?[A-Za-z]+$"
pattern_2 = r"^([A-Za-z]+('|-)?[A-Za-z]+(('|-)?[A-Za-z]+)?\s?)*$"
pattern_3 = r"[\w.-]+@([-\w]+\.)+[\w]+$"
pattern_4 = r"^[0-9]+$"
list_user = []
list_id = []

# Course constants
COURSES = ["Python", "DSA", "Databases", "Flask"]
MAX_POINTS = {"Python": 600, "DSA": 400, "Databases": 480, "Flask": 550}


class Hashtable:
    def __init__(self, size=1000):
        self.keys = [[] for _ in range(size)]
        # Store: [[points_list, submissions_list, full_name, email, notified_set]]
        self.values = [[] for _ in range(size)]
        self.size = size
        self.hash_key = 987

    def hash_func(self, hashing):
        hashing = str(hashing)
        return sum(ord(hashing[i]) ** (i + 1) for i in range(0, len(hashing))) % self.hash_key

    def add_hash(self, key, value, full_name, email):
        index = self.hash_func(key)
        self.keys[index].append(key)
        # We store [points], [submissions], full_name, email, and a set of notified course indices
        self.values[index].append([value, [0, 0, 0, 0], full_name, email, set()])
        list_id.append(str(index))

    def find_by_id(self, user_id):
        try:
            idx = int(user_id)
            if 0 <= idx < self.size and self.values[idx]:
                return self.values[idx][0]
        except ValueError:
            pass
        return None


hashtable = Hashtable()


def checking_data(first_name, last_name, email):
    if re.match(pattern_1, first_name) is None or len(first_name) <= 1:
        print('Incorrect first name.')
        return menu_add()
    elif re.match(pattern_2, last_name) is None or len(last_name) <= 1:
        print('Incorrect last name.')
        return menu_add()
    elif re.match(pattern_3, email) is None:
        print('Incorrect email.')
        return menu_add()

    for x in list_user:
        if email == x[2]:
            print("This email already taken.")
            return menu_add()

    user = (first_name, last_name, email)
    full_name = f"{first_name} {last_name}"
    user_h = f"{first_name}{last_name}{email}"
    list_user.append(user)
    hashtable.add_hash(key=user_h, value=[0, 0, 0, 0], full_name=full_name, email=email)
    print("The student has been added.")
    return menu_add()


def menu_add():
    while True:
        user_input = input().split()
        if not user_input:
            print("Incorrect credentials.")
            continue
        if user_input[0] == "back":
            print(f"Total {len(list_user)} students have been added.")
            return menu_choice()
        if len(user_input) < 3:
            print("Incorrect credentials.")
            continue

        first_name = user_input[0]
        last_name = " ".join(user_input[1:-1])
        email = user_input[-1]
        return checking_data(first_name, last_name, email)


def add_points():
    while True:
        user_input = input().split()
        if not user_input:
            continue
        if user_input[0] == "back":
            return menu_choice()

        if user_input[0] not in list_id:
            print(f"No student is found for id={user_input[0]}.")
            continue

        if len(user_input) != 5:
            print("Incorrect points format.")
            continue

        try:
            points = [int(p) for p in user_input[1:]]
            if any(p < 0 for p in points):
                raise ValueError
        except ValueError:
            print("Incorrect points format.")
            continue

        student_data = hashtable.find_by_id(user_input[0])
        pts_list = student_data[0]
        subs_list = student_data[1]

        for i in range(4):
            pts_list[i] += points[i]
            if points[i] > 0:
                subs_list[i] += 1

        print("Points updated.")


def find_points():
    print("Enter an id or 'back' to return:")
    while True:
        user_id = input()
        if user_id == "back":
            return menu_choice()

        student_data = hashtable.find_by_id(user_id)
        if student_data:
            pts = student_data[0]
            print(f"{user_id} points: Python={pts[0]}; DSA={pts[1]}; Databases={pts[2]}; Flask={pts[3]}")
        else:
            print(f"No student is found for id={user_id}.")


def id_students():
    if not list_id:
        print("No students found.")
    else:
        print("Students:")
        for x in list_id:
            print(x)
    return menu_choice()


def get_stats():
    pop = [0] * 4
    act = [0] * 4
    total_pts = [0] * 4

    for sid in list_id:
        data = hashtable.find_by_id(sid)
        pts, subs = data[0], data[1]
        for i in range(4):
            if subs[i] > 0:
                pop[i] += 1
                act[i] += subs[i]
                total_pts[i] += pts[i]

    pop_res = []
    for i in range(4): pop_res.append((pop[i], COURSES[i]))
    act_res = []
    for i in range(4): act_res.append((act[i], COURSES[i]))
    avg_res = []
    for i in range(4): avg_res.append((total_pts[i] / act[i] if act[i] > 0 else 0, COURSES[i]))

    def calculate_min_max(results):
        results.sort(key=lambda x: x[0], reverse=True)
        high_val = results[0][0]
        low_val = results[-1][0]

        if high_val == 0: return "n/a", "n/a"

        highest = [x[1] for x in results if x[0] == high_val]
        lowest = [x[1] for x in results if x[0] == low_val and x[1] not in highest]

        return ", ".join(highest), (", ".join(lowest) if lowest else "n/a")

    p_high, p_low = calculate_min_max(pop_res)
    a_high, a_low = calculate_min_max(act_res)
    e_high, h_low = calculate_min_max(avg_res)

    print(f"Most popular: {p_high}")
    print(f"Least popular: {p_low}")
    print(f"Highest activity: {a_high}")
    print(f"Lowest activity: {a_low}")
    print(f"Easiest course: {e_high}")
    print(f"Hardest course: {h_low}")


def course_details(course_name):
    c_idx = -1
    for i, name in enumerate(COURSES):
        if name.lower() == course_name.lower():
            c_idx = i
            real_name = name
            break

    if c_idx == -1:
        print("Unknown course.")
        return

    print(real_name)
    print("id     points completed")

    learners = []
    for sid in list_id:
        data = hashtable.find_by_id(sid)
        pts = data[0][c_idx]
        if pts > 0:
            perc = round((pts / MAX_POINTS[real_name]) * 100, 1)
            learners.append((sid, pts, perc))

    learners.sort(key=lambda x: (-x[1], x[0]))

    for l in learners:
        print(f"{l[0]:<7}{l[1]:<7}{l[2]}%")


def notify():
    count = 0
    for sid in list_id:
        data = hashtable.find_by_id(sid)
        # Structure: [points, subs, full_name, email, notified_set]
        pts, _, name, email, notified_set = data
        newly_notified = False
        for i, course in enumerate(COURSES):
            if pts[i] >= MAX_POINTS[course] and i not in notified_set:
                print(f"To: {email}")
                print("Re: Your Learning Progress")
                print(f"Hello, {name}! You have accomplished our {course} course!")
                notified_set.add(i)
                newly_notified = True
        if newly_notified:
            count += 1
    print(f"Total {count} students have been notified.")


def statistics_menu():
    print("Type the name of a course to see details or 'back' to quit:")
    get_stats()
    while True:
        cmd = input().strip()
        if cmd.lower() == "back":
            return menu_choice()
        if not cmd:
            continue
        course_details(cmd)


def menu_choice():
    while True:
        user_choice = input().strip()
        if not user_choice:
            print("No input.")
            continue
        if user_choice == "add students":
            print("Enter student credentials or 'back' to return:")
            return menu_add()
        elif user_choice == "list":
            return id_students()
        elif user_choice == "add points":
            print("Enter an id and points or 'back' to return:")
            return add_points()
        elif user_choice == "find":
            return find_points()
        elif user_choice == "statistics":
            return statistics_menu()
        elif user_choice == "notify":
            notify()
        elif user_choice == "back":
            print("Enter 'exit' to exit the program.")
        elif user_choice == "exit":
            print("Bye!")
            exit()
        else:
            print("Error: unknown command!")


if __name__ == "__main__":
    menu_choice()
