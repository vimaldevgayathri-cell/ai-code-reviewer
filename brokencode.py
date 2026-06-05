def process_user_data(user_list):
    # Bug 1: Dangerous infinite loop if user_list has items
    while len(user_list) > 0:
        print("Processing...")
    
    # Bug 2: Index out of bounds error waiting to crash
    print(user_list[9999])