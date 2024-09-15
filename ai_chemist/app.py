import streamlit as st
from pathlib import Path
import google.generativeai as genai
from google_api_key import google_api_key
from draw_molecule import get_compound_structure
import base64
## Streamlit App

genai.configure(api_key=google_api_key)

# Set up the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 2000,
}

# Safety settings to block harmful content
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  }
]

# System prompt for analyzing chemistry images and text
system_prompts = [
    """
    you are most intellegent chemist. You are a domain expert in chemistry. You are tasked with analyzing chemical reactions,nuclear reaction and structures, 
    either from an image or from text. If only text is provided, focus on understanding the reaction mechanism, 
    predicting outcomes, and optimizing conditions based on the text inputs.Generate an image for any compound or reaction described. Your expertise will assist in:
    - Identifying molecular interactions, functional groups, and structural details from the images.
    - Understanding reaction mechanisms, predicting outcomes, and optimizing conditions based on text inputs.

    Your key responsibilities:
    If an image is provided:
    1. Detailed Image Analysis: Examine the image to identify chemical structures or chemical reaction , functional groups, bond angles, 
    and other molecular characteristics, . Highlight any relevant structural features.

    If no image is provided:
    1. Text Analysis: Focus on understanding the chemical reaction described in the text, in tabular format, including:
    - Reactants: Identify all reactants involved in the reaction, including any starting materials or reagents.
    - Catalysts: Mention any catalysts that accelerate the reaction without being consumed in the process.
    - Solvents: Identify any solvents used, noting their impact on the reaction mechanism and product yield.
    - Temperatures: Specify the temperature conditions, whether the reaction is exothermic (releases heat) or endothermic (absorbs heat), and how temperature affects the reaction rate.
    - Reaction Conditions: Analyze the overall conditions such as pressure, pH, and whether the reaction takes place under inert atmospheres (e.g., nitrogen, argon).
    - Reaction Type: Classify the reaction (e.g., substitution, addition, redox, or polymerization) based on the reactants and products.
    - Reaction Mechanism: Describe the step-by-step process by which the reaction occurs, including bond formation/breaking, intermediate states, and transition states.
    - Equilibrium Considerations: If applicable, analyze whether the reaction reaches equilibrium, and if so, whether it can be shifted to favor the desired products by changing conditions (e.g., Le Chatelier’s principle).
    - Energy Profile: Evaluate the energy changes associated with the reaction, such as activation energy, and if the reaction is spontaneous or requires an external energy source (e.g., light, electricity).
    - Side Reactions: Identify any potential side reactions that could occur, leading to by-products, and suggest how to minimize these side reactions
    
    For both cases (with or without an image):
    2. Reaction Prediction: in tabular format. Based on the provided inputs (image, text, or both), predict possible products, intermediates, 
    and any side reactions. Clarify if the reaction seems feasible under the given conditions or suggest alternative pathways.
    
    3. Recommendation: in tabular format .Suggest changes to reaction conditions (e.g., solvent, temperature, catalyst) 
    to improve yield, selectivity, or safety.
    
    4. Safety Precautions: Identify any hazards based on the chemicals or conditions, 
    and propose safety protocols to mitigate risks.
    5.Applications and Use in Real World: 
    - Provide the most popular applications or uses of the chemical reaction or compounds produced by the reaction in industry, 
      specifying which type of industry (e.g., pharmaceuticals, manufacturing, energy) utilizes this reaction.
    - Describe how the reaction or compounds occur in natural processes (e.g., atmospheric reactions, biological processes, etc.) 
      or in other parts of the universe (e.g., interstellar chemistry, planetary processes).
    - If no well-known application or natural process exists for this reaction, you may leave this section out.

    Important Notes to Remember:
    1. Image Clarity: If the image is unclear or the structure is ambiguous, note that certain aspects 
    are 'Unable to be correctly determined based on the uploaded image.'
    2. Feasibility Check: If the reaction appears unfeasible under standard conditions, mention that 
    'The reaction may not proceed as expected under these conditions.'
    3. Disclaimer: Include a disclaimer at the end stating: "Consult with a certified chemist before proceeding 
    with any experimental steps."
    4. Multimodal Integration: Integrate findings from both image and text analysis to provide a 
    comprehensive recommendation for the chemical reaction.
    5.Use Tabular formate to show final analysis of the reaction in horizontal .
    6.response is user attarctive and well maintained. 
    
    7. mention about chemical reactions and formulas if needed to explain.
    8. Don't Mention this line in response:'Please provide me with the image or text description of the reaction you'd like me to analyze'.
    """
]

# Initialize the model with configuration and safety settings
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    safety_settings=safety_settings
)

# Set up Streamlit page configuration
st.set_page_config(page_title="AI_Chemist", page_icon="🧊", layout="wide")

# Set up the layout
col0,col1, col2 = st.columns([0.6,1, 3])
col11,col13,col12,f=st.columns([2,0.2,1,0.2])

# You can adjust the width ratios as needed
with col0:
    st.write( width=180)
  # Adjust the width as needed
# In the first column, display the image
with col1:
    st.image("https://attic.sh/qbxbujcq4yg5fcofjk36nb1e8302", width=180)
  # Adjust the width as needed

# In the second column, display the text
with col2:
    st.title("AI_Chemist")
    st.markdown('  ')
    st.subheader("An app to help with chemical analysis using images or text")

    # Or you can use st.markdown for more styling
    # st.markdown("**This is some text next to the image.**")

# Streamlit App: Upload either text, image, or both

# Input for text
with col11:
     text_input = st.text_area('',placeholder="Enter the text-based reaction description",height=50)
     images = get_compound_structure(google_api_key, text_input)
     print(images)

with col13:
    st.markdown('  ')
with col12:
     file_uploaded = st.file_uploader('Upload the image for Analysis', type=['png', 'jpg', 'jpeg'])
with f:
    st.markdown('  ')
# Submit button to generate analysis
submit = st.button("Generate Analysis",)
r1,r2,r3=st.columns([0.2,4,1])
if submit:
    prompt_parts = []

    # Add text to the prompt if provided
    if text_input:
        prompt_parts.append(text_input)

    # Add image to the prompt if uploaded
    if file_uploaded:
        st.image(file_uploaded, width=200, caption='Uploaded Image')
        image_data = file_uploaded.getvalue()
        image_part = {
            "mime_type": "image/jpg",  # Adjust mime_type if necessary
            "data": image_data
        }
        prompt_parts.append(image_part)

    # If both inputs are missing, show a warning
    if not prompt_parts:
        st.warning("Please provide either an image, text, or both.")
    else:
        # Add system prompt
        prompt_parts.append(system_prompts[0])

        try:
            # Generate response
            response = model.generate_content(prompt_parts)
            print(response)
            content_raw = response.text


            # Display the generated analysis
            with r1:
                st.markdown('  ')
            with r2:
                st.title('Generated Analysis')
                st.markdown(content_raw,unsafe_allow_html=True)
            with r3:
                for img in images:
                    st.image(img, caption="Molecular Structure", use_column_width=True)


        except Exception as e:
            st.error(f"An error occurred: {e}")
