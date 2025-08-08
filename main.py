import streamlit as st
from utils import generate_dialogue, translate_text, text_to_audio
from PIL import Image
import os
import time

# Set page configuration
st.set_page_config(page_title="AI NPC Dialogue Generator", layout="wide")

# Preload RPG background images (make sure they are in the media/ folder)
rpg_images = [
    "media/Screenshot 2025-08-08 063102.png",
    "media/Screenshot 2025-08-08 062600.png",
    "media/Screenshot 2025-08-08 062701.png",
    "media/Screenshot 2025-08-08 062733.png",
]

# Streamlit slideshow in the background
def rpg_background_slideshow():
    img_slot = st.empty()
    while True:
        for img_path in rpg_images:
            with img_slot.container():
                img = Image.open(img_path)
                st.image(img, use_container_width=True)
            time.sleep(5)

# Sidebar with language
st.sidebar.title("Settings")
language = st.sidebar.selectbox("Translate Dialogue To:", ("None", "Tamil", "Hindi", "French", "Spanish", "Japanese"))

# Default NPC examples
example_characters = {
    "Darius the Blade": {
        "traits": "Brave, strategic, loyal",
        "scenario": "Facing a dragon in the final battle",
        "tone": "Epic and intense"
    },
    "Elyra the Mystic": {
        "traits": "Wise, calm, powerful",
        "scenario": "Teaching an apprentice a forbidden spell",
        "tone": "Mysterious and gentle"
    },
    "Thorn the Rogue": {
        "traits": "Sneaky, sarcastic, agile",
        "scenario": "Breaking into a noble’s mansion",
        "tone": "Witty and mischievous"
    }
}

st.title("🎮 AI NPC Dialogue Generator")
st.markdown("Create rich, game-style conversations for your NPCs with emotional voice and multilingual support.")

# Left side layout for inputs
col1, col2 = st.columns([2, 3])
with col1:
    use_example = st.radio("Choose Character Type", ["Custom Character", "Use Example NPC"])
    if use_example == "Use Example NPC":
        selected_npc = st.selectbox("Choose Example NPC", list(example_characters.keys()))
        character_name = selected_npc
        character_traits = example_characters[selected_npc]["traits"]
        scenario = example_characters[selected_npc]["scenario"]
        tone = example_characters[selected_npc]["tone"]
    else:
        character_name = st.text_input("Character Name", placeholder="e.g., Kael the Archer")
        character_traits = st.text_area("Character Traits", placeholder="e.g., Brave, loyal, skilled with a bow")
        scenario = st.text_area("Scenario", placeholder="e.g., About to confront a rival clan")
        tone = st.text_input("Tone / Voice Style", placeholder="e.g., Dramatic and emotional")

    if st.button("Generate Dialogue"):
        if character_name and character_traits and scenario and tone:
            st.session_state.dialogue = generate_dialogue(character_name, character_traits, scenario, tone)
            if language != "None":
                lang_map = {
                    "Tamil": "ta",
                    "Hindi": "hi",
                    "French": "fr",
                    "Spanish": "es",
                    "Japanese": "ja"
                }
                translated = translate_text(st.session_state.dialogue, target_lang=lang_map[language])
                st.session_state.dialogue = translated
            st.session_state.audio_path = text_to_audio(st.session_state.dialogue)

    if "dialogue" in st.session_state:
        st.markdown(f"### 🎭 Dialogue by **{character_name}**:")
        st.write(st.session_state.dialogue)
        st.audio(st.session_state.audio_path)

        if st.button("Continue the Chat"):
            new_dialogue = generate_dialogue(character_name, character_traits, scenario, tone)
            if language != "None":
                translated = translate_text(new_dialogue, target_lang=lang_map[language])
                new_dialogue = translated
            audio_path = text_to_audio(new_dialogue)
            st.session_state.dialogue = new_dialogue
            st.session_state.audio_path = audio_path
            st.rerun()

with col2:
    st.markdown("### 🌄 RPG Slideshow")
    img_placeholder = st.empty()
    if 'image_index' not in st.session_state:
        st.session_state.image_index = 0

    img_path = rpg_images[st.session_state.image_index]
    image = Image.open(img_path)
    img_placeholder.image(image, use_container_width=True)

    # Cycle image every 5 seconds
    if 'last_image_time' not in st.session_state or time.time() - st.session_state.last_image_time > 5:
        st.session_state.image_index = (st.session_state.image_index + 1) % len(rpg_images)
        st.session_state.last_image_time = time.time()
