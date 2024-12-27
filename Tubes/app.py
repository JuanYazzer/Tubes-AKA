import math
import time
import matplotlib.pyplot as plt
import io
import base64
from flask import Flask, render_template, request, flash
import sys
sys.setrecursionlimit(100000)  # Menyesuaikan batas rekursi

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Used for session and flash messages

# Function to check if a number is an Armstrong number
def is_armstrong(num):
    original_num = num
    digit_count = len(str(num))
    total = sum(int(digit) ** digit_count for digit in str(num))
    return total == original_num

# Define search methods
def sequential_search(range_start, range_end, target):
    for num in range(range_start, range_end + 1):
        if is_armstrong(num) and num == target:
            return True
    return False

def recursive_sequential_search(range_start, range_end, target):
    if range_start > range_end:
        return False  # Reached the end of the range without finding the target
    
    # If current number is Armstrong, check if it matches the target
    if is_armstrong(range_start) and range_start == target:
        return True

    # Continue the search
    return recursive_sequential_search(range_start + 1, range_end, target)

# Function to run the search tests and collect data
def run_search_tests(data_sizes, input_num, search_method):
    search_times = []
    for size in data_sizes:
        start_time = time.time()

        if search_method == 'Sequential Search':
            result = sequential_search(1, size, input_num)
        elif search_method == 'Recursive Sequential Search':
            result = recursive_sequential_search(1, size, input_num)

        end_time = time.time()
        time_taken_ms = (end_time - start_time) * 1000
        search_times.append(time_taken_ms)

    return search_times

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    input_num = None
    graph_url_iterative = None
    graph_url_recursive = None

    if request.method == 'POST':
        try:
            input_num = int(request.form['input_num'])

            # Prepare data for plotting
            data_sizes = list(range(1, 100001, 1000))  # Data sizes in increments of 1000

            # Check if the input number is an Armstrong number
            if is_armstrong(input_num):
                flash(f"{input_num} is an Armstrong number.", "success")
            else:
                flash(f"{input_num} is NOT an Armstrong number.", "warning")

            # Run search tests for the number using iterative method
            search_method = 'Sequential Search'
            sequential_search_times = run_search_tests(data_sizes, input_num, search_method)

            # Run search tests for the number using recursive method
            search_method = 'Recursive Sequential Search'
            recursive_sequential_search_times = run_search_tests(data_sizes, input_num, search_method)

            # Create plot for Sequential Search methods
            plt.figure(figsize=(14, 8))

            # Plot for Sequential methods
            plt.plot(data_sizes, sequential_search_times, label=f'Sequential Search', color='blue')
            plt.plot(data_sizes, recursive_sequential_search_times, label=f'Recursive Sequential Search', color='orange')
            plt.xlabel('Banyaknya Data')
            plt.ylabel('Waktu Running (ms)')
            plt.title('Sequential Search - Perbandingan Waktu')
            plt.legend()

            plt.tight_layout()

            # Save the plot to a PNG image and encode it to base64
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            graph_url_iterative = base64.b64encode(img.getvalue()).decode('utf8')
            plt.close()

        except ValueError:
            flash("Input is not a valid number. Please enter a valid integer.", "error")
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "error")

    return render_template('index.html', input_num=input_num, graph_url_iterative=graph_url_iterative)

if __name__ == '__main__':
    app.run(debug=True)
