import streamlit as st
import openai
import random

# Set your OpenAI API key
openai.api_key = 'your_openai_api_key'

def generate_trivia():
    # Generate a famous person
    person_prompt = "Generate the name of a well-known historical or contemporary figure."
    person_response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=person_prompt,
        max_tokens=10,
        temperature=0.7,
        n=1,
        stop=None
    )
    person_name = person_response.choices[0].text.strip()

    # Generate one true fact about the person
    true_fact_prompt = f"Provide one interesting and verifiable fact about {person_name}."
    true_fact_response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=true_fact_prompt,
        max_tokens=60,
        temperature=0.7,
        n=1,
        stop=None
    )
    true_fact = true_fact_response.choices[0].text.strip()

    # Generate three false but plausible facts about the person
    false_facts = []
    false_fact_prompt = f"Provide a false but plausible fact about {person_name} that is not true."
    for _ in range(3):
        false_fact_response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=false_fact_prompt,
            max_tokens=60,
            temperature=0.9,
            n=1,
            stop=None
        )
        false_fact = false_fact_response.choices[0].text.strip()
        false_facts.append(false_fact)

    # Combine and shuffle the facts
    all_facts = false_facts + [true_fact]
    random.shuffle(all_facts)

    return person_name, true_fact, all_facts

def main():
    st.title("Trivia Game")

    if 'person_name' not in st.session_state:
        st.session_state['person_name'], st.session_state['true_fact'], st.session_state['all_facts'] = generate_trivia()
        st.session_state['answered'] = False

    st.subheader(f"Guess the true fact about {st.session_state['person_name']}:")

    selected_fact = st.radio("Select one fact:", st.session_state['all_facts'])

    if st.button("Submit Answer"):
        if not st.session_state['answered']:
            st.session_state['answered'] = True
            if selected_fact == st.session_state['true_fact']:
                st.success("Correct! You selected the true fact.")
            else:
                st.error("Incorrect. That was not the true fact.")
                st.info(f"The correct fact was: {st.session_state['true_fact']}")

    if st.button("Play Again"):
        st.session_state['person_name'], st.session_state['true_fact'], st.session_state['all_facts'] = generate_trivia()
        st.session_state['answered'] = False
        st.experimental_rerun()

if __name__ == "__main__":
    main()
