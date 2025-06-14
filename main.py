
import tkinter as tk           # GUI window
import time                    # For countdown
import threading               # To run timer in background
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from plyer import notification



running = False
paused = False
remaining_time = 0


root = tk.Tk()
root.title("🧠 Smart Study Timer")
root.geometry("350x400")
root.configure(bg="#ffffff")

timer_label = tk.Label(root, text="25:00", font=("Courier", 48), fg="#000000", bg="#ffffff")
timer_label.pack(pady=20)


# Task input box
task_entry = tk.Entry(root, width=30, font=("Arial", 12))
task_entry.insert(0, "What are you working on?")
task_entry.pack(pady=20)


# Variable to control timer
running = False

# Countdown function
def countdown(time_sec):
    global running, paused, remaining_time
    remaining_time = time_sec

    while remaining_time > 0 and running:
        if not paused:
            mins, secs = divmod(remaining_time, 60)
            time_display = '{:02d}:{:02d}'.format(mins, secs)
            timer_label.config(text=time_display)
            root.update()
            time.sleep(1)
            remaining_time -= 1
        else:
            time.sleep(0.1)

    if running and not paused and remaining_time == 0:
        timer_label.config(text="Time’s Up!")
        task = task_entry.get()
        duration = int(time_entry.get())
        save_session(task, duration)
        notification.notify(
            title="⏰ Time's Up!",
            message=f"You finished: {task}",
            timeout=5
        )
    if running and not paused and remaining_time == 0:
        timer_label.config(text="Time’s Up!")
        task = task_entry.get()
        duration = int(time_entry.get())
        save_session(task, duration)

        # 🔔 Notify
        notification.notify(
            title="⏰ Time's Up!",
            message=f"You finished: {task}",
            timeout=5
    )

    # 🧹 Clear fields
    task_entry.delete(0, tk.END)
    time_entry.delete(0, tk.END)

    # 👁 Hide buttons again
    pause_button.pack_forget()
    resume_button.pack_forget()
    reset_button.pack_forget()



# Start button function
def start_timer():
    global running, paused, remaining_time
    if not running:
        try:
            minutes = int(time_entry.get())
            if minutes <= 0:
                raise ValueError

            running = True
            paused = False
            remaining_time = minutes * 60

            # Show control buttons when timer starts
            pause_button.pack()
            resume_button.pack()
            reset_button.pack()

            thread = threading.Thread(target=countdown, args=(remaining_time,))
            thread.start()

        except ValueError:
            timer_label.config(text="Enter valid minutes")



def pause_timer():
    global paused
    paused = True

def resume_timer():
    global paused
    paused = False

def reset_timer():
    global running, paused, remaining_time
    running = False
    paused = False
    remaining_time = 0
    timer_label.config(text="00:00")

    # 🧹 Clear input fields
    task_entry.delete(0, tk.END)
    time_entry.delete(0, tk.END)

    # 👁 Hide control buttons
    pause_button.pack_forget()
    resume_button.pack_forget()
    reset_button.pack_forget()




def save_session(task_name, duration):
    # Get today's date
    date = datetime.now().strftime("%Y-%m-%d")
    
    # Create a dictionary with data
    data = {
        "Date": [date],
        "Task": [task_name],
        "Duration (min)": [duration]
    }

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Save to CSV (append if file exists)
    try:
        df.to_csv("sessions.csv", mode='a', header=False, index=False)
    except:
        df.to_csv("sessions.csv", index=False)

def show_study_chart():
    try:
        # Read the CSV file
        df = pd.read_csv("sessions.csv")

        # Group by Date and add all durations
        summary = df.groupby("Date")["Duration (min)"].sum()

        # Plot
        summary.plot(kind="bar", color="#6C5CE7")
        plt.title("Study Time Per Day")
        plt.xlabel("Date")
        plt.ylabel("Total Minutes")
        plt.tight_layout()
        plt.show()

    except FileNotFoundError:
        print("No data file found.")

time_label = tk.Label(root, text="⏱ Enter Minutes:", font=("Arial", 12), bg="#FDF6EC", fg="#2d3436")
time_label.pack()

time_entry = tk.Entry(root, width=10, font=("Arial", 12))
time_entry.insert(0, "25")  # default 25 mins
time_entry.pack(pady=5)

# Start button
start_button = tk.Button(root, text="Start Timer", command=start_timer, bg="#55EFC4", font=("Arial", 12), width=20)
start_button.pack(pady=10)

chart_button = tk.Button(root, text="View Progress Chart", command=show_study_chart, bg="#74B9FF", font=("Arial", 12), width=20)
chart_button.pack(pady=10)

footer = tk.Label(root, text="Made with ❤️ by Sowbarnika", bg="#FDF6EC", fg="#636E72", font=("Arial", 9))
footer.pack(side="bottom", pady=10)

# Control buttons (initially hidden)
pause_button = tk.Button(root, text="⏸ Pause", command=pause_timer, bg="#fab1a0", font=("Arial", 12), width=10)
resume_button = tk.Button(root, text="▶️ Resume", command=resume_timer, bg="#81ecec", font=("Arial", 12), width=10)
reset_button = tk.Button(root, text="🔁 Reset", command=reset_timer, bg="#ffeaa7", font=("Arial", 12), width=10)

# Place them under the timer but hide for now
pause_button.pack(pady=2)
resume_button.pack(pady=2)
reset_button.pack(pady=2)

pause_button.pack_forget()
resume_button.pack_forget()
reset_button.pack_forget()


# Run the app
root.mainloop()

