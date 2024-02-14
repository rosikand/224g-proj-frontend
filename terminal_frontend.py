import backend

backend_int = backend.BackendInterface()


while True:
    user_input = input("Enter your prompt containing a valid current player name from NHL or NBA... \n")
    if user_input:
        res = backend_int.get_result(user_input)
        print("-------------------------------")
        print(res)
    print("-------------------------------")
