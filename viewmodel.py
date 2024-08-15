import pickle

def error_decorator(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as ex:
            message = str(ex)
            if message == "Name.Required":
                return "Name can not be empty"
            elif message == "Phone.NotNumeric":
                return "Phone must be numeric"
            elif message == "Phone.LengthMustBe10":
                return "Phone lenght must be 10 digits"
            elif message == "Birthday.Invalid":
                return "Birthday should be in format d.m.Y (e.g. 27.1.2000)"
            elif message == "Email.Required":
                return "Email can not be empty"
            elif message == "Email.Invalid":
                return "Input a valid email"
            elif message == "Address.Required":
                return "Address can not be empty"
            else:
                return "Input a valid command."
        except IOError as ex:
            message = str(ex)
            if message == "IO.SaveFailed":
                return "Failed to save address book"
            elif message == "IO.LoadFailed":
                return "Failed to save address book"
            else:
                return "Oops... Something went wrong"
        except Exception as ex:
            print(ex)
            return "Oops... Something went wrong"

    return inner

@error_decorator
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@error_decorator
def save_data(book, filename):
    try:
        with open(filename, "wb") as f:
            pickle.dump(book, f)
        return None
    except Exception:
        raise IOError("IO.SaveFailed")
    
@error_decorator
def load_data(filename):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None
    except Exception:
        raise IOError("IO.LoadFailed")