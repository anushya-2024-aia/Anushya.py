import streamlit as st
import random


def user_guesses():
    st.title("User Guessing Game")

    def get_secret_number():
        return random.randint(1, 10)

    def initial_state(post_init=False):
        if not post_init:
            st.session_state.input = 0
        st.session_state.number = get_secret_number()
        st.session_state.attempts = 0
        st.session_state.over = False

    def restart_game():
        initial_state(post_init=True)
        st.session_state.input += 1

    def get_hint(number):
        operation_list = ["+", "-", "*"]
        operation = random.choice(operation_list)
        if operation == "+":
            op1 = random.randint(1, number - 1)
            op2 = number - op1
            return f"{op1} + {op2} = ?"
        elif operation == "-":
            op1 = random.randint(number + 1, 100)
            op2 = op1 - number
            return f"{op1} - {op2} = ?"
        else:
            for op1 in range(1, 101):
                for op2 in range(1, 101):
                    if op1 * op2 == number:
                        return f"{op1} * {op2} = ?"
        return "No hint available."

    def main():
        st.write(
            """
            # Guess the number  🤔🤔🤔
            """
        )

        if "number" not in st.session_state:
            initial_state()

        st.button('New game', on_click=restart_game)

        placeholder, debug, hint_text = st.empty(), st.empty(), st.empty()

        guess = placeholder.number_input(
            "Enter your guess from 1 - 10",
            key=st.session_state.input,
            min_value=1,
            max_value=10
        )

        col1, _, _, _, col2 = st.columns(5)

        with col1:
            hint = st.button("Hint")

        with col2:
            attempts_left = 6 - st.session_state.attempts
            st.write(f"Attempts Left: {attempts_left if not st.session_state.over else 0}")

        if hint:
            hint_response = get_hint(st.session_state.number)
            hint_text.info(f"{hint_response}")

        if guess:
            if st.session_state.attempts < 6:
                st.session_state.attempts += 1
                if guess < st.session_state.number:
                    debug.warning(f"{guess} is too low")
                elif guess > st.session_state.number:
                    debug.warning(f"{guess} is too high")
                else:
                    debug.success(f"Right🥳🥳 You guessed it right🎈🎉")
                    st.balloons()
                    st.session_state.over = True
                    placeholder.empty()
            else:
                debug.error(f"Sorry you lost😔😔 ! Correct guess is {st.session_state.number}")
                st.session_state.over = True
                placeholder.empty()
                hint_text.empty()

    main()


def machine_guesses():
    st.title("Machine Guessing Game")
    st.write("Think of a number between 1 and 100, and I'll try to guess it!")

    if "lower_bound" not in st.session_state:
        st.session_state.lower_bound = 1
        st.session_state.upper_bound = 100
        st.session_state.attempts = 0

    st.write("For my guesses, please respond with:")
    st.write("- 'h' if my guess is *higher* than your number")
    st.write("- 'l' if my guess is *lower* than your number")
    st.write("- 'c' if my guess is *correct*")

    guess = (st.session_state.lower_bound + st.session_state.upper_bound) // 2
    st.write(f"My guess is: *{guess}*")

    feedback = st.text_input("Your feedback:", "").strip().lower()

    if feedback:
        st.session_state.attempts += 1

        if feedback == 'c':
            st.success(f"Yay! I guessed your number in {st.session_state.attempts} attempts!")
            # Reset state after game ends
            del st.session_state.lower_bound
            del st.session_state.upper_bound
            del st.session_state.attempts
        elif feedback == 'h':
            st.session_state.upper_bound = guess - 1
            st.write("Okay, I'll guess lower next time.")
        elif feedback == 'l':
            st.session_state.lower_bound = guess + 1
            st.write("Got it, I'll guess higher next time.")
        else:
            st.warning("Please enter 'h', 'l', or 'c'.")

        if st.session_state.lower_bound > st.session_state.upper_bound:
            st.error("It seems there's a contradiction in your feedback. Please restart the game.")
            # Reset the game state
            del st.session_state.lower_bound
            del st.session_state.upper_bound
            del st.session_state.attempts

st.sidebar.title("Choose Game Mode")
game_mode = st.sidebar.radio("Select a game mode:", ("User Guessing", "Machine Guessing"))

if game_mode == "User Guessing":
    user_guesses()
else:
    machine_guesses()
